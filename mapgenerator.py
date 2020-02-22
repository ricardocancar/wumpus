# -*- coding: utf-8 -*-
import numpy as np
from random import randint

def table_generator(table_size):
    """generate a table for the game 
       table size is an int"""
    return np.zeros((table_size, table_size))


def hole_positions(table, map_size, num_holes):
    """generate holes depending on de map size"""
    
    i = 0
    while i < num_holes:
        # inside the matrix 1 mean a hole in the game
        j = randint(0, map_size - 1)
        k = randint(0, map_size - 1)
        if table[j][k] == 0:
            table[j][k] = 1
            i += 1
    return table


def wumpus_init_pos(table, map_size):
    """generate a wunpus in the map"""
    wum = True
    while wum:
        # inside the matrix 1 mean a hole in the game
        j = randint(0, map_size - 1)
        k = randint(0, map_size - 1)
        if table[j][k] == 0:
            table[j][k] = 2
            wum = False
    return table

def exit_positions(table, map_size):
    """exit in the map"""
    init = True
    while init:
        # inside the matrix 1 mean a hole in the game
        j = randint(0, map_size - 1)
        if j == 0 or j == map_size - 1:
            k = randint(0, map_size - 1)
        else:
            init_k = {0: 0, 1: map_size - 1}
            k = init_k[randint(0, 1)]
        if table[j][k] == 0:
            table[j][k] = 3
            init = False
    return table


def goldbar_generator(table, map_size):
    """generate a goldbar in the map"""
    gold = True
    player_x, player_y = np.where(table == 3)
    while gold:
        # inside the matrix 1 mean a hole in the game
        j = randint(0, map_size - 1)
        k = randint(0, map_size - 1)
        diff_x = j - player_x
        diff_y = k - player_y
        treshold = int(map_size/3)
        # player can't be near the gold bar
        if table[j][k] == 0 and abs(
                diff_x) > treshold and abs(diff_y) > treshold:
            table[j][k] = 4
            gold = False
    return table


def init_map(map_size, num_holes):
    # call the funtion to init the table 
    table = table_generator(map_size)
    table = hole_positions(table, map_size, num_holes)
    table = wumpus_init_pos(table, map_size)
    table = exit_positions(table, map_size)
    table = goldbar_generator(table, map_size)
    return table