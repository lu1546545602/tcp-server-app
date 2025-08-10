FROM ubuntu:20.04

# 设置环境变量避免交互式安装
ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=${PATH}:${ANDROID_HOME}/tools:${ANDROID_HOME}/platform-tools

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    zip \
    unzip \
    openjdk-8-jdk \
    python3 \
    python3-pip \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
RUN pip3 install --upgrade pip
RUN pip3 install buildozer cython kivy

# 创建工作目录
WORKDIR /app

# 复制项目文件
COPY . /app/

# 设置buildozer权限
RUN chmod +x /usr/local/bin/buildozer

# 编译APK
CMD ["buildozer", "android", "debug"]