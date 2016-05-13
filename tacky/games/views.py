# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from tacky.users import models as u_models
from tacky.games import models as g_models
from tacky.games import forms


class GameView(LoginRequiredMixin, TemplateView):

    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)
        if self.request.method == "POST":
            game = g_models.Game.objects.get(id=self.request.POST['game'])
        else:
            game = self.start_game()
        context['board'] = forms.BoardForm(initial={'player': self.request.user.id, 'game': game })
        context['player_moves'] = game.board.player_moves()
        return context

    def start_game(self):
    	computer = u_models.User.objects.get(name='computer')
    	board = g_models.Board.objects.create(current_player=self.request.user)
        game = g_models.Game.objects.create(player1=self.request.user, player2=computer, board=board)

    	return game

    def post(self, request, *args, **kwargs):

        form = forms.BoardForm(self.request.POST)
        context = self.get_context_data(**kwargs)

        if form.is_valid():
            post_data = form.cleaned_data
            game = g_models.Game.objects.get(id=post_data['game'])
            user = u_models.User.objects.get(id=post_data['player'])
            coordinate = g_models.Coordinate.objects.create(position=post_data['move'], player=user)
            game.board.coordinates.add(coordinate)
            is_win = game.board.is_win(game.board.player_moves())

            if is_win:
                return HttpResponse('Game is over!!', status=200, content_type='application/json')
            else:
                player2 = u_models.User.objects.get(name='computer')
                coordinate =  g_models.Coordinate.objects.create(position=game.board.get_move(), player=player2)
                game.board.coordinates.add(coordinate)
                is_win = game.board.is_win(game.board.player_moves())

                if is_win:
                    return HttpResponse('Game is over!!', status=200, content_type='application/json')

                context = self.get_context_data(**kwargs)
                context['player_moves'] = game.board.player_moves()
                return self.render_to_response(context)


    def win(self):
        return HttpResponse('Game is over!!', status=200, content_type='application/json')
