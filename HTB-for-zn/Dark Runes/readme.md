# Usage

本题的文件树如下：

```
/ ---+---- src/
       |
       +---- static/
       |
       +---- views/
       |
       +---- some necessary file for this project
```

如果你没有使用 docker 的基础，你可以使用如下指令来创建并运行 docker application image：

```bash
chmod +x ./build-docker.sh
./build-docker.sh
```

> Note：我们建议你使用国内加速源 + 流量使用更加。当然会科学上网是最好的。

# Hint

如果你想要破解本题，你需要知道以下知识或技术：

- 注入
- 代码审计