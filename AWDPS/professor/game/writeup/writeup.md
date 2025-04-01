# vuln1

缓冲区溢出

main.c:125行至main.c:133，`scanf()`函数输入没有限制。导致存在栈溢出，后续检查只是阻断栈溢出影响到堆溢出。

```c
  char tmp_name[64];
  puts("[*] What is your name?");
  scanf("%s", tmp_name);
  getchar();
  int name_length = strlen(tmp_name);
  if (name_length >= 64) {
    tmp_name[63] = '\0';
    name_length = 64;
  }
  char *name = malloc(name_length);
  strcpy(name, tmp_name);
```

```c
  char tmp_name[64];
  puts("[*] What is your name?");
  // fix
  scanf("%63s", tmp_name);
  getchar();
  int name_length = strlen(tmp_name);
  char *name = malloc(name_length);
  strcpy(name, tmp_name);
```

# vuln2

格式化字符串问题

main.c:152行可以更换玩家皮肤，如果皮肤是恶意格式化字符串加上main.c:144行`show()`函数中的`printf()`缺失参数，导致格式化字符串漏洞

```c
printf(gameinfo.skins[map[i][j] & TREASUREMARK ? SKIN_OF_TREASURE : map[i][j]]);
```
增加参数：

```c
printf("%5s", gameinfo.skins[map[i][j] & TREASUREMARK ? SKIN_OF_TREASURE : map[i][j]]); // fix
```

# vuln3

差一错误

main.c : 152 行 `changSkin()` 函数中 `scanf()` 会自动填充 `\x00` 导致存在差一错误，通过阅读代码可以知道实际给 gameinfo.skins[SKIN_OF_PLAYER] 分配的只有 24 的空间。

```c
scanf("%24s", gameinfo.skins[SKIN_OF_PLAYER]);
```

限制读入即可：

```c
scanf("%5s", gameinfo.skins[SKIN_OF_PLAYER]); // fix
```

# vuln4

除 0 问题

在 main.c : 218 行 `operations()` 函数中，在做除法时没有检测 `gameinfo.player.score` 是否为 0。

```c
gameinfo.player.score += 1000 / gameinfo.player.score;
break;
```

增加检查：

```c
if (gameinfo.player.score > 0) // fix
	gameinfo.player.score += 1000 / gameinfo.player.score;
break;
```

# vuln5

不正确的数组索引

在 main.c : 153 至 main.c : 162 的 `brustTheWall()` 函数没有限制破坏边界墙体导致存在错误索引的可能

```c
    _printf("Content:");
    scanf("%s",chunks[index].buf);
```
限制对边界墙体的破坏：
```c
void burstTheWall() { // fix
  int towards_x = gameinfo.player.position.x + mov[gameinfo.player.towards][0], towards_y = gameinfo.player.position.y + mov[gameinfo.player.towards][1];
  if (towards_x == 1 || towards_x == 22 || towards_y == 1 || towards_y == 22) { // fix
    return ;
  }
  if (map[towards_x][towards_y] == WALL)
    map[towards_x][towards_y] = 0;
  else
    printf("[ERROR] !");
}
```
