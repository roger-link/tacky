import factory
from factory import fuzzy
import json

from tacky.users.tests import factories as users_factories

class BoardFactory(factory.django.DjangoModelFactory):
    coordinates = json.dumps({
                              0:'computer',
                              1:'player',
                              2:'computer',
                              3:'player',
                              4:'computer',
                              5:'player',
                              6:'computer',
                              7:'player',
                              8:'empty'}
                             , ensure_ascii=False)

    class Meta:
        model = 'games.Board'

class GameFactory(factory.django.DjangoModelFactory):
    player1 = factory.SubFactory(users_factories.UserFactory)
    player2 = factory.SubFactory(users_factories.UserFactory)
    active = True
    winner =  factory.SubFactory(users_factories.UserFactory)
    board = factory.SubFactory(BoardFactory)

    class Meta:
        model = 'games.Game'