# 编辑细节与 DAY060 示例

## 音频与时间线

- 古风片头字幕默认参考已获用户确认的 DAY071 V3：`out/omni/DAY071-song-you-ren-recut/DAY071-intro-lower-subtitles-v3.mp4`。该流程保持1080×1920完整构图，字幕透明图层使用 `overlay y=150` 作为下移约两行后的起点；字体大小、行距仍按画面逐镜调整。DAY063 顶部版可作为旧版对照，但不再是默认位置。原讲解版式不随片头字幕位置改变。
- 字幕位置修改时，从无字幕头段重新烧录，不能叠在旧字幕上。完整片使用最新确认的片头，保留旧版并更新清单中的当前成片路径、哈希和验收状态。SRT交付仍保留，顶部位置由渲染配置保存。

- 默认 Omni 使用纯文生视频：不上传参考图、参考视频、WAV 或配音；常规生成可统一每段10秒、9:16、纯画面、无字、无声，回收后再按原旁白实际时长适配画面。只有用户明确要求音轨参考时，才用 `python3 scripts/package_mp4_references.py /absolute/recut-directory` 生成可上传参考MP4；原 WAV 始终只在本地用于最终配音。

- 优先复用本诗 `voice/cue-*-clean.wav`，结合 manifest 的 text 和实测时长验证；完整 narration.wav 中可能有长停顿。不要将混有音乐的音轨当作纯旁白。
- 字幕可以 SRT/ASS 保存。句内拆分结合实际录音的停顿和听辨，时长按字数估算只可作为待校对草稿。最后一条字幕不能超出最终视频。
- 若目标头段短于完整自然语音，先评估停顿；无法完整容纳时延长头段或明确阻塞，不能丢字。画面可以适度调速以适配音轨，配音无明确要求不变速。
- 按时间线采样数放置音频，按帧计算视频；将非整帧分段误差控制在一帧内，避免多个片段累计漂移。

## 去字与构图

- 区分硬字幕、软字幕、题头、错字。每段至少检查开始、中间、结束及文字变化时刻，动态文字不能只看一张图。
- 默认要求生成阶段直接得到无字源，并保持完整原始构图。发现硬字幕、书法、伪文字时优先重新生成，不得默认通过裁掉上下区域来去字，也不能把大面积 delogo 拉丝、模糊或遮盖称作无痕删除。
- 取段、裁切、像素修补属于兼容兜底，仅在用户明确接受时使用；任何兜底都不能损害主体、诗意或人物连续性。
- DAY060 的处理只是已接受的个案，不固定所有诗的裁切区域、取段秒数、顺序或镜头时长。

## 已确认的 DAY071 V3 默认范式

- 纯文生视频提示词：`out/omni/DAY071-song-you-ren-recut/DAY071-Omni-text-to-video-prompts-v2.md`；生成时不上传图片、视频或配音。
- 回收5段均为10秒、1080×1920；即使容器带生成音轨，也统一弃用，最终只恢复本机原豆包旁白。
- 画面保持完整原始构图，不裁切去字；每段只按对应原旁白 cue 时长做必要的视觉时长适配，旁白不加速。
- 已确认字幕头段：`out/omni/DAY071-song-you-ren-recut/DAY071-intro-lower-subtitles-v3.mp4`。
- 已确认完整成片：`out/omni/DAY071-song-you-ren-recut/DAY071-song-you-ren-complete-v3.mp4`，187.266667秒；该例原片译文切点为53秒，但其他 DAY 必须重新识别实际切点。

## 本机可用性经验

- 当前 ffmpeg 可用 H.264/AAC、concat，但曾没有 `ass` 滤镜；使用前通过 `ffmpeg -h filter=ass` 检查。
- 缺少字幕滤镜时，可用 Pillow 将每条字幕渲染为透明 PNG，以 overlay 和起止时间烧录，仍交付 SRT。字体先检查真实路径；本机曾使用 `/System/Library/Fonts/Supplemental/Songti.ttc`。
- 不假设 OpenCV 已安装或能联网安装。macOS AVFoundation 在本次环境曾解码失败；检查视频帧可直接用 ffmpeg。
- 手工新增代码用 apply_patch；脚本的正常运行可生成字幕、清单和媒体文件。不要复制带 DAY060 硬编码的脚本直接处理后续诗。

## 通用合并工具

```sh
python3 scripts/concat_videos.py --head /absolute/new-intro.mp4 --tail /absolute/original.mp4 --tail-start 53 --output /absolute/complete.mp4 --dry-run
python3 scripts/concat_videos.py --head /absolute/new-intro.mp4 --tail /absolute/original.mp4 --tail-start 53 --output /absolute/complete.mp4
```

`53` 只展示参数用法，必须替换为当前诗的实际切点。若 tail 已经是删去头段的文件，使用 `--tail-start 0`。脚本只检查技术参数、时长与解码，不自动批准画面和声音。输出不能覆盖任一输入，且已存在时停止。

## 已接受的 DAY060 结果

- 原片：项目目录下的 `out/final/ye-wang.mp4`，206 秒。
- 原切点：53 秒，剩余153秒译文与讲解。
- 用户返回五段动画中 Part4 实际是孤独诗人，Part5 是牧人猎马，故最终语义顺序为1、2、3、5、4。
- 硬字修补出现拉丝，最终采用取段和裁切。重新排列现成旁白，头段50秒，完整成片203秒。
- 已接受成片：项目目录下的 `out/final/DAY060-ye-wang-complete-203s.mp4`。
- 参考头段、字幕、联系表位于 `out/omni/day060-assembled/`。该目录的 `assemble.py` 是历史个案，不是通用执行器。
