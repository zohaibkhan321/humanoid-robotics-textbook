---
title: 'Gazebo Physics Simulation'
tags: [gazebo, physics, simulation, gravity, collisions, joints, world-files, humanoid]
difficulty: intermediate
time: '45 minutes'
learningObjectives:
  - 'Understand the fundamentals of physics simulation in Gazebo'
  - 'Configure gravity, collisions, and joint properties for humanoid models'
  - 'Create and customize world files for simulation environments'
---

# Gazebo Physics Simulation

## Learning Objectives
After completing this chapter, you will be able to:
- Explain the core concepts of physics simulation in Gazebo
- Configure gravity parameters for different simulation scenarios
- Set up collision properties and joint constraints for humanoid models
- Create custom world files with various environmental properties

## Introduction
Gazebo is a powerful physics simulation engine widely used in robotics research and development. It provides realistic simulation of robots in complex environments, allowing developers to test algorithms and behaviors before deploying to real hardware. This chapter focuses on the physics aspects of Gazebo, particularly as they apply to humanoid robotics.

## Core Concepts

### Physics Engine Fundamentals
Gazebo uses Open Dynamics Engine (ODE), Bullet, or DART as its underlying physics engine. These engines calculate the motion of rigid bodies, handle collisions, and simulate other physical phenomena.

### Gravity Configuration
Gravity is a fundamental force in physics simulation that affects all objects in the environment. In Gazebo, gravity can be configured globally for the entire world or locally for specific models.

The default gravity vector in Gazebo is (0, 0, -9.8), representing Earth's gravity pulling objects downward along the z-axis. This can be modified in the world file:

```xml
<sdf version='1.7'>
  <world name='default'>
    <gravity>0 0 -9.8</gravity>
    <!-- Other world properties -->
  </world>
</sdf>
```

### Collision Detection
Collision detection is crucial for realistic physics simulation. Gazebo uses both broad-phase and narrow-phase collision detection algorithms to efficiently identify when objects intersect.

Collision properties include:
- Surface friction coefficients
- Bounce restitution
- Contact properties
- Collision filtering

### Joint Constraints
Joints connect different parts of a robot model and constrain their relative motion. Common joint types in humanoid robots include:
- Revolute joints (rotational motion)
- Prismatic joints (linear motion)
- Fixed joints (no motion)
- Continuous joints (unlimited rotation)
- Ball joints (3 rotational degrees of freedom)

## Hands-on Lab

### Setting up a Basic Humanoid Model Simulation

1. Create a simple humanoid model file (`humanoid_model.sdf`):

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="simple_humanoid">
    <link name="base_link">
      <pose>0 0 1.0 0 0 0</pose>
      <inertial>
        <mass>5.0</mass>
        <inertia>
          <ixx>0.1</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.1</iyy>
          <iyz>0.0</iyz>
          <izz>0.1</izz>
        </inertia>
      </inertial>
      <visual name="visual">
        <geometry>
          <box>
            <size>0.5 0.5 0.5</size>
          </box>
        </geometry>
      </visual>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.5 0.5 0.5</size>
          </box>
        </geometry>
      </collision>
    </link>

    <link name="leg_link">
      <inertial>
        <mass>2.0</mass>
        <inertia>
          <ixx>0.05</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.05</iyy>
          <iyz>0.0</iyz>
          <izz>0.05</izz>
        </inertia>
      </inertial>
      <visual name="visual">
        <geometry>
          <cylinder>
            <radius>0.05</radius>
            <length>0.5</length>
          </cylinder>
        </geometry>
      </visual>
      <collision name="collision">
        <geometry>
          <cylinder>
            <radius>0.05</radius>
            <length>0.5</length>
          </cylinder>
        </geometry>
      </collision>
    </link>

    <joint name="hip_joint" type="revolute">
      <parent>base_link</parent>
      <child>leg_link</child>
      <axis>
        <xyz>0 0 1</xyz>
        <limit>
          <lower>-1.57</lower>
          <upper>1.57</upper>
        </limit>
      </axis>
    </joint>
  </model>
</sdf>
```

2. Create a world file (`humanoid_world.world`) with custom gravity:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="humanoid_world">
    <!-- Set gravity to Earth normal -->
    <gravity>0 0 -9.8</gravity>

    <!-- Include a ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Include a sun for lighting -->
    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Include our custom humanoid model -->
    <include>
      <uri>file://humanoid_model.sdf</uri>
    </include>
  </world>
</sdf>
```

3. Launch Gazebo with your custom world:
```bash
gazebo humanoid_world.world
```

## Exercises
1. Modify the gravity in the world file to simulate lunar gravity (1/6 of Earth's gravity) and observe the differences in the simulation.
2. Add a second leg to the humanoid model with appropriate joint constraints.
3. Create a custom world with obstacles and test how the humanoid model interacts with them.

## Summary
This chapter introduced the fundamentals of physics simulation in Gazebo, focusing on gravity configuration, collision detection, and joint constraints. We explored how to create basic humanoid models with proper physical properties and how to set up simulation environments with custom world files. These concepts form the foundation for more complex humanoid robotics simulations.

## References
1. Open Robotics. (2023). *Gazebo Classic Documentation: Physics*. https://classic.gazebosim.org/tutorials?tut=physics
2. Koenig, N., & Howard, A. (2004). *Design and use paradigms for Gazebo, an open-source multi-robot simulator*. Proceedings of the 2004 IEEE/RSJ International Conference on Intelligent Robots and Systems.
3. Tedrake, R. (2023). *Underactuated Robotics: Algorithms for Walking, Running, Swimming, Flying, and Manipulation*. MIT Press. Available: https://underactuated.mit.edu/