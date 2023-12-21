# beerBot Drager

## Primeros pasos

### Habilitar puertos 1 wire

Editar archivo `sudo nano /boot/config.txt`

'''
dtoverlay=w1-gpio
dtparam=gpiopin=18
dtoverlay=w1-gpio
dtparam=gpiopin=27
dtoverlay=w1-gpio
dtparam=gpiopin=22
dtoverlay=w1-gpio
dtparam=gpiopin=23
'''

### Ver los sensores conectados

`ls /sys/bus/w1/devices/`

### Ver un dato de temperatura

`cat /sys/bus/w1/devices/28-020592453487/w1_slave`

## Instalar Node.js

1. Before we begin installing NodeJS to our Raspberry Pi, let us first update the packages running on our operating system.

We can update the package list and upgrade existing packages using the following two commands.

`sudo apt update`
`sudo apt upgrade`

2. Our next step is ensuring we have all the packages we need to access the Nodesource repository.

Install these packages by using the following command in the terminal.

`sudo apt install -y ca-certificates curl gnupg`

3. With our Raspberry Pi up to date, we can now set up the NodeSource repository.

This repository will allow us to install the latest versions of NodeJS to the Raspberry Pi easily.

Let us start this process by downloading the Nodesource GPG key and storing it within the `/usr/share/keyrings` directory.

`curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/nodesource.gpg`

4. With the GPG key stored on our Raspberry Pi, we can now the Nodesource Node.JS repository to the sources list.

Before we do this, you must decide what NodeJS version you want to install. Use the relevant line for which version you would like to install. If a newer release exists, replace the number with that version.

These lines simply set an environment variable we will reference in the next step.

- LTS Release

`NODE_MAJOR=18`

- Current Release

`NODE_MAJOR=20`

5. Using the following command, You can now add the Node.JS repository to your Raspberry Pi’s sources list.

`echo "deb [signed-by=/usr/share/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list`

6. Since we made changes to your sources list you will need to run an update of the package list again.

Update the package list on your Raspberry Pi by using the following command.

`sudo apt update`

7. With the NodeJS repositories added to our Raspberry Pi, we can proceed to install the runtime to our device.

As the script we ran in the previous step runs a package update, we simply need to install the package.

`sudo apt install nodejs`

8. To verify that we have now successfully installed NodeJS, we can run the following command.

This command will retrieve the version number from the runtime environment.

`node -v`

9. When using NPM to install additional modules you may have issues when the module needs compiling to support the native hardware.

We can install the “build-essential” package to solve most of these issues. This package contains various tools used to compile software.

You can install this package to your Raspberry Pi by using the following command on your device.

`sudo apt install build-essential`

## Clonar el repo

`git clone https://github.com/nicoleal88/beerBot-p5.git`

`cd beerBot-p5/`

## Instalar dependencias de servidor

`npm install`

## Instalar pm2

### Instalar PM2

Si quieres disponer de tu gestor de procesos en el servidor, tendrás que instalarlo como cualquier otra aplicación Node.

`npm install -g pm2`

### Arrancar y parar procesos

Lo primero que debes aprender es a arrancar y detener procesos, o volverlos a arracar cuando sea necesario. Obviamente, en vez de solicitar a Node que ejecute tal o cual fichero, se lo pediremos directamente a PM2.

`pm2 start index.js`

Para detener el proceso se usará el comando stop, indicando el nombre del proceso que quieres parar.

`pm2 stop mi-api`
O para reiniciarlo, el comando restart.

`pm2 restart mi-api`

### Mantenimiento de los procesos

Tal como lo tienes ahora, gracias a que PM2 controla estos procesos listados, se arrancarán nuevamente en caso de error, manteniéndose encendidos mientras la máquina permanezca encendida. Es decir, en el hipotético caso que uno de ellos se termine por cualquier motivo, como un error en el programa que haga que el proceso se acabe, PM2 lo iniciará de nuevo automáticamente.

Para encontrar información sobre los procesos controlados por PM2 puedes listarlos con el comando list:

`pm2 list`

La administración de los log en PM2 es bastante configurable. Hay un comando que te permite ver en tiempo real todos los log que se están produciendo en tus procesos.

`pm2 log`

Este comando te mostrará los últimos log y se quedará arrancado, mostrando nuevos mensajes que los procesos envíen como salida por consola. En caso de reinicio de un proceso arrancado con PM2 podrás observar en tiempo real cómo el gestor de procesos se encarga de reiniciarlo.

### Generación del script de startup

Para acabar nuestra configuración básica de PM2 necesitamos configurar el script de startup del servidor.

Con tus procesos en marcha, arrancados mediante PM2, ahora puedes generar de manera automatizada el correspondiente script, sin tener que preocuparte por la programación, ya que PM2 lo generará para ti. Para ello tenemos el comando siguiente:

`pm2 startup`

En algunos casos me ha tocado hacer después un comando adicional para guardar la lista de procesos, me figuro es cuando necesitas cambiar la lista de procesos después de haber generado el script de startup:

`pm2 save`

## Configurar aplicaciones y escritorios

1- Editar archivo para que las ventanas se lancen en un escritorio determinado:
nano /home/pi/.config/openbox/lxde-pi-rc.xml

```bash
  <!-- i want firefox on desktop 3 and maximized -->
  <application name="chromium-browser*">
    <desktop>2</desktop>
    <maximized>yes</maximized>
  </application>
<!-- i want firefox on desktop 3 and maximized -->
  <application name="lxterminal*">
    <desktop>3</desktop>
  </application>
  <application name="python3*">
    <desktop>3</desktop>
  </application>

2- Lanzar aplicaciones automáticamente desde:

/etc/xdg/lxsession/LXDE-pi/autostart

@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
point-rpi

@chromium-browser --start-fullscreen 34.227.26.80
@lxterminal -e python3 /home/pi/beerBot-p5/RPI_python_post_request_buffer.py
@lxterminal -e python3 /home/pi/beerBot-p5/local_data_vis.py
@vlc -L --qt-minimal-view /home/pi/Videos/VideosTapRoom/ListaTapRoom.xspf

```

## BOT

## Instalar paquetes

`sudo apt install python3-prettytable`
`pip3 install python-telegram-bot==13.7 --break-system-packages`
