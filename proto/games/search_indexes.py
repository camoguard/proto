from haystack import indexes

from proto.games.models import Game, Platform, Franchise, Character, DLC, Company, Genre, Theme
from proto.wiki.search_indexes import WikiIndex


class GameIndex(WikiIndex, indexes.Indexable):
    def get_model(self):
        return Game


class PlatformIndex(WikiIndex, indexes.Indexable):
    def get_model(self):
        return Platform


class FranchiseIndex(WikiIndex, indexes.Indexable):
    def get_model(self):
        return Franchise


class CharacterIndex(WikiIndex, indexes.Indexable):
    def get_model(self):
        return Character


class DLCIndex(WikiIndex, indexes.Indexable):
    def get_model(self):
        return DLC


class CompanyIndex(WikiIndex, indexes.Indexable):
    def get_model(self):
        return Company


class GenreIndex(WikiIndex, indexes.Indexable):
    def get_model(self):
        return Genre


class ThemeIndex(WikiIndex, indexes.Indexable):
    def get_model(self):
        return Theme
