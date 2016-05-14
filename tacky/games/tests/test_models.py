# -*- coding: utf-8 -*-

from django.test import TestCase
from tacky.users.tests import factories as users_factories
from tacky.games.tests import factories as games_factories

class TestBoardModel(TestCase):

    def test_generate_move_last(self):
    	"""
    	When all spots except the 8th are taken, get move should return the 9th
    	"""

        coord0 = games_factories.CoordinateFactory(position=0)
        coord1 = games_factories.CoordinateFactory(position=1)
        coord2 = games_factories.CoordinateFactory(position=2)
        coord3 = games_factories.CoordinateFactory(position=3)
        coord4 = games_factories.CoordinateFactory(position=4)
        coord5 = games_factories.CoordinateFactory(position=5)
        coord6 = games_factories.CoordinateFactory(position=6)
        coord7 = games_factories.CoordinateFactory(position=7)

        board = games_factories.BoardFactory(coordinates=(coord0, coord1, coord2, coord3, coord4, coord5, coord6, coord7))
        self.assertTrue(board.generate_move == 8)

    def test_generate_first(self):
    	"""
    	When all spots except the 1st are taken, get move should return the 1st
    	"""
        coord1 = games_factories.CoordinateFactory(position=1)
        coord2 = games_factories.CoordinateFactory(position=2)
        coord3 = games_factories.CoordinateFactory(position=3)
        coord4 = games_factories.CoordinateFactory(position=4)
        coord5 = games_factories.CoordinateFactory(position=5)
        coord6 = games_factories.CoordinateFactory(position=6)
        coord7 = games_factories.CoordinateFactory(position=7)
        coord8 = games_factories.CoordinateFactory(position=8)

        board = games_factories.BoardFactory(coordinates=(coord1, coord2, coord3, coord4, coord5, coord6, coord7, coord8))
        self.assertTrue(board.generate_move == 0)

    def test_generate_all(self):
        """
        When all spots eare taken, generate_move should return false
        """
        coord0 = games_factories.CoordinateFactory(position=0)
        coord1 = games_factories.CoordinateFactory(position=1)
        coord2 = games_factories.CoordinateFactory(position=2)
        coord3 = games_factories.CoordinateFactory(position=3)
        coord4 = games_factories.CoordinateFactory(position=4)
        coord5 = games_factories.CoordinateFactory(position=5)
        coord6 = games_factories.CoordinateFactory(position=6)
        coord7 = games_factories.CoordinateFactory(position=7)
        coord8 = games_factories.CoordinateFactory(position=8)

        board = games_factories.BoardFactory(coordinates=(coord0, coord1, coord2, coord3, coord4, coord5, coord6, coord7, coord8))
        self.assertEqual(board.generate_move, False)

    def test_generate_none(self):
        """
        When no spots are taken,
        """
        board = games_factories.BoardFactory()
        self.assertTrue(board.generate_move in range(9))

    def test_board_moves_123(self):
    	"""
    	board_moves returns the correct player positions
    	"""
    	player = users_factories.UserFactory()
        computer = users_factories.UserFactory(name='computer')
    	coord1 = games_factories.CoordinateFactory(position=1, player=player)
        coord2 = games_factories.CoordinateFactory(position=2, player=player)
        coord3 = games_factories.CoordinateFactory(position=3, player=computer)

        board = games_factories.BoardFactory(coordinates=(coord1, coord2, coord3))

        output = {   0: "empty",
                     1: 'player',
                     2: 'player',
                     3: 'computer',
                     4: "empty",
                     5: "empty",
                     6: "empty",
                     7: "empty",
                     8: "empty"}
        self.assertEqual(board.board_moves, output)

    def test_board_moves_empty(self):
        """
        board_moves returns the correct player positions
        """
        users_factories.UserFactory(name='computer')
        board = games_factories.BoardFactory()

        output = {   0: "empty",
                     1: 'empty',
                     2: 'empty',
                     3: 'empty',
                     4: "empty",
                     5: "empty",
                     6: "empty",
                     7: "empty",
                     8: "empty"}
        self.assertEqual(board.board_moves, output)

    def test_is_win_success(self):
    	player = users_factories.UserFactory()
        users_factories.UserFactory(name='computer')
    	coord1 = games_factories.CoordinateFactory(position=1, player=player)
        coord4 = games_factories.CoordinateFactory(position=4, player=player)
        coord7 = games_factories.CoordinateFactory(position=7, player=player)

        board = games_factories.BoardFactory(coordinates=(coord1, coord4, coord7))
        self.assertTrue(board.is_win(board.board_moves, 'player' ))

    def test_is_win_fail(self):
    	player = users_factories.UserFactory()
        users_factories.UserFactory(name='computer')
    	coord1 = games_factories.CoordinateFactory(position=1, player=player)
        coord4 = games_factories.CoordinateFactory(position=2, player=player)
        coord7 = games_factories.CoordinateFactory(position=4, player=player)

        board = games_factories.BoardFactory(coordinates=(coord1, coord4, coord7))
        self.assertFalse(board.is_win(board.board_moves, 'player' ))

    def test_make_move_empty(self):
        player = users_factories.UserFactory()
        board = games_factories.BoardFactory()
        self.assertEqual(len(board.coordinates.all()), 0)
        board.make_move(player.id)
        self.assertEqual(len(board.coordinates.all()), 1)

    def test_make_move(self):
        player = users_factories.UserFactory()
        board = games_factories.BoardFactory()
        self.assertEqual(len(board.coordinates.all()), 0)
        board.make_move(player.id, 0)
        board.make_move(player.id, 0)
        self.assertEqual(len(board.coordinates.all()), 2)
