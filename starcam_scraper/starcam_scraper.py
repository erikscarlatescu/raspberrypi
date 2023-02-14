#!/usr/bin/env python3

import os
from datetime import datetime

import time

def capture_and_upload_img():
    os.system("wget https://extcityservices.roanokeva.gov/api/citycams/v1/getjpg/sc03")

    now = datetime.now()
    filename = "sc03_" + now.strftime("%d_%m_%Y_%H:%M:%S") + ".jpg"
    os.system("mv sc03 " + filename)

    os.system("gdrive upload --delete -p 1FwFTOAiQWmoIONFLYyrexQ5KY0hd3TtB " + filename)

while True:
    capture_and_upload_img()
    time.sleep(3600) # capture an image every hour
