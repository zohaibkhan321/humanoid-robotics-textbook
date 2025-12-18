---
title: 'Testing & Deployment'
tags: [ros2, testing, ci, docker, debugging, deployment]
difficulty: intermediate
time: '90 minutes'
learningObjectives:
  - 'Implement comprehensive testing strategies for ROS 2 systems'
  - 'Set up continuous integration pipelines for ROS 2 packages'
  - 'Create Docker containers for ROS 2 applications'
  - 'Apply debugging techniques for ROS 2 systems'
---

# Testing & Deployment

## Learning Objectives

After completing this chapter, you will be able to:
- Implement comprehensive testing strategies for ROS 2 systems
- Set up continuous integration pipelines for ROS 2 packages
- Create Docker containers for ROS 2 applications
- Apply debugging techniques for ROS 2 systems
- Deploy ROS 2 applications in production environments

## Introduction

Testing and deployment are critical aspects of developing robust and reliable ROS 2 systems. Proper testing ensures that your robot software behaves as expected under various conditions, while effective deployment strategies ensure that your software can be reliably installed and run in different environments.

This chapter covers best practices for testing ROS 2 applications at multiple levels, from unit tests of individual components to system-level integration tests. We'll also explore containerization techniques using Docker and continuous integration strategies.

## Core Concepts

### Testing Strategies

ROS 2 applications require testing at multiple levels:

- **Unit Testing**: Testing individual functions and classes in isolation
- **Integration Testing**: Testing how components work together
- **System Testing**: Testing the complete system behavior
- **Acceptance Testing**: Testing against user requirements

### Testing Frameworks

ROS 2 supports several testing frameworks:

- **gtest**: Google's C++ testing framework
- **pytest**: Python testing framework
- **rostest**: ROS-specific testing framework that manages nodes during tests
- **launch testing**: Testing launch files and system configurations

### Continuous Integration (CI)

CI practices for ROS 2 include:

- Automated testing on code changes
- Code quality checks (linting, formatting)
- Coverage analysis
- Performance regression testing
- Multi-platform testing

### Containerization

Docker containers provide:

- Consistent deployment environments
- Dependency isolation
- Easy scaling and orchestration
- Reproducible builds

### Deployment Strategies

Common deployment approaches include:

- **Monolithic Deployment**: All nodes in a single container
- **Microservices Deployment**: Each node in its own container
- **Hybrid Deployment**: Grouped services in containers
- **Edge Deployment**: Optimized for resource-constrained devices

## Hands-on Lab

### Setup

For this lab, we'll create a testing framework and deployment setup for a simple ROS 2 package.

### Implementation

Let's start with a simple ROS 2 package structure and create tests for it:

```python
# math_utils.py
def add_two_ints(a, b):
    """Add two integers and return the result."""
    return a + b

def multiply_two_ints(a, b):
    """Multiply two integers and return the result."""
    return a * b

def is_even(number):
    """Check if a number is even."""
    return number % 2 == 0
```

Now let's create a test file using pytest:

```python
# test_math_utils.py
import pytest
from math_utils import add_two_ints, multiply_two_ints, is_even


class TestMathUtils:
    def test_add_two_ints_positive(self):
        result = add_two_ints(2, 3)
        assert result == 5

    def test_add_two_ints_negative(self):
        result = add_two_ints(-1, 1)
        assert result == 0

    def test_add_two_ints_zero(self):
        result = add_two_ints(0, 0)
        assert result == 0

    def test_multiply_two_ints_positive(self):
        result = multiply_two_ints(3, 4)
        assert result == 12

    def test_multiply_two_ints_by_zero(self):
        result = multiply_two_ints(5, 0)
        assert result == 0

    def test_is_even_true(self):
        assert is_even(4) is True

    def test_is_even_false(self):
        assert is_even(5) is False

    def test_is_even_zero(self):
        assert is_even(0) is True


if __name__ == '__main__':
    pytest.main(['-v'])
```

Now let's create a ROS 2 node that we want to test:

```python
# simple_calculator.py
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class SimpleCalculator(Node):
    def __init__(self):
        super().__init__('simple_calculator')

        # Create a service that adds two integers
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_callback)

    def add_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Returning {request.a} + {request.b} = {response.sum}')
        return response


def main(args=None):
    rclpy.init(args=args)

    simple_calculator = SimpleCalculator()

    rclpy.spin(simple_calculator)

    simple_calculator.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Now let's create a test for the ROS 2 service:

```python
# test_simple_calculator.py
import pytest
import rclpy
from rclpy.executors import SingleThreadedExecutor
from example_interfaces.srv import AddTwoInts
from simple_calculator import SimpleCalculator


class TestSimpleCalculator:
    @classmethod
    def setup_class(cls):
        rclpy.init()

    @classmethod
    def teardown_class(cls):
        rclpy.shutdown()

    def setup_method(self):
        self.node = SimpleCalculator()
        self.executor = SingleThreadedExecutor()
        self.executor.add_node(self.node)

    def teardown_method(self):
        self.node.destroy_node()

    def test_add_two_ints_service(self):
        # Create a client for the service
        client = self.node.create_client(AddTwoInts, 'add_two_ints')

        # Wait for the service to be available
        while not client.wait_for_service(timeout_sec=1.0):
            self.node.get_logger().info('Service not available, waiting again...')

        # Create a request
        request = AddTwoInts.Request()
        request.a = 2
        request.b = 3

        # Call the service
        future = client.call_async(request)
        self.executor.spin_until_future_complete(future)

        # Check the result
        assert future.result().sum == 5


if __name__ == '__main__':
    pytest.main(['-v'])
```

Now let's create a Dockerfile for the ROS 2 application:

```dockerfile
# Dockerfile
# Use ROS 2 Humble Hawksbill base image
FROM ros:humble

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble

# Set the workspace directory
WORKDIR /ws

# Copy the package source code
COPY . /ws/src/my_robot_package

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3-pip && \
    rosdep update && \
    rosdep install --from-paths src --ignore-src -r -y && \
    rm -rf /var/lib/apt/lists/*

# Build the workspace
RUN . /opt/ros/$ROS_DISTRO/setup.sh && \
    colcon build --packages-select my_robot_package

# Source the workspace
SHELL ["/bin/bash", "-c"]
RUN echo "source /ws/install/setup.bash" >> ~/.bashrc
RUN echo "source /opt/ros/$ROS_DISTRO/setup.sh" >> ~/.bashrc

# Set the default command
CMD ["bash", "-c", "source /opt/ros/$ROS_DISTRO/setup.sh && source /ws/install/setup.bash && ros2 run my_robot_package simple_calculator"]
```

And a docker-compose file for multi-container deployment:

```yaml
# docker-compose.yml
version: '3.8'

services:
  calculator:
    build: .
    image: ros-calculator:latest
    container_name: ros-calculator
    environment:
      - ROS_DOMAIN_ID=42
    networks:
      - ros-network
    volumes:
      - ./logs:/logs
    command: >
      bash -c "
        source /opt/ros/humble/setup.sh &&
        source /ws/install/setup.bash &&
        ros2 run my_robot_package simple_calculator
      "

  monitor:
    build: .
    image: ros-calculator:latest
    container_name: ros-monitor
    environment:
      - ROS_DOMAIN_ID=42
    networks:
      - ros-network
    depends_on:
      - calculator
    command: >
      bash -c "
        source /opt/ros/humble/setup.sh &&
        source /ws/install/setup.bash &&
        ros2 run my_robot_package calculator_client
      "

networks:
  ros-network:
    driver: bridge
```

### Running the Example

1. Create a new ROS 2 package: `ros2 pkg create --build-type ament_python my_robot_package`
2. Add the Python files to the package source directory
3. Create the test files in the test directory of your package
4. Build the package: `colcon build --packages-select my_robot_package`
5. Run the tests: `source install/setup.bash && pytest -v test/test_*.py`
6. Build the Docker image: `docker build -t ros-calculator .`
7. Run the container: `docker-compose up`

## Exercises

1. **Exercise 1**: Create a launch test that verifies multiple nodes start correctly
2. **Exercise 2**: Implement a CI pipeline using GitHub Actions for your ROS 2 package
3. **Exercise 3**: Add code coverage analysis to your testing pipeline

## Summary

In this chapter, we covered testing and deployment for ROS 2 systems:
- Implementing comprehensive testing strategies at multiple levels
- Setting up continuous integration pipelines
- Creating Docker containers for ROS 2 applications
- Applying debugging techniques for ROS 2 systems
- Deploying ROS 2 applications in production environments

These practices ensure that your ROS 2 applications are reliable, maintainable, and can be deployed consistently across different environments.

## References

1. ROS.org. (2023). *ROS 2 Testing Documentation*. https://docs.ros.org/en/humble/How-To-Guides/Testing.html
2. ROS.org. (2023). *ROS 2 Docker Guide*. https://docs.ros.org/en/humble/How-To-Guides/Run-2-nodes-in-single-or-separate-docker-containers.html
3. Foote, T., & Lalancette, S. (2022). *ROS 2 Developer Guide*. Open Robotics.
4. Docker Documentation. (2023). *Best Practices for Writing Dockerfiles*. https://docs.docker.com/develop/develop-images/dockerfile_best-practices/