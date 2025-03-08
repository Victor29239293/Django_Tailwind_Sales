from datetime import datetime
from django.contrib.auth.models import Group
from django.http import HttpRequest
from app.security.models import GroupModulePermission, User


class MenuModule:
    def __init__(self, request: HttpRequest):
        self._request = request
        self._path = self._request.path
        print(self._request)

    def fill(self, data):
        """ Llena el diccionario `data` con información del usuario, grupos y menús """

        # Añadir usuario y fecha actual
        data['user'] = self._request.user
        data['date_time'] = datetime.now()
        data['date_date'] = datetime.now().date()

        # Verificar si el usuario está autenticado
        if self._request.user.is_authenticated:
            data['group_list'] = self._request.user.groups.all().order_by('id')

            # Si no hay `group_id` en la sesión, se guarda el primer grupo disponible
            if 'group_id' not in self._request.session:
                if data['group_list'].exists():
                    self._request.session['group_id'] = data['group_list'].first().id

            # Obtener el `group_id` de la URL o la sesión
            group_id = self._request.GET.get('gpid') or self._request.session.get('group_id')

            if group_id:
                try:
                    group_id = int(group_id)  # Convertir a entero para evitar errores
                    group = Group.objects.get(id=group_id)

                    # Guardar solo el ID y el nombre en `data`, evitando objetos no serializables
                    data['group'] = {
                        'id': group.id,
                        'name': group.name,
                    }

                    # Guardar lista de menús
                    data['menu_list'] = self.__get_menu_list(data['user'], group)

                    # Actualizar `group_id` en la sesión
                    self._request.session['group_id'] = group.id

                except (Group.DoesNotExist, ValueError):
                    # Si el grupo no existe o `group_id` no es válido, limpiar valores
                    data['group'] = None
                    data['menu_list'] = []
                    self._request.session.pop('group_id', None)  # Eliminar `group_id` inválido

    def __get_menu_list(self, user: User, group: Group):
        """ Obtiene la lista de menús disponibles para el grupo """

        # Obtener permisos de grupo con optimización de consulta
        group_module_permission_list = (
            GroupModulePermission.get_group_module_permission_active_list(group.id)
            .select_related('module__menu')
            .order_by('module__name')
        )

        # Obtener una lista única de menús basados en los módulos
        menu_unicos = group_module_permission_list.order_by('module__menu_id').distinct('module__menu_id')

        # Construir la lista de menús con sus submódulos
        menu_list = [self._get_data_menu_list(x, group_module_permission_list) for x in menu_unicos]
        return menu_list

    def _get_data_menu_list(self, group_module_permission: GroupModulePermission, group_module_permission_list):
        """ Genera la estructura de menú con permisos """
        group_module_permissions = group_module_permission_list.filter(
            module__menu_id=group_module_permission.module.menu_id
        )

        return {
            'menu': group_module_permission.module.menu,
            'group_module_permission_list': group_module_permissions,
        }
