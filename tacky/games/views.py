# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Game


class GameView(LoginRequiredMixin, TemplateView):

    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)
        return context
