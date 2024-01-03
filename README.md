# Co2Monitor
Repo donde está el código del proyecto del monitor de CO2

## Dependencia común
[SCD30 Python Driver](https://pypi.org/project/scd30-i2c/)

## Montaje recomendado
[Montaje](https://github.com/Sensirion/python-i2c-scd30)

## Distribución de Archivos

### Main.py
Archivo principal para la ejución del servior web, require de FastApi instalado. Tienes que cambiar la url del websocket a la tuya

### co2_web.service
Archivo para generar el servicio que corra en background en nuestra raspberry pi

### check_co2_service.py
Archivo para correr el script y que mande notificaciones push. Cambia el topic al tuyo

### co2_background_checker.service
Archivo para generar el servicio que corra en segundo plano

