FROM ubuntu:24.04

# install base tools
ENV DEBIAN_FRONTEND=noninteractive TZ=Asia/Shanghai
ENV LC_ALL=en_US.UTF-8
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
    sed -i "s/deb http:\/\/se/#/g" /etc/apt/sources.list && \
    sed -i "s/deb-src http:\/\/se/#/g" /etc/apt/sources.list && \
    apt-get update  && \
    apt-get install -y lib32z1 openssh-server unzip make wget bison flex build-essential curl python3-dev python3 python3-pip git vim nano locales && \
    rm -rf /var/lib/apt/lists/* && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen && \
    python3 -m pip install pwn -i https://pypi.tuna.tsinghua.edu.cn/simple --break-system-packages && \
    python3 -m pip install pycryptodome -i https://pypi.tuna.tsinghua.edu.cn/simple --break-system-packages


# 开启ssh登录 添加运维public key、添加选手账户
RUN rm -f /etc/service/sshd/down && \
    sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -ri 's/#UseDNS\ no/UseDNS\ no/g' /etc/ssh/sshd_config && \
    sed -ri "s/StrictModes yes/StrictModes no/g" /etc/ssh/sshd_config && \
    sed -ri "s/UsePAM yes/UsePAM no/g" /etc/ssh/sshd_config && \
    echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config && \
    # mkdir /root/.ssh && \
    echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCmb+HMOVNQUM/85LfQ5l8FG1TbTfk9iPemWTF3WBRa8dmZ1oEbiZJeAjF9ykQtHFUthYRrsAL8JMP+giDSDNO6c48CvWIlm2oZGEm22//seB6MTnfhsb4jgJP24kIW08kT12tqVn1OebNLeFnaNv/R7qj0XBOQ/oEuHI5qs1gEAAXNQ8wMD2u9Fv2INAN35pNLjKs0GpwcviA2gG5wwAZEZ2KAtxbvktPU4SLMcE/srDjR3EuK5WPADUgu+kqL8wqTM/bk6s94e9nE8Xcxe6uACiFz/IpIXYarFCwg/WJSpcJ7axUGuQcCLr9Fa9lZjVyoe3SrlkhwPy+vr68zXqedZXbyKMBoX7g/maToWYfaQZPSlxC6BQxf57zLGe3n7CjT0d4x2afbsKaVgRRw/CVRgY9JmKmhoAYN4eTHB+ihE/Q3pLeKzXNJ1EiM0iMIqH12oBHxwug2+la9mQKr7GhZXHRDF7Jq0Vs5fkTKccxiZ7+VYRNtKwigWsxe8qIRaqk= huaweiad@virtual.com' >> /root/.ssh/authorized_keys  && \
    chmod 600 /root/.ssh/authorized_keys && \
    useradd -m -s /bin/bash sectest && \
    useradd -r -s /usr/sbin/nologin -d /nonexistent test && \
    echo "sectest:UWF9GN05yXSV" | chpasswd && \
    echo "root:QY6jAK5s" | chpasswd

WORKDIR /home/sectest/challenge

# add problem file
ADD ./challenge /home/sectest/challenge
# backup problem file
ADD ./challenge/ /root/
# use run submit ot check
ADD ./bin/submit /home/sectest/challenge/submit
# add nessacry file
ADD ./bin /root/
ADD ./start.sh /start.sh

# Disable pwntools updating
RUN mkdir -p /root/.config && \
    mkdir -p /root/bak_main && \
    echo '[update]' >> /root/.config/pwn.conf && \
    echo 'interval=never' >> /root/.config/pwn.conf

# safe perm  set gcc compile
RUN chown -R root:root /home/sectest && \
    chown -R root:sectest /home/sectest/challenge/* && \
    chmod -R 775 /home/sectest && \
    chmod +x /root/* && \
    chown root:root /home/sectest/challenge/submit && \
    chmod 4755 /home/sectest/challenge/submit && \
    chmod 644 /home/sectest/challenge/readme.txt && \
    mkdir /home/sectest/.ssh && \
    rm /usr/bin/gcc /usr/bin/g++ /usr/bin/cc /usr/bin/c++ && \
    mv /root/gcc /usr/bin/gcc && \
    mv /root/g++ /usr/bin/g++ && \
    chown root:root /usr/bin/gcc /usr/bin/g++ && \
    chmod 755 /usr/bin/gcc /usr/bin/g++ && \
    chmod 700 /start.sh

# Header doesn't contain vulnerabilities, so it does't need to be edited.
RUN sh -c "[ -e /home/sectest/challenge/header.h ] && chmod 644 /home/sectest/challenge/header.h; exit 0"

CMD ["/start.sh"]
