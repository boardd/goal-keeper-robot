# Autonomous Goal Keeper

## The Robot

<img src="robotIsoView.jpeg" alt="Robot Isometric View" width="1000" class="center"/>

## The Software

### Tracking the Ball

### PID Control

### LQR Control

### Performance Demonstration

## The Hardware

The robot was constructed using 3D-Printed parts as this was the most efficient way for us to prototype and manufacture the robot. At first we wanted to use a stick shaped goalie to block balls but found that this would perform poorly for several reasons. A thin stick shaped goalie would require much more precise inverse kinematics which would be difficult for a project with such a short time frame. We would need a lot of control over the arm which would be difficult given the inconsistencies that could be present with our computer vision algorithm. A rectangular goal also proved difficult to cover for a single linked revolute arm as it only moves in one dimension, but needs to be able to defend the xy-plane formed by the front face of the robot. We eventually arrived at the design as shown in the picture below, which allowed us to cover the entire goal, including all of the corners. The goalie blocker also has cutouts so that we are able to optimize the rotational inertia and achieve larger accelerations by the motor.

<img src="robotFrontView.jpeg" alt="Robot Front View" width="600" class="center"/>

Most of the mounting hardware was recycled from the <a href="https://www.elegoo.com/collections/robot-kits/products/elegoo-tumbller-self-balancing-robot-car">Elegoo Tumbller</a>, which was the robot we used in labs in the past. This included 8 standoffs, 2 motor mounts, one plastic plate, and a few M3 screws. Although we designed the goal to be printed in 2 parts and glued together, we also used the motor mounts to strengthen the bridging by screwing it between the two halves. By mounting all of the hardware on top of the robot, we make the robot portable and easy to relocate to anywhere it might need to be. The two motors are set up in a counter-rotating configuration so that we are able to maximize the amount of availiable torque whilst still maintaining the maximum speed that we are able to reach. We chose to direct drive the motors as it was the most robust and simple design to implement given the time constraints.

<img src="robotTopView.jpeg" alt="Robot Top View" width="600" class="center"/>

### Electronics

The electronics of the robot are also mostly recycled from the Elegoo Tumbller. We used an Arduino Nano microcontroller to recieve and command joint positions to the two motors that came with the Elegoo kit. The motors have encoders which have 1560 ticks per revolution, enough resolution to allow us to have relatively high precision on the position of the motor. Additionally, we used a camera rigged to provide a top view of the course as shown below. The camera uses a global shutter to minimize distortion and runs at roughly 37 fps. You can get the same camera <a href="https://www.amazon.com/Global-Shutter-Monochrome-Cameras-Windows/dp/B089QFRTVX/ref=sr_1_3?crid=137QCXP3HAXIZ&keywords=global+shutter+usb+camera&qid=1650942030&sprefix=global+shutter%2Caps%2C218&sr=8-3">here</a>, though we do recommend a different camera with a higher framerate if you able to get one. We also used the battery from the Elegoo kit to power our whole setup.  

<img src="cameraMount.jpeg" alt="Camera Mount" width="600" class="center"/>

### The Setup

We built the majority of the setup using cardboard. We first started by covering a large piece of cardboard with white paper to help our vision system more easily identify the ball. In hindsight, we would have used a color camera rather than a monochrome one as this made detecting the orange colored ping pong ball more difficult. We placed the camera roughly 4 feet above the ground so it is able to see most of the setup. We placed 4 ArUco markers in the corners of a rectangle

<img src="setup.jpeg" alt="Full Setup" width="600" class="center"/>
<img src="setupTopView.jpeg" alt="Top View of Setup" width="600" class="center"/>


### Robot Dimensions

### Robot CAD Images

### Parts Used
