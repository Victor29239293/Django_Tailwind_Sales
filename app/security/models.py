from crum import get_current_request
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.forms import model_to_dict


class Menu(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=150, unique=True)
    icon = models.CharField(verbose_name='Icono', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_model_to_dict(self):
        return model_to_dict(self)

    def get_icon(self):
        return self.icon if self.icon else 'bi bi-calendar-x-fill'

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
        ordering = ['-name']


class Module(models.Model):
    url = models.CharField(verbose_name='URL', max_length=100, unique=True)
    name = models.CharField(verbose_name='Nombre', max_length=100)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT, verbose_name='Menú')
    description = models.CharField(verbose_name='Descripción', max_length=200, blank=True, null=True)
    icon = models.CharField(verbose_name='Icono', max_length=100, blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Activo', default=True)
    permissions = models.ManyToManyField(Permission, verbose_name='Permisos', blank=True)

    def __str__(self):
        return f"{self.name} [{self.url}]"

    def get_model_to_dict(self):
        return model_to_dict(self)

    def get_icon(self):
        return self.icon if self.icon else 'bi bi-x-octagon'

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ('-name',)


class GroupModulePermission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name='Grupo')
    module = models.ForeignKey(Module, on_delete=models.PROTECT, verbose_name='Módulo')
    permissions = models.ManyToManyField(Permission, verbose_name='Permisos')

    def __str__(self):
        return f"{self.module.name} - {self.group.name}"

    @staticmethod
    def get_group_module_permission_active_list(group_id):
        return GroupModulePermission.objects.select_related('module', 'module__menu').filter(
            group_id=group_id, module__is_active=True
        )

    class Meta:
        verbose_name = 'Permiso de módulo del grupo'
        verbose_name_plural = 'Permisos de módulos de grupos'
        ordering = ('-id',)


class User(AbstractUser):
    dni = models.CharField(verbose_name='Cédula o RUC', max_length=13, blank=True, null=True)
    image = models.ImageField(verbose_name='Imagen', upload_to='users/', max_length=1024, blank=True, null=True)
    email = models.EmailField(verbose_name='Email', unique=True)
    direction = models.CharField(verbose_name='Dirección', max_length=200, blank=True, null=True)
    phone = models.CharField(verbose_name='Teléfono', max_length=50, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        permissions = (
            ("change_userprofile", "Cambiar perfil de usuario"),
            ("change_userpassword", "Cambiar contraseña de usuario"),
        )

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_groups(self):
        return self.groups.all()

    def get_short_name(self):
        return self.username

    def get_group_session(self):
        request = get_current_request()
        return Group.objects.get(pk=request.session.get('group_id'))

    def set_group_session(self):
        request = get_current_request()

        if 'group' not in request.session:
            groups = self.groups.all().order_by('id')
            if groups.exists():
                request.session['group_id'] = groups.first().id

    def get_image(self):
        return self.image.url if self.image else '/static/img/usuario_anonimo.png'


class AuditUser(models.Model):
    TIPOS_ACCIONES = (
        ('A', 'Adición'),
        ('M', 'Modificación'),
        ('E', 'Eliminación')
    )

    usuario = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.PROTECT)
    tabla = models.CharField(max_length=100, verbose_name='Tabla')
    registroid = models.IntegerField(verbose_name='Registro ID')
    accion = models.CharField(choices=TIPOS_ACCIONES, max_length=1, verbose_name='Acción')
    fecha = models.DateField(auto_now_add=True, verbose_name='Fecha')
    hora = models.TimeField(auto_now_add=True, verbose_name='Hora')
    estacion = models.CharField(max_length=100, verbose_name='Estación')

    def __str__(self):
        return f"{self.usuario.username} - {self.tabla} [{self.accion}]"

    class Meta:
        verbose_name = 'Auditoría de usuario'
        verbose_name_plural = 'Auditorías de usuarios'
        ordering = ('-fecha', 'hora')
