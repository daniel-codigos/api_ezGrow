import os
import subprocess



def reset_prin():
    subprocess.Popen(["screen","-dmL","-Logfile", "/home/pi/logs/screenproyect.0","-S", "ezWater_api", "python3", "/home/pi/proyecto_porta/auth/manage.py", "runserver", "192.168.1.44:8590"])



if __name__ == "__main__":
    reset_prin()

