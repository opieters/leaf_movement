import pyzed.sl as sl
from datetime import datetime

if __name__ == "__main__:
    # Create a ZED camera object
    zed = sl.Camera()
    
    # Set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD2K
    init_params.camera_fps = 1
    
    # Open the camera
    err = zed.open(init_params)
    if (err != sl.ERROR_CODE.SUCCESS) :
        exit(-1);
    
    # Capture frames
    image = sl.Mat()
    while 1:
        # Grab an image
        if (zed.grab() == sl.ERROR_CODE.SUCCESS) :
            # A new image is available if grab() returns SUCCESS
            zed.retrieve_image(image, sl.VIEW.LEFT) # Get the left image
            
            timestamp = zed.get_timestamp(sl.TIME_REFERENCE.IMAGE) # Get the timestamp at the time the image was captured
    	print("Image resolution: ", image.get_width(), " x ", image.get_height()," || Image timestamp: ", timestamp.get_milliseconds())
            i = i+1
    
    zed.close()
