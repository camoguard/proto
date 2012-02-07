from django.contrib import admin

from proto.games.models import Game, Platform, DLC, Company, Genre, Theme
from proto.wiki.admin import WikiPageAdmin

class GameAdmin(WikiPageAdmin):
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('developers', 'publishers',)
    autocomplete_lookup_fields = {
        'm2m': [['developers'], ['publishers']],
    }


class PlatformAdmin(WikiPageAdmin):
    pass


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
admin.site.register(DLC, DLCAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Theme, ThemeAdmin)
