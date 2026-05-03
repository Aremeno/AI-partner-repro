# AI 智能伴侣 - 学习复现项目

## 项目说明

本项目为**个人跟随教程学习复现练手项目**，主要目的是巩固基本语法和大模型调用逻辑，核心业务逻辑基本依照开源教程，只在原版基础上自行微调代码细节、优化交互逻辑与页面布局，仅用于个人编程学习、技术复盘、代码仓库归档，**非原创从零开发，无商业用途**

## 原教程链接

b 站视频：

[黑马程序员AI智能伴侣项目(free)](https://www.bilibili.com/video/BV1sHU9BmEne?spm_id_from=333.788.videopod.episodes&vd_source=eedf222b3d05e94e8684d4171436c506&p=109)；

## 功能介绍

基于 Streamlit 搭建轻量化 Web 端 AI 虚拟智能伴侣，核心功能如下：
- 自定义 AI 伴侣昵称、人物性格人设
- 大模型流式输出实时对话，模拟微信日常聊天风格
- 支持会话新建、历史会话加载与删除管理
- 本地 JSON 文件自动持久化保存聊天记录
- 侧边栏集成控制面板，界面简洁易用

## 技术栈

- 开发语言：Python 3.8+
- Web搭建工具：Streamlit
- 模型调用：OpenAI 兼容接口（可适配各类国内大模型中转服务）
- 数据存储：本地 JSON 文件会话持久化

## 运行环境
### 推荐版本

Python 3.8 ~ 3.11

### 依赖库

- streamlit
- openai


## 快速启动

1. 安装依赖

```bath
pip install streamlit openai
```

2. 运行项目

```bath
streamlit run app.py
```

## 配置说明

源码中 `your-api-key`、`your-base-url`、`your-model-id` 均为**占位标识**；

本地运行时自行替换为个人大模型接口配置，但是建议使用环境变量管理密钥。

## 项目目录结构

plaintext

```
AI-partner-repro/
├── ai-partner_1.py                # 项目主程序源码
├── resources/            # 静态资源、项目Logo图片
├── sessions/             # 自动生成，存放历史会话JSON文件
├── LEARNING-NOTES.md             # 个人学习复盘整理笔记
└── README.md             # 项目说明文档
```

## 学习收获

1. 掌握 Streamlit 常用组件布局、`session_state` 全局状态管理逻辑；
2. 熟悉 OpenAI 兼容接口调用方式，理解流式对话的实现原理；
3. 学会 Python 本地 JSON 文件读写、会话数据持久化的基础方案；
4. 掌握角色类 AI 应用 System Prompt 人设设定与规则编写技巧；
5. 提升阅读他人源码、复刻功能并自主微调优化的实践能力。

## 免责声明

1. 本项目仅为个人学习复现归档，核心逻辑参考公开教程，仅作学习交流使用；
2. 所有聊天会话数据仅保存在本地，不上传第三方服务器；
3. 严禁将本项目代码及衍生版本用于商业运营、违规场景使用。
