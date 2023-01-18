# moon_lander_demo_for_kids
This is a cool moon landing demo for kids.
We simulate a lunar lander with camera relative navigation system.
User gets height readings from camera, and uses a joystick to controll lander height.
The mission is to try and land the lander safely!


The demo is made of:
- a lunar lander model with OAK-D stereo cameras to measure distance to ground
- a 1m height frame with cord and pulley so pulling/releasing the coard takes
the lunar lander up \ down
- a servo and a joystick to pull \ release the cord, and thus control
the lander height
- a laptop for user UI and controlling joystick \ lander cameras \ servo in realtime


![lunar_lander_demo_4_kids](https://user-images.githubusercontent.com/32566844/213310963-2004f37a-1c88-407b-a339-2b3ddd92da6f.png)

---

## Demo setup:

### components:

1) laptop 
2) OAK-D usb stereo camera set  see: ![OAK-D tutorial](https://docs.luxonis.com/en/latest/pages/depth/)
2) usb joystick
3) servo motor
4) pololu maestro usb servo controller see  ![Maestro python repo](https://github.com/FRC4564/Maestro)
5) battery pack (for servo)
6) Theater set:

    - lunar lander mockup 
    - 1m frame with polley and cord
    - lunar surface mockup 


### setup:

- laptop gets joystick input via USB
- laptop controlles servo via servo controller (USB input)
- laptop displays stereo camera OAK D depth image and height above surface in real time


---

## instalation:

python 3

- install opencv
- install OAKD package
- install pyjoystick
- install maestro-servo




