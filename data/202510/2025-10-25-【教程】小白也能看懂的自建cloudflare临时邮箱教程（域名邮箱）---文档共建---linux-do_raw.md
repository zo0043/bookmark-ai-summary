Title: 【教程】小白也能看懂的自建Cloudflare临时邮箱教程（域名邮箱） - 文档共建 - LINUX DO

URL Source: https://linux.do/t/topic/316819

Published Time: 2025-06-15T15:43:58+00:00

Markdown Content:
[Skip to main content](https://linux.do/t/topic/316819#main-container)

*   [写在前面](https://linux.do/t/topic/316819#p-3040413-h-1)

*   [注意](https://linux.do/t/topic/316819#p-3040413-h-2)

*   [我为什么想搭临时邮箱？](https://linux.do/t/topic/316819#p-3040413-h-3)

*   [临时邮箱有什么好处？](https://linux.do/t/topic/316819#p-3040413-h-4)

*   [什么是临时邮箱？](https://linux.do/t/topic/316819#p-3040413-h-5)

*   [准备](https://linux.do/t/topic/316819#p-3040413-h-6)

*   [关于域名](https://linux.do/t/topic/316819#p-3040413-h-7)

*   [项目原作者](https://linux.do/t/topic/316819#p-3040413-h-8)

*   [第一步，将域名交给Cloudflare托管](https://linux.do/t/topic/316819#p-3040413-cloudflare-9)
    *   [打开Clouflare，配置转移域](https://linux.do/t/topic/316819#p-3040413-clouflare-10)
    *   [打开域名服务商，这里以我的腾讯为例，其它平台都是同理的](https://linux.do/t/topic/316819#p-3040413-h-11)
    *   [回到Cloudflare继续，一般改过之后需要等一阵子才会生效（大概10分钟）](https://linux.do/t/topic/316819#p-3040413-cloudflare10-12)
    *   [如果你不需要搭临时邮箱服务，只需要自己的域名邮箱](https://linux.do/t/topic/316819#p-3040413-h-13)

*   [搭建临时邮箱服务](https://linux.do/t/topic/316819#p-3040413-h-14)
    *   [创建D1数据库](https://linux.do/t/topic/316819#p-3040413-d1-15)
    *   [打开项目地址，找到db/schema.sql](https://linux.do/t/topic/316819#p-3040413-dbschemasql-16)
    *   [部署邮箱服务后端](https://linux.do/t/topic/316819#p-3040413-h-17)

*   [nodejs_compat可以在这里复制！](https://linux.do/t/topic/316819#p-3040413-nodejs_compat-18)
    *   [然后我们返回，继续配置D1数据库！](https://linux.do/t/topic/316819#p-3040413-d1-19)
    *   [接下来，我们设置环境变量](https://linux.do/t/topic/316819#p-3040413-h-20)

*   [ADMIN_PASSWORDS](https://linux.do/t/topic/316819#p-3040413-admin_passwords-21)

*   [DEFAULT_DOMAINS](https://linux.do/t/topic/316819#p-3040413-default_domains-22)

*   [DOMAINS](https://linux.do/t/topic/316819#p-3040413-domains-23)

*   [USER_ROLES](https://linux.do/t/topic/316819#p-3040413-user_roles-24)
    *   [如何配置？看图](https://linux.do/t/topic/316819#p-3040413-h-25)
    *   [配置KV缓存](https://linux.do/t/topic/316819#p-3040413-kv-26)
    *   [配置邮件转发【非常重要，必须配置】](https://linux.do/t/topic/316819#p-3040413-h-27)

*   [搭建前端服务，也就是操作界面！](https://linux.do/t/topic/316819#p-3040413-h-28)

*   [【注意】这里图片里打错字了，图片里说的是“自定义域”，我打成了“兹定于”](https://linux.do/t/topic/316819#p-3040413-h-29)

*   [测试是否正常](https://linux.do/t/topic/316819#p-3040413-h-30)
    *   [创建用户](https://linux.do/t/topic/316819#p-3040413-h-31)
    *   [测试接收邮件](https://linux.do/t/topic/316819#p-3040413-h-32)

*   [调用API创建邮件获取邮件（请根据实际情况去修改代码！这是之前测试用的代码！）](https://linux.do/t/topic/316819#p-3040413-api-33)

*   [关于发送邮件](https://linux.do/t/topic/316819#p-3040413-h-34)

*   [另外一个佬友写的发送邮件教程](https://linux.do/t/topic/316819#p-3040413-h-35)

*   [结束](https://linux.do/t/topic/316819#p-3040413-h-36)

*   [最后接好运](https://linux.do/t/topic/316819#p-3040413-h-37)

*   [祝佬友们也好运连连！](https://linux.do/t/topic/316819#p-3040413-h-38)

[![Image 1: 小黄](https://linux.do/user_avatar/linux.do/xiaohuang/48/338864_2.png)](https://linux.do/u/xiaohuang)

### [](https://linux.do/t/topic/316819#p-3040413-h-1)写在前面

我一开始也没怎么用过Cloudflare，就最早的时候是用它来部署过Openai的接口中转，防止被墙（已经是很早很早之前的事情了，已经失效了），然后呢那天我打开[cloudflare临时邮箱项目的官方教程文档](https://temp-mail-docs.awsl.uk/)，给我搞的一脸懵的，不过好在最后是成功搭建好了！写这个教程，也是为了帮助那些想搭，但是弄不明白的佬友，希望可以帮到你！

### [](https://linux.do/t/topic/316819#p-3040413-h-2)注意

此为临时邮箱，**如果你需要注册自己觉得比较重要的平台且账号数据需要保留的情况下，请不要使用临时邮箱注册！！！** 除非你打算一直使用你的域名邮箱！且自己有能力一直维护自己的邮箱服务！

### [](https://linux.do/t/topic/316819#p-3040413-h-3)我为什么想搭临时邮箱？

起初是一天晚上，半夜没睡着，然后不知道抽什么风，就想去域名注册看看，看能不能弄个好看点的域名，然后我试啊试，最终注册了一个`goai.love`，我想着不浪费的情况下，用它来做点什么，于是首先想到的就是搭建临时邮箱供给自己的朋友们一起使用，**对打算搭个私有的临时邮箱**

### [](https://linux.do/t/topic/316819#p-3040413-h-4)临时邮箱有什么好处？

我们知道，很多平台注册都会使用到邮箱，我们见过的常用邮箱有 `gmail`、`qq`、`163`等，一般会给一个固定的前缀，例如`xiaohuang@qq.com`，这时，你会发现注册`cursor`，`openai`，`claude`你只能用一个邮箱来注册，无法多次注册！**说人话就是方便你可以无限注册薅羊毛**（当然我也知道gmail可以有特殊的办法使它前缀不一致发送给同一个邮箱，我没试过就不说啦）

### [](https://linux.do/t/topic/316819#p-3040413-h-5)什么是临时邮箱？

标题上已经写了，它其实就是域名邮箱，只是我们用到的这个项目取名叫做**临时邮箱**，它是通过你自己购买的域名来在Cloudflare上搭建一个邮箱服务来实现的，所以你也可以叫它自建域名邮箱

### [](https://linux.do/t/topic/316819#p-3040413-h-6)准备

*   至少一个域名
*   Cloudflare账号，你可以注册一个，官网：[https://www.cloudflare.com/](https://www.cloudflare.com/)
*   cloudflare_temp_email项目代码（记得给作者点个star）：[GitHub - dreamhunter2333/cloudflare_temp_email: CloudFlare free temp domain email 免费收发 临时域名邮箱 支持附件 IMAP SMTP TelegramBot](https://github.com/dreamhunter2333/cloudflare_temp_email)
*   临时邮箱搭建官方文档：[https://temp-mail-docs.awsl.uk/](https://temp-mail-docs.awsl.uk/) （佬友也可以去看官方文档搭建）

### [](https://linux.do/t/topic/316819#p-3040413-h-7)关于域名

*   你可以寻找便宜的服务商去注册，我一般会在阿里云、腾讯云买域名，比如我为了写教程就买了一个`linuxdo.love`
*   如果你想便宜，那就用不常见的后缀且域名前缀给长一点，不要学我，我这个域名续费180一年，18首年！
*   在买域名的时候，你可以注意一下之后续费是多少钱一年，如果看不到，你可以尝试把1年加到2年一般就可以看到之后续费的价格了

### [](https://linux.do/t/topic/316819#p-3040413-h-8)项目原作者

### [](https://linux.do/t/topic/316819#p-3040413-cloudflare-9)第一步，将域名交给Cloudflare托管

#### [](https://linux.do/t/topic/316819#p-3040413-clouflare-10)打开Clouflare，配置转移域

[![Image 2: image](https://linux.do/uploads/default/optimized/4X/a/9/8/a9814c155afe545d275c5d5d048f066aacaab66e_2_690x353.png)](https://linux.do/uploads/default/original/4X/a/9/8/a9814c155afe545d275c5d5d048f066aacaab66e.png "image")

[![Image 3: image](https://linux.do/uploads/default/optimized/4X/9/0/7/90758f146a4e889c366d31c698b269933e25fe50_2_690x432.png)](https://linux.do/uploads/default/original/4X/9/0/7/90758f146a4e889c366d31c698b269933e25fe50.png "image")

[![Image 4: image](https://linux.do/uploads/default/optimized/4X/7/3/7/7372518d0521803b1186a2aaa6306e8dd5a504b4_2_690x494.png)](https://linux.do/uploads/default/original/4X/7/3/7/7372518d0521803b1186a2aaa6306e8dd5a504b4.png "image")

[![Image 5: image](https://linux.do/uploads/default/optimized/4X/7/6/2/7622c464f089c194dee73fd884be0a75b507d162_2_690x356.png)](https://linux.do/uploads/default/original/4X/7/6/2/7622c464f089c194dee73fd884be0a75b507d162.png "image")

[![Image 6: image](https://linux.do/uploads/default/optimized/4X/5/f/3/5f315b7c9e5459b355378af5908b1d7b8a66e33f_2_641x500.png)](https://linux.do/uploads/default/original/4X/5/f/3/5f315b7c9e5459b355378af5908b1d7b8a66e33f.png "image")

#### [](https://linux.do/t/topic/316819#p-3040413-h-11)打开域名服务商，这里以我的腾讯为例，**其它平台都是同理的**

[![Image 7: image](https://linux.do/uploads/default/optimized/4X/6/a/1/6a1eda112363e93cce9b90f6097308954c9b4118_2_690x398.png)](https://linux.do/uploads/default/original/4X/6/a/1/6a1eda112363e93cce9b90f6097308954c9b4118.png "image")

[![Image 8: image](https://linux.do/uploads/default/original/4X/7/1/8/718dc8ae937b5c4324040facc68b22d3f9ab8f61.png)](https://linux.do/uploads/default/original/4X/7/1/8/718dc8ae937b5c4324040facc68b22d3f9ab8f61.png "image")

[![Image 9: image](https://linux.do/uploads/default/optimized/4X/e/0/6/e06f24e121f3f7b4367c9b3da002c50f294fb1f1_2_690x218.png)](https://linux.do/uploads/default/original/4X/e/0/6/e06f24e121f3f7b4367c9b3da002c50f294fb1f1.png "image")

[![Image 10: image](https://linux.do/uploads/default/optimized/4X/3/1/a/31accf425fd3b51934d1abf73bf489dacedb8473_2_578x500.png)](https://linux.do/uploads/default/original/4X/3/1/a/31accf425fd3b51934d1abf73bf489dacedb8473.png "image")

[![Image 11: image](https://linux.do/uploads/default/optimized/4X/2/4/8/248d769358bb9f769486decb61e9fa125625c98d_2_690x464.png)](https://linux.do/uploads/default/original/4X/2/4/8/248d769358bb9f769486decb61e9fa125625c98d.png "image")

[![Image 12: image](https://linux.do/uploads/default/original/4X/e/c/c/ecc583c08aadfe9d1de0a378c52b5a73166007c7.png)](https://linux.do/uploads/default/original/4X/e/c/c/ecc583c08aadfe9d1de0a378c52b5a73166007c7.png "image")

#### [](https://linux.do/t/topic/316819#p-3040413-cloudflare10-12)回到Cloudflare继续，一般改过之后需要等一阵子才会生效（大概10分钟）

[![Image 13: image](https://linux.do/uploads/default/optimized/4X/7/5/e/75e0a0c2ddd77356973a7a3fb44e102449a36759_2_593x500.png)](https://linux.do/uploads/default/original/4X/7/5/e/75e0a0c2ddd77356973a7a3fb44e102449a36759.png "image")

[![Image 14: image](https://linux.do/uploads/default/optimized/4X/1/7/0/170b29f85aa5b28b84806fb504c53e78d2a8f021_2_538x500.png)](https://linux.do/uploads/default/original/4X/1/7/0/170b29f85aa5b28b84806fb504c53e78d2a8f021.png "image")

[![Image 15: image](https://linux.do/uploads/default/optimized/4X/a/7/d/a7d614fcc835c0295aa2828458b8765450fb3bd6_2_690x369.png)](https://linux.do/uploads/default/original/4X/a/7/d/a7d614fcc835c0295aa2828458b8765450fb3bd6.png "image")

[![Image 16: image](https://linux.do/uploads/default/optimized/4X/1/4/0/14070cac6e5a4c77ebf9681d3c988ee6f4d4e1f9_2_655x499.png)](https://linux.do/uploads/default/original/4X/1/4/0/14070cac6e5a4c77ebf9681d3c988ee6f4d4e1f9.png "image")

[![Image 17: image](https://linux.do/uploads/default/optimized/4X/c/0/c/c0c03e387845aec494dbda7202e3bbedf9131a9e_2_690x323.png)](https://linux.do/uploads/default/original/4X/c/0/c/c0c03e387845aec494dbda7202e3bbedf9131a9e.png "image")

[![Image 18: image](https://linux.do/uploads/default/optimized/4X/1/5/4/154c9e7f44aeb9bfee6493053f532596ae8c204a_2_677x499.png)](https://linux.do/uploads/default/original/4X/1/5/4/154c9e7f44aeb9bfee6493053f532596ae8c204a.png "image")

[![Image 19: image](https://linux.do/uploads/default/optimized/4X/5/f/7/5f7ec64564ac49354086959ff63236a61c14c760_2_690x411.png)](https://linux.do/uploads/default/original/4X/5/f/7/5f7ec64564ac49354086959ff63236a61c14c760.png "image")

[![Image 20: image](https://linux.do/uploads/default/optimized/4X/4/e/4/4e400b526591105b7b6f9aa86a33423406474f37_2_690x350.png)](https://linux.do/uploads/default/original/4X/4/e/4/4e400b526591105b7b6f9aa86a33423406474f37.png "image")

[![Image 21: image](https://linux.do/uploads/default/optimized/4X/4/b/4/4b460f6a7d161bdb7052a39c52b643c542101596_2_690x453.png)](https://linux.do/uploads/default/original/4X/4/b/4/4b460f6a7d161bdb7052a39c52b643c542101596.png "image")

[![Image 22: image](https://linux.do/uploads/default/optimized/4X/d/4/b/d4b94f268e55de3277795b6b15f5c54719c35334_2_690x286.png)](https://linux.do/uploads/default/original/4X/d/4/b/d4b94f268e55de3277795b6b15f5c54719c35334.png "image")

#### [](https://linux.do/t/topic/316819#p-3040413-h-13)如果你不需要搭临时邮箱服务，只需要自己的域名邮箱

自此你可以设置成**发送到电子邮件**，也就是说这个`xxx所有的邮件@linuxdo.love`都会转发到你指定的邮箱里去

 例如：

*   xiaohuang@linuxdo.love → [xiaohuang@qq.com](mailto:xiaohuang@qq.com)
*   ilovelinuxdo@linuxdo.love → [xiaohuang@qq.com](mailto:xiaohuang@qq.com)

[![Image 23: image](https://linux.do/uploads/default/optimized/4X/f/3/4/f34b5449f16bf3e9be3f99ee7d2a21fef13f809d_2_689x368.png)](https://linux.do/uploads/default/original/4X/f/3/4/f34b5449f16bf3e9be3f99ee7d2a21fef13f809d.png "image") 

如果你需要继续搭建临时邮箱，**请往下看！**

### [](https://linux.do/t/topic/316819#p-3040413-h-14)搭建临时邮箱服务

#### [](https://linux.do/t/topic/316819#p-3040413-d1-15)创建D1数据库

[![Image 24: image](https://linux.do/uploads/default/optimized/4X/3/c/7/3c73f255108dc3f9920632b2b32b81396b12aae0_2_690x400.png)](https://linux.do/uploads/default/original/4X/3/c/7/3c73f255108dc3f9920632b2b32b81396b12aae0.png "image")

[![Image 25: image](https://linux.do/uploads/default/optimized/4X/4/8/e/48e960d248fbdb6267144f2d36341c1fe24cd41e_2_690x376.png)](https://linux.do/uploads/default/original/4X/4/8/e/48e960d248fbdb6267144f2d36341c1fe24cd41e.png "image")

#### [](https://linux.do/t/topic/316819#p-3040413-dbschemasql-16)打开项目地址，找到`db/schema.sql`

[直达请点我](https://github.com/dreamhunter2333/cloudflare_temp_email/blob/main/db/schema.sql)

[![Image 26: image](https://linux.do/uploads/default/optimized/4X/1/4/9/14943b3a7f6a81f3b856a6be0ecf5e05486e2f36_2_690x445.png)](https://linux.do/uploads/default/original/4X/1/4/9/14943b3a7f6a81f3b856a6be0ecf5e05486e2f36.png "image")

[![Image 27: image](https://linux.do/uploads/default/optimized/4X/f/2/e/f2e7191508f3eb3b2455ed6aa46b6c6b9aa6c4fc_2_690x447.png)](https://linux.do/uploads/default/original/4X/f/2/e/f2e7191508f3eb3b2455ed6aa46b6c6b9aa6c4fc.png "image")

[![Image 28: image](https://linux.do/uploads/default/original/4X/d/b/b/dbb30982686ba876479ebde45a7dfc3b60e6a3ed.png)](https://linux.do/uploads/default/original/4X/d/b/b/dbb30982686ba876479ebde45a7dfc3b60e6a3ed.png "image")

[![Image 29: image](https://linux.do/uploads/default/optimized/4X/0/7/b/07b619d78079130d421173e41c37f1d33dd383ba_2_690x399.png)](https://linux.do/uploads/default/original/4X/0/7/b/07b619d78079130d421173e41c37f1d33dd383ba.png "image")

#### [](https://linux.do/t/topic/316819#p-3040413-h-17)部署邮箱服务后端

[![Image 30: image](https://linux.do/uploads/default/optimized/4X/b/9/4/b94bfb131e8a3e0d5a9074a2c65bed9dcdf89031_2_690x382.png)](https://linux.do/uploads/default/original/4X/b/9/4/b94bfb131e8a3e0d5a9074a2c65bed9dcdf89031.png "image")

[![Image 31: image](https://linux.do/uploads/default/optimized/4X/7/6/6/7669a4ca1abd46bcd14dee468c724dc128fb5c83_2_690x450.png)](https://linux.do/uploads/default/original/4X/7/6/6/7669a4ca1abd46bcd14dee468c724dc128fb5c83.png "image")

[![Image 32: image](https://linux.do/uploads/default/optimized/4X/2/b/3/2b3b8fd140f4701dfa1e2a719ab79dfc213d20eb_2_690x484.png)](https://linux.do/uploads/default/original/4X/2/b/3/2b3b8fd140f4701dfa1e2a719ab79dfc213d20eb.png "image")

### [](https://linux.do/t/topic/316819#p-3040413-nodejs_compat-18)`nodejs_compat`可以在这里复制！

[![Image 33: image](https://linux.do/uploads/default/optimized/4X/3/e/d/3ed5cfb42b22da45cf050e1730fe56cd45923e39_2_663x500.png)](https://linux.do/uploads/default/original/4X/3/e/d/3ed5cfb42b22da45cf050e1730fe56cd45923e39.png "image")

[![Image 34: image](https://linux.do/uploads/default/optimized/4X/2/4/9/249d367b1d3256b22bfdd2b7aed09b6cd8bbc8f2_2_690x350.png)](https://linux.do/uploads/default/original/4X/2/4/9/249d367b1d3256b22bfdd2b7aed09b6cd8bbc8f2.png "image")

[代码直达地址，点我！](https://github.com/dreamhunter2333/cloudflare_temp_email/releases/latest/download/worker.js)

下载代码后，**打开代码直接全部复制！**

[![Image 35: image](https://linux.do/uploads/default/optimized/4X/5/b/9/5b91616aa36973c2e5387c6364e52b3da6e2cea7_2_690x321.png)](https://linux.do/uploads/default/original/4X/5/b/9/5b91616aa36973c2e5387c6364e52b3da6e2cea7.png "image")

[![Image 36: image](https://linux.do/uploads/default/optimized/4X/9/e/e/9ee9e64a38ed0a2134f56205d1b499a8bdc564b8_2_690x332.png)](https://linux.do/uploads/default/original/4X/9/e/e/9ee9e64a38ed0a2134f56205d1b499a8bdc564b8.png "image")

#### [](https://linux.do/t/topic/316819#p-3040413-d1-19)然后我们返回，继续配置D1数据库！

[![Image 37: image](https://linux.do/uploads/default/optimized/4X/f/5/a/f5aa60edadd95afe14eab6322b9b5e7c21fdcd83_2_690x339.png)](https://linux.do/uploads/default/original/4X/f/5/a/f5aa60edadd95afe14eab6322b9b5e7c21fdcd83.png "image")

[![Image 38: image](https://linux.do/uploads/default/optimized/4X/3/0/c/30c661e066e6041fd2fa9596b5cff1afe8e9e9be_2_690x407.png)](https://linux.do/uploads/default/original/4X/3/0/c/30c661e066e6041fd2fa9596b5cff1afe8e9e9be.png "image")

[![Image 39: image](https://linux.do/uploads/default/optimized/4X/7/e/4/7e4cec6cc07fb81f07ef5da4abef198c82a99636_2_690x427.png)](https://linux.do/uploads/default/original/4X/7/e/4/7e4cec6cc07fb81f07ef5da4abef198c82a99636.png "image")

[![Image 40: image](https://linux.do/uploads/default/optimized/4X/9/5/4/9549ccd6dd3cc5eec5341439fe9e9abbb35c03c0_2_690x457.png)](https://linux.do/uploads/default/original/4X/9/5/4/9549ccd6dd3cc5eec5341439fe9e9abbb35c03c0.png "image")

[![Image 41: image](https://linux.do/uploads/default/optimized/4X/0/1/6/016d46440d57347d81a730c506e20b1a94df6320_2_690x353.png)](https://linux.do/uploads/default/original/4X/0/1/6/016d46440d57347d81a730c506e20b1a94df6320.png "image")

#### [](https://linux.do/t/topic/316819#p-3040413-h-20)接下来，我们设置环境变量

你可以直接按我给的配置来配，如果你需要额外的配置可以查阅官方文档

[文档直达](https://temp-mail-docs.awsl.uk/zh/guide/cli/worker.html#%E4%BF%AE%E6%94%B9-wrangler-toml-%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6)

**注意：请不要从表格里直接复制配置，你可以下拉到表格下方去复制，表格内的引号会自动将英文的转成中文的，所以请去下面代码块内复制！ ![Image 42: :tieba_087:](https://linux.do/uploads/default/original/3X/2/e/2e09f3a3c7b27eacbabe9e9614b06b88d5b06343.png?v=14)**

**请仔细查看参数说明，不要直接复制就不管了**

| 值 | 类型 | 值 | 说明 |
| --- | --- | --- | --- |
| ADMIN_PASSWORDS | JSON | [“your_password”,“your_password_two”] | admin 控制台密码, 不配置则不允许访问控制台，大白话：管理员密码不配置你怎么管理？可以多个，你也可以只配置一个！ |
| ADMIN_USER_ROLE | 纯文本 | admin | admin 角色配置, 如果用户角色等于 ADMIN_USER_ROLE 则可以访问 admin 控制台 大白话：如果角色是admin的用户就可以直接看到admin控制台 |
| DEFAULT_DOMAINS | JSON | [“”] 或者 [“你自己的域名”] | 这里给了一个空数组，也就是说没有登录的用户没有可用的域名，如果你想给没有登录的用户使用域名，你可以加上自己的域名[“各自域名”] 它是一个数组也可以多个 |
| DOMAINS | JSON | [“你的域名.love”] | 这里是用来配置你的域名的，例如我的域名就是linuxdo.love，实际上还可以添加多个，例如[“linuxdo.love”,“goai.love”]，当然配置的域名都得接入cloudflare哈！没接入你配了也没用！ |
| ENABLE_AUTO_REPLY | 纯文本 | false | 是否允许自动回复邮件，官方默认是false，我们也设置为false |
| ENABLE_USER_CREATE_EMAIL | 纯文本 | true | 是否允许用户随机创建邮箱账户，默认为true就行，这样就可以创建不同的邮件账户啦！ |
| ENABLE_USER_DELETE_EMAIL | 纯文本 | true | 是否允许用户删除邮件，如果你不想用户删除邮件改成false就行 |
| JWT_SECRET | 纯文本 | 自己去生成一个！ | 这里需要一个密钥，打开[GitHub](https://www.librechat.ai/toolkit/creds_generator) 生成后复制“JWT_SECRET”里的内容 |
| NO_LIMIT_SEND_ROLE | 纯文本 | admin | 可以无限发送邮件的角色，我设置成了admin，也就是说admin角色的用户可以无限发送邮件了！ |
| USER_ROLES | JSON | [{“domains”:[“你的域名.love”],“prefix”:“”,“role”:“vip”},{“domains”:[“你的域名.love”],“prefix”:“”,“role”:“admin”}] 别从这里复制从表格下的代码块复制这个不然报错 | 设置两个系统角色，一个为vip一个为admin！ |

### [](https://linux.do/t/topic/316819#p-3040413-admin_passwords-21)ADMIN_PASSWORDS

```
["your_password","your_password_two"]
```

### [](https://linux.do/t/topic/316819#p-3040413-default_domains-22)DEFAULT_DOMAINS

```
[""]
```

```
["你自己的域名"]
```

### [](https://linux.do/t/topic/316819#p-3040413-domains-23)DOMAINS

```
["你的域名.love"]
```

### [](https://linux.do/t/topic/316819#p-3040413-user_roles-24)USER_ROLES

```
[{"domains":["你的域名.love"],"prefix":"","role":"vip"},{"domains":["你的域名.love"],"prefix":"","role":"admin"}]
```

#### [](https://linux.do/t/topic/316819#p-3040413-h-25)如何配置？看图

[![Image 43: image](https://linux.do/uploads/default/optimized/4X/b/f/1/bf16fd1f60113d689508bc9f9a85aeb48f182b0b_2_690x370.png)](https://linux.do/uploads/default/original/4X/b/f/1/bf16fd1f60113d689508bc9f9a85aeb48f182b0b.png "image")

[![Image 44: image](https://linux.do/uploads/default/optimized/4X/f/1/3/f13b42f348ff0764a77b1232e21d3c0542923233_2_499x500.png)](https://linux.do/uploads/default/original/4X/f/1/3/f13b42f348ff0764a77b1232e21d3c0542923233.png "image")

一次性**可以配置多个哈！**

[![Image 45: image](https://linux.do/uploads/default/optimized/4X/c/c/0/cc08bda2f39b53474666aafa7f6627e27a392c0b_2_690x387.png)](https://linux.do/uploads/default/original/4X/c/c/0/cc08bda2f39b53474666aafa7f6627e27a392c0b.png "image")

[![Image 46: image](https://linux.do/uploads/default/original/4X/9/d/d/9dd484146ce40852c73a57aeacb3ca5da97bef69.png)](https://linux.do/uploads/default/original/4X/9/d/d/9dd484146ce40852c73a57aeacb3ca5da97bef69.png "image")

#### [](https://linux.do/t/topic/316819#p-3040413-kv-26)配置KV缓存

[![Image 47: image](https://linux.do/uploads/default/optimized/4X/6/8/c/68ca2c7c848f971b87ef0c95a09810a55bc1bf58_2_690x376.png)](https://linux.do/uploads/default/original/4X/6/8/c/68ca2c7c848f971b87ef0c95a09810a55bc1bf58.png "image")

[![Image 48: image](https://linux.do/uploads/default/optimized/4X/b/a/3/ba36d447404457092a887ca4e7301344f783f973_2_690x339.png)](https://linux.do/uploads/default/original/4X/b/a/3/ba36d447404457092a887ca4e7301344f783f973.png "image")

[![Image 49: image](https://linux.do/uploads/default/optimized/4X/b/f/e/bfededb738740f983e259134ea319767ccc644fa_2_690x376.png)](https://linux.do/uploads/default/original/4X/b/f/e/bfededb738740f983e259134ea319767ccc644fa.png "image")

[![Image 50: image](https://linux.do/uploads/default/optimized/4X/f/6/4/f64ac0288518185ed975e20b01803bbdbafa1587_2_690x376.png)](https://linux.do/uploads/default/original/4X/f/6/4/f64ac0288518185ed975e20b01803bbdbafa1587.png "image")

[![Image 51: image](https://linux.do/uploads/default/optimized/4X/1/6/4/164125d78e7a0684b9b04c095434877ff7d8440e_2_515x500.png)](https://linux.do/uploads/default/original/4X/1/6/4/164125d78e7a0684b9b04c095434877ff7d8440e.png "image")

[![Image 52: image](https://linux.do/uploads/default/optimized/4X/5/3/2/532f79be014a7f2fa0a4b419a861318848a7d012_2_281x500.png)](https://linux.do/uploads/default/original/4X/5/3/2/532f79be014a7f2fa0a4b419a861318848a7d012.png "image")

#### [](https://linux.do/t/topic/316819#p-3040413-h-27)配置邮件转发【非常重要，必须配置】

[![Image 53: image](https://linux.do/uploads/default/optimized/4X/d/6/7/d677a2d1e644d6d63c1c09154e377f0e4b5604c3_2_690x376.png)](https://linux.do/uploads/default/original/4X/d/6/7/d677a2d1e644d6d63c1c09154e377f0e4b5604c3.png "image")

[![Image 54: image](https://linux.do/uploads/default/optimized/4X/b/6/8/b68e846f17dd33c122465705e19f57d37da32e3c_2_690x376.png)](https://linux.do/uploads/default/original/4X/b/6/8/b68e846f17dd33c122465705e19f57d37da32e3c.png "image")

[![Image 55: image](https://linux.do/uploads/default/optimized/4X/0/3/c/03c326dea19af381f3a17c33f6664219bc1171d7_2_690x473.png)](https://linux.do/uploads/default/original/4X/0/3/c/03c326dea19af381f3a17c33f6664219bc1171d7.png "image")

自此！**恭喜你！临时邮箱后端服务搭建完成！**

### [](https://linux.do/t/topic/316819#p-3040413-h-28)搭建前端服务，也就是操作界面！

[![Image 56: image](https://linux.do/uploads/default/optimized/4X/3/2/5/32520990f7b39dc0e3f12f31adf2c53ff403021e_2_690x376.png)](https://linux.do/uploads/default/original/4X/3/2/5/32520990f7b39dc0e3f12f31adf2c53ff403021e.png "image")

我们需要生成前端代码，打开官方文档，一个生成器！

[直达地址](https://temp-mail-docs.awsl.uk/zh/guide/ui/pages.html)

### [](https://linux.do/t/topic/316819#p-3040413-h-29)【注意】这里图片里打错字了，图片里说的是“自定义域”，我打成了“兹定于”

[![Image 57: image](https://linux.do/uploads/default/optimized/4X/6/2/8/628b24165c1147d6b483d75cbe6c7ed24ce542f1_2_680x500.png)](https://linux.do/uploads/default/original/4X/6/2/8/628b24165c1147d6b483d75cbe6c7ed24ce542f1.png "image")

[![Image 58: image](https://linux.do/uploads/default/optimized/4X/f/3/5/f35bf2c2c47f7fe7911fd15eba007f69871849c9_2_690x376.png)](https://linux.do/uploads/default/original/4X/f/3/5/f35bf2c2c47f7fe7911fd15eba007f69871849c9.png "image")

[![Image 59: image](https://linux.do/uploads/default/optimized/4X/1/1/b/11bf60d07e0fe59f528aa6e716a151ecfada83a6_2_690x376.png)](https://linux.do/uploads/default/original/4X/1/1/b/11bf60d07e0fe59f528aa6e716a151ecfada83a6.png "image")

[![Image 60: image](https://linux.do/uploads/default/optimized/4X/8/5/4/854d4751a42444a96e25e2e5bc2573d6c7251036_2_690x227.png)](https://linux.do/uploads/default/original/4X/8/5/4/854d4751a42444a96e25e2e5bc2573d6c7251036.png "image")

[![Image 61: image](https://linux.do/uploads/default/optimized/4X/2/6/f/26f90b726c92cc104e81dc12328c612f3aa43ff8_2_690x336.png)](https://linux.do/uploads/default/original/4X/2/6/f/26f90b726c92cc104e81dc12328c612f3aa43ff8.png "image")

[![Image 62: image](https://linux.do/uploads/default/optimized/4X/8/8/c/88c9b2b55c116602f078b109f96146f4ec0431d1_2_690x378.png)](https://linux.do/uploads/default/original/4X/8/8/c/88c9b2b55c116602f078b109f96146f4ec0431d1.png "image")

[![Image 63: image](https://linux.do/uploads/default/optimized/4X/9/c/8/9c8ab64cea2575bd35c5bd20af3a15ff029f7f57_2_690x374.png)](https://linux.do/uploads/default/original/4X/9/c/8/9c8ab64cea2575bd35c5bd20af3a15ff029f7f57.png "image")

[![Image 64: image](https://linux.do/uploads/default/optimized/4X/7/9/d/79d03f1f18df3427c22fea759e29109a3da44f64_2_690x388.png)](https://linux.do/uploads/default/original/4X/7/9/d/79d03f1f18df3427c22fea759e29109a3da44f64.png "image")

[![Image 65: image](https://linux.do/uploads/default/optimized/4X/f/1/c/f1cea7a882dd96ceb1e451fe2298ed7271eba6d8_2_690x267.png)](https://linux.do/uploads/default/original/4X/f/1/c/f1cea7a882dd96ceb1e451fe2298ed7271eba6d8.png "image")

**也许也不需要等十分钟**，你可以用无痕浏览器，或者别的浏览器访问一下，看是否可以访问了！

[![Image 66: image](https://linux.do/uploads/default/optimized/4X/f/a/8/fa80f0503ddaff982bfd5442e6c1307294601989_2_520x500.png)](https://linux.do/uploads/default/original/4X/f/a/8/fa80f0503ddaff982bfd5442e6c1307294601989.png "image")

### [](https://linux.do/t/topic/316819#p-3040413-h-30)测试是否正常

#### [](https://linux.do/t/topic/316819#p-3040413-h-31)创建用户

[![Image 67: image](https://linux.do/uploads/default/original/4X/9/3/a/93ae1d72cc92c581e4570c4211bede4ce8e72434.png)](https://linux.do/uploads/default/original/4X/9/3/a/93ae1d72cc92c581e4570c4211bede4ce8e72434.png "image")

[![Image 68: image](https://linux.do/uploads/default/optimized/4X/c/b/2/cb28fb9afe0af122e713c5c610eee23a814d1d61_2_572x500.png)](https://linux.do/uploads/default/original/4X/c/b/2/cb28fb9afe0af122e713c5c610eee23a814d1d61.png "image")

[![Image 69: image](https://linux.do/uploads/default/optimized/4X/f/c/6/fc6f3b9e0b05f348bfd79c215513495abf031735_2_690x391.png)](https://linux.do/uploads/default/original/4X/f/c/6/fc6f3b9e0b05f348bfd79c215513495abf031735.png "image")

[![Image 70: image](https://linux.do/uploads/default/optimized/4X/a/e/a/aea60ad0a623f2d16f0ac9ca821e8069f7fa9ff8_2_690x184.png)](https://linux.do/uploads/default/original/4X/a/e/a/aea60ad0a623f2d16f0ac9ca821e8069f7fa9ff8.png "image")

[![Image 71: image](https://linux.do/uploads/default/optimized/4X/d/3/c/d3c2cc6a3aa298caa34f176e8294a15c5fb080d2_2_690x244.png)](https://linux.do/uploads/default/original/4X/d/3/c/d3c2cc6a3aa298caa34f176e8294a15c5fb080d2.png "image")

#### [](https://linux.do/t/topic/316819#p-3040413-h-32)测试接收邮件

[![Image 72: image](https://linux.do/uploads/default/optimized/4X/d/7/4/d74898b276443cf2e2d51633149ae7eae206b1be_2_690x407.png)](https://linux.do/uploads/default/original/4X/d/7/4/d74898b276443cf2e2d51633149ae7eae206b1be.png "image")

[![Image 73: image](https://linux.do/uploads/default/optimized/4X/9/6/b/96b4aff3792b0e23f63c9ae19e568214435ee887_2_690x295.png)](https://linux.do/uploads/default/original/4X/9/6/b/96b4aff3792b0e23f63c9ae19e568214435ee887.png "image")

[![Image 74: image](https://linux.do/uploads/default/optimized/4X/4/1/8/4181fe44a40636240892c05a7559456ef1c96cfd_2_690x348.png)](https://linux.do/uploads/default/original/4X/4/1/8/4181fe44a40636240892c05a7559456ef1c96cfd.png "image")

[![Image 75: image](https://linux.do/uploads/default/optimized/4X/d/5/6/d56855df766934b36a2ec45e4ce8b45176572a5a_2_690x434.png)](https://linux.do/uploads/default/original/4X/d/5/6/d56855df766934b36a2ec45e4ce8b45176572a5a.png "image")

[![Image 76: image](https://linux.do/uploads/default/optimized/4X/3/0/2/3023c7b885d15edaeeeee70d9eec122df1800ba9_2_690x314.png)](https://linux.do/uploads/default/original/4X/3/0/2/3023c7b885d15edaeeeee70d9eec122df1800ba9.png "image")

### [](https://linux.do/t/topic/316819#p-3040413-api-33)调用API创建邮件获取邮件（请根据实际情况去修改代码！这是之前测试用的代码！）

```
import requests
import json
from time import sleep
import random
import string
import re

# 配置信息
WORKER_DOMAIN = ""  # 替换为你的后台域名，比如我的，apimail.linuxdo.love
EMAIL_DOMAIN = "" # 你的域名地址
ADMIN_PASSWORD = "" # 你的管理员密码

def generate_random_name():
    """生成随机邮箱名称"""
    letters1 = ''.join(random.choices(string.ascii_lowercase, k=5))  # 5个小写字母
    numbers = ''.join(random.choices(string.digits, k=random.randint(1, 3)))  # 1-3个数字
    letters2 = ''.join(random.choices(string.ascii_lowercase, k=random.randint(1, 3)))  # 1-3个小写字母
    return letters1 + numbers + letters2

def create_test_email():
    """创建测试邮箱"""
    try:
        random_name = generate_random_name()
        res = requests.post(
            f"https://{WORKER_DOMAIN}/admin/new_address",
            json={
                "enablePrefix": True,
                "name": random_name,
                "domain": EMAIL_DOMAIN,
            },
            headers={
                'x-admin-auth': ADMIN_PASSWORD,
                "Content-Type": "application/json"
            }
        )
        
        if res.status_code == 200:
            data = res.json()
            print("创建邮箱成功：")
            print(f"JWT: {data.get('jwt')}")
            print(f"邮箱地址: {data.get('address')}")
            return data.get('jwt'), data.get('address')
        else:
            print(f"创建邮箱失败: {res.status_code}")
            return None, None
    except Exception as e:
        print(f"创建邮箱出错: {e}")
        return None, None

def check_verification_code(jwt):
    """查看验证码"""
    try:
        limit = 10
        offset = 0
        res = requests.get(
            f"https://{WORKER_DOMAIN}/api/mails",
            params={
                "limit": limit,
                "offset": offset
            },
            headers={
                "Authorization": f"Bearer {jwt}",
                "Content-Type": "application/json"
            }
        )
        
        if res.status_code == 200:
            data = res.json()
            # print("\n收到的邮件：")
            # print(json.dumps(data, indent=2))
            
            # 使用正则表达式提取验证码
            if data.get('results') and len(data['results']) > 0:
                raw_content = data['results'][0].get('raw', '')  # 获取最新邮件的raw内容
                # 使用更简单的正则表达式，直接匹配数字
                code_matches = re.findall(r'code is: (\d{6})', raw_content)
                if code_matches:
                    verification_code = code_matches[0]  # 获取第一个匹配的6位数字
                    print(f"\n提取到的验证码: {verification_code}")
                    return True, verification_code
                else:
                    # 尝试另一种匹配方式
                    code_matches = re.findall(r'code is:\s*(\d{6})', raw_content)
                    if code_matches:
                        verification_code = code_matches[0]
                        print(f"\n提取到的验证码: {verification_code}")
                        return True, verification_code
                    print("未找到验证码")
                    return False, None
            else:
                print("邮件列表为空")
                return False, None
        else:
            print(f"获取邮件失败: {res.status_code}")
            return False, None
            
    except Exception as e:
        print(f"获取邮件出错: {e}")
        return False, None

def main():
    # 1. 创建测试邮箱
    jwt, address = create_test_email()
    if not jwt or not address:
        print("无法继续测试")
        return
        
    print("\n创建的邮箱信息：")
    print(f"JWT: {jwt}")
    print(f"邮箱地址: {address}")
        
    # 2. 等待一会儿，让邮件有时间送达
    print("\n等待10秒钟让邮件送达...")
    sleep(10)
    
    # 3. 查看验证码
    success, code = check_verification_code(jwt)
    if success:
        print(f"成功获取验证码: {code}")
    else:
        print("获取验证码失败")
```

### [](https://linux.do/t/topic/316819#p-3040413-h-34)关于发送邮件

由于我一直在弄自己的学习，然后平常也就上L站看看，一直没有空写发邮件的教程，今天看到有佬友写了一篇有关发送邮件的配置，贴在这里哈！感谢佬友的教程！

### [](https://linux.do/t/topic/316819#p-3040413-h-35)另外一个佬友写的发送邮件教程

### [](https://linux.do/t/topic/316819#p-3040413-h-36)结束

啊，从21点写到现在01点03分，终于写完了，希望能帮到佬友，发送邮件我就不写了，需要的可以去看看官方文档，第一次写教程，如果有错误或者欠缺的地方，欢迎佬友们补充！我去睡觉了！我还说我调整作息呢…又熬到1点了

 访问地址：[https://mail.linuxdo.love/](https://mail.linuxdo.love/)

### [](https://linux.do/t/topic/316819#p-3040413-h-37)最后接好运

昨天中了40 [5块钱中了40块钱！自己买疯狂星期四！ - #6，来自 XiaoHuang](https://linux.do/t/topic/314805/6)

 今天中了50

[![Image 77: 19d7641cdf17bff85e8ac81c41eb128f](https://linux.do/uploads/default/optimized/4X/5/1/f/51f81529bb3468753cee39fa259ea2989d66715f_2_666x500.jpeg)](https://linux.do/uploads/default/original/4X/5/1/f/51f81529bb3468753cee39fa259ea2989d66715f.jpeg "19d7641cdf17bff85e8ac81c41eb128f")

### [](https://linux.do/t/topic/316819#p-3040413-h-38)祝佬友们也好运连连！

> 本教程允许搬运，但请标注出处，谢谢

read  37 min
