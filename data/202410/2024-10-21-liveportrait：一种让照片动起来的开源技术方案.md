# LivePortrait：一种让照片动起来的开源技术方案
- URL: https://juejin.cn/post/7398461918906531850
- Added At: 2024-10-21 03:57:42
- [Link To Text](2024-10-21-liveportrait：一种让照片动起来的开源技术方案_raw.md)

## TL;DR
LivePortrait 是一个开源项目，能让静态照片动起来。通过上传照片和视频素材，生成动态视频。应用于怀念视频、风格转换等。技术基于隐式关键点框架，高效可控。支持视频编辑，提供安装包简化使用。项目地址在 Huggingface 和 GitHub。

## Summary
1. **项目介绍**：LivePortrait 是一个开源项目，主要功能是让静态照片动起来。

2. **使用方法**：
   - 需要提供两个素材：
     - 第一个素材：指定要让谁动，通常是静态照片。
     - 第二个素材：指定如何动，通常是动态视频。
   - 将素材上传至 LivePortrait 网站，点击确定后即可生成动态视频。

3. **应用场景**：
   - 制作亲人照片怀念视频、萌宠搞怪视频等。
   - 可以用于改变视频中人物的表情和风格，如将冷酷风改为嘻哈风。

4. **技术原理**：
   - LivePortrait 是基于隐式关键点的框架，平衡了计算效率和可控性。
   - 使用了混合图像-视频训练策略，升级网络架构，并设计了更好的运动转换和优化目标。
   - 框架在 RTX 4090 GPU 上使用 PyTorch 的生成速度显著达到 12.8 毫秒。

5. **搭建方法**：
   - 使用 conda 创建新环境，并安装项目所需的依赖。
   - 下载项目源码，并进入项目目录。
   - 下载模型权重，并放置到指定文件夹。
   - 准备好素材后，使用 `python inference.py` 命令进行生成。

6. **项目更新**：
   - 7月19日，框架开始支持视频编辑，即 v2v。
   - 7月25日，官方发布了安装包，可以通过下载安装包直接使用。

7. **项目地址**：
   - 官方网站：[huggingface.co/spaces/KwaiVGI/LivePortrait](https://huggingface.co/spaces/KwaiVGI/LivePortrait)
   - 项目源码：[github.com/KwaiVGI/LivePortrait](https://github.com/KwaiVGI/LivePortrait)
