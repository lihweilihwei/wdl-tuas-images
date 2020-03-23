# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 14:18:26 2020

@author: yeowl
"""

import requests, os, sys, time
from bs4 import BeautifulSoup, re

os.chdir(os.path.dirname(sys.argv[0]))    # set the working directory to where the .py script is

def sleepCountdown(duration, interval):
    for i in range(duration,0,-interval):
        sys.stdout.write(str(i)+' ')
        sys.stdout.flush()
        time.sleep(interval)

def savePic(ImageUrl, retry_count = 0):
    # download image, retry after 2 seconds if image saved is size 0.
	
    imageData = requests.get(ImageUrl).content
    with open(ImageUrl.split("/")[-1], 'wb') as outpic:
        outpic.write(imageData)
    if os.stat(ImageUrl.split("/")[-1]).st_size > 0:
        print("saved image:", ImageUrl.split("/")[-1])
    elif retry_count < 3:
        print(ImageUrl.split("/")[-1], "size is 0. imageData size:", len(imageData), ". Retrying...")
        sleepCountdown(2, 1)
        savePic(ImageUrl, retry_count = retry_count + 1)
    else:
        print(ImageUrl.split("/")[-1], "failed. Giving up.")

url = "https://www.onemotoring.com.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/woodlands.html"

Cameras = {'4703': 'Tuas Second Link',
           '4713': 'Tuas Checkpoint',
           '2701': 'Woodlands Causeway Towards Johor',
           '2702': 'Woodlands Checkpoint (Towards BKE)'}

time_interval = 55 # in seconds

while True:
    print("getting data...")
    r = requests.get(url=url)
    images = BeautifulSoup(r.content, "lxml").find_all(src = re.compile("mytransport"))    # get the image links

    print("Image links obtained. Length", len(images))

    for image in images:
        savePic("http:" + image["src"])    # save the image

    print("Waiting for", time_interval, "seconds... Press Ctrl+C to stop.")
    sleepCountdown(time_interval, 2)