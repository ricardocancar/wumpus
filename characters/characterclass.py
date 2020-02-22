# -*- coding: utf-8 -*-
import numpy as np
from random import randint


INIT_DIRECTON = {0: 'x', 1: 'y'}


class Wumpus:
    def __init__(self, table):
        init_x, init_y = np.where(table == 2)
        self.x_post = int(init_x)
        self.y_post = int(init_y)
        self.sense = 1
        self.direction = 'y'
        
        
class Hounter:
    
    def __init__(self, table):
        init_x, init_y = np.where(table == 3)
        self.x_post = int(init_x)
        self.y_post = int(init_y)
        self.goldbar = False
        self.arrows = 3
        self.table_size = table.shape[1] - 1
        self.direction = INIT_DIRECTON[randint(0, 1)]
        """Para poder movernos una casilla para ir adelante y girar 90 grados
           necesitamos darle direccion y sentido al casador."""
        if self.x_post == 0:
            # el sentido del cazador
            self.sense = 1
            if self.y_post == self.table_size:
                self.direction = 'x'
        if self.x_post == self.table_size:
            self.sense = -1
            if self.y_post == 0:
                self.direction = 'y'
        if self.y_post == 0:
            # el sentido del cazador
            self.sense = 1
            if self.x_post == self.table_size:
                self.direction = 'y'
        if self.y_post == self.table_size:
            self.sense = -1
            if self.x_post == 0:
                self.direction = 'x'

    def movement(self):
        if self.direction == 'x':
            self.x_post = self.x_post + self.sense
        if self.direction == 'y':
            self.y_post = self.y_post + self.sense
    
    def turn_left(self):
        if self.direction == 'y' and self.sense == -1:
            self.direction = 'x'
        elif self.direction == 'x' and self.sense == -1:
            self.direction = 'y'
            self.sense = 1
        elif self.direction == 'y' and self.sense == 1:
            self.direction = 'x'
        elif self.direction == 'x' and self.sense == 1:
            self.direction = 'y'
            self.sense = -1
    
    def turn_right(self):
        if self.direction == 'y' and self.sense == -1:
            self.direction = 'x'
            self.sense = 1
        elif self.direction == 'x' and self.sense == 1:
            self.direction = 'y'
        elif self.direction == 'y' and self.sense == 1:
            self.direction = 'x'
            self.sense = -1
        elif self.direction == 'x' and self.sense == -1:
            self.direction = 'y'
            
    def get_gold(self, table):
        """set true goldbar hounter attribute when it get in the same place than 
           the gold bar"""
        if int(table.item(self.x_post, self.y_post)) == 4:
            self.goldbar = True
            