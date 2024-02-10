#!/bin/bash

echo "Updating and upgrading system..."
sudo apt-get update -y > /dev/null 2>&1
sudo apt-get upgrade -y > /dev/null 2>&1

echo "Installing curl, git, fish, tree, tmux, pip, and vim..."
sudo apt-get install -y curl git tree fish vim tmux python3-pip > /dev/null 2>&1

echo "Installing Pimoroni Inky..."
curl -sS https://get.pimoroni.com/inky | bash > /dev/null 2>&1

echo "Cloning Inky library from GitHub..."
git clone https://github.com/pimoroni/inky.git > /dev/null 2>&1
cd inky

echo "Installing Inky library..."
pip install inky > /dev/null 2>&1
pip install Flask > /dev/null 2>&1
pip install gunicorn > /dev/null 2>&1

echo "Installing AxiDraw CLI and Python API"
pip install https://cdn.evilmadscientist.com/dl/ad/public/AxiDraw_API.zip

echo "Setting fish as the default shell..."
sudo chsh -s /usr/bin/fish
fish

echo "Setting up crontab..."
{
  echo "@reboot cd /home/paolo/rpi_stuff/inky_server && sudo PYTHONPATH=/home/paolo/.local/lib/python3.9/site-packages /home/paolo/.local/bin/gunicorn -w 4 -b 0.0.0.0:80 app:app &"
  echo "@reboot cd /home/paolo/rpi_stuff && PYTHONPATH=/home/paolo/.local/lib/python3.9/site-packages /usr/bin/python /home/paolo/rpi_stuff/buttons.py &"
} | crontab -


echo "Installation completed!"

