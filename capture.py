import pyzed.sl as sl
from datetime import datetime, timedelta
from time import sleep
import sys
import logging
import os
import json

# sample every 10 seconds
dt = timedelta(seconds=10)

# log config
log_fn = datetime.now().strftime("capture_log_%Y_%m_%d-%H_%M_%S")
log_path = "log"

# img storage
img_path = "img"


if __name__ == "__main__":
    if not os.path.isdir(log_path):
        os.makedirs(log_path)
    if not os.path.isdir(img_path):
        os.makedirs(img_path)

    # Create logging object
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(f"{log_path}/{log_fn}.log")
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    # Create a ZED camera object
    zed = sl.Camera()

    # sample every 10 seconds
    dt = timedelta(seconds=10)

    # Set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD2K
    init_params.camera_fps = 1

    # Open the camera
    err = zed.open(init_params)
    if (err != sl.ERROR_CODE.SUCCESS) :
        exit(-1)

    # store camera metadata
    info = zed.get_camera_information()
    cam_info = dict()
    cam_info["model"] = str(info.camera_model)
    cam_info["serial"] = info.serial_number
    cam_info["camera firmware"] = info.camera_configuration.firmware_version
    cam_info["sensor firmware"] = info.sensors_configuration.firmware_version
    with open(os.path.join(img_path, datetime.now().strftime("camera_info_%Y_%m_%d-%H_%M_%S.json")), "w") as f:
        json.dump(cam_info, f)

    # Capture frames
    image = sl.Mat()
    st = datetime.now()
    st = st.replace(microsecond=0,second=0) + timedelta(minutes=1)

    # Capture sensor data
    sensors_data = sl.SensorsData()

    logging.info(f"Capturing from {st}")

    while 1:
        while datetime.now() < st:
            sleep(0.1)
        st += dt
        # Grab an image
        if (zed.grab() == sl.ERROR_CODE.SUCCESS):
            timestamp = zed.get_timestamp(sl.TIME_REFERENCE.IMAGE)
            logging.info(f"Image captured at {timestamp.get_milliseconds()}")

            fn_prefix = datetime.now().strftime("img_%Y_%m_%d-%H_%M_%S")

            # left and right image
            for view, label in zip([sl.VIEW.LEFT, sl.VIEW.RIGHT], ["left", "right"]):
                zed.retrieve_image(image, view) # Get the left image
                img_fn = fn_prefix + f"_{label}.png"
                if image.write(os.path.join(img_path, img_fn)) != sl.ERROR_CODE.SUCCESS:
                    logging.error(f"Unable to save image {image_fn}")

            # depth maps
            for measurement, label in zip([sl.MEASURE.DEPTH], ["depth"]):
                zed.retrieve_measure(image, measurement) # Get the left image
                img_fn = fn_prefix + f"_{label}.png"
                if image.write(os.path.join(img_path, img_fn)) != sl.ERROR_CODE.SUCCESS:
                    logging.error(f"Unable to save depth map {image_fn}")
        if zed.get_sensors_data(sensors_data, sl.TIME_REFERENCE.CURRENT) == sl.ERROR_CODE.SUCCESS:
            sensor_info = dict()
            sensor_info["pressure_hPa"] = sensors_data.get_barometer_data().pressure
            sensor_info["temperature_left_C"] = sensors_data.get_temperature_data().get(sl.SENSOR_LOCATION.ONBOARD_LEFT)
            sensor_info["temperature_right_C"] = sensors_data.get_temperature_data().get(sl.SENSOR_LOCATION.ONBOARD_RIGHT)
            sensor_info["temperature_imu_C"] = sensors_data.get_temperature_data().get(sl.SENSOR_LOCATION.IMU)
            sensor_info["temperature_barometer_C"] = sensors_data.get_temperature_data().get(sl.SENSOR_LOCATION.BAROMETER)
            with open(os.path.join(img_path, fn_prefix + "_sensor_data.json"), "w") as f:
                json.dump(sensor_info, f)

            
    zed.close()
