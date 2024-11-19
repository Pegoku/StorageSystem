# Interactive Storage System

## Overview
This is a versatile and customizable Storage System. It has the ability to combine multiple Storage Systems via the use of ESP32 (a cheap microcontroller) as controllers for the neopixels (indicators). It has a simple but useful WebUI and an API. The storage bins are compatible with Gridfinity 1x4 bins.

## Features
- [x] **Gridfinity Compatible**: Easily integrates with the Gridfinity storage system for modular storage.
- [x] **Parametric Design**: Easily customizable bins.
- [x] **ESP32 Controlled**: Scalable system using ESP32 as wireless controllers.
- [x] **Neopixels**: Dynamic lighting indicators.
- [x] **Web UI to Manage Storage**: User-friendly web interface for managing the items.
- [x] **API**: Simple to use API.

## Getting Started

### Prerequisites
- [PlatformIO](https://platformio.org) installed on your development environment.
- ESP32 DevBoard or Controller PCB (WIP).
- Neopixels (WS2812B) or [Indicator PCB](https://github.com/Pegoku/StorageSystem/tree/master/PCB/Indicators).
- Some wire.

### API
1. Clone the repository:
    ```sh
    git clone https://github.com/Pegoku/StorageSystem.git
    cd StorageSystem/Code/Server
    ```
2. Create a Python virtual environment and install the requirements:
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
3. Run the main Python file:
    ```sh
    python3 main.py
    ```

### ESP32
1. Clone the repository:
    ```sh
    git clone https://github.com/Pegoku/StorageSystem.git
    cd StorageSystem/Code/Node
    ```
2. Install the required libraries and dependencies:
    ```sh
    platformio run
    ```
3. Connect your ESP32 to your computer.
4. Edit the `include/.env.template` file and rename it to `include/.env`.
5. Upload the firmware to the ESP32:
    ```sh
    platformio upload
    ```
6. Open the serial monitor to check if the installation was successful:
    ```sh
    platformio device monitor
    ```

### Website
1. Clone the repository:
    ```sh
    git clone https://github.com/Pegoku/StorageSystem.git
    cd StorageSystem/Code/App
    ```
2. Create a Python virtual environment and install the requirements:
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
3. Run the main Python file:
    ```sh
    python3 main.py
    ```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.