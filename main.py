#!/usr/bin/env python3

import cv2
import depthai as dai
import numpy as np
import pygame

if __name__ == "__main__":

    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    print("joysticks found:")
    print(joysticks)

    # Closer-in minimum depth, disparity range is doubled (from 95 to 190):
    extended_disparity = False
    # Better accuracy for longer distance, fractional disparity 32-levels:
    subpixel = False
    # Better handling for occlusions:
    lr_check = True

    # Create pipeline
    pipeline = dai.Pipeline()

    # Define sources and outputs
    monoLeft = pipeline.create(dai.node.MonoCamera)
    monoRight = pipeline.create(dai.node.MonoCamera)
    depth = pipeline.create(dai.node.StereoDepth)
    xout = pipeline.create(dai.node.XLinkOut)

    xout.setStreamName("disparity")

    # Properties
    monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
    monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
    monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
    monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

    # Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
    depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
    # Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
    depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
    depth.setLeftRightCheck(lr_check)
    depth.setExtendedDisparity(extended_disparity)
    depth.setSubpixel(subpixel)

    # Linking
    monoLeft.out.link(depth.left)
    monoRight.out.link(depth.right)
    depth.disparity.link(xout.input)

    # Connect to device and start pipeline
    with dai.Device(pipeline) as device:

        # Output queue will be used to get the disparity frames from the outputs defined above
        q = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)

        while True:

            # get stereo depth image

            inDisparity = q.get()  # blocking call, will wait until a new data has arrived
            frame = inDisparity.getFrame()
            # Normalization for better visualization
            frame = (frame * (255 / depth.initialConfig.getMaxDisparity())).astype(np.uint8)

            # get joystick input

            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         break
            #     # joystick axis is between [-1,1]  on each axis
            #     x_speed = round(pygame.joystick.Joystick(0).get_axis(0) * 5)
            #     y_speed = round(pygame.joystick.Joystick(0).get_axis(1) * 5)
            #     if event.type == pygame.JOYBUTTONDOWN:
            #         if pygame.joystick.Joystick(0).get_button(0):
            #             pass
            #         if pygame.joystick.Joystick(0).get_button(1):
            #             pass

            cv2.imshow("disparity", frame)

            # Available color maps: https://docs.opencv.org/3.4/d3/d50/group__imgproc__colormap.html
            frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
            cv2.imshow("disparity_color", frame)

            if cv2.waitKey(1) == ord('q'):
                break