# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from tacky.users import models as user_models



@python_2_unicode_compatible
class Game(models.Model):

    player1 = models.ForeignKey(user_models.User, related_name='player1')
    player2 = models.ForeignKey(user_models.User, related_name='player2')
    current_player = models.ForeignKey(user_models.User, null=True, blank=True, related_name='current_user')
    active = models.BooleanField(default=True)
    winner =  models.ForeignKey(user_models.User, null=True, blank=True, related_name='winner')

    one = models.ForeignKey(user_models.User, null=True, blank=True, related_name='one')
    two = models.ForeignKey(user_models.User, null=True, blank=True, related_name='two')
    three = models.ForeignKey(user_models.User, null=True, blank=True, related_name='three')
    four = models.ForeignKey(user_models.User, null=True, blank=True, related_name='four')
    five = models.ForeignKey(user_models.User, null=True, blank=True, related_name='five')
    six = models.ForeignKey(user_models.User, null=True, blank=True, related_name='six')
    seven = models.ForeignKey(user_models.User, null=True, blank=True, related_name='seven')
    eight = models.ForeignKey(user_models.User, null=True, blank=True, related_name='eight')
    nine = models.ForeignKey(user_models.User, null=True, blank=True, related_name='nine')

    def __str__(self):
        return str(self.id)

    def get_winner(self):

        WINNING_POSITIONS = [[self.one, self.two, self.three]]

        for position in WINNING_POSITIONS:
            if self.current_player in position:
                self.active = False
                self.winner = self.current_player
                return self.winner


