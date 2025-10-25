Title: 【教程】在 leaflow 上部署自己的 searxng 搜索服务，10分钟内搞定 - 资源荟萃 - LINUX DO

URL Source: https://linux.do/t/topic/1061446

Published Time: 2025-10-19T13:43:23+00:00

Markdown Content:
[![Image 1](https://linux.do/user_avatar/linux.do/hahadalin/48/982803_2.gif)](https://linux.do/u/hahadalin)

searxng 是一个开源的搜索服务，可以在 web 页面搜索，也可以通过 api 搜索，许多 AI 工具都支持配置 searxng api 来实现搜索功能。

 跟随本帖，你将10分钟内完成：在 leaflow 上部署自己的 searxng，并开放出 json 格式 api。

 （别看帖子很长，实际上很多话都是防呆，你要做的很少）

* * *

【**第一步：在 leaflow 部署清单一键部署容器、挂载存储、创建对外服务**】

复制以下 yaml 部署配置

点我展开
```
kind: Storage
name: searxng-config
size: 128
---
kind: Storage
name: searxng-data
size: 512
---
kind: Deployment
name: searxng
replicas: 1
image_pull_secrets: {  }
containers:
  -
    name: searxng
    image: 'docker.io/searxng/searxng:latest'
    working_dir: ''
    command: {  }
    args: {  }
    ports:
      -
        name: port8080
        container_port: 8080
        protocol: TCP
    env: {  }
    env_from_configmap: {  }
    env_from_secret: {  }
    resources:
      cpu: 1000
      memory: 1024
    volume_mounts:
      -
        mount_path: /etc/searxng/
        storage_name: searxng-config
        sub_path: ''
        read_only: false
      -
        mount_path: /var/cache/searxng/
        storage_name: searxng-data
        sub_path: ''
        read_only: false
    configmap_mounts: {  }
    secret_mounts: {  }
---
kind: Service
name: searxng
type: LoadBalancer
target_workload_type: Deployment
target_workload_name: searxng
ports:
  -
    name: port8080
    port: 8888
    target_port: 8080
    protocol: TCP
session_affinity: None
external_traffic_policy: Cluster
```

在 [leaflow 部署清单](https://leaflow.net/apply)**最大的输入框**里，粘贴以上 yaml 配置，点击【应用/更新】按钮，稍等10-20秒。

验证是否成功：

*   新增了一个应用（searxng）、一个服务（searxng）、两个[存储](https://leaflow.net/storages)（searxng-config、 searxng-data）
*   到 [searxng 服务内](https://leaflow.net/services/searxng)，拿到【可访问地址】（一个ipv4的ip+端口），在浏览器打开，你应该看到这样的界面（已经可以搜索了）：

[![Image 2: image](https://linux.do/uploads/default/optimized/4X/a/0/8/a08b3e6db7f651cfbf9cef29954a6abfebc0d134_2_690x310.png)](https://linux.do/uploads/default/original/4X/a/0/8/a08b3e6db7f651cfbf9cef29954a6abfebc0d134.png "image") 

* * *

【**第二步：修改配置，支持 json 格式 api 调用**】

 上一步我们已经可以在 web 页面搜索了，但还不能使用 json 格式 api，需要改配置、重启应用。

*   来到 [searxng 应用](https://leaflow.net/deployments/searxng)，点击【终端】按钮，一步步进入终端。
*   终端执行：`cd /etc/searxng/`
*   终端执行：`vi settings.yml`，这个文件里应该已经有很多东西，不用管
*   （搜索、编辑、保存涉及到 vi 编辑器的使用技巧，如果你不会，问问 AI） 搜索（按`/`）`formats:`，找到
```
formats:                                           
    - html
```
 这两行，进入编辑模式（按 i），在 html 下面加`- json`（注意缩进对齐），变成：
```
formats:                                           
    - html
    - json
```
*   退出编辑模式（尝试`ctrl-c`、`ctrl-[`、`esc`），保存并退出（`:wq`回车）

验证是否成功：

*   执行 `less settings.yml` 应该能看到
```
formats:                                           
    - html
    - json
```

【**第三步：重启应用**】

这一步听上去很简单，但是如果你直接点重启，可能等半天新容器都启不起来。

 这样做：

*   还是来到[searxng 应用](https://leaflow.net/deployments/searxng)
*   点【停止】-【确认停止】，然后应用就停止了，没有容器了
*   点【编辑】
*   【副本数】显示 0，因为刚才你停止应用了，改为 1。其他的不要动
*   点击页面底部的【更新工作负载】
*   等待容器启动（不会超过1分钟）

* * *

**完事了！**

验证 json 格式 api 是否正常：

*   来到 [searxng 服务内](https://leaflow.net/services/searxng)，拿到【可访问地址】
*   在【可访问地址】后面拼接`/search?q=hello&format=json`，完整的地址是这样的：`http://ip:port/search?q=hello&format=json`，浏览器打开这个地址，你应该能看到页面上展示了一堆 json 文本。

如果没有问题，在 AI 工具里直接使用这个【可访问地址】或者在[网站管理](https://leaflow.net/ingresses)中给它绑定一个域名都可以，随意探索更多玩法吧少年！

**如果有用就给我点个赞吧~**
