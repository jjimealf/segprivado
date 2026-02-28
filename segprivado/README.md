# SegPrivado

Aplicacion web en Django para gestion basica de pacientes, citas medicas y farmacia.

El proyecto incluye:

- Autenticacion con usuario personalizado y roles (`paciente`, `medico`, `admin`).
- Solicitud e historial de citas para pacientes.
- Agenda e historial de pacientes para medicos.
- Catalogo de medicamentos para administracion.
- Flujo de compra en farmacia con carrito, validacion de stock e historial de compras.
- Endpoints API basicos para login y consultas de citas.

## Modulos principales

- `users`: autenticacion, registro, perfil y usuario personalizado.
- `appointments`: creacion e historial de citas, filtros y API de citas.
- `pharmacy`: medicamentos, carrito, compras e historial de compras.
- `nucleo`: vistas del panel y enrutado principal de la aplicacion.
- `templates` / `static`: layout global, estilos y recursos compartidos.

## Requisitos

- Python 3.x
- SQLite (se usa por defecto mediante `dev.sqlite3`)

Dependencias visibles en el proyecto:

- `Django`
- `django-cors-headers`
- `djangorestframework`
- `django-cleanup`
- `Pillow` (recomendado por el uso de `ImageField` en usuarios)

## Configuracion local

1. Crear y activar un entorno virtual.
2. Instalar las dependencias del proyecto.
3. Aplicar migraciones.
4. Iniciar el servidor.

Ejemplo:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install django django-cors-headers djangorestframework django-cleanup pillow
python manage.py migrate
python manage.py runserver
```

## Variables de entorno

El proyecto usa estas variables en `segprivado/settings/base.py`:

- `DJANGO_SECRET_KEY`: clave secreta de Django.
- `DJANGO_DEBUG`: activa o desactiva `DEBUG`.
- `DJANGO_ALLOWED_HOSTS`: hosts permitidos separados por comas.
- `DJANGO_CORS_ALLOW_ALL`: habilita CORS global.
- `DJANGO_CORS_ALLOWED_ORIGINS`: origenes CORS separados por comas.
- `DJANGO_SQLITE_NAME`: nombre del archivo SQLite (por defecto `dev.sqlite3`).

Si no defines variables, el proyecto usa valores por defecto de desarrollo.

## Base de datos

- La configuracion por defecto usa SQLite.
- El repositorio incluye `dev.sqlite3` para desarrollo local.
- El proyecto ya incorpora migraciones de compatibilidad para esquemas antiguos en `appointments` y `pharmacy`.

## Datos demo

Existe un comando para poblar una base limpia con datos minimos:

```bash
python manage.py seed_demo
```

Credenciales demo creadas/actualizadas por ese comando:

- Admin: `admin` / `admin12345`
- Medico: `doctor_demo` / `doctor12345`
- Paciente: `paciente_demo` / `paciente12345`

Tambien crea medicamentos de ejemplo si no existen.

## Flujos funcionales

### Autenticacion y perfiles

- El login principal entra por la raiz `/`.
- El logout se realiza por `POST`.
- El proyecto usa un modelo de usuario personalizado (`users.User`) con banderas `is_paciente` e `is_medico`.

### Citas

- Los pacientes pueden pedir una cita seleccionando fecha y medico.
- No se permiten citas duplicadas del mismo paciente en la misma fecha.
- Los pacientes pueden consultar su historial y filtrarlo por rango de fechas.
- Los medicos pueden ver agenda actual e historial de pacientes.

### Farmacia

- Los pacientes pueden agregar medicamentos a un carrito en sesion.
- El carrito no permite superar el stock disponible.
- Al confirmar una compra:
  - se recalcula el total real,
  - se valida stock dentro de transaccion,
  - se crea `Purchase`,
  - se crean sus `PurchaseItem`,
  - se descuenta stock,
  - y se vacia el carrito.
- Los pacientes disponen de una pantalla separada de historial de compras.

## Endpoints y rutas utiles

- Login web: `/`
- Panel: `/home`
- Logout: `/logout`
- Citas paciente: `/cita/`
- Historial de citas paciente: `/cita/index/`
- Farmacia: `/compra/`
- Historial de compras: `/compra/history/`
- API login: `/api/login/`
- API citas: `/api/citas/`

## Desarrollo y pruebas

Comandos utiles:

```bash
python manage.py migrate
python manage.py runserver
python manage.py test
python manage.py seed_demo
```

Nota: si falta `corsheaders`, `manage.py` no arrancara. Asegurate de instalar `django-cors-headers` antes de ejecutar comandos de Django.

## Estructura rapida

```text
appointments/   Gestion de citas
pharmacy/       Medicamentos, carrito y compras
users/          Autenticacion y perfiles
nucleo/         Panel principal y composicion de vistas
templates/      Layouts globales
static/         CSS, JS y assets
manage.py       Entrada principal de Django
```

## Estado actual

Es un proyecto funcional orientado a desarrollo local. El README documenta el estado actual del codigo y los flujos existentes, sin cubrir despliegue en produccion.
