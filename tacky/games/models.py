# -*- coding: utf-8 -*-
import random

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from tacky.users import models as user_models

ALL_MOVES = [0,1,2,3,4,5,6,7,8]
WINNING_MOVES = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]

@python_2_unicode_compatible
class Coordinate(models.Model):
    position = models.IntegerField()
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
        board_moves = [x.position for x in self.coordinates.all()]
        free_moves = list(set(ALL_MOVES) - set(board_moves))
        return random.choice(free_moves)

    def player_moves(self):
        computer = user_models.User.objects.get(name='computer')
        moves = {coordinate.position:('computer' if coordinate.player.id == computer.id else 'player') for coordinate in self.coordinates.all()}
        for x in range(9):
            if x in moves.keys():
                pass
            else:
                moves[x] = None
        return  moves


    def is_win(self, moves):
        player_moves = [key for key, val in moves.iteritems() if val == 'player']
        computer_moves = [key for key, val in moves.iteritems() if val == 'computer']
        thing = [any([set(spot).issubset(set(player_moves)) for spot in WINNING_MOVES]),
                 any([set(spot).issubset(set(computer_moves)) for spot in WINNING_MOVES])]
        return any(thing)


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


