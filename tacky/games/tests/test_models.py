# -*- coding: utf-8 -*-

from django.test import TestCase
from tacky.users.tests import factories as users_factories
from tacky.games.tests import factories as games_factories

class TestBoardModel(TestCase):

    def test_get_move_last(self):
    	"""
    	When all spots except the 9th are taken, get move should return the 9th
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
        self.assertTrue(board.get_move() == 9)

    def test_get_move_first(self):
    	"""
    	When all spots except the 1st are taken, get move should return the 1st
    	"""
        coord2 = games_factories.CoordinateFactory(position=2)
        coord3 = games_factories.CoordinateFactory(position=3)
        coord4 = games_factories.CoordinateFactory(position=4)
        coord5 = games_factories.CoordinateFactory(position=5)
        coord6 = games_factories.CoordinateFactory(position=6)
        coord7 = games_factories.CoordinateFactory(position=7)
        coord8 = games_factories.CoordinateFactory(position=8)
        coord9 = games_factories.CoordinateFactory(position=9)

        board = games_factories.BoardFactory(coordinates=(coord2, coord3, coord4, coord5, coord6, coord7, coord8, coord9))
        self.assertTrue(board.get_move() == 1)

    def test_player_moves(self):
    	"""
    	player_moves returns the correct player positions
    	"""
    	player = users_factories.UserFactory()
    	coord1 = games_factories.CoordinateFactory(position=1, player=player)
        coord2 = games_factories.CoordinateFactory(position=2, player=player)
        coord3 = games_factories.CoordinateFactory(position=3, player=player)

        board = games_factories.BoardFactory(coordinates=(coord1, coord2, coord3))
        self.assertTrue(board.player_moves() == [1,2,3])

    def test_is_win_success(self):
    	player = users_factories.UserFactory()
    	coord1 = games_factories.CoordinateFactory(position=1, player=player)
        coord4 = games_factories.CoordinateFactory(position=4, player=player)
        coord7 = games_factories.CoordinateFactory(position=7, player=player)

        board = games_factories.BoardFactory(coordinates=(coord1, coord4, coord7))
        moves = board.player_moves()
        self.assertTrue(board.is_win(moves))

    def test_is_win_fail(self):
    	player = users_factories.UserFactory()
    	coord1 = games_factories.CoordinateFactory(position=1, player=player)
        coord4 = games_factories.CoordinateFactory(position=2, player=player)
        coord7 = games_factories.CoordinateFactory(position=4, player=player)

        board = games_factories.BoardFactory(coordinates=(coord1, coord4, coord7))
        moves = board.player_moves()
        self.assertFalse(board.is_win(moves))
