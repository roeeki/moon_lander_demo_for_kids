#!/usr/bin/env python3

import cv2
import depthai as dai
import numpy as np


class ScenarioPlotter(object):

    def __init__(self, image_height, image_width, ground_pixel_height, spaceship_top_height_pixels, spaceship_top_height_meter):
        self.image_height = image_height
        self.image_width = image_width
        self.ground_pixel_height = ground_pixel_height
        self.spaceship_top_height_pixels = spaceship_top_height_pixels
        self.spaceship_top_height_meters = spaceship_top_height_meter
        self.meter_to_pixel = self.spaceship_top_height_pixels/self.spaceship_top_height_meters

        # init frame
        self.frame = np.zeros((self.image_height, self.image_width, 3), dtype=np.uint8)

        # plot ground
        self.frame[self.ground_pixel_height:self.ground_pixel_height+5, 10:self.image_width-10, :] = 255

        # spaceship
        # space_ship_patch_2D = np.array([[0, 0, 0, 0, 1, 0, 0, 0, 0],
        #                                 [0, 0, 0, 1, 1, 1, 0, 0, 0],
        #                                 [0, 0, 0, 1, 1, 1, 1, 0, 0],
        #                                 [0, 0, 1, 1, 0, 1, 1, 0, 0],
        #                                 [0, 0, 1, 0, 0, 0, 1, 0, 0],
        #                                 [0, 1, 1, 0, 0, 0, 1, 1, 0],
        #                                 [0, 1, 1, 1, 0, 1, 1, 1, 0],
        #                                 [0, 1, 1, 1, 1, 1, 1, 1, 0],
        #                                 [0, 1, 1, 1, 1, 1, 1, 1, 0],
        #                                 [0, 1, 1, 1, 1, 1, 1, 1, 0],
        #                                 [1, 1, 1, 1, 1, 1, 1, 1, 1],
        #                                 [1, 1, 1, 0, 0, 0, 1, 1, 1],
        #                                 [1, 1, 0, 0, 0, 0, 0, 1, 1]], dtype=np.uint8)

        space_ship_patch_2D = np.array([[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                                        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                                        [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                                        [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                                        [0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0],
                                        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                        [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                                        [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1]], dtype=np.uint8)

        self.space_ship_patch = np.zeros((space_ship_patch_2D.shape[0], space_ship_patch_2D.shape[1], 3), dtype=np.uint8)
        self.space_ship_patch[:, :, 0] = space_ship_patch_2D
        self.space_ship_patch[:, :, 1] = space_ship_patch_2D
        self.space_ship_patch[:, :, 2] = space_ship_patch_2D
        self.space_ship_patch = self.space_ship_patch * 255

        self.space_ship_patch_height = self.space_ship_patch.shape[0]
        self.space_ship_patch_width = self.space_ship_patch.shape[1]

        self.space_ship_patch_left_pix = int(self.image_width/2 - self.space_ship_patch_width/2)
        self.space_ship_patch_right_pix = self.space_ship_patch_left_pix + self.space_ship_patch_width
        self.text_bl_width_pix = int(self.image_width/2 + self.space_ship_patch_width/2 + 5)

    def draw_spaceship(self, spaceship_height_meter):
        self.frame[0:self.ground_pixel_height, :, :] = 0
        space_ship_pix = int(self.ground_pixel_height - (spaceship_height_meter * self.meter_to_pixel))
        self.frame[space_ship_pix-self.space_ship_patch_height:space_ship_pix, self.space_ship_patch_left_pix:self.space_ship_patch_right_pix, :] = self.space_ship_patch

        height_str = '{:.1f}'.format(spaceship_height_meter)
        cv2.putText(self.frame, height_str, [self.text_bl_width_pix, space_ship_pix],
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, color=(255, 255, 255), thickness=1)
        # cv2.imshow("disparity_color", self.frame)
        # cv2.waitKey(70)
        return self.frame


if __name__ == "__main__":

    # scenario draw setup
    # -------------------------

    frame_full = np.zeros((400, 840, 3), dtype=np.uint8)
    right_frame = np.zeros((400, 200, 3), dtype=np.uint8)

    ground_height_pix = 30
    max_height_pix = 300
    max_height_measured = 100  # [cm]
    scen_plotter = ScenarioPlotter(right_frame.shape[0], right_frame.shape[1], right_frame.shape[0]-ground_height_pix,
                                   max_height_pix, max_height_measured)

    # height_measured = 30  # [cm]
    # right_frame = scen_plotter.draw_spaceship(height_measured)
    # cv2.imshow("disparity_color", right_frame)
    # cv2.waitKey(70)

    # depth camera parameters
    # ---------------------

    # Closer-in minimum depth, disparity range is doubled (from 95 to 190):
    extended_disparity = True
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

    frame_full = np.zeros((400, 840, 3), dtype=np.uint8)


    # Connect to device and start pipeline
    with dai.Device(pipeline) as device:

        # Output queue will be used to get the disparity frames from the outputs defined above
        q = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)

        calibData = device.readCalibration()
        intrinsics = calibData.getCameraIntrinsics(dai.CameraBoardSocket.RIGHT)
        focal_length_in_pixels = intrinsics[0][0]
        stereo_baseline = 7.5

        while True:
            inDisparity = q.get()  # blocking call, will wait until a new data has arrived
            frame = inDisparity.getFrame()
            # Normalization for better visualization
            # frame = (frame * (255 / depth.initialConfig.getMaxDisparity())).astype(np.uint8)
            # cv2.imshow("disparity", frame)

            depth_map = np.divide(focal_length_in_pixels * stereo_baseline, frame+1e-5)
            depth_map = np.where(depth_map >= max_height_measured, np.nan, depth_map)
            # depth_map = np.minimum(depth_map, max_height)
            # depth_map[depth_map==max_height] = np.nan

            # calc distance to center frame
            ch = int(depth_map.shape[0]/2)
            cw = int(depth_map.shape[1]/2)
            height = np.nanmedian(depth_map[cw-50:cw+50, ch-50:ch+50])
            print('height: {}'.format(height))

            depth_map = (depth_map * (255 / max_height_measured)).astype(np.uint8)

            depth_map_color = cv2.applyColorMap(depth_map, cv2.COLORMAP_JET)
            # Available color maps: https://docs.opencv.org/3.4/d3/d50/group__imgproc__colormap.html
            # frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)

            # draw scenario
            if not(np.isnan(height)):
                right_frame = scen_plotter.draw_spaceship(height)
            # cv2.imshow("disparity_color", right_frame)
            # cv2.waitKey(50)

            frame_full[0:depth_map_color.shape[0], 0:depth_map_color.shape[1], :] = depth_map_color
            frame_full[:, depth_map_color.shape[1]:, :] = right_frame

            cv2.imshow("disparity_color", frame_full)
            if cv2.waitKey(10) == ord('q'):
                break