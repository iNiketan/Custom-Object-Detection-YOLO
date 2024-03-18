# Custom-Object-Detection-YOLO
This project explores custom object detection with YOLO (You Only Look Once), a powerful algorithm for real-time object identification. Our specific goal is to train YOLO to detect the Volkswagen logo in images.

By training a custom YOLO model, we aim to achieve:
<li>Accurate Volkswagen Logo Identification: The model will learn to distinguish the Volkswagen logo from other objects in an image.
<li>Real-Time Performance: YOLO is known for its speed, making it suitable for applications requiring fast detection.

The Potential Applications:
<li>Automated Image Analysis: The model could be used to automatically identify Volkswagen vehicles in images or videos, streamlining tasks in various industries.
<li>Augmented Reality Overlays: Imagine using the model to overlay information or advertisements specifically on Volkswagen logos in an AR experience.

![](predicitions/Screenshot%20from%202019-10-12%2022-02-42.png)

![](predicitions/Screenshot%20from%202019-10-13%2017-09-18.png)

### Setting up the system
we will be using yolov3 for this project. I suggest you use linux base os it perform better for yolo but window is
fine too. its easy on linux than on window thats all. on windows you have to download a terminal(cmd of linux) extension
for commands as yolo was made for/on linux.
Firstly installing darknet-yolo on system. use following commands

git clone https://github.com/pjreddie/darknet
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install build-essential
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-d
sudo apt-get install libopencv-dev
### changing directory to darknet forlder
cd darknet
make

above commands will create and configure the folder now lets just check the if it is done correctly
download the following weights

wget https://pjreddie.com/media/files/yolov3.weights

from darknet directory run
./darknet detect cfg/yolov3.cfg yolov3.weights data/dog.jpg

if it show prediction then we are good to go
##############
for window see this video
https://www.youtube.com/watch?v=-HtiYHpqnBs
##############

install opencv and configure your gpu(if you want)
go to Makefile in darknet directory and change value of opencv and gpu 1. now this commands

sudo apt install g++-5
sudo apt install gcc-5

sudo apt update
sudo apt upgrade

from darknet directory run

make

this will config pc for yolo with gpu and opencv

############################################################
creating dataset use labelImg for creating bounding boxes. it will genrate a xml
for each image.
get labelImg from here
https://github.com/tzutalin/labelImg.git

then use xmltotxt to genrate txt file which is our dataset format required for yolo
https://github.com/Isabek/XmlToTxt.git

this folder requires a classes.txt in which you have to write name of classes(logos name you are giving during labelImg).
you can edit it or just copy txt file genrated after labelImg

#########################################################################################
directory format for project
logodetection
  -dataset
    -images
      imges.jpg #preferably
    -label
      txt files
  -custom
    .cfg file
    .names file
    train.txt
    test.txt
    .data file

name file contain all labels for logos
see the file in my project for help

################################################################
### how to create a train.txt file
use parsefiles.py to create it then open train.py and remove location of parsefiles.py
#there are other ways but i came up with this and used this

create test.txt and put some(3) of image location in it

now cut and paste train and test in custom
for cfg file use yolov3.cfg in cfg folder of darknet copy that and put it inside custom

### changing .cfg file
Option 1: yolov3.cfg

Go to the cfg directory under the Darknet directory and make a copy of yolov3.cfg:

cd cfg
cp yolov3.cfg obj.cfg

Open obj.cfg with a text editor and edit as following:

In line 3, set batch=24 to use 24 images for every training step.
In line 4, set subdivisions=8 to subdivide the batch by 8 to speed up the training process and encourage generalization.
In line 603, set filters=(classes + 5)*3, e.g. filters=18.
In line 610, set classes=1, the number of custom classes.
In line 689, set filters=(classes + 5)*3, e.g. filters=18.
In line 696, set classes=1, the number of custom classes.
In line 776, set filters=(classes + 5)*3, e.g. filters=18.
In line 783, set classes=1, the number of custom classes.

Then, save the file.

Option 2: yolov3-tiny.cfg

Go to the cfg directory under the Darknet directory and make a copy of yolov3-tiny.cfg:

cd cfg
cp yolov3-tiny.cfg obj.cfg

Open obj.cfg with a text editor and edit as following:

In line 3, set batch=24 to use 24 images for every training step.
In line 4, set subdivisions=8 to subdivide the batch by 8 to speed up the training process and encourage generalization.
In line 127, set filters=(classes + 5)*3, e.g. filters=1.
In line 135, set classes=1, the number of custom classes.
In line 171, set filters=(classes + 5)*3, e.g. filters=1.
In line 177, set classes=1, the number of custom classes.

(filters= num/3*(classes+1+4)
for each convolution layer before [yolo] layer) this how to decide filters value num = 9 in yolov3.cfg and 6 in yolov3-tiny.cfg


Then, save the file.

#download pretrained weights for trainging
from terminal

wget https://pjreddie.com/media/files/darknet53.conv.74

put the darknet53 file in darknet folder


###############################################
### starting the fun part training
also put a custom.data file in darknet

from terminal run the command

./darknet detector train custom/trainer.data custom/yolov3-tiny-custom.cfg darknet53.conv.74

training will start weights get saved every 100 iteration and after 900 every 10000 let it run
for at least 30000
after that move a copy of weights from backup/ to darknet and run

./darknet detector test custom/trainer.data custom/yolov3-tiny.cfg yolov3-tiny_20000.weights dataset/01.jpg

####################################################


                                                                                                  

