# Raspberry Pi Inky Impression 7.3" setup

A collection of scripts and apps to use with Inky Impression 7.3" e-ink display on a Raspberry Pi.


## Setup
### Prerequisites
If **git** is missing, run the following:
```bash
sudo apt update
sudo apt install git -y
```

### Install
Clone this repo and run setup.sh
```bash
git clone https://github.com/patakk/rpi_stuff.git
cd rpi_stuff
./setup.sh
```

## Using the Image Server
```bash
cd inky_server
python app.py &
```

## Enabling Button Functionality

```bash
python buttons.py &
```
---

