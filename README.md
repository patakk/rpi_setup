# Raspberry Pi Utilities Repository

Welcome to the Raspberry Pi Utilities repository! This collection of scripts and applications is designed to enhance your Raspberry Pi experience. Whether you're setting up a new device or adding functionality to an existing setup, you've come to the right place.

## Getting Started

Before you can use these utilities, there are a few steps you'll need to follow to get everything set up on your Raspberry Pi. This guide assumes you're starting with a fresh install of Raspberry OS.

### Prerequisites

- **Install Git**: To clone this repository, you'll first need to have Git installed on your Raspberry Pi. If Git is not already installed, you can install it by running:

  ```bash
  sudo apt update
  sudo apt install git -y
  ```

### Installation

Once Git is installed, you can clone this repository to your Raspberry Pi by following these steps:

1. Open a terminal and run the following command to clone the repository:

    ```bash
    git clone https://github.com/patakk/rpi_stuff.git
    ```

2. Change into the cloned repository's directory:

    ```bash
    cd rpi_stuff
    ```

3. Run the setup script:

    ```bash
    ./setup.sh
    ```

This script will install any necessary dependencies and set up the environment for the utilities included in this repository.

## Using the Image Server

To run the image server application, follow these steps:

1. Navigate to the `inky_app` directory:

    ```bash
    cd inky_app
    ```

2. Run the `app.py` script:

    ```bash
    python3 app.py
    ```

This will start the image server, which you can then access according to the application's documentation.

## Enabling Button Functionality

If your project includes buttons and you'd like to enable their functionality, you'll need to run the `buttons.py` script in the background:

```bash
python3 buttons.py &
```

The `&` at the end of the command runs the script in the background, allowing you to continue using the terminal for other tasks.

---

For more information on how to use these utilities or if you encounter any issues, please refer to the documentation or open an issue in this repository.
