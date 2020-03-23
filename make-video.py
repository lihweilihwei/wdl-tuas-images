# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 21:01:15 2020

@author: yeowl
"""

from PIL import Image, ImageDraw, ImageFont
import ffmpeg, os
import pandas as pd

os.chdir("C:/Users/yeowl/Desktop/wdl-tuas-images")

def drawText(image, text, x_buffer=5, y_buffer=5):
    (x, y) = image.size
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size=int(y/40))
    text_size = font.getsize(text)

    draw = ImageDraw.Draw(image)

    # draw the text on the bottom right
    draw.rectangle([(x, y), (x-text_size[0]-2*x_buffer, y-text_size[1]-2*y_buffer)], fill='rgb(255,255,255)')
    draw.text((x-text_size[0]-x_buffer, y-text_size[1]-y_buffer), text, fill='rgb(0, 0, 0)', font=font)

    return image

def getDateTime(imageString):
    # converts the image file name into a datetime string yyyy/mm/dd hh:mm

    dateTimeString = list(imageString.split("_")[2])
    dateTimeString.insert(4, "/")
    dateTimeString.insert(7, "/")
    dateTimeString.insert(10, " ")
    dateTimeString.insert(13, ":")
    return(''.join(dateTimeString[:-2]))

image_list = [img for img in os.listdir() if "jpg" in img]    # get the list of all images

# create dataframe, sort by cameraID, then by dateTime
image_list_df = pd.DataFrame({"name": image_list,
                              "cameraID": [x[:4] for x in image_list],
                              "dateTime": [x.split("_")[2] for x in image_list]}).sort_values(["cameraID", "dateTime"])

image_list_df["count"] = image_list_df.groupby("cameraID").cumcount() + 1    # sequential order so that ffmpeg can turn it into a video
image_list_df["out_file"] = image_list_df["cameraID"].astype(str) + "/" + image_list_df["count"].astype(str) + ".jpg"

for index, row in image_list_df.iterrows():
    print(row["name"])
    try:
        image = drawText(image=Image.open(row["name"]), text=getDateTime(row["name"]))
        image.save(row["out_file"])
    except:
        print(row["name"], "failed")

# I ended up using ffmpeg on the command prompt.
#ffmpeg.input("2701/%d.jpg").output("2701/2701.mp4").run()
