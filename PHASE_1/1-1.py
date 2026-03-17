from picamera2 import Picamera2
import time
from PIL import Image
picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)

picam2.start()

time.sleep(2)

import os
filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "python_test.jpg")
picam2.capture_file(filename)

picam2.stop()

print(f"Saved: {filename}")

img = Image.open(filename)
img.show()

