#!/bin/bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y curl git
curl https://get.pimoroni.com/inky | bash
git clone https://github.com/pimoroni/inky.git
cd inky
pip install inky
