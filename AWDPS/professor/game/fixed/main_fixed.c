#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdarg.h>
#include <time.h>

void startMenu() {
  printf(
    "========================= MENU =========================\n"
    "[S]tart new game\n"
    "[E]xit\n"
    "========================================================\n"
    "You choice : "
  );
  fflush(stdout);
  return ;
}

typedef struct Position {
  int x, y;
}Position;

#define SKIN_OF_GRASS         0
#define SKIN_OF_WALL          1
#define SKIN_OF_PLAYER        2
#define SKIN_OF_BOX           3
#define SKIN_OF_TARGET        4
#define SKIN_OF_TREASURE      5
#define LENGTH_OF_SKIN_ARRAY  6
typedef struct Player {
  char *name;
  Position position;
  int towards;
  unsigned int score;
} Player;
typedef struct GameInfo {
  Position box_position;
  Position target_position;
  Player player;
  char* skins[LENGTH_OF_SKIN_ARRAY];
} GameInfo;

#define GRASS  SKIN_OF_GRASS
#define WALL   SKIN_OF_WALL
#define MAN    SKIN_OF_PLAYER
#define BOX    SKIN_OF_BOX
#define TARGET SKIN_OF_TARGET
#define TREASUREMARK 8
#define ADD_TREASURE (TREASUREMARK | 1)
#define SUB_TREASURE (TREASUREMARK | 2)
#define MUL_TREASURE (TREASUREMARK | 3)
#define DIV_TREASURE (TREASUREMARK | 4)
int map[25][25] = {
  {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
  {0, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, 0},
  {0, WALL,            0, WALL,    0,            0,    0,    0,    0,    0,    0,    0,    0, WALL,    0,    0, WALL, WALL,    0,    0,    0,    0, WALL, 0},
  {0, WALL,            0,    0,    0,            0,    0,    0,    0,    0,    0,    0,    0,    0, WALL,    0,    0, WALL,    0,    0,    0,    0, WALL, 0},
  {0, WALL,            0,    0,    0,            0,    0,    0,    0,    0,    0,    0, WALL, WALL,    0,    0,    0,    0,    0,    0,    0,    0, WALL, 0},
  {0, WALL,            0,    0,    0,            0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0, WALL,    0,    0,    0, WALL, 0},
  {0, WALL,            0,    0,    0,         WALL,    0, WALL,    0, WALL,    0,    0,    0,    0,    0,    0,    0,    0, WALL, WALL, WALL,    0, WALL, 0},
  {0, WALL,            0,    0,    0,         WALL, WALL, WALL,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0, WALL,    0, WALL, 0},
  {0, WALL,            0,    0,    0,            0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0, WALL, WALL, WALL, 0},
  {0, WALL,            0,    0, WALL,            0, WALL,    0, WALL,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0, WALL, WALL, WALL, 0},
  {0, WALL,            0,    0, WALL, MUL_TREASURE,    0, WALL, WALL, WALL,    0,    0, WALL,    0, WALL,    0,    0,    0,    0,    0, WALL,    0, WALL, 0},
  {0, WALL,            0,    0, WALL,            0,    0,    0,    0,    0,    0,    0, WALL,    0,    0, WALL,    0,    0,    0,    0,    0,    0, WALL, 0},
  {0, WALL,            0,    0, WALL,            0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0, WALL,    0,    0,    0, WALL,    0, WALL, 0},
  {0, WALL,            0,    0,    0,            0,    0,    0,    0,    0, WALL,    0,    0,    0,    0, WALL,    0,    0,    0,    0,    0,    0, WALL, 0},
  {0, WALL,            0,    0,    0,            0,    0,    0,    0,    0,    0,    0,    0,    0, WALL,    0,    0,    0,    0,    0,    0,    0, WALL, 0},
  {0, WALL,            0,    0,    0, ADD_TREASURE,    0,    0,    0, WALL,    0,    0,    0,    0,    0,    0,    0,    0, WALL,    0,    0,    0, WALL, 0},
  {0, WALL, DIV_TREASURE, WALL,    0,            0,    0,    0,    0,    0,    0,    0,    0,    0, WALL,    0,    0, WALL,    0,    0,    0,    0, WALL, 0},
  {0, WALL,            0, WALL,    0,            0,    0,    0,    0,    0,    0,    0,    0, WALL,    0,    0,    0, WALL,    0,    0,    0,    0, WALL, 0},
  {0, WALL,            0, WALL,    0,            0,    0,    0,    0, WALL,    0, WALL,    0, WALL,    0,    0,    0,    0, WALL,    0,    0,    0, WALL, 0},
  {0, WALL,            0,    0,    0,            0,    0,    0,    0,    0,    0,    0, WALL,    0,    0,    0,    0,    0,    0, WALL,    0,    0, WALL, 0},
  {0, WALL,            0,    0,    0,            0,    0,    0,    0,    0, WALL,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0, WALL, 0},
  {0, WALL,            0, WALL,    0,            0,    0,    0,    0, WALL, WALL,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0, WALL, 0},
  {0, WALL,         WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, 0}
};

#define UP    0
#define DOWN  1
#define LEFT  2
#define RIGHT 3
int mov[4][2] = {
  {-1, 0}, // UP
  { 1, 0}, // DOWN
  { 0,-1}, // LEFT
  { 0, 1}  // RIGHT
};
char toward_flag[4] = { 'U', 'D', 'L', 'R'};
GameInfo gameinfo;
void initializeGameConfiguration() {
  gameinfo.skins[SKIN_OF_GRASS]    = "     ";
  gameinfo.skins[SKIN_OF_WALL]     = "  W  ";
  gameinfo.skins[SKIN_OF_PLAYER]   = (char *)malloc(0x18);
  gameinfo.skins[SKIN_OF_PLAYER][0]=' ';gameinfo.skins[SKIN_OF_PLAYER][1]='0';gameinfo.skins[SKIN_OF_PLAYER][2]='w';gameinfo.skins[SKIN_OF_PLAYER][3]='0';gameinfo.skins[SKIN_OF_PLAYER][4]=' ';
  gameinfo.skins[SKIN_OF_BOX]      = "  B  ";
  gameinfo.skins[SKIN_OF_TARGET]   = "  T  ";
  gameinfo.skins[SKIN_OF_TREASURE] = "  *  ";
  
  gameinfo.player.position.x = 3;
  gameinfo.player.position.y = 2;
  gameinfo.player.towards    = DOWN;
  gameinfo.player.score      = 0;
  map[gameinfo.player.position.x][gameinfo.player.position.y] = MAN;

  while (1) {
    gameinfo.box_position.x = rand() % 18 + 3;
    gameinfo.box_position.y = rand() % 18 + 3;
    if (map[gameinfo.box_position.x][gameinfo.box_position.y] == 0) {
      map[gameinfo.box_position.x][gameinfo.box_position.y] = BOX;
      break;
    }
  }

  while (1) {
    gameinfo.target_position.x = rand() % 20 + 2;
    gameinfo.target_position.y = rand() % 20 + 2;
    if (map[gameinfo.target_position.x][gameinfo.target_position.y] == 0) {
      map[gameinfo.target_position.x][gameinfo.target_position.y] = TARGET;
      break;
    }
  }

  char tmp_name[64];
  puts("[*] What is your name?");
  fflush(stdout);
  scanf("%63s", tmp_name);
  while (getchar() != '\n');
  int name_length = strlen(tmp_name);
  char *name = malloc(name_length);
  strcpy(name, tmp_name);
  gameinfo.player.name = name;
}

void show() {
  printf("\033[2J\033[1:1H"); // 清除屏幕
  printf("User Name : %s\n", gameinfo.player.name);
  printf("User Toward : %c\n", toward_flag[gameinfo.player.towards]);
  printf("User Score : %u\n", gameinfo.player.score);
  for (int i = 1; i <= 22; ++i) {
    for (int j = 1; j <= 22; ++j)
      printf("%5s", gameinfo.skins[map[i][j] & TREASUREMARK ? SKIN_OF_TREASURE : map[i][j]]); // fix
    puts("");
  }
  printf("You can use 'wsad' to move!\n[b]urst the facing wall.\n[C]hange Your skin\n[q]uit\nYour operation : ");
  fflush(stdout);
}

void changeSkin() {
  printf("Your style of skin : ");
  fflush(stdout);
  scanf("%5s", gameinfo.skins[SKIN_OF_PLAYER]); // fix
  while (getchar() != '\n');
}

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

int operations() {
  char operation;
  scanf("%c", &operation);
  getchar();
  int moving_direction = -1;
  switch (operation) {
  case 'w':
    moving_direction = UP;
    break;
  case 's':
    moving_direction = DOWN;
    break;
  case 'a':
    moving_direction = LEFT;
    break;
  case 'd':
    moving_direction = RIGHT;
    break;
  case 'b': // burst the wall
    burstTheWall();
    break;
  case 'C':
    changeSkin();
    break;
  case 'q':
    free(gameinfo.player.name); free(gameinfo.skins[SKIN_OF_PLAYER]);
    return 1;
    return 1;
  default:
    break;
  }

  if (moving_direction != -1) {
    int nxt_x = gameinfo.player.position.x + mov[moving_direction][0], nxt_y = gameinfo.player.position.y + mov[moving_direction][1];
    if (map[gameinfo.target_position.x][gameinfo.target_position.y] == 0)
      map[gameinfo.target_position.x][gameinfo.target_position.y] = TARGET;
    if (map[nxt_x][nxt_y] == BOX) {
      int nnxt_x = nxt_x + mov[moving_direction][0], nnxt_y = nxt_y + mov[moving_direction][1];
      if (map[nnxt_x][nnxt_y] == WALL || map[nnxt_x][nnxt_y] & TREASUREMARK) {
        gameinfo.player.towards = moving_direction; 
        return 0;
      }
      map[nnxt_x][nnxt_y] = BOX;
      gameinfo.box_position.x = nnxt_x;
      gameinfo.box_position.y = nnxt_y;
    }
    else if (map[nxt_x][nxt_y] == WALL) {
      gameinfo.player.towards = moving_direction; 
      return 0;
    }
    else if (map[nxt_x][nxt_y] & TREASUREMARK) {
      switch (map[nxt_x][nxt_y]) {
      case ADD_TREASURE:
        gameinfo.player.score += 10;
        break;
      case SUB_TREASURE:
        gameinfo.player.score += -10;
        break;
      case MUL_TREASURE:
        gameinfo.player.score *= 10;
        break;
      case DIV_TREASURE:
        if (gameinfo.player.score > 0)
          gameinfo.player.score += 1000 / gameinfo.player.score;
        break;
      }
    }
    map[nxt_x][nxt_y] = MAN;
    map[gameinfo.player.position.x][gameinfo.player.position.y] = 0;
    gameinfo.player.position.x = nxt_x; gameinfo.player.position.y = nxt_y; // update player's position
    gameinfo.player.towards = moving_direction; 
  }
  return 0;
}

int bootNewGame() {
  srand(time(NULL));
  initializeGameConfiguration();
  while (1) {
    if (gameinfo.box_position.x == gameinfo.target_position.x && gameinfo.box_position.y == gameinfo.target_position.y) {
      puts("YOU ARE WIN!!!!!!!!!!!!!!");
      exit(0);
    }
    show();
    int res = operations();
    if (res)
      break;
  }
  return 0;
}

int main() {
  char user_choice;
  while (1) {
    startMenu();
    scanf("%c", &user_choice);
    getchar(); // Remove 
    switch (user_choice) {
      case 's':
      case 'S': {
        bootNewGame();
        break;
      }
      case 'e':
      case 'E': {
        puts("[*] Closing Game...Wait a moment, please!");
        exit(0);
      }
      default:
        puts("Error : Invalid choice!");
        break;
    }
  }
  return 0;
}