# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from tacky.users import models as u_models
from tacky.games import models as g_models


class GameView(LoginRequiredMixin, TemplateView):

    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)
        game = self.start_game()
        context['game'] = game
        return context

    def start_game(self):
    	computer = u_models.User.objects.get(name='computer')

    	coordinate1 = g_models.Coordinate(player=self.request.user, coordinate=1)
        coordinate1.save()
        coordinate3 = g_models.Coordinate(player=self.request.user, coordinate=3)
        coordinate3.save()

    	board = g_models.Board(current_player=self.request.user)
        board.save()
        board.coordinates.add(coordinate1, coordinate3)
        board.save()


        game = g_models.Game.objects.create(
        	player1 = self.request.user,
        	player2 = computer,
        	board = board
        	)


    	return game

