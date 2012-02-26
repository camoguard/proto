from django.contrib import admin

from proto.games.models import Game, Platform, Franchise, Character, DLC, Company, Genre, Theme
from proto.wiki.admin import WikiAdmin


class GameAdmin(WikiAdmin):
    raw_id_fields = ('developers', 'publishers',)
    autocomplete_lookup_fields = {
        'm2m': [['developers'], ['publishers']],
    }


class PlatformAdmin(WikiAdmin):
    raw_id_fields = ('company',)
    autocomplete_lookup_fields = {
        'fk': [['company']],
    }


class FranchiseAdmin(WikiAdmin):
    raw_id_fields = ('games',)
    autocomplete_lookup_fields = {
        'm2m': [['games']],
    }


class CharacterAdmin(WikiAdmin):
    raw_id_fields = ('games',)
    autocomplete_lookup_fields = {
        'm2m': [['games']],
    }


class DLCAdmin(WikiAdmin):
    pass


class CompanyAdmin(WikiAdmin):
    pass


class GenreAdmin(WikiAdmin):
    pass


class ThemeAdmin(WikiAdmin):
    pass


admin.site.register(Game, GameAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Franchise, FranchiseAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(DLC, DLCAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Theme, ThemeAdmin)
