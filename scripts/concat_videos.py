"""Join a replacement intro to a retained lesson without overwriting inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def probe(path):
    return json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_format', '-show_streams',
        '-of', 'json', str(path)
    ]))


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--head', required=True, type=Path)
    parser.add_argument('--tail', required=True, type=Path)
    parser.add_argument('--tail-start', type=float, default=0)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    head, tail, output = (p.resolve() for p in (args.head, args.tail, args.output))
    report = output.with_suffix('.qa.json')
    if output in (head, tail) or output.exists() or report.exists():
        parser.error('Output or report exists, or output aliases an input; use a new path.')
    durations = []
    for path in (head, tail):
        info = probe(path)
        types = {s['codec_type'] for s in info['streams']}
        if not {'video', 'audio'} <= types:
            parser.error(f'Video and audio are required: {path}')
        durations.append(float(info['format']['duration']))
    if not 0 <= args.tail_start < durations[1]:
        parser.error('tail-start must be within the tail video.')
    expected = sum(durations) - args.tail_start
    vf = 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,setpts=PTS-STARTPTS'
    af = 'aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS'
    graph = f'[0:v]{vf}[v0];[1:v]{vf}[v1];[0:a]{af}[a0];[1:a]{af}[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]'
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n', '-i', str(head),
           '-ss', str(args.tail_start), '-i', str(tail), '-filter_complex', graph,
           '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'fast',
           '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
           '-movflags', '+faststart', str(output)]
    if args.dry_run:
        print(json.dumps({'expected_seconds': expected, 'command': cmd}, ensure_ascii=False, indent=2))
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(cmd, check=True)
    actual_info = probe(output)
    actual = float(actual_info['format']['duration'])
    if abs(actual - expected) > .1:
        raise RuntimeError(f'Duration mismatch: expected {expected}, got {actual}')
    subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(output), '-f', 'null', '-'], check=True)
    result = {'head': str(head), 'head_sha256': digest(head), 'tail': str(tail),
              'tail_sha256': digest(tail), 'tail_start': args.tail_start,
              'output': str(output), 'duration': actual, 'sha256': digest(output),
              'decode_check': 'passed', 'visual_and_audio_review': 'pending'}
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
