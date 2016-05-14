# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from tacky.users.models  import User
from tacky.games.models import Game
from tacky.games.forms import BoardForm


class GameView(LoginRequiredMixin, TemplateView):

    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):

        if self.request.method == "POST":
            game = Game.objects.get(id=self.request.POST['game'])
        else:
            game = Game.objects.start_game(self.request.user)

        context = super(GameView, self).get_context_data(**kwargs)
        context['form'] = BoardForm(initial={'player': self.request.user.id, 'game': game })
        context['board'] = game.board
        return context


    def post(self, request, *args, **kwargs):

        form = BoardForm(self.request.POST)
        context = self.get_context_data(**kwargs)

        if form.is_valid():
            game = Game.objects.get(id=form.cleaned_data['game'])
            game.board.make_move(form.cleaned_data['player'], form.cleaned_data['move'])
            player_win = game.board.is_win(game.board.board_moves, 'player')

            if player_win:
                context['win_message'] = 'You won!!!'
            elif game.board.is_full:
                context['win_message'] = 'You tied!!!'

            else:
                # computers turn
                computer = User.objects.get(name='computer')
                game.board.make_move(computer.id)
                computer_win = game.board.is_win(game.board.board_moves, 'computer')
                if computer_win:
                    context['win_message'] = 'You lost!!!'
                elif game.board.is_full:
                    context['win_message'] = 'You tied!!!'

                context['board'] = game.board
            return self.render_to_response(context)
        else:
            return HttpResponseRedirect(reverse('games::game'))
