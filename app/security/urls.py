from django.urls import path
from app.security.views import auth, menu, modulos, grupo
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = "security"

urlpatterns = [
    # URLs de autenticación
    path('auth/login', auth.signin, name="auth_login"),
    path('auth/signup', auth.signup, name='auth_signup'),
    path('auth/logout', auth.signout, name='auth_logout'),
    path('my/profile/<int:pk>/', auth.profile, name='auth_profile'),
    path('my/profile/update_profile/<int:pk>/', auth.UpdateProfileView.as_view(), name='auth_update_profile'),
    path('my/change_password/<int:pk>/', auth.CustomPasswordChangeView.as_view(), name='auth_change_password'),

    # URLs de recuperación de contraseña
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='security/auth/password_reset_form.html',
             email_template_name='security/auth/password_reset_email.html',
             subject_template_name='security/auth/password_reset_subject.txt',
             success_url=reverse_lazy('security:password_reset_done')
         ), 
         name='password_reset'),

    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='security/auth/password_reset_done.html'
         ), 
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='security/auth/password_reset_confirm.html',
             success_url=reverse_lazy('security:password_reset_complete')
         ), 
         name='password_reset_confirm'),

    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='security/auth/password_reset_complete.html'
         ), 
         name='password_reset_complete'),

    # Rutas de menú
    path('menus_list/', menu.MenuListView.as_view(), name='menu_list'),
    path('menus/create/', menu.MenuCreateView.as_view(), name='menu_create'),
    path('menus/update/<int:pk>/', menu.MenuUpdateView.as_view(), name='menu_update'),
    path('menus/delete/<int:pk>/', menu.MenuDeleteView.as_view(), name='menu_delete'),

    # Rutas de módulos
    path('modules_list/', modulos.ModuleListView.as_view(), name='module_list'),
    path('modules/create/', modulos.ModuleCreateView.as_view(), name='module_create'),
    path('modules/update/<int:pk>/', modulos.ModuleUpdateView.as_view(), name='module_update'),
    path('modules/delete/<int:pk>/', modulos.ModuleDeleteView.as_view(), name='module_delete'),

    # URLs de grupo
    path('group_module_permissions_list/', grupo.GroupModulePermissionListView.as_view(), name='group_module_permission_list'),
    path('group_module_permissions/create/', grupo.GroupModulePermissionCreateView.as_view(), name='group_module_permission_create'),
    path('group_module_permissions/update/<int:pk>/', grupo.GroupModulePermissionUpdateView.as_view(), name='group_module_permission_update'),
    path('group_module_permissions/delete/<int:pk>/', grupo.GroupModulePermissionDeleteView.as_view(), name='group_module_permission_delete'),

    # Obtener permisos por módulo y grupo
    path('get-module-permissions/<int:module_id>/', grupo.get_module_permissions, name='get_module_permissions'),
]
    