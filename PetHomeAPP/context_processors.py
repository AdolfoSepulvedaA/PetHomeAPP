def user_info(request):
    return {
        'es_autenticado': request.user.is_authenticated,
        'nombre_usuario': request.user.username if request.user.is_authenticated else '',
        'es_admin': request.user.is_authenticated and request.user.tipo_cuenta == 'admin',
    }