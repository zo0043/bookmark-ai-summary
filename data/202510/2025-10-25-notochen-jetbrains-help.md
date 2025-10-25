# NotoChen/Jetbrains-Help
- URL: https://github.com/NotoChen/Jetbrains-Help
- Added At: 2025-10-25 07:57:21
- [Link To Text](2025-10-25-notochen-jetbrains-help_raw.md)

## TL;DR
Jetbrains-Help项目提升Jetbrains产品易用性，支持全产品及插件，提供自动更新、配置和管理功能，支持多种运行环境。

## Summary
1. **项目概述**：
   - 项目名称：Jetbrains-Help
   - 仓库地址：[GitHub - NotoChen/Jetbrains-Help](https://github.com/NotoChen/Jetbrains-Help)
   - 目标：提升Jetbrains服务商相关产品易用性

2. **功能特性**：
   - 支持Jetbrains全产品及插件
   - 自动订阅插件库更新
   - 自动生成和管理公私钥/证书
   - 自动配置power.conf文件
   - 自动打包ja-netfilter.zip
   - 支持自定义License Show
   - 支持实时搜索
   - 插件默认按名称排序
   - 支持local/jar/dockerfile运行
   - 单码全家桶激活支持

3. **运行环境**：
   - Java环境：版本21
   - Maven环境：最新版推荐
   - Docker环境：最新版推荐（可选）

4. **运行教程**：
   - **拉取项目**：使用`clone`命令将项目克隆至本地
   - **配置环境**：
     - **本地运行**：配置Java和Maven环境
     - **容器运行**：配置Docker环境（可选）
   - **运行服务**：
     - **本地运行**：
       - **有IDE**：通过IDE打开项目，配置环境，运行JetbrainsHelpApplication.java
       - **无IDE**：系统终端进入项目根目录，运行打包命令和启动命令
     - **容器运行**：
       - **使用Docker**：运行Docker命令构建和运行
       - **使用Docker-Compose**：使用Docker-Compose命令构建和运行

5. **使用教程**：
   - 项目运行后，Console会打印服务地址，默认端口和地址为`10768`
   - 可以直接访问[Jetbrains-Help](http://127.0.0.1:10768/)进行使用
   - **下载依赖**：根据页面头部指引下载`ja-netfilter.zip`
   - **依赖配置**：
     - **可打开IDE**：在IDE中编辑自定义虚拟机选型，键入配置并重启IDE
     - **不可打开IDE**：使用Toolbox安装并配置IDE，键入配置并重启IDE
