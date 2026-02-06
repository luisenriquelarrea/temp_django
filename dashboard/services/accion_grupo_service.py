from dashboard.models import AccionGrupo

def get_allowed_breadcrumbs_for_group(user, seccionMenuId):
    """
    Returns AccionGrupo queryset for breadcrumbs allowed to a group
    """
    grupos = user.groups.all()

    return (
        AccionGrupo.objects
        .filter(
            grupo__in=grupos,
            status=True,
            accion__status=True,
            accion__on_breadcrumb=True,
            accion__seccion_menu_id=seccionMenuId,
        )
        .select_related(
            "accion",
        )
    )

def get_allowed_navbar_for_group(user, seccionMenuId):
    """
    Returns AccionGrupo queryset for navbar allowed to a group
    """
    grupos = user.groups.all()

    return (
        AccionGrupo.objects
        .filter(
            grupo__in=grupos,
            status=True,
            accion__status=True,
            accion__on_navbar=True,
            accion__seccion_menu_id=seccionMenuId,
        )
        .select_related(
            "accion",
        )
    )

def get_allowed_menus_for_group(user):
    """
    Returns AccionGrupo queryset for menus allowed to a group
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

def get_allowed_table_actions_for_group(user, seccionMenuId):
    """
    Returns AccionGrupo queryset for table actions allowed to a group
    """
    grupos = user.groups.all()

    return (
        AccionGrupo.objects
        .filter(
            grupo__in=grupos,
            status=True,
            accion__status=True,
            accion__on_table=True,
            accion__seccion_menu_id=seccionMenuId,
        )
        .select_related(
            "accion",
        )
    )