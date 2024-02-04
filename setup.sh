#!/bin/bash

echo "Updating and upgrading system..."
sudo apt-get update -y > /dev/null 2>&1
sudo apt-get upgrade -y > /dev/null 2>&1

echo "Installing curl, git, fish, tmux, and vim..."
sudo apt-get install -y curl git fish vim, tmux > /dev/null 2>&1

echo "Installing Pimoroni Inky..."
curl -sS https://get.pimoroni.com/inky | bash > /dev/null 2>&1

echo "Cloning Inky library from GitHub..."
git clone https://github.com/pimoroni/inky.git > /dev/null 2>&1
cd inky

echo "Installing Inky library..."
pip install inky > /dev/null 2>&1

echo "Setting fish as the default shell..."
chsh -s /usr/bin/fish
fish

echo "Installation completed!"

