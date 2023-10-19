FROM stereolabs/zed:4.0-py-devel-jetson-jp4.6.1
ENV DEBIAN_FRONTEND noninteractive

# Install GPIO
RUN python3 -m pip install Jetson.GPIO

# Install Git to clone scripts
RUN apt-get update
RUN apt-get install git

WORKDIR /usr/local/zed

# clone scripts
git clone https://github.com/opieters/leaf_movement.git /usr/local/zed/leaf_movement

