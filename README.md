
# Gestión de Eventos 🎉

¡Bienvenido a la aplicación de Gestión de Eventos! Esta plataforma está diseñada para facilitar la organización y gestión de eventos académicos y conferencias. Ofrece funcionalidades para la creación de eventos, envío y revisión de trabajos, y gestión de cronogramas.

## Características principales 📋

- **Gestión de eventos**: Crea y personaliza eventos con facilidad.
- **Envío de trabajos**: Los autores pueden enviar sus trabajos para revisión.
- **Revisión por pares**: Asigna revisores y gestiona revisiones de trabajos.
- **Gestión de cronogramas**: Organiza sesiones y cronogramas de eventos.
- **Configuración dinámica**: Personaliza la configuración del sitio según tus necesidades.

## Tecnologías utilizadas 🛠️

- **Django**: Framework web de alto nivel para el backend.
- **Bootstrap**: Framework de diseño para una interfaz de usuario atractiva y responsive.
- **SQLite**: Base de datos para el almacenamiento de datos.
- **Font Awesome**: Librería de iconos para una mejor experiencia visual.

## Instalación 🚀

Sigue estos pasos para poner en marcha el proyecto en tu máquina local:

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/tuusuario/gestion-eventos.git
   cd gestion-eventos
   ```

2. **Crea un entorno virtual y actívalo:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la base de datos:**

   ```bash
   python manage.py migrate
   ```

5. **Crea un superusuario para acceder al panel de administración:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecuta el servidor de desarrollo:**

   ```bash
   python manage.py runserver
   ```

7. **Accede a la aplicación en tu navegador:**

   ```
   http://127.0.0.1:8000/
   ```

## Uso 📚

### Autores

- Regístrate e inicia sesión.
- Envía tus trabajos para revisión en los eventos disponibles.

### Revisores

- Inicia sesión con tu cuenta de revisor.
- Revisa y evalúa los trabajos asignados.

### Organizadores

- Inicia sesión con tu cuenta de organizador.
- Crea y personaliza eventos.
- Asigna revisores a los trabajos.
- Gestiona el cronograma del evento.

## Contribuciones 🤝

¡Las contribuciones son bienvenidas! Si deseas contribuir, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza los cambios necesarios y haz commit (`git commit -am 'Añadir nueva característica'`).
4. Envía tus cambios a tu fork (`git push origin feature/nueva-caracteristica`).
5. Abre un Pull Request en GitHub.

## Licencia 📄

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Contacto ✉️

Si tienes alguna pregunta o sugerencia, no dudes en ponerte en contacto con nosotros:

- **Correo electrónico:** anthony.quiranza@cloudsofts.net
- **GitHub:** [tuusuario](https://github.com/anthonyquiranza)

---

¡Gracias por usar Gestión de Eventos! Esperamos que esta herramienta te sea de gran ayuda para la organización y gestión de tus eventos. 🎉
