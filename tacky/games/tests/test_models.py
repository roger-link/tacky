# -*- coding: utf-8 -*-

from django.test import TestCase
from tacky.users.tests import factories as users_factories
from tacky.games.tests import factories as games_factories

class TestBoardModel(TestCase):

    def test_generate_move_last(self):
    	"""
    	When all spots except the 8th are taken, get move should return the 9th
    	"""

        board_moves = {
                        0:'computer',
                        1:'player',
                        2:'computer',
                        3:'player',
                        4:'computer',
                        5:'player',
                        6:'computer',
                        7:'player',
                        8:'empty'}

        board = games_factories.BoardFactory(coordinates=board_moves)
        self.assertTrue(board.generate_move == 8)

    def test_generate_first(self):
    	"""
    	When all spots except the 1st are taken, get move should return the 1st
    	"""
        board_moves = {
                        0:'empty',
                        1:'player',
                        2:'computer',
                        3:'player',
                        4:'computer',
                        5:'player',
                        6:'computer',
                        7:'player',
                        8:'computer'}

        board = games_factories.BoardFactory(coordinates=board_moves)
        self.assertTrue(board.generate_move == 0)

    def test_generate_all(self):
        """
        When all spots eare taken, generate_move should return false
        """
        board_moves = {
                        0:'computer',
                        1:'player',
                        2:'computer',
                        3:'player',
                        4:'computer',
                        5:'player',
                        6:'computer',
                        7:'player',
                        8:'computer'}

        board = games_factories.BoardFactory(coordinates=board_moves)
        self.assertEqual(board.generate_move, False)

    def test_generate_none(self):
        """
        When no spots are taken,
        """
        board_moves = {
                        0:'empty',
                        1:'empty',
                        2:'empty',
                        3:'empty',
                        4:'empty',
                        5:'empty',
                        6:'empty',
                        7:'empty',
                        8:'empty'}
        board = games_factories.BoardFactory(coordinates=board_moves)
        self.assertTrue(board.generate_move in range(9))


    def test_is_win_success(self):
        board_moves = {
                         '0': "empty",
                         '1': "player",
                         '2': "empty",
                         '3': "empty",
                         '4': "player",
                         '5': "empty",
                         '6': "empty",
                         '7': "player",
                         '8': "empty"}
        board = games_factories.BoardFactory(coordinates=board_moves)
        self.assertTrue(board.is_win('player' ))

    def test_is_win_fail(self):
        board_moves = {
                         '0': "empty",
                         '1': "player",
                         '2': "player",
                         '3': "empty",
                         '4': "player",
                         '5': "empty",
                         '6': "empty",
                         '7': "empty",
                         '8': "empty"}

        board = games_factories.BoardFactory(coordinates=board_moves)
        self.assertFalse(board.is_win('player' ))

    def test_make_move_player(self):

        board_moves = {
                 0: "empty",
                 1: "empty",
                 2: "empty",
                 3: "empty",
                 4: "empty",
                 5: "empty",
                 6: "empty",
                 7: "empty",
                 8: "empty"}

        users_factories.UserFactory()
        board = games_factories.BoardFactory(coordinates=board_moves)
        player_moves = [key for key, val in board.coordinates.iteritems() if val == 'player']
        computer_moves = [key for key, val in board.coordinates.iteritems() if val == 'computer']
        self.assertEqual(len(player_moves), 0)
        self.assertEqual(len(computer_moves), 0)
        board.make_move(move=4)
        player_moves = [key for key, val in board.coordinates.iteritems() if val =='player']
        computer_moves = [key for key, val in board.coordinates.iteritems() if val == 'computer']
        self.assertEqual(len(player_moves), 1)
        self.assertEqual(len(computer_moves), 0)

    def test_make_move_computer(self):

        board_moves = {
                 0: "empty",
                 1: "empty",
                 2: "empty",
                 3: "empty",
                 4: "empty",
                 5: "empty",
                 6: "empty",
                 7: "empty",
                 8: "empty"}

        users_factories.UserFactory()
        board = games_factories.BoardFactory(coordinates=board_moves)
        player_moves = [key for key, val in board.coordinates.iteritems() if val == 'player']
        computer_moves = [key for key, val in board.coordinates.iteritems() if val == 'computer']
        self.assertEqual(len(player_moves), 0)
        self.assertEqual(len(computer_moves), 0)
        board.make_move()
        player_moves = [key for key, val in board.coordinates.iteritems() if val =='player']
        computer_moves = [key for key, val in board.coordinates.iteritems() if val == 'computer']
        self.assertEqual(len(player_moves), 0)
        self.assertEqual(len(computer_moves), 1)

    # def test_minimax(self):
    #     player = users_factories.UserFactory()
    #     computer = users_factories.UserFactory(name='computer')
    #     coord1 = games_factories.CoordinateFactory(position=1, player=player)
    #     coord4 = games_factories.CoordinateFactory(position=2, player=player)
    #     board = games_factories.BoardFactory(coordinates=(coord1, coord4))
    #     board.minimax()
