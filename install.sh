# install VNC, based on https://developer.nvidia.com/embedded/learn/tutorials/vnc-setup
#   enable start at boot
mkdir -p ~/.config/autostart
cp /usr/share/applications/vino-server.desktop ~/.config/autostart/.

# configure VNC
gsettings set org.gnome.Vino prompt-enabled false
gsettings set org.gnome.Vino require-encryption false

# configure password
gsettings set org.gnome.Vino authentication-methods "['vnc']"
gsettings set org.gnome.Vino vnc-password $(echo -n 'gontrode2023'|base64)

# install fan control
sudo apt update
sudo apt-get -y install git
git clone https://github.com/Pyrestone/jetson-fan-ctl.git /tmp/jetson-fan-control
pushd /tmp/jetson-fan-control
sudo source install.sh
popd

# start docker container
docker run --gpus all -it --privileged CONTAINER
