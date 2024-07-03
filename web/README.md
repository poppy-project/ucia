# Web Interface for the ROSA Robot

The Rosa can be managed via a website.

## Table of Contents :

1. [Getting Started](#getting-started)
    - [Connecting to the UCIA Access Point](#connecting-to-the-ucia-access-point)
    - [Accessing the Robot Management Page](#accessing-the-robot-management-page)
2. [Description](#description)
    - [Webcam](#webcam)
    - [Program Upload](#program-upload)
    - [Web Terminal](#web-terminal)
    - [Logs](#logs)
    - [Documentation](#documentation)
    - [Settings](#settings)
    - [Shutdown](#shutdown)
    - [Restart](#restart)
    - [Interface](#interface)
        - [Block Programming Interface](#block-programming-interface)
        - [Teleoperation Interface](#teleoperation-interface)
3. [Troubleshooting](#troubleshooting)

## Getting Started :

### Connecting to the UCIA Access Point :

- On your computer, open Wi-Fi settings.
- Look for the Wi-Fi network named "ucia".
- Select this network and enter the password "rosaucia" to connect.

### Accessing the Robot Management Page :

- Open a web browser on your connected device.
- In the address bar, type the following URL: rosa.local.
- Once on the rosa.local page, you should see a user interface similar to this:

![website](./img/website.png)

## Description :

Nine buttons are available on the homepage. Here are their descriptions and functionalities.

### Webcam:

- **Webcam** : Useful only during the initial version of ROSA. This feature allows the user to view a live feed from the robot's camera.

### Program Upload :

- **Program Upload** : This page allows the user to upload, delete, and execute their own Python programs on the robot. Users can interact with the robot by running custom scripts.

### Web Terminal :
*Coming Soon!*

- **Web Terminal** : A web-based terminal for direct command-line access to the robot's system. This feature is planned for future releases.

### Logs :
*Coming Soon!*

- **Logs** : This section will display system logs and other relevant information for troubleshooting and monitoring the robot's performance.

### Documentation :
*Coming Soon!*

- **Documentation** : A comprehensive guide and API documentation for developing and interacting with the robot.

### Settings :

- **Settings** : This page allows the user to change de Hotspot configuration and update the robot.

### Shutdown :
**Not accessible**

- **Shutdown** : This feature is currently not accessible.

### Restart :
**Not accessible**

- **Restart** : This feature is currently not accessible.

### Interface :

This page consists of two sub-interfaces:
- **Block Programming Interface** : (accessible via the "manual control" button)

#### Block Programming Interface :

- A dropdown menu to choose the block language,
- A toolbox with seven categories:
    - **ROSA** : Contains blocks for direct interaction with ROSA, such as:
        - Moving forward or backward at a given speed (0 to 100) for an optional duration.
        - Rotating left or right at a given speed (0 to 100) for an optional duration.
        - Pausing for a specified duration.
        - Measuring line sensor values.
        - Measuring front and rear distance sensor values.
        - Turning on LED(s) to a specified color from a list for a given time (minimum 2 seconds by default).
        - Producing sounds of a specified duration and frequency.
        - Playing music from a provided list.
    - **Logic** : Includes all logical operations.
    - **Loops** : Contains all loop structures and increment operations.
    - **Mathematics** : Includes all types of mathematical operations.
    - **Text** : Contains blocks for text manipulation and display.
    - **Variables** : Used to define and interact with variables.
    - **Functions** : Used to define and call functions.

- A "whiteboard" area to arrange and assemble the blocks with a trash bin (for discarded blocks),
- An area to view the corresponding code in real-time,
- An output area to display console feedback ("Erreur" for code execution errors, "Error" for internal server errors, and "Sortie" for standard output like prints).

- **Teleoperation Interface** : (accessible via the "programming" button)

#### Teleoperation Interface :

- A joystick for moving the robot,
- A slider to choose the speed,
- A display of sensor values (updated every 5 seconds, with 0 indicating no obstacles detected).

## Troubleshooting :

➜ In case of issues:

- If you cannot detect the "ucia" network, try restarting the robot.
- If you cannot access the rosa.local website, ensure your device is connected to the "ucia" Wi-Fi network.
