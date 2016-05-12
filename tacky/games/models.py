# -*- coding: utf-8 -*-
import random

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from tacky.users import models as user_models

ALL_SPOTS = [1,2,3,4,5,6,7,8,9]

@python_2_unicode_compatible
class Coordinate(models.Model):
    coordinate = models.IntegerField()
    player = models.ForeignKey(user_models.User)

    def __str__(self):
        return str(self.id)

@python_2_unicode_compatible
class Board(models.Model):
    coordinates = models.ManyToManyField(Coordinate)
    current_player = models.ForeignKey(user_models.User)

    def __str__(self):
        return str(self.id)

    def get_move(self):
        board_spots = [x.coordinate for x in self.coordinates.all()]
        free_spots = list(set(ALL_SPOTS) - set(board_spots))
        return random.choice(free_spots)

@python_2_unicode_compatible
class Game(models.Model):

    player1 = models.ForeignKey(user_models.User, related_name='player1')
    player2 = models.ForeignKey(user_models.User, related_name='player2')
    active = models.BooleanField(default=True)
    winner =  models.ForeignKey(user_models.User, null=True, blank=True, related_name='winner')
    board = models.ForeignKey(Board, related_name='board', null=True)

    def __str__(self):
        return str(self.id)

    def get_winner(self):

        WINNING_POSITIONS = [[self.one, self.two, self.three]]

        for position in WINNING_POSITIONS:
            if self.current_player in position:
                self.active = False
                self.winner = self.current_player
                return self.winner


