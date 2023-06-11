MoverRemover
===========

- [Overview](#overview)
- [Operation](#Operation)
- [Results](#Results)
- [Examples](#Examples)
- [Installation](#installation)



## Overview
A Camera Application which will take and blend together multiple images.  The goal being: removing temporary items in the scene (for example tourists) or to produce a "long shutter" effect, such as with moving water.

## Operation
1. Mount the phone on a tripod and frame the desired scene. 
2. Press the camera icon.
3. Wait
4. Press the camera icon again, wait until it stops being red

## Results
You will see three images:
1. An image with the extension _first.jpg: This is the image captured immediately after pressing the camera icon
2. An image with the extension _mean.jpg: This image is the mean of all images sampled together.  It is useful for the "blurred water" effect
3. An image with the extension _median.jpg: This image is the median of all images sampled together.  It is useful removing temporary objects (people walking around) in a scene.

## Examples
![First Image](sample_images/Sample_1_first.jpeg?raw=true "First")
![Mean Image](sample_images/Sample_1_mean.jpeg?raw=true "Mean")
![Median Image](sample_images/Sample_1_median.jpeg?raw=true "Median")

## Installation
1. Install Kivy: https://kivy.org/doc/stable/gettingstarted/installation.html
2. Install Camera4Kivy: https://github.com/Android-for-Python/Camera4Kivy/blob/main/README.md#install
3. Clone this repo
4. In the repo type: buildozer android debug deploy run
