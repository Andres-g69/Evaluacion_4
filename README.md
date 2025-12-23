Bastian Cabello y Andrés González

🛠️ Instalación del Sistema NUAM en Linux

Sigue los pasos a continuación para instalar y ejecutar el proyecto NUAM en un entorno Linux.


1️⃣ Clonar el repositorio

Abre una terminal y clona el proyecto desde GitHub:

- git clone https://github.com/Andres-g69/Evaluacion_4.git


Luego entra al directorio del proyecto:

- cd Evaluacion_4


2️⃣ Crear un entorno virtual (recomendado)

Crea un entorno virtual de Python para aislar las dependencias del proyecto:

- python3 -m venv environment


Activa el entorno virtual:

- source environment/bin/activate


💡 Si al intentar usar python3 no funciona, puedes probar con python.


3️⃣ Instalar las dependencias

Antes de instalar las librerias se aplican los siguientes comandos requeridos:

- sudo apt update (colocar su contraseña de dispositivo si la requiere)
- sudo apt install mysql-server
- sudo apt install pkg-config libmysqlclient-dev build-essential (instala paquetees esenciales para mysqlclient)

Instala todas las librerías necesarias desde el archivo requirements.txt:

- pip install -r requirements.txt

- sudo mysql
- source /home/frontend1/Evaluacion_4/db_setup.sql; (colocar direccion de archivo db_setup.ql)
- exit

- Instalación de los componentes de Kafka

El sistema utiliza Apache Kafka junto con Zookeeper, desplegados mediante contenedores Docker.

🔹 Requisitos previos

Antes de comenzar, asegúrese de contar con:

Docker

Docker Compose

Git

🔹 Instalación y ejecución

Clonar el repositorio del proyecto:

git clone <url-del-repositorio>
cd <nombre-del-proyecto>


Levantar los servicios de Kafka y Zookeeper:

docker-compose up -d


Verificar que los contenedores estén en ejecución:

docker ps

Instalación de certificados de seguridad

Para asegurar la comunicación entre los servicios y las APIs, el sistema utiliza certificados de seguridad (SSL/TLS).

🔹 Generación de certificados

Crear un directorio para los certificados:

mkdir certs


Generar un certificado autofirmado:

openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes


Guardar los certificados generados en el directorio correspondiente del proyecto.

🔹 Configuración

Los certificados deben ser referenciados en la configuración del servidor API.

Kafka puede configurarse para usar SSL si se requiere comunicación segura entre brokers y clientes.


4️⃣ Aplicar las migraciones de la base de datos

Ejecuta los siguientes comandos para crear las tablas necesarias en la base de datos:

- python manage.py makemigrations
- python manage.py migrate


5️⃣ Crear un superusuario (opcional, para administración)

Si deseas acceder al panel de administración de Django, crea un superusuario:

- python manage.py createsuperuser


Sigue las instrucciones en pantalla (nombre, correo y contraseña).


6️⃣ Ejecutar el servidor

Inicia el servidor de desarrollo de Django:

- python manage.py runserver


Por defecto, el servidor estará disponible en:

👉 https://127.0.0.1


7️⃣ Acceder al sistema

Una vez iniciado el servidor, puedes acceder a las siguientes rutas principales:

- Login: /login/

- Registro: /register/

- Dashboard principal: /dashboard/

Ejemplo:
https://127.0.0.1/login/


8️⃣Acceder a Panel de Administración

De la misma manera de las rutas principales seguiremos con el panel de administración:

- https://127.0.0.1/admin/

- con los valores del superuser creados anteriormente iniciar sesion

- full acceso al panel de administración del sistema


9️⃣Detener el servidor

Para detener el servidor presiona Ctrl + C en la terminal donde se esté ejecutando.
