# 古诗词 Omni 古风片头改剪 Skill

这是一个供 Codex 使用的古诗词视频改剪流程。它把**已有** DAY 古诗词学习视频的导入与完整原诗朗读部分，替换为 Omni 生成的古风动画，重新配回原旁白和字幕，再接上原视频的译文、解读等后段内容。

本仓库只包含 Skill 指令、参考说明和两个辅助脚本，**不包含**课程项目、原视频、音频、Omni 生成片段或付费平台账号。它不负责新建课程、自动批量发布，也不会覆盖已经发布的原片。

## 示例视频

| 示例一 | 示例二 | 示例三 |
| :---: | :---: | :---: |
| <video src="https://github.com/user-attachments/assets/51a49187-efdc-41cc-9762-8d9a8a6524ca" controls width="240"></video> | <video src="https://github.com/user-attachments/assets/32a0149e-7020-4130-bb7f-241f547365b5" controls width="240"></video> | <video src="https://github.com/user-attachments/assets/207b9f68-eef6-4e53-a2bd-a7f0dd9077e4" controls width="240"></video> |

## 适用范围与当前默认流程

- 适用于已经完成的 DAY 古诗词视频改剪，例如 DAY061-DAY090。一次只处理用户指定的 DAY；仅指定一首时，不自动处理整批。
- 默认采用已确认的 DAY071 V3 做法：向 Omni 提交**纯中文文字提示词**，生成 9:16、无字、无声的古风画面。不上传参考图、参考视频或旁白。
- 按导入和原诗语义分段生成画面。Omni 片段可以每段约 10 秒，但最终长度以原旁白实际时长为准，不为凑整改变语速。
- 用户把生成的视频交回 Codex 后，先检查画面与顺序，再弃用生成视频自带音轨，恢复原旁白，制作新字幕，并接回原视频的译文与讲解。
- 只有用户**明确要求**用原音轨作为 Omni 生成时序参考时，才使用兼容的 MP4 参考包流程。WAV 始终留在本地，不直接上传给 Omni。
- 不修改原学习模板、发布序号或发布台账；不自动向任何平台上传成片。

详细执行规则见 [SKILL.md](SKILL.md)，剪辑与验收细节见 [references/workflow.md](references/workflow.md)，提示词约束见 [references/omni-prompts.md](references/omni-prompts.md)。

## 安装前准备

1. 已安装 Codex，并能使用本机 Skill 目录。需要一个已有的 `knowledge-paper-template` 古诗词学习项目，且目标 DAY 已有原成片、课程数据、字幕/旁白 cue 和配音清单。本 Skill 不能凭空补齐这些源素材。
2. 安装 Python 3、FFmpeg 和 FFprobe；确认终端能运行 `python3 --version`、`ffmpeg -version` 和 `ffprobe -version`。两个随附脚本仅使用 Python 标准库，但调用 FFmpeg/FFprobe。
3. 准备可自行使用的 Omni 1.1 Flash 文生视频服务。生成操作由用户在平台完成，Codex 负责提示词、回收后的剪辑和验收。
4. 若本机 FFmpeg 缺少 ASS 字幕滤镜，而需要用透明 PNG 叠字方案，可额外安装 Pillow；它不是安装本 Skill 或运行两个随附脚本的必需依赖。

## 安装与更新

在 macOS 或 Linux 终端执行：

```sh
mkdir -p "$HOME/.codex/skills"
git clone https://github.com/pcyone/poetry-omni-intro-recut.git "$HOME/.codex/skills/poetry-omni-intro-recut"
```

若目录已存在，请先确认它是否有自己的修改；不要直接覆盖。以 Git 克隆方式安装的副本可这样更新：

```sh
git -C "$HOME/.codex/skills/poetry-omni-intro-recut" pull --ff-only
```

安装后在 Codex 中开启或重新载入会话，让它读取新 Skill。若你的 Codex 使用自定义技能目录，把仓库克隆到该目录，并确保目录结构中的 `SKILL.md` 位于 `poetry-omni-intro-recut/` 根目录。

## 使用方法

打开已有的 `knowledge-paper-template` 项目，然后向 Codex 说明目标 DAY。项目不在当前工作区时，附上项目的绝对路径。例如：

```text
按 poetry-omni-intro-recut 技能修改 DAY072 视频。
项目目录：/你的工作区/knowledge-paper-template
先核对原片、旁白和原诗结束切点，给我 Omni 1.1 Flash 纯文生视频的完整中文提示词；等我返回生成片段后再剪辑。
```

标准流程分两次交互：

1. Codex 从课程顺序、目标 episode、配音清单和原片定位诗题、slug、旁白节点及原诗结束切点。切点必须逐首实测，不能照搬其他 DAY 的秒数。
2. Codex 交付逐段中文提示词。每段明确场景、人物与镜头衔接，要求 9:16、无字幕/书法/伪文字/水印、无配音/音乐/环境声。此时流程停在等待用户生成素材。
3. 用户在 Omni 生成对应片段，将 MP4 文件路径交给 Codex，并说明哪段对应哪段；编号与画面语义不符时，以实际内容为准重新排序。
4. Codex 逐段检查画面与文字残留，按原旁白时长调整画面，重配音、制作 SRT 和新字幕，再接原片的译文/解读后段。硬字幕或生成错字原则上重新生成；裁切或修补须用户明确接受。
5. Codex 检查字幕、接点、完整口播、声音、画幅、时长、完整解码和关键帧。合格后交付完整 MP4、带字幕头段、无字幕头段、SRT，以及清单和验收记录。

交给 Codex 的本机素材通常位于项目的 `content/episodes.json`、`content/poetry/publish-sequence.json`、`public/episodes/<slug>/voice/manifest.json`、`out/final/<slug>.mp4`。实际结构以项目当前版本为准。改剪产物保存在独立的 `out/omni/DAYNNN-<slug>-recut/`，其中 `edit-manifest.json` 记录来源、切点、分镜、阶段、输出与哈希；不会占用新的 DAY 编号。

## 辅助脚本

### 合并头段与原讲解

`scripts/concat_videos.py` 负责统一编码并把新头段接到**当前诗实测的**原片切点之后。先用 `--dry-run` 检查，再正式运行。下例中的 `53` 仅演示参数，**不是通用切点**：

```sh
python3 scripts/concat_videos.py \
  --head /绝对路径/新片头.mp4 \
  --tail /绝对路径/原片.mp4 \
  --tail-start 53 \
  --output /绝对路径/完整成片.mp4 \
  --dry-run
```

确认无误后去掉 `--dry-run`。如果后段文件已经预先剪掉头段，设 `--tail-start 0`。输出不能覆盖任一输入，已存在的输出文件也不会被默认覆盖。脚本的技术检查不能替代人工视觉与听觉验收。

### 仅在明确要求时制作配音参考 MP4

`scripts/package_mp4_references.py` 是旧式音轨参考的兼容工具，**不是默认文生视频流程**。它要求改剪目录中已有 `edit-manifest.json`、对应的 `DAYNNN-omni-prompts.md`、`DAYNNN-intro-script.txt`，并且清单的 `segments` 包含可读取的音频路径和分段编号。运行前先备份或核对这两个文本文件及清单，因为脚本会更新提示词、清单并生成参考 MP4 与 ZIP：

```sh
python3 scripts/package_mp4_references.py /绝对路径/out/omni/DAYNNN-诗名-recut
```

输出的参考 MP4 是中性纯色画面加本地旁白音轨，只用来为 Omni 提供音频与时间基准，**不是最终动画**。最终成片仍应重新使用本机原旁白，弃用 Omni 返回视频的音轨。不要把 WAV 或带字的原视频上传到 Omni。

## 验收与边界

- 每首单独检查全部生成片段、字幕条目、接点前后、片尾声音和完整视频。无人工视觉检查时不能宣称视觉验收通过。
- 默认保留生成画面的完整构图，不用裁掉主体、模糊遮盖或有痕修补来冒充“去字幕”。
- 原片、原音频与发布记录不在本仓库中，也不应提交到公开仓库。请自行检查本地素材的授权、平台使用条款和发布权限。
- 需要替换正式发布版本时，应另外按原学习模板的发布验收流程执行；本 Skill 只产出独立改剪版本。

## 仓库文件

```text
SKILL.md                         Codex 执行入口与边界
agents/openai.yaml               Skill 展示元数据
references/workflow.md           时间线、字幕、质检与历史案例
references/omni-prompts.md       Omni 中文提示词约束
scripts/concat_videos.py         头段与原讲解合并
scripts/package_mp4_references.py 可选的 MP4 配音参考包
README.md                        本安装使用说明
```
