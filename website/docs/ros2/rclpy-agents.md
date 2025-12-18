---
title: 'rclpy Python Agents'
tags: [ros2, rclpy, python, agents, parameters, lifecycle, launch]
difficulty: intermediate
time: '75 minutes'
learningObjectives:
  - 'Understand the rclpy client library and its role in ROS 2'
  - 'Create parameterized ROS 2 nodes with dynamic configuration'
  - 'Implement lifecycle nodes for robust system management'
  - 'Use launch files to manage complex system deployments'
---

# rclpy Python Agents

## Learning Objectives

After completing this chapter, you will be able to:
- Use the rclpy client library to create ROS 2 nodes in Python
- Implement parameterized nodes with dynamic configuration
- Create and manage lifecycle nodes for robust system operation
- Write launch files to coordinate multi-node systems
- Apply agent patterns for distributed robotics systems

## Introduction

The ROS 2 Python Client Library (rclpy) provides Python bindings for ROS 2, allowing you to create ROS 2 nodes using Python. rclpy is the Python equivalent of rclcpp (for C++) and provides access to all core ROS 2 functionality including nodes, topics, services, actions, and parameters.

Python is an excellent choice for rapid prototyping and development of ROS 2 agents due to its ease of use, extensive ecosystem, and interactive development capabilities.

## Core Concepts

### rclpy Architecture

rclpy sits on top of the ROS Client Library (rcl) and provides a Python-friendly interface to the underlying ROS 2 system. The architecture includes:

- **Node**: The basic execution unit that can communicate with other nodes
- **Executor**: Manages the execution of callbacks and timers
- **Entity classes**: Publishers, subscribers, services, clients, and actions
- **Parameter system**: Dynamic configuration management
- **Timer system**: Periodic execution of callbacks

### Parameter Management

Parameters in ROS 2 provide a way to configure nodes at runtime. They offer several advantages:

- Dynamic reconfiguration without restarting nodes
- Hierarchical parameter namespacing
- Type safety with validation
- Storage in parameter files for deployment

Parameters can be declared with default values, descriptions, and constraints to ensure proper configuration.

### Lifecycle Nodes

Lifecycle nodes provide a structured approach to node state management. They implement a state machine with well-defined transitions:

- **Unconfigured**: Node is created but not configured
- **Inactive**: Node is configured but not active
- **Active**: Node is running and operational
- **Finalized**: Node is shutting down

This approach enables more robust system management, especially in complex deployments.

### Launch System

The launch system in ROS 2 provides a declarative way to start and manage multiple nodes and other processes. Key features include:

- XML and Python-based launch files
- Parameter passing to nodes
- Remapping of names
- Conditional launching
- Process management and monitoring

## Hands-on Lab

### Setup

For this lab, we'll create a parameterized lifecycle node and a corresponding launch file.

### Implementation

Let's create a parameterized node that can adjust its behavior based on configuration:

```python
# parameterized_agent.py
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import QoSProfile
from std_msgs.msg import String


class ParameterizedAgent(Node):
    def __init__(self):
        super().__init__('parameterized_agent')

        # Declare parameters with default values and descriptions
        self.declare_parameter('agent_name', 'default_agent')
        self.declare_parameter('publish_rate', 1.0)
        self.declare_parameter('message_prefix', 'Hello from')

        # Get parameter values
        self.agent_name = self.get_parameter('agent_name').value
        self.publish_rate = self.get_parameter('publish_rate').value
        self.message_prefix = self.get_parameter('message_prefix').value

        # Create publisher
        qos_profile = QoSProfile(depth=10)
        self.publisher = self.create_publisher(String, 'agent_messages', qos_profile)

        # Create timer based on parameter
        self.timer = self.create_timer(1.0 / self.publish_rate, self.timer_callback)

        # Log initial configuration
        self.get_logger().info(
            f'Agent {self.agent_name} initialized with rate {self.publish_rate}Hz'
        )

    def timer_callback(self):
        msg = String()
        msg.data = f'{self.message_prefix} {self.agent_name}: {self.get_clock().now()}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Published: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = ParameterizedAgent()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Now let's create a lifecycle node example:

```python
# lifecycle_agent.py
import rclpy
from rclpy.lifecycle import LifecycleNode, LifecycleState, TransitionCallbackReturn
from rclpy.qos import QoSProfile
from std_msgs.msg import String


class LifecycleAgent(LifecycleNode):
    def __init__(self):
        super().__init__('lifecycle_agent')
        self.get_logger().info('Lifecycle agent created, current state: unconfigured')

        # Initialize publisher but don't create it yet
        self.pub = None

    def on_configure(self, state):
        self.get_logger().info('on_configure() is called.')

        # Create publisher in this callback
        self.pub = self.create_publisher(String, 'lifecycle_chatter', 10)

        # Return success to indicate this step is complete
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state):
        self.get_logger().info('on_activate() is called.')

        # Activate the publisher
        self.pub.on_activate()

        # Create a timer that is called every second
        self.timer = self.create_timer(1.0, self.timer_callback)

        # Return success to indicate this step is complete
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state):
        self.get_logger().info('on_deactivate() is called.')

        # Deactivate the publisher
        self.pub.on_deactivate()

        # Cancel the timer
        self.timer.cancel()

        # Return success to indicate this step is complete
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state):
        self.get_logger().info('on_cleanup() is called.')

        # Destroy the publisher
        self.destroy_publisher(self.pub)
        self.pub = None

        # Return success to indicate this step is complete
        return TransitionCallbackReturn.SUCCESS

    def timer_callback(self):
        msg = String()
        msg.data = f'Lifecycle agent message at {self.get_clock().now()}'
        self.pub.publish(msg)
        self.get_logger().info(f'Published: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = LifecycleAgent()

    try:
        # Use the spin function to process callbacks
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Now let's create a launch file to manage these agents:

```python
# agent_launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Declare launch arguments
    agent_name_arg = DeclareLaunchArgument(
        'agent_name',
        default_value='launch_agent',
        description='Name of the agent'
    )

    publish_rate_arg = DeclareLaunchArgument(
        'publish_rate',
        default_value='1.0',
        description='Publish rate in Hz'
    )

    # Get launch configurations
    agent_name = LaunchConfiguration('agent_name')
    publish_rate = LaunchConfiguration('publish_rate')

    # Create parameterized agent node
    parameterized_agent = Node(
        package='your_package_name',  # Replace with actual package name
        executable='parameterized_agent',  # Replace with actual executable name
        name=agent_name,
        parameters=[
            {
                'agent_name': agent_name,
                'publish_rate': publish_rate,
                'message_prefix': 'Launched from'
            }
        ],
        output='screen'
    )

    # Create lifecycle agent node
    lifecycle_agent = Node(
        package='your_package_name',  # Replace with actual package name
        executable='lifecycle_agent',  # Replace with actual executable name
        name='lifecycle_agent',
        output='screen'
    )

    return LaunchDescription([
        agent_name_arg,
        publish_rate_arg,
        parameterized_agent,
        lifecycle_agent
    ])
```

### Running the Example

1. Save the Python files in your ROS 2 workspace
2. Make sure your Python files are executable: `chmod +x *.py`
3. Source your ROS 2 environment: `source /opt/ros/humble/setup.bash`
4. Run the parameterized agent: `python3 parameterized_agent.py`
5. In another terminal, run the lifecycle agent: `python3 lifecycle_agent.py`
6. To use the launch file: `ros2 launch agent_launch.py agent_name:=my_agent publish_rate:=2.0`

## Exercises

1. **Exercise 1**: Create a parameterized node that accepts a list of topics to publish to and cycles through them
2. **Exercise 2**: Implement a lifecycle node that transitions through all states based on external service calls
3. **Exercise 3**: Create a launch file that starts multiple parameterized agents with different configurations

## Summary

In this chapter, we covered advanced ROS 2 Python development concepts:
- Using rclpy for Python-based ROS 2 nodes
- Implementing parameterized nodes for dynamic configuration
- Creating lifecycle nodes for robust system management
- Using launch files to coordinate complex deployments

These concepts enable the development of sophisticated ROS 2 agents that can adapt to changing conditions and be managed effectively in complex systems.

## References

1. ROS.org. (2023). *ROS 2 Documentation: Using Parameters in a Class*. https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html
2. ROS.org. (2023). *ROS 2 Documentation: Lifecycle Nodes*. https://docs.ros.org/en/humble/Tutorials/Advanced/Lifecycle-Nodes.html
3. ROS.org. (2023). *ROS 2 Documentation: Launch System*. https://docs.ros.org/en/humble/Launch-Quick-Guide.html
4. Kamga, G. (2022). *Effective Robotics Programming with ROS 4*. Packt Publishing.