# install fan control

sudo apt update
sudo apt-get -y install git
git clone https://github.com/Pyrestone/jetson-fan-ctl.git /tmp/jetson-fan-control
pushd /tmp/jetson-fan-control
sudo source install.sh
popd

# start docker container
docker run --gpus all -it --privileged CONTAINER
