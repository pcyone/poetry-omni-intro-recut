"""Package local narration as text-free H.264/AAC MP4 references for Omni."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    root = args.directory.resolve()
    manifest_path = root / 'edit-manifest.json'
    manifest = json.loads(manifest_path.read_text())
    day = manifest['day']
    prompt_path = root / f'{day}-omni-prompts.md'
    prompts = prompt_path.read_text()
    outputs = []
    for segment in manifest['segments']:
        audio = Path(segment['audio'])
        duration = float(probe(audio)['format']['duration'])
        target = root / f'{day}-part{segment["part"]}-reference.mp4'
        if not target.exists():
            subprocess.run(['ffmpeg', '-v', 'error', '-n', '-f', 'lavfi', '-i', 'color=c=0x303638:s=1080x1920:r=30',
                            '-i', str(audio), '-map', '0:v', '-map', '1:a', '-t', str(duration),
                            '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23', '-pix_fmt', 'yuv420p',
                            '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2', '-movflags', '+faststart', str(target)], check=True)
        info = probe(target)
        codecs = {stream['codec_name'] for stream in info['streams']}
        if not {'h264', 'aac'} <= codecs or abs(float(info['format']['duration']) - duration) > .06:
            raise RuntimeError(f'Invalid reference: {target}')
        subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(target), '-f', 'null', '-'], check=True)
        segment['reference_video'] = str(target)
        segment['reference_sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
        prompts = prompts.replace(audio.name, target.name)
        outputs.append(target)
        print(f'{target.name}: {duration:g}s verified', flush=True)
    note = '上传格式：只上传下列 MP4 参考，不上传 WAV。MP4 的中性纯色画面仅承载原配音和时间基准；请忽略参考底色和布局，按每段提示词从零生成古风动画。参考片不是最终动画。原配音内容和语速保持不变，WAV 仅在本地保留。'
    prompts = prompts.replace('只用纯配音参考，不上传带字原片。', '只上传无字 MP4 配音参考，不上传带字原片。')
    if note not in prompts:
        title, rest = prompts.split('\n', 1)
        prompts = title + '\n\n' + note + '\n' + rest
    constraint = '参考MP4仅提供音轨和时间基准；忽略其纯色画面，按本段描述从零生成古风动画。'
    if constraint not in prompts:
        prompts = prompts.replace('```text\n', '```text\n' + constraint + '\n')
    prompt_path.write_text(prompts)
    manifest['reference_format'] = 'mp4-h264-aac'
    manifest['reference_qa'] = 'all durations, codecs and full decodes passed'
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    for name in (f'{day}-Omni-reference-pack.zip', f'{day}-Omni-MP4-reference-pack.zip'):
        with zipfile.ZipFile(root / name, 'w', zipfile.ZIP_DEFLATED) as archive:
            for path in outputs + [prompt_path, root / f'{day}-intro-script.txt']:
                archive.write(path, path.name)
        with zipfile.ZipFile(root / name) as archive:
            assert archive.testzip() is None
            assert len([n for n in archive.namelist() if n.endswith('.mp4')]) == len(outputs)
            assert not any(n.endswith('.wav') for n in archive.namelist())


if __name__ == '__main__':
    main()
