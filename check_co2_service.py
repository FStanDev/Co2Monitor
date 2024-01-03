import time
import subprocess
from scd30_i2c import SCD30

scd30 = SCD30()
scd30.set_measurement_interval(2)
scd30.start_periodic_measurement()

def main():
   ultimo_envio = -1
   subprocess.run("curl -d 'Estoy Arrancando' ntfy.sh/lainteligenciamepersigue", shell=True)
   try:
    while True:
        if scd30.get_data_ready():
            m = scd30.read_measurement()
            if m is not None:
                number = m[0]
                print(number)
                if number > 2000 and number < 2500 and (ultimo_envio == -1 or ultimo_envio >= 30):
                    subprocess.run("curl -d 'Concentración elevada: " + str(number) + "' ntfy.sh/lainteligenciamepersigue", shell=True)
                    ultimo_envio=0
                elif number > 2500 and ultimo_envio > 15:
                    subprocess.run("curl -d 'Concentración muy elevada: " + str(number) + ". Ventila inmediatamente' ntfy.sh/lainteligenciamepersigue", shell=True)
                    ultimo_envio=5
            if ultimo_envio != -1:
                ultimo_envio+=1
            time.sleep(60)
   except Exception:
      subprocess.run("curl -d 'Excepción: " + str(Exception) + "' ntfy.sh/lainteligenciamepersigue", shell=True)

main()
