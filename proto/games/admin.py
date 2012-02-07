from django.contrib import admin

import reversion

from proto.games.models import Game, Platform, DLC, Company, Genre, Theme

class GameAdmin(reversion.VersionAdmin):
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('developers', 'publishers',)
    autocomplete_lookup_fields = {
        'm2m': [['developers'], ['publishers']],
    }


class PlatformAdmin(admin.ModelAdmin):
    pass


class DLCAdmin(admin.ModelAdmin):
    pass


class CompanyAdmin(admin.ModelAdmin):
    pass


class GenreAdmin(admin.ModelAdmin):
    pass


class ThemeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Game, GameAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(DLC, DLCAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Theme, ThemeAdmin)
