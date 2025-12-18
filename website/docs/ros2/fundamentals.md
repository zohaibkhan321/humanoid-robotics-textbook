---
title: 'ROS 2 Fundamentals'
tags: [ros2, fundamentals, nodes, topics, services, actions, qos]
difficulty: intermediate
time: '60 minutes'
learningObjectives:
  - 'Understand the core concepts of ROS 2 architecture'
  - 'Create and manage ROS 2 nodes for communication'
  - 'Implement publisher/subscriber communication patterns'
---

# ROS 2 Fundamentals

## Learning Objectives

After completing this chapter, you will be able to:
- Explain the core concepts of ROS 2 architecture
- Create and manage ROS 2 nodes
- Implement publisher/subscriber communication patterns
- Understand Quality of Service (QoS) policies
- Use services and actions for request/response communication

## Introduction

Robot Operating System 2 (ROS 2) is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms.

ROS 2 is designed to be suitable for real-world applications, addressing the limitations of ROS 1 in areas such as security, real-time support, and deployment in production environments.

## Core Concepts

### Nodes

A node is an executable that uses ROS 2 to communicate with other nodes. Nodes are the fundamental building blocks of a ROS 2 system. They encapsulate the functionality of a single purpose (e.g., a motor controller, a steering controller, a localization algorithm).

In ROS 2, nodes are designed to be:
- Modular: Each node should have a single responsibility
- Communicative: Nodes communicate with other nodes through topics, services, and actions
- Managed: Nodes can be started, stopped, and monitored

### Topics and Message Passing

Topics are named buses over which nodes exchange messages. They provide one-way, many-to-many communication. Any number of nodes can subscribe to a topic, and any number of nodes can publish to a topic.

The publisher-subscriber pattern allows for:
- Decoupling: Publishers and subscribers don't need to know about each other
- Scalability: Multiple nodes can listen to the same data stream
- Asynchronous communication: Publishers and subscribers operate independently

### Services

Services provide a request/response communication pattern. A service client sends a request to a service server, which processes the request and sends back a response. This is a synchronous communication pattern.

Services are appropriate for:
- Request/response interactions
- Tasks that return a result immediately
- Configuration operations

### Actions

Actions are a more advanced communication pattern that extends services to support long-running tasks. Actions include:
- Goal: Request sent to the action server
- Feedback: Periodic updates during goal processing
- Result: Final outcome of the goal processing

Actions are appropriate for:
- Long-running tasks
- Tasks that provide feedback during execution
- Tasks that can be canceled

### Quality of Service (QoS)

QoS policies allow you to configure the behavior of topics and services to meet the requirements of your application. Key QoS settings include:

- Reliability: Whether messages should be guaranteed to be delivered
- Durability: Whether late-joining subscribers should receive old messages
- History: How many messages to store for late-joining subscribers
- Deadline: Expected frequency of message publication
- Lifespan: How long messages are kept before being dropped

## Hands-on Lab

### Setup

Before starting the lab, ensure you have ROS 2 Humble Hawksbill installed on your system. For this lab, we'll use the Python client library (rclpy).

### Implementation

Let's create a simple publisher and subscriber example to understand the communication pattern.

First, create a publisher node:

```python
# publisher_member_function.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Now, create a subscriber node:

```python
# subscriber_member_function.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Running the Example

1. Save both files in your ROS 2 workspace
2. Source your ROS 2 environment: `source /opt/ros/humble/setup.bash`
3. Run the publisher: `python3 publisher_member_function.py`
4. In another terminal, run the subscriber: `python3 subscriber_member_function.py`

You should see the publisher sending messages and the subscriber receiving them.

## Exercises

1. **Exercise 1**: Modify the publisher to send different types of messages (e.g., integers or custom message types)
2. **Exercise 2**: Create a service server that responds to requests with the current time
3. **Exercise 3**: Implement a simple action server that counts from 0 to 10, providing feedback during the process

## Summary

In this chapter, we covered the fundamental concepts of ROS 2:
- Nodes as the basic building blocks of ROS 2 systems
- Topics for publisher/subscriber communication
- Services for request/response communication
- Actions for long-running tasks with feedback
- Quality of Service policies for configuring communication behavior

These concepts form the foundation for more advanced ROS 2 development and are essential for building robust robotic systems.

## References

1. ROS.org. (2023). *ROS 2 Documentation: Concepts*. https://docs.ros.org/en/humble/Concepts.html
2. Quigley, M., Gerkey, B., & Smart, W. (2022). *Programming Robots with ROS: A Practical Introduction to the Robot Operating System*. O'Reilly Media.
3. ROS Industrial Consortium. (2023). *ROS 2 Best Practices Guide*. https://rosindustrial.github.io/ros_i_faq/