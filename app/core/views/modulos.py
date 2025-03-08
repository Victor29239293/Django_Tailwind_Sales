from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import PermissionMixin
from django.views.generic import TemplateView

class ModuloTemplateView(PermissionMixin, TemplateView):
    template_name = 'components/modulos.html'
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title1"] = "IC - Módulos"
        context["title2"] = "Módulos Disponibles"

        # Agregar información de usuario, grupos y menús al contexto
        MenuModule(self.request).fill(context)

        # Debugging: eliminar en producción
        print(context)

        return context
