# 🚀 GSR Project – Detection and Visualization of Galvanic Skin Response

## 🗂️ Project Folder Structure

The `GSR` folder is the core of the project and contains the following elements:

- **`GSR.ino`**: Arduino script responsible for measuring the GSR signal and transmitting it via Bluetooth.
- **`GSR_Receiver.py`**: Python script that connects to the Arduino via Bluetooth, triggers data collection every 0.1 seconds, and logs each entry to a CSV file.
- **`ReceiverGSR.csv`**: The data storage file. It can be deleted at any time — it will be automatically recreated upon the next execution of `GSR_Receiver.py`.
- **`server.py`**: Python script acting as a bridge between the CSV file and the local environment on port 5000 (`http://0.0.0.0:5000`).
- **`index.html`**: HTML (with CSS) file that queries the server and displays the data in any web browser through a clean and readable user interface. This file is standalone: it can be copied to another device on the same local network and, once configured, used to display the data.
- **`__pycache__`**: Auto-generated Python cache files. They are not essential and can be ignored.
- **`README_GSR.md.html`**: This documentation file. We recommend reading it with the preview mode enabled in Visual Studio Code (`Ctrl + Shift + V`).
- **`Lancement_du_projet.mp4`**: A demonstration video showing the key steps to launch the project on a Windows PC.

---

## ⚙️ Deployment Modes

The project can be deployed in two main ways:

### 1. Using a Windows PC as a server

In this setup, both Python scripts are executed in Visual Studio Code. The PC handles Bluetooth connection, collects the data, logs it into the CSV file, and serves it on port 5000.

### 2. Using a Raspberry Pi as a server

Here, the scripts run directly on a Raspberry Pi equipped with a lightweight OS (e.g., Raspberry Pi OS Lite). The Pi performs the same tasks as the PC.

> ⚠️ **Attention**: This setup is more complex. It requires OS installation, SSH configuration for remote access, and a stable Wi-Fi connection. Networks like `eduroam` that require login credentials are not suitable. A practical workaround is to use mobile tethering to create a simple, easily identifiable local network.

> 🔧 This README only details the setup for Windows PC. Arduino configuration is the same in both cases.

---

## 🛠️ Arduino Setup

### Required Hardware

- An **Arduino UNO R4 WiFi** (essential for built-in Bluetooth support).
- A GSR sensor connected to the **A0** pin through a shield. This is configured in `GSR.ino` and must be changed in the code if a different pin is used.

### Configuration Steps

1. Install and launch **Arduino IDE**.
2. Connect the Arduino via USB. If no driver installation is prompted, it is likely already installed.
3. Install the **ArduinoBLE** library:
   - Go to `Tools` → `Manage Libraries`
   - Search for `ArduinoBLE`, then click **Install**
4. Open the `GSR.ino` file via `File` → `Open`.
5. Upload the script to the Arduino using the upload button (right arrow).

Once done, the Arduino is ready: it enters standby mode, waiting for a BLE connection initiated by `GSR_Receiver.py`. When this script is executed, data transmission begins automatically.

---

## 💻 Using a Windows PC as a Server

### Prerequisites

1. Connect the PC to a stable local Wi-Fi network.
2. Make sure **Python** is installed (if not, install it via the Microsoft Store).
3. Open a terminal (`cmd` or PowerShell) and install the required libraries:

```bash
pip install bleak waitress flask flask_cors pandas
```

4. Install **Visual Studio Code**, then open the `GSR` folder:
   - `File` → `Open Folder` → select the `GSR` folder.

5. Accept any recommended extension prompts from VSCode.

### Launching the Project

> 📺 **Tip**: Watch the demo video **`Lancement_du_projet.mp4`** (included in the `GSR` folder) for a visual guide to the steps below. We strongly recommend viewing it for a smoother setup experience.

1. Open `GSR_Receiver.py` in VSCode and run it by clicking the play button.
2. Split the terminal: click `Split Terminal` → choose `PowerShell`. This allows two scripts to run simultaneously.
3. In the second terminal, launch the server with:

```bash
python -m waitress --listen=0.0.0.0:5000 server:app
```

> 🔐 **Note**: The first time you run this, Windows may ask for firewall permissions. Allow access.

4. Get your PC’s local IP address:
   - Open a terminal (`cmd`)
   - Type `ipconfig`
   - Look for the `IPv4 Address` line (e.g., `172.20.10.4`)

5. Open `index.html` and update line 268 with the IP address you just found:

```html
http://172.20.10.4:5000
```

6. Open `index.html` in any browser — either on the same PC or any other device connected to the same local network.

> 🌐 **Remote Access**: Only `index.html` is needed to display the data on another device. The rest of the `GSR` folder stays on the server machine.

---

## 📝 Final Notes

- Arduino configuration is identical regardless of whether you use a PC or Raspberry Pi.
- The project can be adapted for other transmission types (e.g., USB, direct Wi-Fi).
- For ease of reuse, a future version could include Docker containers or launch scripts.
