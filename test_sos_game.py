# test_sos_game.py

import unittest
import random
from sos_game import Player, HumanPlayer, ComputerPlayer, SOSGameLogic

class TestComputerPlayer(unittest.TestCase):
    def setUp(self):
        self.game = SOSGameLogic(3)  # Using 3x3 board for simple tests
        self.game.game_mode = "Simple"
        self.game.blue_player = ComputerPlayer("Blue")
        self.game.red_player = HumanPlayer("Red")
        self.computer_player = self.game.blue_player
        
    def test_computer_completes_sos(self):
        # Set up board where computer can complete SOS
        self.game.board[0][0] = 'S'
        self.game.board[0][1] = 'O'
        
        # Get computer move
        move = self.computer_player.make_move(self.game)
        self.assertIsNotNone(move, "Computer should make a move")
        
        row, col, letter = move
        # Computer should place 'S' at (0,2) to complete SOS
        self.assertEqual(row, 0)
        self.assertEqual(col, 2)
        self.assertEqual(letter, 'S')
        
    def test_computer_blocks_opponent_sos(self):
        # Set up board where opponent could complete SOS
        self.game.board[0][0] = 'S'
        self.game.board[0][1] = 'O'
        
        # Get computer move
        move = self.computer_player.make_move(self.game)
        self.assertIsNotNone(move, "Computer should make a move")
        
        row, col, letter = move
        # Computer should block at (0,2)
        self.assertEqual(row, 0)
        self.assertEqual(col, 2)
        self.assertEqual(letter, 'S')
        
    def test_computer_prefers_corners(self):
        # Empty board, no immediate SOS possibilities
        move = self.computer_player.make_move(self.game)
        self.assertIsNotNone(move, "Computer should make a move")
        row, col, letter = move
        # Move should be in a corner
        corners = {(0,0), (0,2), (2,0), (2,2)}
        self.assertIn((row, col), corners, "Move should be in a corner")
        # Should prefer 'S' for corner moves
        self.assertEqual(letter, 'S')
        
    def test_computer_plays_valid_moves(self):
        # Fill some squares
        self.game.board[0][0] = 'S'
        self.game.board[1][1] = 'O'
        self.game.board[2][2] = 'S'
        
        move = self.computer_player.make_move(self.game)
        self.assertIsNotNone(move, "Computer should make a move")
        
        row, col, letter = move
        # Move should be on empty square
        self.assertEqual(self.game.board[row][col], '', 
                        "Computer should only play on empty squares")
        self.assertIn(letter, ['S', 'O'], 
                     "Computer should only play valid letters")
        
    def test_computer_strategy_priority(self):
        # Setup board where computer can either complete SOS or block opponent
        self.game.board[0][0] = 'S'
        self.game.board[0][1] = 'O'  # Potential SOS completion
        self.game.board[1][0] = 'S'
        self.game.board[1][1] = 'O'  # Another potential SOS
        
        move = self.computer_player.make_move(self.game)
        self.assertIsNotNone(move, "Computer should make a move")
        
        row, col, letter = move
        # Should choose move to form SOS
        potential_moves = {(0,2), (1,2)}
        self.assertIn((row, col), potential_moves, 
                     "Computer should prioritize completing SOS")
        self.assertEqual(letter, 'S')

if __name__ == '__main__':
    unittest.main()
