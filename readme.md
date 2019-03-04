4ZeroBox LoRaWAN
========

4ZeroBox demo firmware for "UP LoRa Edge industrial 4.0 solution kit" composed of a 4ZeroBox + Mikroelektronika LoRa Click + AAEON Gateway + RESIoT. More info: https://up-shop.org/home/293-up-lora-edge-industrial-40-solution-kit.html

This firmware allows to connect your 4ZeroBox to a LoRa network, publish temperature and power consumption data and control remotely the onboard relays.

HARDWARE SETUP
--------

A Microchip RN2483 LoRa module is needed for this firmware example. The Mikroe LoRa Click shall be mounted on 4ZeroBox Mikrobus Slot 1. Be sure to set the 4ZeroBox SW1 pins 3, 5 and 11 on ON position to enable the communication with the LoRa module.
More info about Dip-Switches and Jumper Settings: https://downloads.4zeroplatform.com/documents/4zerobox-usermanual.pdf 

Connect the NTC temperature sensor to "GND" and "Sense1" terminals, and the non-invasive current probe on "CurCOM" and "Cur1" terminals. If you have one, connect a 10 DoF Click in the Mikrobus Slot 2 and uncomment some lines on the main.py to get and send accelerometer data.

Connect the board to a laptop via the USB port to start program the 4ZeroBox. During the programming phase, jumper JP1 must be in U5V position and the external power supply must be detached. Be sure to set the 4ZeroBox SW2 pin 11 on ON position and 12 on OFF position to enable the USB communication. 

FIRMWARE SETUP
--------

1 - The “4ZeroPlatform Configurator” is the tool that guides the user during the installation of all the
required softwares, drivers, libraries and tools needed for programming the 4ZeroBox. 
Download the 4ZeroPlatform Configurator and start the setup procedure by visiting:
https://docs.4zeroplatform.com/guide/getting-started/

2 - The 4ZeroBox official programming framework is Zerynth® (www.zerynth.com). Zerynth allows
programming the 4ZeroBox applications in Python (or hybrid C/Python). Zerynth® and all the required libraries will be installed by the 4ZeroPlatform Configurator during the setup phase

3 - Follow the Getting Started until "Configure your Device" section: https://docs.4zeroplatform.com/guide/getting-started/#configure_your_device

4 - Create a new project and insert the link to this repo into the field "Clone from GitHub"
More info here: https://docs.zerynth.com/latest/official/core.zerynth.docs/gettingstarted/docs/index.html#develop-your-first-zerynth-project

5 - Edit the code with the OTAA credentials you can find on ResIoT portal.

6 - Verify and uplink the code. More info here: https://docs.zerynth.com/latest/official/core.zerynth.docs/gettingstarted/docs/index.html#verify-and-uplink-a-zerynth-project

7 - You're done! 

When the firmware starts the on-board RGB led will be magenta color, after the initialization the led will turn blue, and finally, after the lora connection is established, the led will be green.

Sensors data are acquired every 10 seconds, the detected parameters are formatted in a 6-bytes packet and sent through LoRa. If a 2-bytes downlink message is received, the two onboard relays are controlled accordingly.