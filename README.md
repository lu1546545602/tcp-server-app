# 游戏组队服务器 - 安卓版

这是游戏组队TCP服务器的安卓移植版本，使用Kivy框架开发，可以编译成APK在安卓设备上运行。

## 功能特性

- 完整的TCP服务器功能
- 队伍管理系统（创建、加入、离开队伍）
- 实时状态更新
- 场景管理
- 移动端友好的用户界面

## 文件结构

```
tcp_apk/
├── main.py              # 主程序文件（Kivy版本）
├── buildozer.spec       # Buildozer配置文件
├── requirements.txt     # Python依赖
└── README.md           # 说明文档
```

## 编译要求

### 系统要求
- Linux系统（推荐Ubuntu 20.04+）
- Python 3.8+
- Java JDK 8
- Android SDK
- Android NDK

### 安装依赖

1. 安装Python依赖：
```bash
pip install buildozer cython
pip install -r requirements.txt
```

2. 安装系统依赖（Ubuntu）：
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

## APK编译

### ⚠️ 重要说明
由于buildozer主要为Linux环境设计，在Windows上直接编译可能遇到问题。推荐使用以下替代方案：

### 编译方案选择

#### 方案1: GitHub Actions在线编译 (推荐)
- 将代码上传到GitHub仓库
- 使用提供的`.github/workflows/build-apk.yml`配置
- 自动在线编译并下载APK

#### 方案2: Docker编译
- 安装Docker Desktop
- 运行`build_docker.bat`脚本
- 在容器中编译APK

#### 方案3: WSL2编译 (需要重启)
```bash
# 安装WSL2和Ubuntu (需要重启系统)
wsl --install Ubuntu-22.04

# 重启后在WSL中安装依赖
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip
pip3 install buildozer cython kivy
```

#### 方案4: 直接使用Kivy应用
- 当前已可运行Kivy版本进行开发测试
- 运行`python main.py`启动应用

### 传统编译方法 (Linux环境)

1. 进入项目目录：
```bash
cd tcp_apk
```

2. 初始化buildozer（首次运行）：
```bash
buildozer android debug
```

3. 编译APK：
```bash
buildozer android debug
```

编译完成后，APK文件将位于 `bin/` 目录下。

## 安装和使用

1. 将生成的APK文件传输到安卓设备
2. 在安卓设备上启用"未知来源"应用安装
3. 安装APK文件
4. 启动应用
5. 配置服务器IP和端口
6. 点击"启动服务器"开始服务

## 权限说明

应用需要以下权限：
- 网络访问权限：用于TCP服务器功能
- 保持唤醒：防止服务器在后台被系统杀死

## 注意事项

1. **网络配置**：确保安卓设备与客户端在同一网络中，或者正确配置端口转发
2. **防火墙**：检查设备防火墙设置，确保TCP端口可访问
3. **电池优化**：建议将应用加入电池优化白名单，避免后台被杀死
4. **性能**：安卓设备性能可能影响服务器并发处理能力

## 故障排除

### 编译问题
- 确保所有依赖已正确安装
- 检查Java版本（推荐JDK 8）
- 清理buildozer缓存：`buildozer android clean`

### 运行问题
- 检查网络权限
- 查看应用日志
- 确认端口未被占用

## API兼容性

安卓版本完全兼容原版TCP服务器的API，支持所有消息类型：
- 创建队伍
- 加入队伍
- 申请入队
- 离开队伍
- 更新状态
- 查看队员
- 更新场景

## 开发说明

本项目基于原版`tcp_server_gui.py`移植，主要变更：
- 使用Kivy替代tkinter实现跨平台GUI
- 优化移动端用户体验
- 保持完整的服务器功能
- 添加安卓特定的生命周期管理

## 版本信息

- 版本：1.0
- 基于：tcp_server_gui.py
- 框架：Kivy
- 目标平台：Android 5.0+（API 21+）