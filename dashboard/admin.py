from django.contrib import admin
from .models import (
    AccionBasica,
    Accion,
    AccionGrupo,
    Grupo,
    Menu,
    SeccionMenu,
    SeccionMenuInput,
    StyledColumn,
)

admin.site.register(AccionBasica)
admin.site.register(Accion)
admin.site.register(AccionGrupo)
admin.site.register(Grupo)
admin.site.register(Menu)
admin.site.register(SeccionMenu)
admin.site.register(SeccionMenuInput)
admin.site.register(StyledColumn)