# -*- coding: utf-8 -*-
import random
import json

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django_extensions.db.fields.json import JSONField

from tacky.users.models import User

ALL_MOVES = range(9)
WINNING_MOVES = [[u'0', u'1', u'2'], [u'3',u'4',u'5'], [u'6',u'7',u'8'], [u'0',u'3',u'6'], [u'1',u'4',u'7'], [u'2',u'5',u'8'], [u'0',u'4',u'8'], [u'2',u'4',u'6']]

@python_2_unicode_compatible
class Board(models.Model):
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
    coordinates = JSONField(null=True, blank=True, default=board_moves)

    def __str__(self):
        return str(self.id)

    @property
    def available_moves(self):
        """
        calculates all open indices and returns in list
        """
        return [key for key,value in self.coordinates.iteritems() if value=='empty']


    @property
    def generate_move(self):
        # update to minmax algorithm
        try:
            return random.choice(self.available_moves)
        except IndexError:
            return False

    def is_win(self, player):
        """
        player = 'player' or 'computer'
        """
        moves = [key for key, val in self.coordinates.iteritems() if val == player]
        return any([set(spot).issubset(set(moves)) for spot in WINNING_MOVES])

    def make_move(self, move='computer'):
        """generates move or adds move to list of coordinates
        move: index value for square, integer
        """
        if move == 'computer':
            self.coordinates[self.generate_move] = 'computer'
            self.save()

        else:
            self.coordinates[move] = 'player'
            self.save()

    @property
    def sorted_moves(self):
        return [self.coordinates[k] for k in sorted(self.coordinates)]

    @property
    def is_full(self):
        return (len(self.available_moves) == 0)

    # def minimax(self):
    #   moves = self.available_moves
    #   best_move = moves[0]
    #   best_score = float('-inf')
    #   for move in moves:
    #     coordinates = self.coordinates.all()
    #     import ipdb;ipdb.set_trace()
    #     self.make(move)
    #     self.save(commit=False)
    #     clone = Board(coordinates=coordinates)
    #     computer = User.objects.get(name='computer')
    #     clone.make_move(computer.id, move)
    #     score = self.min_play(clone)
    #     if score > best_score:
    #       best_move = move
    #       best_score = score
    #   return best_move

    # def min_play(board):
    #   if board.is_full:
    #     return board.evaluate(board)
    #   moves = board.available_moves
    #   best_score = float('inf')
    #   for move in moves:
    #     coordinates = board.coordinates.all()
    #     clone = Board(coordinates=coordinates)
    #     score = board.max_play(clone)
    #     if score < best_score:
    #       # best_move = move
    #       best_score = score
    #   return best_score

    # def max_play(board):
    #   if board.is_full:
    #     return board.evaluate(board)
    #   moves = board.available_moves
    #   best_score = float('-inf')
    #   for move in moves:
    #     clone = board.next_state(move)
    #     score = board.min_play(clone)
    #     if score > best_score:
    #       # best_move = move
    #       best_score = score
    #   return best_score

    # def evaluate(board):
    #     if board.is_win(board.board_moves, 'computer'):
    #         return float('inf')
    #     elif board.is_win(board.board_moves, 'player'):
    #         return float('-inf')
    #     else:
    #         return 0

class GameManager(models.Manager):
    def start_game(self, user):
        computer = User.objects.get(name='computer')
        board = Board.objects.create()
        game = self.create(player1=user, player2=computer, board=board)
        return game


@python_2_unicode_compatible
class Game(models.Model):

    player1 = models.ForeignKey(User, related_name='player1')
    player2 = models.ForeignKey(User, related_name='player2')
    active = models.BooleanField(default=True)
    winner =  models.ForeignKey(User, null=True, blank=True, related_name='winner')
    board = models.ForeignKey(Board, related_name='board', null=True)

    objects = GameManager()

    def __str__(self):
        return str(self.id)
