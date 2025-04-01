# 题目镜像
名称：game

# 部署目录

bin：包含submit(选手验证程序)、make_and_run.py（checker）、compile_and_run.sh(编译包含沙箱，调用run)等

bin-src：bin涉及的程序源码

challenge：题目源码及readme文件

# 部署

docker-compose up -d

或

docker run --env CHECK_NUMBERS=20 -d -p "0.0.0.0:22:22" -h "game" --name="game" game

# 调用关系

submit->make_and_run.py->compile_and_run.sh->run

