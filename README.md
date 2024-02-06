# Raspberry Pi Inky Impression 7.3" setup

A collection of scripts and apps to use with Inky Impression 7.3" e-ink display on a Raspberry Pi.


## Installation
### Prerequisites
- **Install Git**: To clone this repository, you'll first need to have Git installed on your Raspberry Pi. If Git is not already installed, you can install it by running:
  ```bash
  sudo apt update
  sudo apt install git -y
  ```
  
```bash
    git clone https://github.com/patakk/rpi_stuff.git
    cd rpi_stuff
    ./setup.sh
  ```

## Using the Image Server
    ```bash
    cd inky_app
    python3 app.py &
    ```

## Enabling Button Functionality

```bash
python buttons.py &
```
---

