---
title: 'URDF for Humanoids'
tags: [urdf, xacro, links, joints, sensors, humanoid, kinematics]
difficulty: advanced
time: '105 minutes'
learningObjectives:
  - 'Understand the Unified Robot Description Format (URDF) and its XML structure'
  - 'Create robot models with proper links, joints, and kinematic chains'
  - 'Implement XACRO macros for complex humanoid models'
  - 'Integrate sensors into robot descriptions for perception'
---

# URDF for Humanoids

## Learning Objectives

After completing this chapter, you will be able to:
- Understand the Unified Robot Description Format (URDF) and its XML structure
- Create robot models with proper links, joints, and kinematic chains
- Implement XACRO macros for complex humanoid models
- Integrate sensors into robot descriptions for perception
- Validate URDF models and visualize them in simulation environments

## Introduction

The Unified Robot Description Format (URDF) is an XML-based format used in ROS to describe robots. It defines the kinematic and dynamic properties of a robot, including its links, joints, sensors, and other components. URDF is essential for robot simulation, visualization, and control in ROS-based systems.

For humanoid robots, URDF becomes particularly important as these robots have complex kinematic structures with multiple degrees of freedom, similar to human anatomy. This chapter will focus on creating URDF models specifically for humanoid robots.

## Core Concepts

### URDF Structure

A URDF file consists of several key elements:

- **Robot**: The root element that contains all other elements
- **Link**: Rigid bodies that make up the robot structure
- **Joint**: Connections between links that define how they can move relative to each other
- **Material**: Visual properties like color and texture
- **Visual**: How the link appears in visualization tools
- **Collision**: Collision properties for physics simulation
- **Inertial**: Mass, center of mass, and inertia properties

### Links

Links represent rigid bodies in the robot. Each link has:

- **Inertial properties**: Mass, center of mass, and inertia matrix
- **Visual properties**: How the link appears in visualization
- **Collision properties**: How the link behaves in collision detection

### Joints

Joints connect links and define their relative motion. Joint types include:

- **Fixed**: No relative motion between links
- **Revolute**: Single-axis rotation with limits
- **Continuous**: Single-axis rotation without limits
- **Prismatic**: Single-axis translation with limits
- **Floating**: Six degrees of freedom
- **Planar**: Motion on a plane

### XACRO

XACRO (XML Macros) is a macro language for XML that extends URDF. It allows for:

- Parameterization of URDF files
- Reusable components through macros
- Mathematical expressions
- Conditional inclusion of elements

## Hands-on Lab

### Setup

For this lab, we'll create a simple humanoid model with basic body parts using both URDF and XACRO.

### Implementation

Let's start with a simple URDF file for a basic humanoid torso:

```xml
<!-- simple_humanoid.urdf -->
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.3 0.2 0.4"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.2 0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="5.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Head -->
  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
      <material name="white">
        <color rgba="1.0 1.0 1.0 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="neck_joint" type="revolute">
    <parent link="base_link"/>
    <child link="head"/>
    <origin xyz="0.0 0.0 0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-0.5" upper="0.5" effort="100" velocity="1"/>
  </joint>

  <!-- Left Arm -->
  <link name="left_upper_arm">
    <visual>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
      <material name="blue">
        <color rgba="0.0 0.0 1.0 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.8"/>
      <inertia ixx="0.002" ixy="0.0" ixz="0.0" iyy="0.002" iyz="0.0" izz="0.0001"/>
    </inertial>
  </link>

  <joint name="left_shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="left_upper_arm"/>
    <origin xyz="0.2 0.0 0.1" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="50" velocity="1"/>
  </joint>
</robot>
```

Now let's create a more complex humanoid model using XACRO:

```xml
<!-- humanoid.xacro -->
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="humanoid_robot">

  <!-- Define constants -->
  <xacro:property name="M_PI" value="3.1415926535897931" />
  <xacro:property name="torso_height" value="0.4" />
  <xacro:property name="torso_width" value="0.3" />
  <xacro:property name="torso_depth" value="0.2" />
  <xacro:property name="arm_length" value="0.3" />
  <xacro:property name="arm_radius" value="0.05" />
  <xacro:property name="leg_length" value="0.4" />
  <xacro:property name="leg_radius" value="0.06" />
  <xacro:property name="head_radius" value="0.1" />

  <!-- Materials -->
  <material name="black">
    <color rgba="0.0 0.0 0.0 1.0"/>
  </material>

  <material name="blue">
    <color rgba="0.0 0.0 0.8 1.0"/>
  </material>

  <material name="green">
    <color rgba="0.0 0.8 0.0 1.0"/>
  </material>

  <material name="grey">
    <color rgba="0.2 0.2 0.2 1.0"/>
  </material>

  <material name="orange">
    <color rgba="${255/255} ${108/255} ${10/255} 1.0"/>
  </material>

  <material name="brown">
    <color rgba="${222/255} ${207/255} ${195/255} 1.0"/>
  </material>

  <material name="red">
    <color rgba="0.8 0.0 0.0 1.0"/>
  </material>

  <material name="white">
    <color rgba="1.0 1.0 1.0 1.0"/>
  </material>

  <!-- Macro for creating a limb -->
  <xacro:macro name="limb" params="name parent xyz rpy type *origin">
    <link name="${name}_link">
      <visual>
        <geometry>
          <cylinder length="${leg_length}" radius="${leg_radius}"/>
        </geometry>
        <material name="white"/>
        <xacro:insert_block name="origin"/>
      </visual>
      <collision>
        <geometry>
          <cylinder length="${leg_length}" radius="${leg_radius}"/>
        </geometry>
        <xacro:insert_block name="origin"/>
      </collision>
      <inertial>
        <mass value="0.5"/>
        <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
      </inertial>
    </link>

    <joint name="${name}_joint" type="${type}">
      <parent link="${parent}"/>
      <child link="${name}_link"/>
      <origin xyz="${xyz}" rpy="${rpy}"/>
      <axis xyz="0 1 0"/>
      <limit lower="-1.57" upper="1.57" effort="50" velocity="1"/>
    </joint>
  </xacro:macro>

  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="${torso_width} ${torso_depth} ${torso_height}"/>
      </geometry>
      <material name="orange"/>
    </visual>
    <collision>
      <geometry>
        <box size="${torso_width} ${torso_depth} ${torso_height}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="0.2" ixy="0.0" ixz="0.0" iyy="0.2" iyz="0.0" izz="0.2"/>
    </inertial>
  </link>

  <!-- Head -->
  <link name="head_link">
    <visual>
      <geometry>
        <sphere radius="${head_radius}"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <geometry>
        <sphere radius="${head_radius}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.004" ixy="0.0" ixz="0.0" iyy="0.004" iyz="0.0" izz="0.004"/>
    </inertial>
  </link>

  <joint name="neck_joint" type="revolute">
    <parent link="base_link"/>
    <child link="head_link"/>
    <origin xyz="0.0 0.0 ${torso_height/2 + head_radius}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-0.5" upper="0.5" effort="100" velocity="1"/>
  </joint>

  <!-- Left Arm -->
  <link name="left_upper_arm_link">
    <visual>
      <geometry>
        <cylinder length="${arm_length}" radius="${arm_radius}"/>
      </geometry>
      <material name="blue"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="${arm_length}" radius="${arm_radius}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.002" ixy="0.0" ixz="0.0" iyy="0.002" iyz="0.0" izz="0.0001"/>
    </inertial>
  </link>

  <joint name="left_shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="left_upper_arm_link"/>
    <origin xyz="${torso_width/2} 0.0 ${torso_height/4}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="50" velocity="1"/>
  </joint>

  <!-- Right Arm -->
  <link name="right_upper_arm_link">
    <visual>
      <geometry>
        <cylinder length="${arm_length}" radius="${arm_radius}"/>
      </geometry>
      <material name="blue"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="${arm_length}" radius="${arm_radius}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.002" ixy="0.0" ixz="0.0" iyy="0.002" iyz="0.0" izz="0.0001"/>
    </inertial>
  </link>

  <joint name="right_shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="right_upper_arm_link"/>
    <origin xyz="${-torso_width/2} 0.0 ${torso_height/4}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="50" velocity="1"/>
  </joint>

  <!-- Left Leg -->
  <link name="left_upper_leg_link">
    <visual>
      <geometry>
        <cylinder length="${leg_length}" radius="${leg_radius}"/>
      </geometry>
      <material name="green"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="${leg_length}" radius="${leg_radius}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.5"/>
      <inertia ixx="0.003" ixy="0.0" ixz="0.0" iyy="0.003" iyz="0.0" izz="0.0002"/>
    </inertial>
  </link>

  <joint name="left_hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="left_upper_leg_link"/>
    <origin xyz="${torso_width/4} 0.0 ${-torso_height/2}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <!-- Right Leg -->
  <link name="right_upper_leg_link">
    <visual>
      <geometry>
        <cylinder length="${leg_length}" radius="${leg_radius}"/>
      </geometry>
      <material name="green"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="${leg_length}" radius="${leg_radius}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.5"/>
      <inertia ixx="0.003" ixy="0.0" ixz="0.0" iyy="0.003" iyz="0.0" izz="0.0002"/>
    </inertial>
  </link>

  <joint name="right_hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="right_upper_leg_link"/>
    <origin xyz="${-torso_width/4} 0.0 ${-torso_height/2}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <!-- Adding a simple IMU sensor -->
  <gazebo reference="head_link">
    <sensor type="imu" name="imu_sensor">
      <always_on>true</always_on>
      <update_rate>100</update_rate>
      <imu>
        <angular_velocity>
          <x>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>2e-4</stddev>
            </noise>
          </x>
          <y>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>2e-4</stddev>
            </noise>
          </y>
          <z>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>2e-4</stddev>
            </noise>
          </z>
        </angular_velocity>
        <linear_acceleration>
          <x>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>1.7e-2</stddev>
            </noise>
          </x>
          <y>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>1.7e-2</stddev>
            </noise>
          </y>
          <z>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>1.7e-2</stddev>
            </noise>
          </z>
        </linear_acceleration>
      </imu>
    </sensor>
  </gazebo>

</robot>
```

### Running the Example

1. Save the XACRO file as `humanoid.xacro` in your ROS 2 workspace
2. Source your ROS 2 environment: `source /opt/ros/humble/setup.bash`
3. Convert XACRO to URDF: `ros2 run xacro xacro --inorder humanoid.xacro > humanoid.urdf`
4. Visualize the model in RViz: `rviz2`
5. Add a RobotModel display and set the Robot Description to "robot_description"
6. Load the URDF into a parameter server for visualization

## Exercises

1. **Exercise 1**: Add complete arms with elbow joints to the humanoid model
2. **Exercise 2**: Create a XACRO macro for a complete leg with hip, knee, and ankle joints
3. **Exercise 3**: Add a camera sensor to the head of the humanoid robot

## Summary

In this chapter, we covered URDF and XACRO for humanoid robots:
- Understanding the structure of URDF files and their components
- Creating links and joints for humanoid kinematic chains
- Using XACRO macros to simplify complex robot descriptions
- Adding sensors to robot models for perception capabilities
- Validating and visualizing URDF models

These concepts are fundamental for creating robot models that can be used in simulation, visualization, and control systems.

## References

1. ROS.org. (2023). *URDF/XML Format Documentation*. https://wiki.ros.org/urdf/XML
2. ROS.org. (2023). *XACRO Documentation*. https://wiki.ros.org/xacro
3. Corke, P. (2017). *Robotics, Vision and Control: Fundamental Algorithms in MATLAB*. Springer.
4. Siciliano, B., & Khatib, O. (2016). *Springer Handbook of Robotics*. Springer-Verlag.