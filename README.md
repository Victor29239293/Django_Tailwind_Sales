

# 🛒 Django_Tailwind_Sales - Sistema de Inventario y Ventas 📦  

**Django_Tailwind_Sales** es un sistema de **gestión de inventario y ventas** desarrollado con **Django** y **Tailwind CSS**, diseñado para optimizar la administración de productos, control de stock y registro de transacciones comerciales.  

## 🚀 Características  
✅ **Gestión de productos**: Agrega, edita y elimina productos con facilidad.  
✅ **Control de inventario**: Mantén un seguimiento preciso del stock disponible.  
✅ **Registro de ventas**: Historial detallado de ventas con información de clientes y productos.  
✅ **Reportes y análisis**: Visualiza estadísticas sobre productos vendidos y niveles de inventario.  
✅ **Gestión de usuarios y roles**: Permisos diferenciados para administradores y empleados.  
✅ **Interfaz moderna y responsive**: Diseñada con **Tailwind CSS** para una experiencia rápida y atractiva.  

## 🛠️ Tecnologías utilizadas  
- **Backend:** Django (Python)  
- **Frontend:** Tailwind CSS  
- **Base de datos:** PostgreSQL / SQLite  
- **Autenticación:** Django Auth (con permisos y roles)  

## 📦 Instalación  
1. Clona el repositorio:  
   ```bash
   git clone https://github.com/tuusuario/Django_Tailwind_Sales.git
   ```  
2. Entra en el directorio del proyecto:  
   ```bash
   cd Django_Tailwind_Sales
   ```  
3. Crea un entorno virtual e instala las dependencias:  
   ```bash
   python -m venv venv  
   source venv/bin/activate  # En Windows: venv\Scripts\activate  
   pip install -r requirements.txt
   ```  
4. Aplica las migraciones de la base de datos:  
   ```bash
   python manage.py migrate
   ```  
5. Ejecuta el servidor:  
   ```bash
   python manage.py runserver
   ```  

## 📌 Notas  
- Se puede configurar para usar **PostgreSQL**  como base de datos.  
- Los roles de usuario permiten restringir el acceso a ciertas funcionalidades.  
