from dashboard.models import AccionGrupo

def get_allowed_menus_for_user(user):
    """
    Returns AccionGrupo queryset for menus allowed to a user
    """
    grupos = user.groups.all()

    return (
        AccionGrupo.objects
        .filter(
            grupo__in=grupos,
            status=True,
            accion__status=True,
            accion__on_breadcrumb=True,
            accion__seccion_menu__status=True,
            accion__seccion_menu__menu__status=True,
        )
        .select_related(
            "accion",
            "accion__seccion_menu",
            "accion__seccion_menu__menu"
        )
        .order_by(
            "accion__seccion_menu__menu__descripcion",
            "accion__seccion_menu__navbar_label",
        )
    )
