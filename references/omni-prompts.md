# Omni 无字幕动画提示词

默认采用纯文生视频。每一段单独写清：目标时长、第一帧场景、段内镜头与动作、人物服饰及跨段连续性、末帧衔接，以及全程无字无声约束。不上传参考MP4、图片、WAV或配音；原旁白仅在本地后期恢复。不要把下方说明中的占位词原样交付。

纯文生视频默认统一强调：9:16竖屏、纯画面、无声；禁止字幕、诗句、标题、作者名、书法、印章、牌匾文字、旗帜文字、卷轴/石碑题字、水印、Logo、UI、英文、数字、伪汉字和乱码。人物不说话、不做朗读口型。建筑等容易生成字的位置应保持空白或避免出现文字载体。

常规可将每段生成时长统一为10秒，后期按本机原旁白 cue 的真实时长剪辑或做温和视觉变速；不要为了匹配10秒生成片而改变旁白语速。人物一致性只约束有人物的镜头，不强制给动物或空景加入诗人。结尾保持完整场景，禁止自动生成卷轴、挂画、印章或字卡。

仅当用户明确要求上传原音轨作为 Omni 时序参考时，才启用下方兼容约束；默认纯文生视频不使用参考MP4：

```text
Create a 9:16 ancient Chinese poetic animation. Follow the actual supplied narration's meaning and timing, using restrained ink-wash textures, subtle mineral colors, and smooth camera movement. Keep the same poet's face, age, hairstyle and clothing across scenes.

Use the supplied narration only as the timing and semantic reference. Do not re-voice, clone, paraphrase, retime or add speech. Do not add singing, music, ambience or sound effects. Deliver silent visuals if you cannot preserve the exact supplied audio; the original narration will be restored in Codex.

Generate text-free visuals. Do not reproduce subtitles, poem text, titles, author names, calligraphy, labels, logos, pseudo-characters or text layouts from any reference video. Keep scrolls and signs blank. Do not generate end-card text. All captions will be added in Codex after editing. Avoid lip-sync close-ups and speaking presenters.
```

提示词只能表达约束，不能保证生成模型原样保留声音或完全不出字。回收后必须检查画面并挂回原始旁白。

不要使用“音乐不要盖过旁白”等容许新增声音的旧表述。不要为没有朗读到的诗句提前安排主体动作。十秒片段可能包含上一句尾声或下一句开头，按音轨实际内容安排。
