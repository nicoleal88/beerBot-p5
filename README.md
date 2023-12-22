# beerBot Drager: Software para monitorear temperaturas de fermentadores, visualizarlas en una interfaz web y acceder a los datos mediante un bot de Telegram

## Primeros pasos

### Habilitar puertos 1-Wire

Edite el archivo `/boot/config.txt`:

```bash
sudo nano /boot/config.txt
```

Agregue las siguientes líneas para habilitar los puertos 1-Wire:

```bash
dtoverlay=w1-gpio
dtparam=gpiopin=18
dtoverlay=w1-gpio
dtparam=gpiopin=27
dtoverlay=w1-gpio
dtparam=gpiopin=22
dtoverlay=w1-gpio
dtparam=gpiopin=23
```

### Verificar sensores conectados

Ejecute el siguiente comando para listar los sensores conectados:

```bash
ls /sys/bus/w1/devices/
```

### Verificar una lectura de temperatura

Use el siguiente comando para obtener la temperatura de un sensor específico:

```bash
cat /sys/bus/w1/devices/28-020592453487/w1_slave
```

## Instalar Node.js

1. Actualice los paquetes en su sistema operativo:

```bash
sudo apt update
sudo apt upgrade
```

2. Instale los paquetes necesarios para acceder al repositorio de Nodesource:

```bash
sudo apt install -y ca-certificates curl gnupg
```

3. Descargue la clave GPG de Nodesource y guárdela en el directorio `/usr/share/keyrings`:

```bash
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/nodesource.gpg
```

4. Agregue el repositorio de Node.JS a la lista de fuentes:

```bash
NODE_MAJOR=18  # Cambie a la versión deseada: 18 para LTS, 20 para la versión actual
echo "deb [signed-by=/usr/share/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
```

5. Actualice la lista de paquetes:

```bash
sudo apt update
```

6. Instale NodeJS:

```bash
sudo apt install nodejs
```

7. Verifique la instalación:

```bash
node -v
```

8. Instale el paquete "build-essential" para manejar problemas de compilación al instalar módulos adicionales:

```bash
sudo apt install build-essential
```

## Clonar el repositorio

```bash
git clone https://github.com/nicoleal88/beerBot-p5.git
cd beerBot-p5/
```

## Instalar dependencias del servidor

```bash
npm install
```

## Instalar PM2

### Instalar PM2 globalmente

```bash
npm install -g pm2
```

### Gestión de procesos con PM2

Arrancar un proceso:

```bash
pm2 start index.js
```

Detener un proceso:

```bash
pm2 stop mi-api
```

Reiniciar un proceso:

```bash
pm2 restart mi-api
```

Verificar procesos en ejecución:

```bash
pm2 list
```

Ver registros en tiempo real:

```bash
pm2 log
```

Generar el script de inicio:

```bash
pm2 startup
pm2 save
```

## Configurar aplicaciones y escritorios

1. Edite el archivo para especificar el escritorio de lanzamiento de ventanas:

```bash
nano /home/pi/.config/openbox/lxde-pi-rc.xml
```

```xml
<!-- Quiero que Chromium se ejecute en el escritorio 2 y maximizado -->
<application name="chromium-browser*">
  <desktop>2</desktop>
  <maximized>yes</maximized>
</application>
<!-- Quiero que el terminal se ejecute en el escritorio 3 -->
<application name="lxterminal*">
  <desktop>3</desktop>
</application>
<application name="python3*">
  <desktop>3</desktop>
</application>
```

2. Configure las aplicaciones de inicio en `/etc/xdg/lxsession/LXDE-pi/autostart`:

```bash
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
point-rpi

@chromium-browser --start-fullscreen localhost:3001
@lxterminal -e python3 /home/pi/beerBot-p5/RPI_python_post_request_buffer.py
@lxterminal -e python3 /home/pi/beerBot-p5/local_data_vis.py
@vlc -L --qt-minimal-view /home/pi/Videos/VideosTapRoom/ListaTapRoom.xspf
```

## BOT

## Instalar paquetes

```bash
sudo apt install python3-prettytable
pip3 install python-telegram-bot==13.7 --break-system-packages
```
