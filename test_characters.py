import numpy as np
import unittest
from characters.characterclass import Hounter, Wumpus 
from wumpus import (smell_wumpus, is_windy, is_fall, is_player_kille_by_wumpus,
                    is_a_winner, is_limit_map, hit_wumpus, gold_position_x,
                    gold_position_y)


class TestCharactersInteractions(unittest.TestCase):
    def setUp(self):
        self.table = np.zeros((4, 4))
        self.table[0][0] = 3
        self.table[1][2] = 2
        self.table[0][1] = 1
        self.table[1][1] = 4
        
        self.table_2 = np.zeros((4, 4))
        self.table_2[3][3] = 3
        self.table_2[2][3] = 2
        self.hounter = Hounter(self.table)
        self.hounter_2 = Hounter(self.table_2)
        self.wumpus = Wumpus(self.table)
    def test_character_pos_init(self):
        ## game map init
        
        
        ## hounter
        for i in range(3):
            hounter = Hounter(self.table)
            self.assertEqual(hounter.x_post, 0)
            self.assertEqual(hounter.y_post, 0)
            self.assertEqual(hounter.sense, 1)
            self.assertNotEqual(hounter.sense, -1)
            
            
            hounter_2 = Hounter(self.table_2)
            self.assertEqual(hounter_2.x_post, 3)
            self.assertEqual(hounter_2.y_post, 3)
            self.assertEqual(hounter_2.sense, -1)
            self.assertNotEqual(hounter_2.sense, 1)
            
            
        ### wumpus
        wumpus = Wumpus(self.table)
        self.assertEqual(wumpus.x_post, 1)
        self.assertEqual(wumpus.y_post, 2)
            
    def test_enviroment_hazzards(self):
        # test all the hazzards in the map for the hounter
        self.assertEqual(is_windy(self.hounter, self.table), True)
        self.assertEqual(smell_wumpus(self.hounter, self.wumpus), False)
        self.hounter.x_post = 1
        self.hounter.y_post = 3
        self.assertEqual(smell_wumpus(self.hounter, self.wumpus), True)
        self.assertEqual(is_windy(self.hounter, self.table), False)
        
    def test_hounter_deaths(self):
        # test the two posibilities of death of the player
        
        self.assertEqual(is_fall(0, 1, self.table), True)
        self.assertEqual(is_fall(1, 1, self.table), False)
        self.hounter.x_post = 1
        self.hounter.y_post = 2
        self.assertEqual(
            is_player_kille_by_wumpus(self.hounter, self.table), True)
        
    def test_gold_interactions(self):
        # no gold bar
        self.hounter.x_post = 0
        self.hounter.y_post = 0
        self.assertEqual(self.hounter.goldbar, False)
        self.assertEqual(is_a_winner(self.hounter, self.table), False)
        # get the gold bar but is not in the exit
        self.hounter.x_post = 1
        self.hounter.y_post = 1
        self.hounter.get_gold(self.table)
        self.assertEqual(self.hounter.goldbar, True)
        self.assertEqual(is_a_winner(self.hounter, self.table), False)
        # get the gold bar an is in the exit
        self.hounter.x_post = 0
        self.hounter.y_post = 0
        self.assertEqual(is_a_winner(self.hounter, self.table), True)
        
        
    def test_map_limits(self):
        # test the limit maps
        self.assertEqual(is_limit_map(self.hounter, 4), False)
        self.hounter.x_post = 0
        self.hounter.y_post = 4
        self.assertEqual(is_limit_map(self.hounter, 4), True)
        self.hounter.x_post = 4
        self.hounter.y_post = 0
        self.assertEqual(is_limit_map(self.hounter, 4), True)
        self.hounter.x_post = -1
        self.hounter.y_post = 0
        self.assertEqual(is_limit_map(self.hounter, 4), True)
    
    def test_wumpus_death(self):
        # poor wumpus
        self.assertEqual(hit_wumpus(self.hounter, self.wumpus), False)
        self.hounter.x_post = 0
        self.hounter.y_post = 2
        self.hounter.direction = 'y'
        self.assertEqual(hit_wumpus(self.hounter, self.wumpus), False)
        # wumpus is x = 1 y = 2
        self.hounter.direction = 'x'
        self.hounter.sense = 1
        self.assertEqual(hit_wumpus(self.hounter, self.wumpus), True)
        
    def test_get_gold_position(self):
        # backwards, forwards, to the right, to the left
        self.hounter.x_post = 1
        self.hounter.y_post = 2
        self.hounter.direction = 'x'
        self.hounter.sense = 1
        self.assertEqual(gold_position_x(self.hounter, 3), 'forwards')
        
        self.assertEqual(gold_position_y(self.hounter, 2), '')
        self.hounter.direction = 'x'
        self.hounter.sense = 1
        self.assertEqual(gold_position_x(self.hounter, 0), 'backwards')
        
        self.assertEqual(gold_position_y(self.hounter, 3), 'to the left')
        
        self.hounter.direction = 'x'
        self.hounter.sense = -1
        self.assertEqual(gold_position_x(self.hounter, 0), 'forwards')
        
        self.assertEqual(gold_position_y(self.hounter, 3), 'to the right')
        
        self.hounter.direction = 'y'
        self.hounter.sense = 1
        self.assertEqual(gold_position_x(self.hounter, 0), 'to the left')
        
        self.assertEqual(gold_position_y(self.hounter, 3), 'forwards')
        
        self.hounter.direction = 'y'
        self.hounter.sense = -1
        self.assertEqual(gold_position_x(self.hounter, 0), 'to the right')
        
        self.assertEqual(gold_position_y(self.hounter, 3), 'backwards')
        
        
if __name__ == '__main__':
    unittest.main()
