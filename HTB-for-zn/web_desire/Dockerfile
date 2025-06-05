FROM ubuntu:latest

RUN sed -i s:/archive.ubuntu.com:/mirrors.tuna.tsinghua.edu.cn/ubuntu:g /etc/apt/sources.list
RUN cat /etc/apt/sources.list
RUN apt-get clean
RUN apt-get -y update --fix-missing

RUN apt-get update && \
    apt-get install -y curl wget git supervisor redis-server 

# 动态下载并安装 Go（使用中国镜像源）
ENV GO_VERSION=1.22.2

# 设置阿里云镜像源（国内加速）
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        DOWNLOAD_ARCH="amd64"; \
        DOWNLOAD_URL="https://mirrors.aliyun.com/golang/go${GO_VERSION}.linux-amd64.tar.gz"; \
    elif [ "$ARCH" = "aarch64" ]; then \
        DOWNLOAD_ARCH="arm64"; \
        DOWNLOAD_URL="https://mirrors.aliyun.com/golang/go${GO_VERSION}.linux-arm64.tar.gz"; \
    else \
        echo "Unknow Archive: $ARCH"; exit 1; \
    fi && \
    echo "downloading Go ${GO_VERSION} (${DOWNLOAD_ARCH})..." && \
    wget -q --show-progress -O /tmp/go.tar.gz "${DOWNLOAD_URL}" && \
    tar -C /usr/local -xzf /tmp/go.tar.gz && \
    rm /tmp/go.tar.gz && \
    echo "Go ${GO_VERSION} (${DOWNLOAD_ARCH}) was installed successfully"

ENV PATH=$PATH:/usr/local/go/bin
ENV GOPROXY=https://mirrors.aliyun.com/goproxy,direct  
ENV NODE_VERSION=20.x

RUN curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION} | bash - && \
    apt-get install -y nodejs

RUN go version && node --version && npm --version

WORKDIR /app/service
COPY challenge/service/ ./

RUN go mod tidy
RUN go build -o service .
RUN mkdir /app/service/uploads

WORKDIR /app/sso
COPY challenge/sso/package*.json ./
RUN npm config set registry https://mirrors.cloud.tencent.com/npm/
#RUN npm config set disturl https://npm.taobao.org/dist
RUN npm ci 
COPY challenge/sso/ ./

COPY config/supervisord.conf /etc/supervisord.conf

ARG FLAG
ENV FLAG=$FLAG

CMD service redis-server start  && /usr/bin/supervisord -c /etc/supervisord.conf
