import factory
from factory import fuzzy

from tacky.users.tests import factories as users_factories

class CoordinateFactory(factory.django.DjangoModelFactory):
    position = fuzzy.FuzzyInteger(1, 9)
    player = factory.SubFactory(users_factories.UserFactory)

    class Meta:
        model = 'games.Coordinate'


class BoardFactory(factory.django.DjangoModelFactory):
    current_player = factory.SubFactory(users_factories.UserFactory)

    class Meta:
        model = 'games.Board'

    @factory.post_generation
    def coordinates(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for coordinate in extracted:
                self.coordinates.add(coordinate)

class GameFactory(factory.django.DjangoModelFactory):
    player1 = factory.SubFactory(users_factories.UserFactory)
    player2 = factory.SubFactory(users_factories.UserFactory)
    active = True
    winner =  factory.SubFactory(users_factories.UserFactory)
    board = factory.SubFactory(BoardFactory)

    class Meta:
        model = 'games.Game'