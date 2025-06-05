# Version Detector Pro 

Burp Suite 被动式版本检测插件，自动识别HTTP响应中的中间件/组件版本信息

![Burp Extension](https://img.shields.io/badge/Burp_Extension-v1.0-orange)
![Python](https://img.shields.io/badge/Python-2.7-green)

## ✨ 功能特性
- **多源检测**：同时分析Server头、Via头和HTML正文中的版本信息
- **广泛覆盖**：支持识别50+种常见中间件/云服务
- **智能提示**：自动高亮包含版本信息的请求（橙色标记）
- **精准匹配**：使用优化后的正则表达式减少误报
- **多编码支持**：完美处理中文及其他非ASCII字符

## 🛠️ 安装指南

### 环境要求
- Burp Suite Professional/Community v2022.x+
- Jython 2.7独立JAR包

### 安装步骤
1. 下载本仓库中的`VersionDetector.py`
2. 打开Burp Suite → Extender → Options
3. 在Python环境设置中添加Jython JAR路径
4. 点击Add按钮选择插件文件加载

![安装演示]![image](https://github.com/user-attachments/assets/b0f52bbb-af03-40ba-baea-952780712413)

## 🚀 使用方法
插件自动工作，无需手动触发。检测到版本信息时会：
1. 在Proxy/Repeater历史记录中显示橙色高亮
2. 鼠标悬停显示检测到的版本信息，格式：Server:Apache/2.4.6 || Via:kong 0.11.2 || Body:TOMCAT/9.0.83
![image](https://github.com/user-attachments/assets/36bdc3ad-b59c-4af5-973e-3b30efcdd069)


## 📊 支持组件列表

### 中间件
✅ Nginx ✅ Apache ✅ Tomcat ✅ Kong  
✅ IIS ✅ JBoss ✅ Jetty ✅ GlassFish  
✅ PHP ✅ WordPress ✅ Squid ✅ Varnish

### 云服务
✅ AWS ELB ✅ CloudFront ✅ Azure Front Door

## 🤝 贡献指南
欢迎通过Issue提交以下内容：
1. 未检测出的组件样本（请求响应）
2. 正则表达式优化建议
3. 新组件检测需求

### 待覆盖组件
⏳ 等待各位看官补充


