# moon_lander_demo_for_kids
This is a cool moon landing demo for kids.
We simulate a lunar lander with camera relative navigation system.
User gets height readings from camera, and uses a joystick to control lander height.
The mission is to try and land the lander safely!


The demo is made of:
- a lunar lander model with OAK-D stereo cameras to measure distance to ground
- a 1m height frame with cord and pulley so pulling/releasing the line takes
the lunar lander up \ down
- a servo and a joystick to pull \ release the cord, and thus control
the lander height
- a laptop for user UI and controlling joystick \ lander cameras \ servo in realtime


![lunar_lander_demo_4_kids](https://user-images.githubusercontent.com/32566844/213310963-2004f37a-1c88-407b-a339-2b3ddd92da6f.png)

---

## Demo setup:

### components:

1) laptop 
2) OAK-D usb stereo camera set  see: ![OAK-D tutorial](https://github.com/luxonis/depthai)
3) usb joystick
4) servo motor
5) Pololu maestro usb servo controller see  ![Maestro python repo](https://github.com/FRC4564/Maestro)
6) battery pack (for servo)
7) Theater set:

    - lunar lander mockup 
    - 1m frame with polley and cord
    - lunar surface mockup 


### setup:

- laptop gets joystick input via USB
- laptop controls servo via servo controller (USB input)
- laptop displays stereo camera OAK D depth image and height above surface in real time



### requirements:
 
Our main requirements are:
+ lander max speed Vmax = 0.1m/sec
+ lander weight W=0.25kg

We choose servo motor and wheel accordingly.

Noting that:

        r - wheel radious [m]
        w - angular speed [rad/sec]
        f - motor frequency [sec/rotation]

        w[rad/sec] = v[m/sec] / r[m]
        f[sec/rotation] = 2 / w[rad/sec] = 2 * r[m] / v[m/sec]
        
        torque[m*Kg] = r[m]*W[kg]



we choose servo and wheel so that:

        f[sec/rotation] >= 2 * r[m] / vmax[m/sec] = 2 * 0.01 * r[cm] / 0.1 = 0.2 * r[cm]
        f[sec/60deg] >= 0.017 * r[cm]

        torque[kg*cm] >= 0.25*r[cm]



As an example we can choose:

servo with f >= 0.033[sec/60deg] , torque >= 0.5[kg*cm] and 2cm wheel

or

servo with f >= 0.017[sec/60deg] , torque >= 0.25[kg*cm] and 1cm wheel



---

## installation:

Install depthai python:

- install python 3
- make your virtual python env (to be used for this project)
- install depthai module for python:
  1. clone depthai python repo:

         git clone https://github.com/luxonis/depthai-python.git
  2. run depthai python install script in your python env:

         my_python ../depthai-python/examples/install_requirements.py

  3. test your python env. try to run:
  
         my_python OAK_D_stereo_depth_demo.py


- install pyjoystick
- install python maestro-servo



