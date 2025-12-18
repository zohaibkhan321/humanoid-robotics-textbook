---
title: 'Sensors & Environments'
tags: [sensors, simulation, lidar, depth-camera, imu, environment, unity, hri]
difficulty: intermediate
time: '50 minutes'
learningObjectives:
  - 'Configure and simulate various sensor types in Gazebo'
  - 'Understand how to set up complex simulation environments'
  - 'Explore Unity as an alternative for human-robot interaction simulation'
---

# Sensors & Environments

## Learning Objectives
After completing this chapter, you will be able to:
- Configure LiDAR, depth camera, and IMU sensors in Gazebo simulation
- Set up complex environments with multiple objects and lighting conditions
- Understand the conceptual approach to Unity for human-robot interaction simulation

## Introduction
Realistic sensor simulation is crucial for developing and testing robot perception systems. This chapter covers the simulation of various sensor types in Gazebo and explores approaches to creating complex environments for robot testing. We'll also introduce Unity as an alternative simulation platform for human-robot interaction scenarios.

## Core Concepts

### Sensor Simulation in Gazebo
Gazebo provides plugins for simulating various sensor types that mimic real-world sensors. These include:
- LiDAR sensors for distance measurement and mapping
- Depth cameras for 3D scene reconstruction
- IMU sensors for orientation and acceleration data
- RGB cameras for visual perception
- Force/torque sensors for contact detection

### LiDAR Simulation
LiDAR (Light Detection and Ranging) sensors emit laser beams and measure the time it takes for the light to return after reflecting off objects. In Gazebo, LiDAR sensors can be configured with various parameters:
- Number of rays (horizontal and vertical resolution)
- Range (minimum and maximum distance)
- Field of view (horizontal and vertical)
- Noise characteristics

### Depth Camera Simulation
Depth cameras provide both color and depth information for each pixel. They're essential for 3D scene understanding and object recognition. In Gazebo, depth cameras simulate the physics of light and can include realistic noise models.

### IMU Simulation
Inertial Measurement Units (IMUs) measure linear acceleration and angular velocity. They're crucial for robot localization and balance control. Gazebo's IMU simulation includes realistic noise models and drift characteristics.

## Hands-on Lab

### Setting up a Multi-Sensor Robot Model

1. Create a robot model with multiple sensors (`sensor_robot.sdf`):

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="sensor_robot">
    <link name="chassis">
      <pose>0 0 0.5 0 0 0</pose>
      <inertial>
        <mass>10.0</mass>
        <inertia>
          <ixx>0.4</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.4</iyy>
          <iyz>0.0</iyz>
          <izz>0.4</izz>
        </inertia>
      </inertial>
      <visual name="visual">
        <geometry>
          <box>
            <size>1.0 0.5 0.5</size>
          </box>
        </geometry>
      </visual>
      <collision name="collision">
        <geometry>
          <box>
            <size>1.0 0.5 0.5</size>
          </box>
        </geometry>
      </collision>
    </link>

    <!-- LiDAR Sensor -->
    <link name="lidar_link">
      <pose>0.3 0 0.3 0 0 0</pose>
      <inertial>
        <mass>0.1</mass>
        <inertia>
          <ixx>0.001</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.001</iyy>
          <iyz>0.0</iyz>
          <izz>0.001</izz>
        </inertia>
      </inertial>
      <visual name="visual">
        <geometry>
          <cylinder>
            <radius>0.05</radius>
            <length>0.05</length>
          </cylinder>
        </geometry>
      </visual>
      <sensor name="lidar" type="ray">
        <pose>0 0 0 0 0 0</pose>
        <ray>
          <scan>
            <horizontal>
              <samples>360</samples>
              <resolution>1</resolution>
              <min_angle>-3.14159</min_angle>
              <max_angle>3.14159</max_angle>
            </horizontal>
          </scan>
          <range>
            <min>0.1</min>
            <max>10.0</max>
            <resolution>0.01</resolution>
          </range>
        </ray>
        <plugin name="lidar_controller" filename="libgazebo_ros_ray_sensor.so">
          <ros>
            <namespace>/sensor_robot</namespace>
            <remapping>~/out:=scan</remapping>
          </ros>
          <output_type>sensor_msgs/LaserScan</output_type>
        </plugin>
      </sensor>
    </link>

    <!-- Depth Camera Sensor -->
    <link name="camera_link">
      <pose>0.3 0 0.5 0 0 0</pose>
      <inertial>
        <mass>0.01</mass>
        <inertia>
          <ixx>0.0001</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.0001</iyy>
          <iyz>0.0</iyz>
          <izz>0.0001</izz>
        </inertia>
      </inertial>
      <visual name="visual">
        <geometry>
          <box>
            <size>0.05 0.05 0.05</size>
          </box>
        </geometry>
      </visual>
      <sensor name="depth_camera" type="depth">
        <pose>0 0 0 0 0 0</pose>
        <camera>
          <horizontal_fov>1.047</horizontal_fov>
          <image>
            <width>640</width>
            <height>480</height>
          </image>
          <clip>
            <near>0.1</near>
            <far>10</far>
          </clip>
        </camera>
        <plugin name="camera_controller" filename="libgazebo_ros_openni_kinect.so">
          <ros>
            <namespace>/sensor_robot</namespace>
            <remapping>~/rgb/image_raw:=rgb/image_raw</remapping>
            <remapping>~/depth/image_raw:=depth/image_raw</remapping>
            <remapping>~/depth/camera_info:=depth/camera_info</remapping>
          </ros>
          <output_type>sensor_msgs/Image</output_type>
        </plugin>
      </sensor>
    </link>

    <!-- IMU Sensor -->
    <link name="imu_link">
      <pose>0 0 0.3 0 0 0</pose>
      <inertial>
        <mass>0.01</mass>
        <inertia>
          <ixx>0.0001</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.0001</iyy>
          <iyz>0.0</iyz>
          <izz>0.0001</izz>
        </inertia>
      </inertial>
      <sensor name="imu_sensor" type="imu">
        <pose>0 0 0 0 0 0</pose>
        <plugin name="imu_controller" filename="libgazebo_ros_imu.so">
          <ros>
            <namespace>/sensor_robot</namespace>
            <remapping>~/out:=imu</remapping>
          </ros>
        </plugin>
      </sensor>
    </link>

    <!-- Connect sensors to chassis -->
    <joint name="lidar_joint" type="fixed">
      <parent>chassis</parent>
      <child>lidar_link</child>
    </joint>
    <joint name="camera_joint" type="fixed">
      <parent>chassis</parent>
      <child>camera_link</child>
    </joint>
    <joint name="imu_joint" type="fixed">
      <parent>chassis</parent>
      <child>imu_link</child>
    </joint>
  </model>
</sdf>
```

2. Create a complex environment world file (`complex_environment.world`):

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="complex_environment">
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <real_time_update_rate>1000.0</real_time_update_rate>
    </physics>

    <!-- Lighting -->
    <light name="sun" type="directional">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <attenuation>
        <range>1000</range>
        <constant>0.9</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
      <direction>-0.6 0.4 -0.8</direction>
    </light>

    <!-- Ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Objects in the environment -->
    <model name="table">
      <pose>2 2 0 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>1.0 0.8 0.8</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>1.0 0.8 0.8</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.6 0.4 1</ambient>
            <diffuse>0.8 0.6 0.4 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>10.0</mass>
          <inertia>
            <ixx>1.0</ixx>
            <ixy>0.0</ixy>
            <ixz>0.0</ixz>
            <iyy>1.0</iyy>
            <iyz>0.0</iyz>
            <izz>1.0</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <model name="obstacle1">
      <pose>-1 0 0 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <cylinder>
              <radius>0.3</radius>
              <length>1.0</length>
            </cylinder>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <cylinder>
              <radius>0.3</radius>
              <length>1.0</length>
            </cylinder>
          </geometry>
          <material>
            <ambient>0.4 0.4 0.8 1</ambient>
            <diffuse>0.4 0.4 0.8 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>5.0</mass>
          <inertia>
            <ixx>0.5</ixx>
            <ixy>0.0</ixy>
            <ixz>0.0</ixz>
            <iyy>0.5</iyy>
            <iyz>0.0</iyz>
            <izz>0.5</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <model name="obstacle2">
      <pose>0 -2 0 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.5 0.5 1.5</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.5 0.5 1.5</size>
            </box>
          </geometry>
          <material>
            <ambient>0.6 0.8 0.4 1</ambient>
            <diffuse>0.6 0.8 0.4 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>3.0</mass>
          <inertia>
            <ixx>0.3</ixx>
            <ixy>0.0</ixy>
            <ixz>0.0</ixz>
            <iyy>0.3</iyy>
            <iyz>0.0</iyz>
            <izz>0.3</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <!-- Include our sensor robot -->
    <include>
      <uri>file://sensor_robot.sdf</uri>
    </include>
  </world>
</sdf>
```

3. Launch Gazebo with the complex environment:
```bash
gazebo complex_environment.world
```

## Unity for Human-Robot Interaction (Conceptual)

Unity is a powerful 3D development platform that can be used for creating realistic human-robot interaction simulations. While Gazebo is primarily focused on physics simulation, Unity excels in creating visually rich environments and realistic human interactions.

### Key Features for HRI Simulation:
- High-fidelity graphics rendering
- Advanced lighting and material systems
- Realistic human avatars and animations
- VR/AR support for immersive experiences
- Physics simulation through NVIDIA PhysX
- Extensive asset store for environment creation

### Integration with Robotics:
- ROS# library for ROS communication
- Unity Robotics Package for robot simulation
- Perception package for sensor simulation
- ML-Agents for AI training in simulation

## Exercises
1. Add a RGB camera to the robot model and configure it to publish image data.
2. Create a custom environment with moving obstacles and test sensor detection.
3. Research and outline how you would implement a Unity simulation for human-robot interaction scenarios.

## Summary
This chapter covered the simulation of various sensor types in Gazebo, including LiDAR, depth cameras, and IMUs. We explored how to create complex environments with multiple objects and lighting conditions. Additionally, we introduced Unity as an alternative platform for human-robot interaction simulation, highlighting its strengths in creating visually rich and interactive environments.

## References
1. Open Robotics. (2023). *Gazebo Classic Documentation: Sensors*. https://classic.gazebosim.org/tutorials?tut=ros_gzplugins_sensors
2. Unity Technologies. (2023). *Unity Robotics Package*. https://docs.unity3d.com/Packages/com.unity.robotics@latest
3. Fox, D., Burgard, W., & Thrun, S. (1997). *The dynamic window approach to collision avoidance*. IEEE Robotics & Automation Magazine, 4(1), 23-33.