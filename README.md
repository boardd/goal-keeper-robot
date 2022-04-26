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

Most of the mounting hardware was recycled from the Elegoo Tumbller, which was the robot we used in labs in the past. This included 8 standoffs, 2 motor mounts, one plastic plate, and a few M3 screws. Although we designed the goal to be printed in 2 parts and glued together, we also used the motor mounts to strengthen the bridging by screwing it between the two halves.

<img src="robotTopView.jpeg" alt="Robot Top View" width="600" class="center"/>

### Electronics

<img src="cameraMount.jpeg" alt="Camera Mount" width="600" class="center"/>

### The Setup

<img src="setup.jpeg" alt="Full Setup" width="600" class="center"/>
<img src="setupTopView.jpeg" alt="Top View of Setup" width="600" class="center"/>




### Robot Dimensions

### Robot CAD Images


