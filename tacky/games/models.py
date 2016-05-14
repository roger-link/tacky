# -*- coding: utf-8 -*-
import random

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from tacky.users.models import User

ALL_MOVES = [0,1,2,3,4,5,6,7,8]
WINNING_MOVES = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]

@python_2_unicode_compatible
class Coordinate(models.Model):
    position = models.IntegerField()
    player = models.ForeignKey(User)

    def __str__(self):
        return str(self.id)

@python_2_unicode_compatible
class Board(models.Model):
    coordinates = models.ManyToManyField(Coordinate)
    current_player = models.ForeignKey(User)

    def __str__(self):
        return str(self.id)

    @property
    def generate_move(self):
        board_moves = [x.position for x in self.coordinates.all()]
        free_moves = list(set(ALL_MOVES) - set(board_moves))
        try:
            return random.choice(free_moves)
        except IndexError:
            return False

    @property
    def board_moves(self):
        """
        creates dictionary of index:owner
        if not owned value will be "empty"
        if owned value will either be "player" or "computer"
        example:

        {
         0: "player",
         1: "empty",
         2: "empty",
         3: "computer",
         4: "empty",
         5: "empty",
         6: "empty",
         7: "empty",
         8: "empty",}
        """
        computer = User.objects.get(name='computer')
        moves = {coordinate.position:('computer' if coordinate.player.id == computer.id else 'player') for coordinate in self.coordinates.all()}
        for x in range(9):
            if x in moves.keys():
                pass
            else:
                moves[x] = "empty"
        return  moves

    def is_win(self, moves, player):
        """
        moves = dictionary of index:owner ('player', 'computer', 'empty')
        player = 'player' or 'computer'
        """
        moves = [key for key, val in moves.iteritems() if val == player]
        return any([set(spot).issubset(set(moves)) for spot in WINNING_MOVES])

    def make_move(self, player_id, move=None):
        """generates move or adds move to list of coordinates
        move: index value for square, integer
        """
        if not move and move != 0:
            move = self.generate_move
        user = User.objects.get(id=player_id)
        coordinate = Coordinate.objects.create(position=move, player=user)
        self.coordinates.add(coordinate)

    @property
    def is_full(self):
        return (len(self.coordinates.all()) == 9)


class GameManager(models.Manager):
    def start_game(self, user):
        computer = User.objects.get(name='computer')
        board = Board.objects.create(current_player=user)
        game = self.create(player1=user, player2=computer, board=board)
        return game


@python_2_unicode_compatible
class Game(models.Model):

    player1 = models.ForeignKey(User, related_name='player1')
    player2 = models.ForeignKey(User, related_name='player2', default=User.objects.get(name='computer'))
    active = models.BooleanField(default=True)
    winner =  models.ForeignKey(User, null=True, blank=True, related_name='winner')
    board = models.ForeignKey(Board, related_name='board', null=True)

    objects = GameManager()

    def __str__(self):
        return str(self.id)

