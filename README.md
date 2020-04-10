# MediaKaanª
MediaKaana es una aplicación web que corresponde a mi proyecto de fin de grado en Ingeniería Informática la UPV/EHU. Su propósito es servir a los usuarios como medio de comparto multimedia de manera altruista.

La estructura actual del proyecto tiene la siguiente forma:

```
.
|-- LICENSE
|-- MediaKaan
|   |-- __init__.py
|   |-- __pycache__
|   |-- asgi.py
|   |-- settings.py
|   |-- urls.py
|   `-- wsgi.py
|-- README.md
|-- gestionArticulos
|   |-- __init__.py
|   |-- __pycache__
|   |-- admin.py
|   |-- apps.py
|   |-- enums.py
|   |-- migrations
|   |   |-- 0001_initial.py
|   |   |-- 0002_auto_20200410_2103.py
|   |   |-- __init__.py
|   |   `-- __pycache__
|   |-- models.py
|   |-- tests.py
|   |-- urls.py
|   `-- views.py
|-- gestionUsuarios
|   |-- __init__.py
|   |-- __pycache__
|   |-- admin.py
|   |-- apps.py
|   |-- forms.py
|   |-- migrations
|   |   |-- 0001_initial.py
|   |   |-- 0002_usuarioubicacion.py
|   |   |-- __init__.py
|   |   `-- __pycache__
|   |-- models.py
|   |-- tests.py
|   |-- urls.py
|   `-- views.py
|-- manage.py
|-- media
|   |-- articulos
|   `-- avatars
|-- static
|   `-- gestionUsuarios
|       |-- css
|       |   |-- base.css
|       |   |-- bootstrap.css
|       |   `-- signin.css
|       |-- img
|       |   |-- author.jpg
|       |   `-- logo
|       |       |-- mediak-logo.ico
|       |       |-- mediak-logo.png
|       |       |-- motivation.png
|       |       `-- trade-scene.png
|       `-- js
|           |-- bootstrap.js
|           |-- jquery-3.4.1.min.js
|           |-- popper.js
|           |-- registerubication.js
|           `-- signupcounter.js
`-- templates
    |-- about.html
    |-- gestionUsuarios
    |   |-- base.html
    |   |-- registerubication.html
    |   |-- signin.html
    |   `-- signup.html
    `-- index.html

21 directories, 72 files
```
