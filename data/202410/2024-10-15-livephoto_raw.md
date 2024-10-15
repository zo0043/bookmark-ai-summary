Title: LivePhoto: Real Image Animation with Text-guided Motion Control

URL Source: https://xavierchen34.github.io/LivePhoto-Page/

Markdown Content:
1The University of Hong Kong   2Alibaba Group   3Ant Group

Reference Image

![Image 1: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/1.png)

"\*hair flying in the wind."

![Image 2: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/1-The-woman-with-hair-flying-in-the-wind.gif)

Reference Image

![Image 3: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/6.png)

"The panda is eating bamboo."

![Image 4: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/6-The-panda-is-eating%20bamboo.gif)

Reference Image

![Image 5: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/4.png)

"The minion is jumping."

![Image 6: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/4-The-minion-is-jumping.gif)

Reference Image

![Image 7: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/10.png)

"The candles burn fast."

![Image 8: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/10-the-candles-burn-fast.gif)

Reference Image

![Image 9: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/11.png)

"Pouring water into the glass."

![Image 10: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/11-Pouring-water-into-the-glass..gif)

Reference Image

![Image 11: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/12.png)

"The fire is burning."

![Image 12: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/12-The-fire-is-burning-on-the-wood..gif)

Reference Image

![Image 13: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/7.png)

"\* camera from right to left."

![Image 14: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/7-Green-apple-camera-from-right-to-left.gif)

Reference Image

![Image 15: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/8.png)

"\* camera turns around."

![Image 16: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/8-grass%20stacks,%20camera%20turns%20around.gif)

Reference Image

![Image 17: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/9.png)

"\* camera-zooms-in."

![Image 18: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/9-A-pair-of-shoes,-camera-zooms-in-from-far-to-near.gif)

Reference Image

![Image 19: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/14.png)

"Snowflakes falling \*."

![Image 20: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/14-Snowflakes-falling-from-the-branches.gif)

Reference Image

![Image 21: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/13.png)

"Wind blows the sunflowers."

![Image 22: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/13-The-wind-blows-the-sunflowers.gif)

Reference Image

![Image 23: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/15.png)

"Fireworks bloom in the sky."

![Image 24: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Gallery_new/15-Fireworks-bloom-in-the-sky.gif)

Abstract
--------

Despite the recent progress in text-to-video generation, existing studies usually overlook the issue that only spatial contents but not temporal motions in synthesized videos are under the control of text. Towards such a challenge, this work presents a practical system, named **LivePhoto**, which allows users to animate an image of their interest with text descriptions. We first establish a strong baseline that helps a well-learned text-to-image generator (i.e., Stable Diffusion) take an image as a further input. We then equip the improved generator with a motion module for temporal modeling and propose a carefully designed training pipeline to better link texts and motions. In particular, considering the facts that (1) text can only describe motions roughly (e.g., regardless of the moving speed) and (2) text may include both content and motion descriptions, we introduce a motion intensity estimation module as well as a text re-weighting module to reduce the ambiguity of text-to-motion mapping. Empirical evidence suggests that our approach is capable of well decoding motion-related textual instructions into videos, such as actions, camera movements, or even conjuring new contents from thin air (e.g., pouring water into an empty glass). Interestingly, thanks to the proposed intensity learning mechanism, our system offers users an additional control signal (i.e., the motion intensity) besides text for video customization.

Motion Control with Text Instructions
-------------------------------------

Our unique feature is the precise motion control through text instructions. Furthermore, users have the ability to customize these motions by setting different "motion intensities".

Reference image

![Image 25: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Control/Lecun/LivePhoto.png)

"The man smiles."

![Image 26: GIF 1](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Control/Lecun/The-man-smiles-intens2.gif)

"The man gives a thumbs-up."

![Image 27: GIF 2](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Control/Lecun/2-The-man-gives-a-thumb-up..gif)

"The man is drinking beer."

![Image 28: GIF 3](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Control/Lecun/This-man-is-drinking-beer2.gif)

Motion Intensity: 2

![Image 29: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Control/Lecun/The-man-smiles-intens2.gif)

Motion Intensity: 5

![Image 30: GIF 1](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Control/Lecun/The-man-smiles-intens5.gif)

Motion Intensity: 3

![Image 31: GIF 2](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Control/Lecun/2-The-man-gives-a-thumb-up..gif)

Motion Intensity: 7

![Image 32: GIF 3](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Control/Lecun/The-man-gives-a-thumbs-up-intens72.gif)

Comparisons with Existing Alternatives
--------------------------------------

We conducted a comparative analysis of LivePhoto with GEN-2 and Pikalabs, specifically using their versions as of November 2023. The generated videos are presented sequentially from left to right, originating from GEN-2, Pikalabs, and then LivePhoto. Notably, LivePhoto demonstrates superior performance in text-guided motion control.

"Pikachu is dancing happily."

![Image 33: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Pikachu-is-dancing-happily/LivePhoto.png)

Reference Image

![Image 34: GIF 1](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Pikachu-is-dancing-happily/GEN-2.gif)

GEN-2

![Image 35: GIF 2](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Pikachu-is-dancing-happily/Pikalabs.gif)

Pikalabs

![Image 36: GIF 3](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Pikachu-is-dancing-happily/LivePhoto.gif)

LivePhoto

"Kung Fu Panda is practicing Tai Chi."

![Image 37: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Kung-Fu-Panda-is-practicing-Tai-Chi/LivePhoto.png)

Reference Image

![Image 38: GIF 1](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Kung-Fu-Panda-is-practicing-Tai-Chi/GEN-2.gif)

GEN-2

![Image 39: GIF 2](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Kung-Fu-Panda-is-practicing-Tai-Chi/Pikalabs.gif)

Pikalabs

![Image 40: GIF 3](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Kung-Fu-Panda-is-practicing-Tai-Chi/LivePhoto.gif)

LivePhoto

"The little yellow baby dinosaur is waving its hand."

![Image 41: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/The-little-yellow-baby-dinosaur-is-waving-its-hand/LivePhoto.png)

Reference Image

![Image 42: GIF 1](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/The-little-yellow-baby-dinosaur-is-waving-its-hand/GEN-2.gif)

GEN-2

![Image 43: GIF 2](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/The-little-yellow-baby-dinosaur-is-waving-its-hand/Pikalabs.gif)

Pikalabs

![Image 44: GIF 3](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/The-little-yellow-baby-dinosaur-is-waving-its-hand/LivePhoto.gif)

LivePhoto

"The volcano emits thick smoke from its crater."

![Image 45: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/The-volcano-emits-thick-smoke-from-its-crater/LivePhoto.png)

Reference Image

![Image 46: GIF 1](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/The-volcano-emits-thick-smoke-from-its-crater/GEN-2.gif)

GEN-2

![Image 47: GIF 2](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/The-volcano-emits-thick-smoke-from-its-crater/Pikalabs.gif)

Pikalabs

![Image 48: GIF 3](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/The-volcano-emits-thick-smoke-from-its-crater/LivePhoto.gif)

LivePhoto

"Lightning and thunder in the night sky."

![Image 49: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Lightning-and-thunder-in-the-night-sky/LivePhoto.png)

Reference Image

![Image 50: GIF 1](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Lightning-and-thunder-in-the-night-sky/GEN-2.gif)

GEN-2

![Image 51: GIF 2](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Lightning-and-thunder-in-the-night-sky/Pikalabs.gif)

Pikalabs

![Image 52: GIF 3](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Lightning-and-thunder-in-the-night-sky/LivePhoto.gif)

LivePhoto

"Fire burns on the grass stack."

![Image 53: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Fire-burns-on-the-grass-stack/LivePhoto.png)

Reference Image

![Image 54: GIF 1](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Fire-burns-on-the-grass-stack/GEN-2.gif)

GEN-2

![Image 55: GIF 2](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Fire-burns-on-the-grass-stack/Pikalab.gif)

Pikalabs

![Image 56: GIF 3](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Fire-burns-on-the-grass-stack/LivePhoto.gif)

LivePhoto

"Dew dripping from the leaves."

![Image 57: image](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Dew-dripping-from-the-leaves/LivePhoto.png)

Reference Image

![Image 58: GIF 1](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Dew-dripping-from-the-leaves/GEN-2.gif)

GEN-2

![Image 59: GIF 2](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Dew-dripping-from-the-leaves/Pikalabs.gif)

Pikalabs

![Image 60: GIF 3](https://xavierchen34.github.io/LivePhoto-Page/generate_images/Compare/Dew-dripping-from-the-leaves/LivePhoto.gif)

LivePhoto

Pipeline
--------

Overall pipeline of LivePhoto is shown below, besides taking the reference image and text as input, LivePhoto leverages the motion intensity as a supplementary condition. The image and the motion intensity (from level 1 to 10) are obtained from the ground truth video during training and customized by users during inference. The reference latent is first extracted as local content guidance. We concatenate it with the noise latent, a frame embedding, and the intensity embedding. This 10-channel tensor is fed into the UNet for denoising. During inference, we use the inversion of the reference latent instead of the pure Gaussian to provide content priors. At the top, a content encoder extracts the visual tokens to provide global content guidance. At the bottom, we introduce text re-weighting, which learns to emphasize the motion-related part of the text embedding for better text-motion mapping. The visual and textual tokens are injected into the UNet via cross-attention. For the UNet, we freeze the pre-trained stable diffusion and insert motion modules to capture the inter-frame relations. Symbols of flames and snowflakes denote trainable and frozen parameters respectively.

![Image 61: pipeline](https://xavierchen34.github.io/LivePhoto-Page/static/images/pipeline.png)

Video Introduction
------------------
