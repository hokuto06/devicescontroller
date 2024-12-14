# Automatización de Configuración de Dispositivos de Red

Este proyecto en **Django** automatiza la configuración masiva de dispositivos de red como switches, access points, y routers. Facilita la interacción con controladores Ruckus, UniFi y Meraki, y puede leer datos de archivos Excel o mediante una interfaz web.

---

## 🚀 **Características**

- Automatización de configuraciones de switches, APs y routers.
- Integración con APIs de Ruckus, UniFi y Meraki.
- Interfaz web para cargar y visualizar configuraciones.
- Lectura de datos desde archivos Excel.

---

## 🛠️ **Requisitos del sistema**

- **Sistema Operativo**: Ubuntu o Windows
- **Python 3.8+**
- **MongoDB** (para base de datos)

---

## 📦 **Instalación**

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/tu-usuario/tu-proyecto.git
   cd tu-proyecto```

2. **Crea entorno Virtual:**

	python3 -m venv venv
	source venv/bin/activate  # En Windows: venv\Scripts\activate


3. **Instalar dependencias:**

	pip install -r requirements.txt

4. **Configura MongoDB:**
	
	Instalar MongoDB
	Comprobar que MongoDB se este ejecuanto localhost:27017

5. **Ejecutar la aplicacion:**
	
	python manage.py runserver 

	
