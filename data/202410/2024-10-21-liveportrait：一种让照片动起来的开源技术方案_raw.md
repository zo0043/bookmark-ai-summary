Title: LivePortrait：一种让照片动起来的开源技术方案让静态照片动起来。 你要提供两个素材，第一个素材是让谁动。 第二 - 掘金

URL Source: https://juejin.cn/post/7398461918906531850

Markdown Content:
有一款开源项目，它主要功能就是让静态照片动起来。

你只需要提供两个素材，第一个素材是让谁动。就比如下面的这个兵马俑。

![Image 1](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/ee90c5bf3065488c831672e6d1c5c912~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgVEbnlLflrak=:q75.awebp?rk3s=f64ab15b&x-expires=1730004299&x-signature=sh8F6QjiCXMSkojx%2BR05eLftdSo%3D)

第二个素材是如何动，就比如下面这个视频。

![Image 2](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/c3cdce81a4d5438680990bd13cdc0fa7~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgVEbnlLflrak=:q75.awebp?rk3s=f64ab15b&x-expires=1730004299&x-signature=FfB9cI%2FGvGxvMIB%2BmtHUIuiG5aw%3D)

然后，将这俩数据交给开源项目处理，最终就得出如下结果。

![Image 3](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/442447bf2cd745a883f47a1ddd247b6d~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgVEbnlLflrak=:q75.awebp?rk3s=f64ab15b&x-expires=1730004299&x-signature=PPLSEyqllhJSSvNuKWJN4IF2dsI%3D)

不但对一个人有效，多个人也可以了。

![Image 4](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/1e6aeef3dab3487f8a04e7d8b72e361a~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgVEbnlLflrak=:q75.awebp?rk3s=f64ab15b&x-expires=1730004299&x-signature=4REC1E5Gi2%2FjqK6IX0hp0WGOC%2Bk%3D)

不但对人类有效，萌宠动物或者二次元也行。

![Image 5](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/ae66f1113ddf4e5aa6c22482a6af8d7f~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgVEbnlLflrak=:q75.awebp?rk3s=f64ab15b&x-expires=1730004299&x-signature=LZozExxZsbmSW29p9pv%2FQd%2FnOaU%3D)

试用网址是：[huggingface.co/spaces/Kwai…](https://link.juejin.cn/?target=https%3A%2F%2Fhuggingface.co%2Fspaces%2FKwaiVGI%2FLivePortrait "https://huggingface.co/spaces/KwaiVGI/LivePortrait") 这个网址是研究和学习用的。

只需要上传那两个素材，然后点击确定。 ![Image 6](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/ee5d92f049e649e686e6e034676370e9~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgVEbnlLflrak=:q75.awebp?rk3s=f64ab15b&x-expires=1730004299&x-signature=LkAuiKq9OtpwcSTMB9O9LvpK7g0%3D)

就可以获得一个会动的视频。

![Image 7](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/67c701e8e2464e15806c9cda41d72bb2~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgVEbnlLflrak=:q75.awebp?rk3s=f64ab15b&x-expires=1730004299&x-signature=ljzhgkTt%2BlnMrtAHFyTEmWYAYTM%3D)

好了。上面这些操作，其实就可以卖钱了。

有很多人利用信息差，白嫖这项开源技术。用上面的网址，制作一些亲人照片怀念视频、萌宠搞怪视频进行售卖。你得开个会员，或者花上九块九才能使用一次。

下面部分内容是给技术人员看的。如果你对此感兴趣，想进一步了解其中的原理，可以继续阅读。

这项开源框架叫LivePortrait，它是具有拼接和重定向控制的高效肖像动画。它的论文概要内容如下：

![Image 8](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/6eea3e5b184b4a6da9c6758b954d608c~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgVEbnlLflrak=:q75.awebp?rk3s=f64ab15b&x-expires=1730004299&x-signature=2LMWzcnZE6UGAyaExQ116rV4cu4%3D)

肖像动画旨在从单一源图像合成逼真的视频，将其用作外观参考。我们没有遵循主流的基于扩散的方法，而是探索和扩展了基于隐式关键点的框架的潜力，从而有效地平衡了计算效率和可控性。为了提高生成质量和泛化能力，我们将训练数据扩展到大约6900万个高质量帧，采用混合图像-视频训练策略，升级网络架构，并设计更好的运动转换和优化目标。此外，我们发现紧凑的隐式关键点可以有效地表示一种混合形状，并精心提出了一个拼接和两个重新定位模块，它们利用一个计算开销可忽略不计的小型MLP来增强可控性。实验结果表明，与基于扩散的方法相比，我们的框架是有效的。在RTX 4090 GPU上使用 PyTorch的生成速度显著达到12.8毫秒。推理代码和模型可在 [github.com/KwaiVGI/Liv…](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2FKwaiVGI%2FLivePortrait "https://github.com/KwaiVGI/LivePortrait") 获得。

技术人员如何自己搭建呢？

对于技术人员，最直观的方式就是去官方的ReadMe.md文档查看 [github.com/KwaiVGI/Liv…](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2FKwaiVGI%2FLivePortrait "https://github.com/KwaiVGI/LivePortrait")

![Image 9](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/2b3e62e252ad44b2a030d470c2836991~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgVEbnlLflrak=:q75.awebp?rk3s=f64ab15b&x-expires=1730004299&x-signature=eZye6t4jmyZToxQdt7D3QKQ0SKI%3D)

这里面不但有入门操作，项目源码，还有版本更新说明。

比如在7月19日，框架开始支持视频编辑，又名v2v。照片到视频是p2v，即picture to video。v2v就是视频到视频。

图片到视频是让静态图片动起来，感觉很有用。

但是视频到视频有什么用呢？

举个例子，比如有个美女跳舞，她走的是冷酷风。但是老板想让她走嘻哈风，但是美女就是不从。这时就可以找个爱笑的女孩子，通过v2v让不爱笑的美女笑起来。

![Image 10](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/a0c160a733e84e81833fa75bedbe950d~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgVEbnlLflrak=:q75.awebp?rk3s=f64ab15b&x-expires=1730004299&x-signature=CBIAWEmjEeNWvv7hleQ8eeEkl8Q%3D)

其实，你们网上看得那些武松和潘金莲、孙悟空和白骨精的改编版，估计用的也是v2v这项技术。

好了，下面就说说如何搭建和使用。7月25日，官方发布了安装包，可以通过下载安装包直接使用。甚至连搭建都不用了。解压即可使用。

![Image 11](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/46d45ca255974fba9ecf454eec04834f~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgVEbnlLflrak=:q75.awebp?rk3s=f64ab15b&x-expires=1730004299&x-signature=rwQyYDJyMSRCDi%2Fxz2ol1aEd7%2FQ%3D)

两个下载地址如下：

*   [huggingface.co/cleardusk/L…](https://link.juejin.cn/?target=https%3A%2F%2Fhuggingface.co%2Fcleardusk%2FLivePortrait-Windows%2Ftree%2Fmain "https://huggingface.co/cleardusk/LivePortrait-Windows/tree/main")
    
*   [pan.baidu.com/s/1FWsWqKe0…](https://link.juejin.cn/?target=https%3A%2F%2Fpan.baidu.com%2Fs%2F1FWsWqKe0eNfXrwjEhhCqlw%3Fpwd%3D86q2 "https://pan.baidu.com/s/1FWsWqKe0eNfXrwjEhhCqlw?pwd=86q2")
    

如果，你还有执念，就是想自己搭建，并且融于到自己的产品中。那么继续往下看。

我们用conda管理环境，首先要准备一个新环境。相当于给项目批了一块地。

```
conda create -n LivePortrait python=3.9
conda activate LivePortrait
```

然后，将源码下载下来，存放到一个位置。并且进入文件目录。

```
git clone https://github.com/KwaiVGI/LivePortrait
cd LivePortrait
```

下载源码，可以用git形式。也可以直接下载zip文件。

第三步，准备运行支持环境。上面新建了一个环境，批了一块地。现在要进行装修和水电网的铺设。安装采用pip。

```
# Linux和Windows用户执行这个
pip install -r requirements.txt
# macOS用户用这个
pip install -r requirements_macOS.txt
```

requirements.txt里面是：

```
-r requirements_base.txt
onnxruntime-gpu==1.18.0
```

requirements\_macOS.txt里面是：

```
-r requirements_base.txt
onnxruntime-silicon==1.16.3
```

他们都有requirements\_base.txt，然后区分了一些系统特性。

我们看requirements\_base.txt里面是这样：

```
--extra-index-url https://download.pytorch.org/whl/cu118
torch==2.3.0
torchvision==0.18.0
torchaudio==2.3.0

numpy==1.26.4
pyyaml==6.0.1
opencv-python==4.10.0.84
scipy==1.13.1
imageio==2.34.2
lmdb==1.4.1
tqdm==4.66.4
rich==13.7.1
ffmpeg-python==0.2.0
onnx==1.16.1
scikit-image==0.24.0
albumentations==1.4.10
matplotlib==3.9.0
imageio-ffmpeg==0.5.1
tyro==0.8.5
gradio==4.37.1
pykalman==0.9.7
```

很明显，它是需要GPU的。就算是你下载上面那个windows版本的压缩包，也需要你电脑具有GPU。

准备完环境就具备了运行资格。下一步是下载模型权重。不用你训练，只需要你下载人家训练好的模型，放到你电脑中使用即可。

官方的给出的方式比较国际化：

```
git clone https://huggingface.co/KwaiVGI/LivePortrait temp_pretrained_weights
mv temp_pretrained_weights/* pretrained_weights/
rm -rf temp_pretrained_weights
```

其实，在实际操作中，一般很难执行。最好还是去用浏览器下载，然后放到文件目录中。

以下是百度云下载地址：

*   [pan.baidu.com/share/init?…](https://link.juejin.cn/?target=https%3A%2F%2Fpan.baidu.com%2Fshare%2Finit%3Fsurl%3DMGctWmNla_vZxDbEp2Dtzw%26pwd%3Dz5cn "https://pan.baidu.com/share/init?surl=MGctWmNla_vZxDbEp2Dtzw&pwd=z5cn")

下载完了，让文件解压并将它们放在./pretrained\_weights。其实这一步和上面命令行执行的步骤一样。哪一个能走通，更好实现，就走哪一步。

但是，不管怎样，你要确保最终存放模型的文件夹里是这样的结构：

```
pretrained_weights
├── insightface
│   └── models
│       └── buffalo_l
│           ├── 2d106det.onnx
│           └── det_10g.onnx
└── liveportrait
    ├── base_models
    │   ├── appearance_feature_extractor.pth
    │   ├── motion_extractor.pth
    │   ├── spade_generator.pth
    │   └── warping_module.pth
    ├── landmark.onnx
    └── retargeting_models
        └── stitching_retargeting_module.pth
```

最后一步啦，最后一步！开始享受使用过程！准备好两类素材，一个让什么动，一般是图片(假设名字叫p.jpg)。另一个如何动，一般是视频(假设名字叫v.mp4)。然后在环境中，在项目目录下，执行以下命令：

```
python inference.py -s p.jpg -d v.mp4
```

此时会在animations文件夹下生成结果。

如果你一时间找不到素材，也可以使用项目里提供的素材。位置在 assets/examples/下。里面有图片也有视频。

![Image 12](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/1184ba5d1329470cab4a9c146dc730c5~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgVEbnlLflrak=:q75.awebp?rk3s=f64ab15b&x-expires=1730004299&x-signature=9o3C7Hwu9x1E%2Ff2sI42QGKcrjEY%3D)

如果想要操作视频到视频，命令如下：

```
python inference.py -s v1.mp4 -d v2.mp4
```

关于更多的内容，开发者可以去看官方说明，里面讲解的很详细。
