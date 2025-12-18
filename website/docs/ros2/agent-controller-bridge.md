---
title: 'Agent ↔ Controller Bridge'
tags: [ros2, ros2-control, controllers, control-loops, hardware-interface]
difficulty: advanced
time: '90 minutes'
learningObjectives:
  - 'Understand the ros2_control framework and its architecture'
  - 'Implement controller manager and hardware interface components'
  - 'Create control loops connecting high-level agents with low-level controllers'
  - 'Integrate controllers with ROS 2 systems for robot operation'
---

# Agent ↔ Controller Bridge

## Learning Objectives

After completing this chapter, you will be able to:
- Explain the ros2_control framework architecture and components
- Implement controller manager and hardware interface components
- Create control loops that connect high-level agents with low-level controllers
- Integrate controllers with ROS 2 systems for robot operation
- Configure and manage different types of controllers for robotic systems

## Introduction

The ros2_control framework is a hardware abstraction layer for ROS 2 that provides a unified interface between high-level control algorithms and low-level hardware interfaces. It allows for the implementation of various control strategies while maintaining a consistent interface, making it easier to develop, test, and deploy robotic systems.

The framework consists of several key components that work together to provide a flexible and robust control system for robots of various types and configurations.

## Core Concepts

### ros2_control Architecture

The ros2_control framework is built around several key components:

- **Hardware Interface**: Abstraction layer that communicates with physical hardware
- **Controller Manager**: Central component that manages and coordinates controllers
- **Controllers**: Individual control algorithms that implement specific behaviors
- **Resource Manager**: Tracks and manages available hardware resources
- **Realtime Capabilities**: Support for real-time control loops

### Hardware Interface Layer

The hardware interface layer provides an abstraction between the control system and the physical hardware. It handles:

- Reading from sensors (position, velocity, effort)
- Writing commands to actuators
- Resource management and safety checks
- Hardware-specific communication protocols

### Controller Manager

The controller manager is responsible for:

- Loading and unloading controllers
- Managing controller lifecycle (configure, start, stop, cleanup)
- Handling resource conflicts between controllers
- Providing introspection and monitoring capabilities
- Managing controller parameters

### Controller Types

ros2_control supports various types of controllers:

- **Joint Trajectory Controllers**: Execute trajectories for joint positions, velocities, or efforts
- **Forward Command Controllers**: Pass through commands to joints
- **Effort Controllers**: Control joint efforts/torques directly
- **Position Controllers**: Control joint positions
- **Velocity Controllers**: Control joint velocities
- **Custom Controllers**: User-defined controllers for specific applications

### Control Loop Integration

The framework provides two main types of control loops:

- **Non-realtime Loop**: Handles communication with ROS 2 topics/services
- **Realtime Loop**: Handles time-critical hardware communication

## Hands-on Lab

### Setup

For this lab, we'll create a simple controller that bridges a high-level agent with a simulated hardware interface.

### Implementation

Let's create a hardware interface for a simple robot with joint position control:

```python
# simple_hardware_interface.py
import math
from typing import Tuple

import hardware_interface
from hardware_interface import return_type
from rclpy.node import Node
from rclpy.logger import get_logger


class SimpleHardwareInterface(hardware_interface.BaseInterface):
    def __init__(self, hardware_info):
        super().__init__()
        self.hw_position = [0.0, 0.0, 0.0]  # Joint positions
        self.hw_velocity = [0.0, 0.0, 0.0]  # Joint velocities
        self.hw_effort = [0.0, 0.0, 0.0]    # Joint efforts
        self.hw_commands = [0.0, 0.0, 0.0]  # Command positions

        self.joint_names = []
        self.status = hardware_interface.HW_IF_POSITION | hardware_interface.HW_IF_VELOCITY | hardware_interface.HW_IF_EFFORT

        # Parse hardware info
        for joint in hardware_info.joints:
            self.joint_names.append(joint.name)
            self.hw_position.append(0.0)
            self.hw_velocity.append(0.0)
            self.hw_effort.append(0.0)
            self.hw_commands.append(0.0)

    def configure(self, sensor_names) -> return_type:
        # Initialize hardware
        for i in range(len(self.joint_names)):
            self.hw_position[i] = 0.0
            self.hw_velocity[i] = 0.0
            self.hw_effort[i] = 0.0
            self.hw_commands[i] = 0.0
        return return_type.OK

    def get_names(self) -> Tuple[str]:
        return tuple(self.joint_names)

    def get_state_interfaces(self) -> Tuple[hardware_interface.StateInterface]:
        state_interfaces = []
        for i, name in enumerate(self.joint_names):
            state_interfaces.append(hardware_interface.StateInterface(name, hardware_interface.HW_IF_POSITION, self.hw_position[i]))
            state_interfaces.append(hardware_interface.StateInterface(name, hardware_interface.HW_IF_VELOCITY, self.hw_velocity[i]))
            state_interfaces.append(hardware_interface.StateInterface(name, hardware_interface.HW_IF_EFFORT, self.hw_effort[i]))
        return tuple(state_interfaces)

    def get_command_interfaces(self) -> Tuple[hardware_interface.CommandInterface]:
        command_interfaces = []
        for i, name in enumerate(self.joint_names):
            command_interfaces.append(hardware_interface.CommandInterface(name, hardware_interface.HW_IF_POSITION, self.hw_commands[i]))
        return tuple(command_interfaces)

    def read(self, time, period) -> return_type:
        # Simulate reading from hardware
        # In a real implementation, this would communicate with actual hardware
        for i in range(len(self.joint_names)):
            # Simple simulation: command position becomes actual position over time
            self.hw_position[i] += (self.hw_commands[i] - self.hw_position[i]) * 0.1
            self.hw_velocity[i] = (self.hw_commands[i] - self.hw_position[i]) / period
            self.hw_effort[i] = (self.hw_commands[i] - self.hw_position[i]) * 10.0  # Simple PD control
        return return_type.OK

    def write(self, time, period) -> return_type:
        # In a real implementation, this would send commands to actual hardware
        # For simulation, we just store the commands which will be used in the next read cycle
        return return_type.OK
```

Now let's create a simple controller that can be managed by the controller manager:

```python
# position_trajectory_controller.py
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from control_msgs.msg import JointTrajectoryControllerState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import threading


class PositionTrajectoryController(Node):
    def __init__(self):
        super().__init__('position_trajectory_controller')

        # Create subscribers and publishers
        self.subscription = self.create_subscription(
            JointTrajectory,
            'joint_trajectory',
            self.trajectory_callback,
            QoSProfile(depth=10)
        )

        self.publisher = self.create_publisher(
            JointTrajectoryControllerState,
            'controller_state',
            QoSProfile(depth=10)
        )

        # Controller state
        self.current_joint_names = []
        self.current_positions = []
        self.current_velocities = []
        self.current_efforts = []
        self.commanded_positions = []

        # Timer for control loop
        self.control_timer = self.create_timer(0.01, self.control_loop)  # 100 Hz

        self.get_logger().info('Position Trajectory Controller initialized')

    def trajectory_callback(self, msg):
        # Process incoming trajectory
        self.current_joint_names = msg.joint_names
        self.get_logger().info(f'Received trajectory for joints: {self.current_joint_names}')

        # For this example, we'll just take the first point
        if len(msg.points) > 0:
            point = msg.points[0]
            self.commanded_positions = list(point.positions)
            self.get_logger().info(f'Commanded positions: {self.commanded_positions}')

    def control_loop(self):
        # Simple control loop implementation
        if len(self.commanded_positions) > 0:
            # Update current positions (in a real system, these would come from hardware)
            for i in range(len(self.commanded_positions)):
                if i >= len(self.current_positions):
                    self.current_positions.append(0.0)
                    self.current_velocities.append(0.0)
                    self.current_efforts.append(0.0)

                # Simple PD control
                error = self.commanded_positions[i] - self.current_positions[i]
                self.current_positions[i] += error * 0.01  # Integration step
                self.current_velocities[i] = error * 10.0  # Velocity based on error
                self.current_efforts[i] = error * 50.0    # Effort based on error

        # Publish controller state
        state_msg = JointTrajectoryControllerState()
        state_msg.joint_names = self.current_joint_names
        state_msg.desired.positions = self.commanded_positions
        state_msg.actual.positions = self.current_positions
        state_msg.error.positions = [0.0] * len(self.current_positions)  # Placeholder

        self.publisher.publish(state_msg)

    def cleanup(self):
        self.get_logger().info('Cleaning up controller')


def main(args=None):
    rclpy.init(args=args)
    controller = PositionTrajectoryController()

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.cleanup()
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Now let's create an agent that can send commands to the controller:

```python
# agent_controller_bridge.py
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import math
import time


class AgentControllerBridge(Node):
    def __init__(self):
        super().__init__('agent_controller_bridge')

        # Create publisher for joint trajectory commands
        self.trajectory_publisher = self.create_publisher(
            JointTrajectory,
            'joint_trajectory',
            QoSProfile(depth=10)
        )

        # Timer to send commands periodically
        self.command_timer = self.create_timer(2.0, self.send_trajectory_command)

        self.get_logger().info('Agent-Controller Bridge initialized')

    def send_trajectory_command(self):
        # Create a trajectory command
        trajectory_msg = JointTrajectory()
        trajectory_msg.joint_names = ['joint1', 'joint2', 'joint3']

        # Create trajectory point
        point = JointTrajectoryPoint()

        # Set positions (oscillating pattern)
        current_time = self.get_clock().now().nanoseconds / 1e9
        point.positions = [
            math.sin(current_time),
            math.cos(current_time) * 0.5,
            math.sin(current_time * 0.7) * 0.3
        ]

        # Set velocities
        point.velocities = [
            math.cos(current_time),
            -math.sin(current_time) * 0.5,
            math.cos(current_time * 0.7) * 0.3 * 0.7
        ]

        # Set effort (optional)
        point.effort = [0.0, 0.0, 0.0]

        # Set time from start
        point.time_from_start = Duration(sec=1, nanosec=0)

        trajectory_msg.points = [point]

        self.trajectory_publisher.publish(trajectory_msg)
        self.get_logger().info(f'Sent trajectory command: positions={point.positions}')


def main(args=None):
    rclpy.init(args=args)
    bridge = AgentControllerBridge()

    try:
        rclpy.spin(bridge)
    except KeyboardInterrupt:
        pass
    finally:
        bridge.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Running the Example

1. Save all Python files in your ROS 2 workspace
2. Source your ROS 2 environment: `source /opt/ros/humble/setup.bash`
3. In one terminal, run the controller: `python3 position_trajectory_controller.py`
4. In another terminal, run the agent: `python3 agent_controller_bridge.py`
5. Monitor the controller state: `ros2 topic echo /controller_state`

## Exercises

1. **Exercise 1**: Modify the controller to implement a PID control algorithm instead of the simple PD control
2. **Exercise 2**: Create a velocity controller that can be switched between position and velocity control modes
3. **Exercise 3**: Implement a safety layer that limits joint positions and velocities to safe ranges

## Summary

In this chapter, we covered the ros2_control framework:
- Understanding the architecture and components of ros2_control
- Implementing hardware interfaces for robot control
- Creating controllers that manage robot behavior
- Building bridges between high-level agents and low-level controllers
- Configuring control loops for real-time operation

These concepts enable the integration of high-level planning and decision-making agents with low-level hardware controllers, forming the foundation for complex robotic systems.

## References

1. ROS Control. (2023). *ros2_control Documentation*. https://control.ros.org/
2. Rosmann, C. (2022). *Robotics, Vision and Control: Fundamental Algorithms in MATLAB*. Springer.
3. Siciliano, B., & Khatib, O. (2016). *Springer Handbook of Robotics*. Springer-Verlag.
4. ROS.org. (2023). *ROS 2 Control Tutorials*. https://docs.ros.org/en/humble/Tutorials/Advanced/URDF/Using-URDF-With-Robot-State-Publisher.html