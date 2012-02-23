from django.contrib import admin

from proto.games.models import Game, Platform, Franchise, Character, DLC, Company, Genre, Theme
from proto.wiki.admin import WikiPageAdmin


class GameAdmin(WikiPageAdmin):
    raw_id_fields = ('developers', 'publishers',)
    autocomplete_lookup_fields = {
        'm2m': [['developers'], ['publishers']],
    }


class PlatformAdmin(WikiPageAdmin):
    pass


class FranchiseAdmin(WikiPageAdmin):
    raw_id_fields = ('games',)
    autocomplete_lookup_fields = {
        'm2m': [['games']],
    }


class CharacterAdmin(WikiPageAdmin):
    raw_id_fields = ('games',)
    autocomplete_lookup_fields = {
        'm2m': [['games']],
    }


class DLCAdmin(WikiPageAdmin):
    pass


class CompanyAdmin(WikiPageAdmin):
    pass


class GenreAdmin(WikiPageAdmin):
    pass


class ThemeAdmin(WikiPageAdmin):
    pass


admin.site.register(Game, GameAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Franchise, FranchiseAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(DLC, DLCAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Theme, ThemeAdmin)
