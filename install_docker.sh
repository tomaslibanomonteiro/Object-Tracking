# To be able to run this script run on the terminal on
# this directory the following command: chmod +x install_docker.sh

sudo apt update
sudo apt install docker.i
sudo apt install docker-ce docker-ce-cli containerd.io 
sudo apt install docker-compose
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
docker -v