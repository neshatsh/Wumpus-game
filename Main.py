import random
from Consts import *

world = [[[] for i in range(4)] for j in range(4)]
wampus_is_alive = True
X, Y = 3, 0
detective_is_alive = True
gold_grabbed = False
game_over = False
score = 0
has_shot = True
why_game_ended = 'Detective climbed up'
direction = DIRECTION_MAP.get('r')


def get_2_dim_rand():
    return random.randint(0, 3), random.randint(0, 3)


def create_random_world():
    a = (3, 0)
    while a == (3, 0):
        a = get_2_dim_rand()
    # print('wampus location is', a)
    world[a[0]][a[1]].append(WAMPUS)
    a = get_2_dim_rand()
    # print('gold location is', a)
    world[a[0]][a[1]].append(GOLD)
    tmp = set()
    for i in range(random.randint(1, 3)):
        a = get_2_dim_rand()
        if GOLD in world[a[0]][a[1]]:
            continue
        if a not in tmp and a != (3, 0):
            tmp.add(a)
            world[a[0]][a[1]].append(PIT)
            # print('pit {} location is'.format(i), a)


def print_world(world_detail):
    for i in range(4):
        print('+', end='')
        print('----------------+' * 4)
        for k in range(4):
            print('|', end='')
            for j in range(4):
                if k == 3 and X == i and Y == j:
                    print('       {}       |'.format(direction), end='')
                else:
                    try:
                        world[i][j][k]
                        if world_detail == '1' and (world[i][j][k] == GOLD or world[i][j][k] == WAMPUS or world[i][j][k] == PIT):
                            raise IndexError
                        print('       {}        |'.format(world[i][j][k]), end='')
                    except IndexError:
                        print('                |', end='')
            print()
    print('+', end='')
    print('----------------+' * 4)


def audit():
    pit_nearby = 0
    wampus_nearby = 0
    has_gold = 0
    scream = 0 if wampus_is_alive else 1
    x, y = X, Y
    to_check = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
    for i in to_check:
        x, y = i[0], i[1]
        if x < 0 or x > 3 or y < 0 or y > 3:
            continue
        data = world[x][y]
        for j in data:
            if j == PIT:
                pit_nearby += 1
            elif j == WAMPUS:
                wampus_nearby += 1
    if GOLD in world[X][Y]:
        has_gold += 1
    return '[has_gold:{}, wampus_nearby:{}, pit_nearby:{}, scream:{}]'.format(has_gold, wampus_nearby, pit_nearby,
                                                                              scream)


def rotate_left():
    global direction
    if direction == DIRECTION_MAP.get('l'):
        direction = DIRECTION_MAP.get('d')
    elif direction == DIRECTION_MAP.get('r'):
        direction = DIRECTION_MAP.get('u')
    elif direction == DIRECTION_MAP.get('u'):
        direction = DIRECTION_MAP.get('l')
    elif direction == DIRECTION_MAP.get('d'):
        direction = DIRECTION_MAP.get('r')


def rotate_right():
    global direction
    if direction == DIRECTION_MAP.get('l'):
        direction = DIRECTION_MAP.get('u')
    elif direction == DIRECTION_MAP.get('r'):
        direction = DIRECTION_MAP.get('d')
    elif direction == DIRECTION_MAP.get('u'):
        direction = DIRECTION_MAP.get('r')
    elif direction == DIRECTION_MAP.get('d'):
        direction = DIRECTION_MAP.get('l')


def forward_move():
    global direction
    global X, Y
    x, y = X, Y
    if direction == DIRECTION_MAP.get('l'):
        y -= 1
    elif direction == DIRECTION_MAP.get('r'):
        y += 1
    elif direction == DIRECTION_MAP.get('u'):
        x -= 1
    elif direction == DIRECTION_MAP.get('d'):
        x += 1
    if -1 < x < 4 and -1 < y < 4:
        X, Y = x, y


def shoot():
    global direction
    global X, Y
    global wampus_is_alive
    global why_game_ended
    global game_over
    global has_shot
    if has_shot:
        if direction == DIRECTION_MAP.get('l'):
            for i in range(0, Y):
                if WAMPUS in world[X][i]:
                    wampus_is_alive = False
                    break
        elif direction == DIRECTION_MAP.get('r'):
            for i in range(Y + 1, 4):
                if WAMPUS in world[X][i]:
                    wampus_is_alive = False
                    break
        elif direction == DIRECTION_MAP.get('u'):
            for i in range(0, X):
                if WAMPUS in world[i][Y]:
                    wampus_is_alive = False
                    break
        elif direction == DIRECTION_MAP.get('d'):
            for i in range(X + 1, 4):
                if WAMPUS in world[i][Y]:
                    wampus_is_alive = False
                    break
        has_shot = False


def grab():
    global X, Y
    global gold_grabbed
    if GOLD in world[X][Y]:
        gold_grabbed = True
        world[X][Y].remove(GOLD)


def climb():
    global game_over
    global X, Y
    if X == 3 and Y == 0:
        game_over = True


actions_map = {
    'l': rotate_left,
    'r': rotate_right,
    'f': forward_move,
    'g': grab,
    'c': climb,
    's': shoot,
}


def check_over():
    global game_over
    global wampus_is_alive
    global why_game_ended
    global X, Y
    global score
    if PIT in world[X][Y]:
        game_over = True
        why_game_ended = 'Detective falls in pit'
        score -= 1000
    if WAMPUS in world[X][Y] and wampus_is_alive:
        why_game_ended = 'Wampus killed detective'
        game_over = True
        score -= 1000
    return game_over


if __name__ == '__main__':
    print('Game starting...')
    print('generating a world...')
    create_random_world()
    turns = 0
    detail = input('how much detail to print world? (input integer 1 or 2. default 1) ')
    print(detail)
    while True:
        print_world(detail)
        print(audit())
        action = input('your action?')
        if action not in actions_map.keys():
            print('unknown command. l: rotate left, r: rotate right, f: move forward, g: grab, c: climb, s: shoot')
            continue
        turns += 1
        actions_map[action]()
        if check_over():
            break
    if gold_grabbed:
        score += 1000
    if not has_shot:
        score -= 10
    score -= turns
    print('game is over in {} turns. score {}. {}'.format(turns, score, why_game_ended))
    if gold_grabbed:
        print('detective has successfully grabbed gold')
    else:
        print('detective collected no gold')
    if wampus_is_alive:
        print('wampus is still alive')
    else:
        print('wampus is dead')
