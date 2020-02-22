import argparse
import logging
import numpy as np
from random import randint

from text import TEXTS, GAME_DESCRIPTION
from characters.characterclass import Wumpus, Hounter
from mapgenerator import init_map
logging.basicConfig(
    format='%(asctime)s - %(message)s', level=logging.INFO)

MAP_SIZE = {1: 8, 2: 16, 3: 32}
         
    
def is_limit_map(character, size_map):
    """check the limits of the map and denied the player
       traspass this limits"""
    limit = False
    if character.x_post < 0:
        character.x_post = 0
        limit = True
    elif character.x_post > size_map - 1:
        character.x_post = size_map - 1
        limit = True
    elif character.y_post < 0:
        character.y_post = 0
        limit = True
    elif character.y_post > size_map - 1:
        character.y_post = size_map - 1
        limit = True
    return limit
            

def smell_wumpus(hounter, wumpus):
        diff_x = hounter.x_post - wumpus.x_post
        diff_y = hounter.y_post - wumpus.y_post
        if abs(diff_x) == 1 and diff_y == 0:
            return True
        
        if abs(diff_y) == 1 and diff_x == 0:
            return True
        return False
    

def is_windy(hounter, table):
    holes_post = np.where(table == 1)
    
    holes = [(holes_post[0][i], holes_post[1][i])
             for i in range(len(holes_post[0]))]
    for hole_pos in holes:
        diff_x = hounter.x_post - hole_pos[0]
        diff_y = hounter.y_post - hole_pos[1]
        if abs(diff_x) == 1 and diff_y == 0:
            return True
        
        if abs(diff_y) == 1 and diff_x == 0:
            return True
    return False   

def is_fall(x_pos, y_pos, table):
    # check is the player fall in the pit
    if table.item(x_pos, y_pos) == 1:
        return True
    return False

        
def is_a_winner(hounter, table):
    # if the player is in the exit with a the gold bar win the game.
    if int(table.item(
            hounter.x_post, hounter.y_post)) == 3 and hounter.goldbar == True:
        return True
    return False

    
def hit_wumpus(hounter, wumpus):
    # if the wumpus is in te arrow way hit the wumpus
    diff_x = hounter.x_post - wumpus.x_post
    diff_y = hounter.y_post - wumpus.y_post
    if (diff_x < 0 and hounter.sense == 1  and diff_y == 0 
                   and hounter.direction == 'x'):
        return True
    
    if (diff_x > 0 and hounter.sense == -1  and diff_y == 0 
                   and hounter.direction == 'x'):
        return True

    if (diff_y < 0 and hounter.sense == 1 
                   and diff_x == 0 and hounter.direction == 'y'):
        return True
    
    if (diff_y > 0 and hounter.sense == -1 
                   and diff_x == 0 and hounter.direction == 'y'):
        return True
    return False


def is_player_kille_by_wumpus(hounter, table):
    # check if the player was kill by wumpus represent in the table by 2
    return table.item(hounter.x_post, hounter.y_post) == 2



def gold_position_x(hounter, gold_x_pos):
    """show the x direction of the gold bar respect to the hounter"""
    diff_x = hounter.x_post - gold_x_pos
    if diff_x < 0 and hounter.sense < 0 and hounter.direction == 'x':
        return 'backwards'
    if diff_x < 0 and hounter.sense > 0 and hounter.direction == 'x':
        return 'forwards'
    if diff_x < 0 and hounter.sense < 0 and hounter.direction == 'y':
        return 'to the left'
    if diff_x < 0 and hounter.sense > 0 and hounter.direction == 'y':
        return 'to the right' 
    if diff_x > 0 and hounter.sense < 0 and hounter.direction == 'x':
        return 'forwards'
    if diff_x > 0 and hounter.sense > 0 and hounter.direction == 'x':
        return 'backwards'
    if diff_x > 0 and hounter.sense < 0 and hounter.direction == 'y':
        return 'to the right'
    if diff_x > 0 and hounter.sense > 0 and hounter.direction == 'y':
        return 'to the left'        
    return ''

def gold_position_y(hounter, gold_y_pos):
    """show the y direction of the gold bar respect to the hounter"""
    diff_y = hounter.y_post - gold_y_pos
    if diff_y < 0 and hounter.sense < 0 and hounter.direction == 'x':
        return 'to the right'
    if diff_y < 0 and hounter.sense > 0 and hounter.direction == 'x':
        return 'to the left'
    if diff_y < 0 and hounter.sense < 0 and hounter.direction == 'y':
        return 'backwards'
    if diff_y < 0 and hounter.sense > 0 and hounter.direction == 'y':
        return 'forwards'   
    if diff_y > 0 and hounter.sense < 0 and hounter.direction == 'x':
        return 'to the left'
    if diff_y > 0 and hounter.sense > 0 and hounter.direction == 'x':
        return 'to the right'
    if diff_y > 0 and hounter.sense < 0 and hounter.direction == 'y':
        return 'forwards'
    if diff_y > 0 and hounter.sense > 0 and hounter.direction == 'y':
        return 'backwards'
    return ''

    
def update_table(table, x_pos, y_pos, value):
    """insert a new value in de table """
    # use for update the wumpus position !
    table[x_pos][y_pos] = value
    return table

    
def wumpus_random_movement(wumpus, table, map_size):
    """define the random movement of the wumpus"""
    direction_dict = {0: 'x', 1: 'y'}
    sense_dict = {0: -1, 1: 1}
    limit_min = 0
    limit_max = map_size - 1
    move = True
    while move:
        direction = direction_dict[randint(0, 1)]
        sense = sense_dict[randint(0, 1)]
        if direction == 'x':
            new_x_pos = wumpus.x_post + sense
            try:
                # check if the new_x_post is in table index
                cell_value = table.item(new_x_pos, wumpus.y_post)
            except IndexError:
                cell_value = -1
            is_free = False
            if cell_value == 0:
                is_free = True
            if new_x_pos >= limit_min and new_x_pos <= limit_max and is_free:
                table = update_table(table, wumpus.x_post, wumpus.y_post, 0)
                wumpus.x_post += sense
                table = update_table(table, wumpus.x_post, wumpus.y_post, 2)
                move = False
        elif direction == 'y':
            new_y_pos = wumpus.y_post + sense
            try:
                # check if the new_y_post is in table index
                cell_value = table.item(wumpus.x_post, new_y_pos)
            except IndexError:
                cell_value = -1
            is_free = False
            if cell_value == 0:
                is_free = True
            if new_y_pos >= limit_min and new_y_pos <= limit_max and is_free:
               table = update_table(table, wumpus.x_post, wumpus.y_post, 0)
               wumpus.y_post += sense
               table = update_table(table, wumpus.x_post, wumpus.y_post, 2)
               move = False


def is_accepted_key(list_of_characters, text):
    """check the key is accepted
    list_of_characters: list of character accepted for continue the game
    text: is the key of the text intended to show in case is pressed the wrong
          key"""
    exit = 1
    while exit:
        entry = input()
        if entry == 'h':
            print(TEXTS['help_menu'])
        if entry in list_of_characters:
            exit = 0
        elif entry != 'h' and entry not in list_of_characters:
            print(TEXTS[text])
    return entry
        

def main():
    parser = argparse.ArgumentParser(
        description=(GAME_DESCRIPTION))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-s', '--size', type=int,
                        required=True,
                        help='provide the size map 1 for small 2 medium 3 big')
    
    # this argument is usefull to test the program is working right
    parser.add_argument('-c', '--cheat', type=int,
                        required=False, default=0,
                        help='for false 0 and 1 for true, if is true show '
                        'the map the wumpus positions holes gold bar etc.')
    args = parser.parse_args()
    try:
        map_size = MAP_SIZE[args.size]
    except KeyError:
        entry = is_accepted_key(
            ['1', '2', '3'], 'size_map_help')
        map_size = MAP_SIZE[int(entry)]
    cheat = False
    if args.cheat:
        cheat = True
    num_holes = int((map_size**2)/10)
    table = init_map(map_size, num_holes)
    gold_x_pos, gold_y_pos = np.where(table == 4)
    hounter = Hounter(table)
    wumpus = Wumpus(table)
    game = True
    is_wumpus_live = True
    print(GAME_DESCRIPTION)
    while game:
        
        print(TEXTS['gold_position'].format(
            abs(hounter.x_post - int(gold_x_pos)),
            gold_position_x(hounter, gold_x_pos),
            abs(hounter.y_post - int(gold_y_pos)),
            gold_position_y(hounter, gold_y_pos)))
        print(f'Map size: {map_size}x{map_size}\t'
              f'Number of holes: {num_holes}\t'
              f'number of arrow {hounter.arrows}\n\n\n')
        if cheat:
            print('#'*20 + ' CHEAT MODE ' + '#'*20)
            print(table)
            print(
                f"hounter x pos: {hounter.x_post}\t"
                f"hounter y pos: {hounter.y_post}\n"
                f"hounter direction: {hounter.direction}\t"
                f"hounter sense: {hounter.sense}\n"
                f"wum x pos: {wumpus.x_post}\t wum y pos: {wumpus.y_post}")
        entry = is_accepted_key(
            ['a', 'w', 'd', 'q', 'r', 'e'], 'help') 
        if entry == 'w':
            hounter.movement()
        if entry == 'a':
            hounter.turn_left()
        if entry == 'd':
            hounter.turn_right()
        if entry == 'e':
           game = False
           continue
        if entry == 'q':
            # the hounter shoot the arrow
            if hounter.arrows > 0:
                hit = hit_wumpus(hounter, wumpus)
                hounter.arrows -= 1
                if hit:
                    table[wumpus.x_post][wumpus.y_post] = 0
                    is_wumpus_live = False
                    print(TEXTS['wumpus_death'])
                else:
                    print(TEXTS['arrow_wall'])
            else:
                print(TEXTS['no_arrows'])
        limit = is_limit_map(hounter, map_size)
        smell = smell_wumpus(hounter, wumpus)
        windy = is_windy(hounter, table)
        fall = is_fall(hounter.x_post, hounter.y_post, table)
        win = is_a_winner(hounter, table)
        if win:
            print(TEXTS['winner'])
            is_accepted_key(['r', 'e', 'h'], 'winner')
            if entry == 'r':
                table = init_map(map_size)
                hounter = Hounter(table)
                wumpus = Wumpus(table)
        hounter.get_gold(table)
        if hounter.goldbar:
            print(TEXTS['get_gold'])
            table[hounter.x_post][hounter.y_post] = 0
        if is_wumpus_live:
            wumpus_random_movement(wumpus, table, map_size)
        if windy:
            print(TEXTS['warning_hole_near'])
        if smell:
            print(TEXTS['warning_wumpus_near'])
        if limit:
            print(TEXTS['hit_wall'])
        if is_player_kille_by_wumpus(hounter, table):
            print(TEXTS['death_wumpus'])
            is_accepted_key(['r', 'e'], 'death_wumpus')
            if entry == 'r':
                table = init_map(map_size)
                hounter = Hounter(table)
                gold_x_pos, gold_y_pos = np.where(table == 4)
                wumpus = Wumpus(table)
        if fall:
            print(TEXTS['death_hole'])
            is_accepted_key(['r', 'e'], 'death_hole')
            if entry == 'r':
                table = init_map(map_size)
                hounter = Hounter(table)
                gold_x_pos, gold_y_pos = np.where(table == 4)
                wumpus = Wumpus(table)
       
       

if __name__ == '__main__':
    main()