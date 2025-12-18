---
title: 'LLM-Driven Cognitive Planning'
tags: [llm, cognitive-planning, natural-language, ros2-actions, task-planning, ai-robotics]
difficulty: advanced
time: '70 minutes'
learningObjectives:
  - 'Implement cognitive planning systems using large language models'
  - 'Translate natural language tasks into executable ROS 2 action sequences'
  - 'Design task planning architectures for humanoid robots'
---

# LLM-Driven Cognitive Planning

## Learning Objectives
After completing this chapter, you will be able to:
- Implement cognitive planning systems using large language models
- Translate natural language tasks into executable ROS 2 action sequences
- Design task planning architectures that integrate LLMs with robotic systems
- Understand the challenges and opportunities of LLM-driven robotics

## Introduction
Large Language Models (LLMs) represent a paradigm shift in how robots can understand and execute complex tasks expressed in natural language. This chapter explores the integration of LLMs with robotic systems to create cognitive planning capabilities, enabling humanoid robots to interpret high-level human instructions and decompose them into executable action sequences. We'll examine how LLMs can bridge the gap between human communication and robotic action execution.

## Core Concepts

### Cognitive Planning Architecture
Cognitive planning involves decomposing high-level tasks into sequences of executable actions. In the LLM context, this includes:
- Natural language understanding and task decomposition
- Knowledge retrieval and context awareness
- Action sequence generation
- Execution monitoring and adaptation
- Feedback integration and learning

### LLM Integration Patterns
There are several patterns for integrating LLMs with robotic systems:
- **Direct Mapping**: LLM directly generates ROS 2 action calls
- **Intermediate Representation**: LLM generates a structured plan that's then executed
- **Chain-of-Thought**: LLM reasons through steps before generating actions
- **Tool-Use**: LLM uses robotic APIs as tools in its reasoning process

### Task Decomposition
Complex tasks need to be broken down into manageable subtasks:
- High-level goal analysis
- Subtask identification
- Dependency resolution
- Resource allocation
- Error handling and recovery planning

### Execution Monitoring
LLM-driven systems need to monitor execution and adapt to changes:
- Real-time progress tracking
- Failure detection and recovery
- Plan adjustment based on environment changes
- Human-in-the-loop corrections

## Hands-on Lab

### Implementing an LLM-Driven Planning System

1. **LLM Planning Node with LangChain Integration**:
```python
# llm_planning_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from action_msgs.msg import GoalStatus
from rclpy.action import ActionClient
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool
from langchain.agents import initialize_agent, AgentType
import json
import re
from typing import Dict, List, Any, Optional

class RobotActionTool(BaseTool):
    """Tool for executing robot actions"""
    name = "robot_action"
    description = "Execute a robot action with parameters"

    def __init__(self, node):
        super().__init__()
        self.node = node

    def _run(self, action: str, **kwargs: Any) -> str:
        """Execute the robot action"""
        try:
            # Publish the action to appropriate topic/service
            if action == "move_to":
                x = kwargs.get('x', 0.0)
                y = kwargs.get('y', 0.0)
                self.node.execute_move_to(x, y)
                return f"Moving to position ({x}, {y})"
            elif action == "pick_up":
                object_name = kwargs.get('object', 'unknown')
                self.node.execute_pick_up(object_name)
                return f"Picking up {object_name}"
            elif action == "place":
                location = kwargs.get('location', 'default')
                self.node.execute_place(location)
                return f"Placing object at {location}"
            elif action == "greet":
                person = kwargs.get('person', 'human')
                self.node.execute_greet(person)
                return f"Greeting {person}"
            else:
                return f"Unknown action: {action}"
        except Exception as e:
            return f"Error executing action {action}: {str(e)}"

    async def _arun(self, action: str, **kwargs: Any) -> str:
        """Asynchronous version"""
        raise NotImplementedError("Async not implemented")

class LLMPlanningNode(Node):
    def __init__(self):
        super().__init__('llm_planning_node')

        # Publisher for task status
        self.status_pub = self.create_publisher(String, '/task_status', 10)

        # Publisher for robot commands (example)
        self.cmd_pub = self.create_publisher(PoseStamped, '/goal_pose', 10)

        # Initialize LLM
        try:
            self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)
        except Exception as e:
            self.get_logger().error(f"Failed to initialize LLM: {e}")
            self.llm = None

        # Initialize tools
        self.robot_tool = RobotActionTool(self)

        # Initialize agent
        if self.llm:
            self.agent = initialize_agent(
                [self.robot_tool],
                self.llm,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True
            )

        # Subscription for natural language commands
        self.command_sub = self.create_subscription(
            String,
            '/natural_language_command',
            self.command_callback,
            10
        )

        self.get_logger().info('LLM Planning Node initialized')

    def command_callback(self, msg):
        """Handle natural language command"""
        command = msg.data
        self.get_logger().info(f"Received command: {command}")

        if self.llm:
            try:
                # Use the agent to process the command
                result = self.agent.run(f"Execute the following command: {command}")
                self.send_status(f"Task completed: {result}")
            except Exception as e:
                self.get_logger().error(f"Error processing command: {e}")
                self.send_status(f"Error: {str(e)}")
        else:
            self.send_status("LLM not initialized")

    def execute_move_to(self, x: float, y: float):
        """Execute move to position"""
        goal = PoseStamped()
        goal.header.stamp = self.get_clock().now().to_msg()
        goal.header.frame_id = 'map'
        goal.pose.position.x = x
        goal.pose.position.y = y
        goal.pose.position.z = 0.0
        goal.pose.orientation.w = 1.0

        self.cmd_pub.publish(goal.pose)
        self.get_logger().info(f"Moving to ({x}, {y})")

    def execute_pick_up(self, object_name: str):
        """Execute pick up object"""
        self.get_logger().info(f"Picking up {object_name}")
        # In practice, this would call a manipulation action server

    def execute_place(self, location: str):
        """Execute place object"""
        self.get_logger().info(f"Placing object at {location}")
        # In practice, this would call a manipulation action server

    def execute_greet(self, person: str):
        """Execute greeting"""
        self.get_logger().info(f"Greeting {person}")
        # In practice, this would trigger speech synthesis

    def send_status(self, status: str):
        """Send task status"""
        status_msg = String()
        status_msg.data = status
        self.status_pub.publish(status_msg)
        self.get_logger().info(f"Status: {status}")

def main(args=None):
    rclpy.init(args=args)
    llm_planning_node = LLMPlanningNode()

    try:
        rclpy.spin(llm_planning_node)
    except KeyboardInterrupt:
        pass
    finally:
        llm_planning_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

2. **Task Planning with State Management**:
```python
# task_planner.py
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
import json

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    id: str
    description: str
    status: TaskStatus
    actions: List[Dict[str, Any]]
    dependencies: List[str]  # IDs of tasks this task depends on
    result: Optional[str] = None
    error: Optional[str] = None

class TaskPlanner:
    """Manages complex task decomposition and execution"""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.task_counter = 0

    def decompose_task(self, natural_language_task: str) -> List[Task]:
        """Decompose a natural language task into subtasks"""
        # This would typically use an LLM to decompose the task
        # For this example, we'll simulate the decomposition

        # Example: "Clean the living room" -> ["Find cleaning supplies", "Vacuum floor", "Dust surfaces"]
        subtasks = self._simulate_decomposition(natural_language_task)

        tasks = []
        for i, (desc, actions) in enumerate(subtasks):
            task_id = f"task_{self.task_counter}"
            self.task_counter += 1

            task = Task(
                id=task_id,
                description=desc,
                status=TaskStatus.PENDING,
                actions=actions,
                dependencies=[tasks[-1].id] if tasks else []  # Sequential dependencies
            )
            tasks.append(task)
            self.tasks[task_id] = task

        return tasks

    def _simulate_decomposition(self, task: str) -> List[tuple]:
        """Simulate task decomposition (in practice, use LLM)"""
        task = task.lower()

        if "clean" in task and "living room" in task:
            return [
                ("Find cleaning supplies", [
                    {"action": "navigate_to", "params": {"location": "closet"}},
                    {"action": "detect_object", "params": {"object_type": "cleaning_supplies"}}
                ]),
                ("Vacuum floor", [
                    {"action": "navigate_to", "params": {"location": "living_room"}},
                    {"action": "activate_tool", "params": {"tool": "vacuum"}}
                ]),
                ("Dust surfaces", [
                    {"action": "navigate_to", "params": {"location": "living_room"}},
                    {"action": "activate_tool", "params": {"tool": "duster"}}
                ])
            ]
        elif "bring" in task or "fetch" in task:
            # Example: "Bring me a cup of coffee"
            return [
                ("Navigate to kitchen", [
                    {"action": "navigate_to", "params": {"location": "kitchen"}}
                ]),
                ("Find coffee", [
                    {"action": "detect_object", "params": {"object_type": "coffee"}}
                ]),
                ("Grasp coffee", [
                    {"action": "grasp_object", "params": {"object_id": "coffee"}}
                ]),
                ("Return to user", [
                    {"action": "navigate_to", "params": {"location": "user_location"}}
                ])
            ]
        else:
            # Default: simple navigation task
            return [
                ("Navigate to location", [
                    {"action": "navigate_to", "params": {"location": "default_destination"}}
                ])
            ]

    def execute_task(self, task_id: str) -> bool:
        """Execute a single task"""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]

        # Check dependencies
        for dep_id in task.dependencies:
            if dep_id not in self.tasks or self.tasks[dep_id].status != TaskStatus.COMPLETED:
                return False  # Dependencies not met

        try:
            task.status = TaskStatus.IN_PROGRESS

            # Execute each action in the task
            for action in task.actions:
                success = self._execute_action(action)
                if not success:
                    task.status = TaskStatus.FAILED
                    task.error = f"Action failed: {action}"
                    return False

            task.status = TaskStatus.COMPLETED
            task.result = "Task completed successfully"
            return True
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            return False

    def _execute_action(self, action: Dict[str, Any]) -> bool:
        """Execute a single action (placeholder)"""
        action_type = action.get("action")
        params = action.get("params", {})

        # In practice, this would interface with ROS 2 services/actions
        print(f"Executing action: {action_type} with params: {params}")

        # Simulate action execution
        import time
        time.sleep(0.1)  # Simulate processing time

        return True  # Simulate success

    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Get the status of a task"""
        if task_id in self.tasks:
            return self.tasks[task_id].status
        return None

    def execute_all_tasks(self) -> bool:
        """Execute all tasks in dependency order"""
        completed = 0
        total = len(self.tasks)

        while completed < total:
            any_executed = False

            for task_id, task in self.tasks.items():
                if task.status in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS]:
                    if self.execute_task(task_id):
                        any_executed = True
                        completed += 1

            if not any_executed:
                # No progress made, likely a circular dependency or failure
                break

        return all(task.status == TaskStatus.COMPLETED for task in self.tasks.values())

# Example usage
if __name__ == "__main__":
    planner = TaskPlanner()

    # Decompose a complex task
    tasks = planner.decompose_task("Clean the living room")

    print(f"Decomposed into {len(tasks)} subtasks:")
    for task in tasks:
        print(f"- {task.description} (ID: {task.id})")
        print(f"  Actions: {task.actions}")

    # Execute all tasks
    success = planner.execute_all_tasks()
    print(f"Overall success: {success}")

    # Print final status
    for task_id, task in planner.tasks.items():
        print(f"Task {task_id}: {task.status.value}")
        if task.error:
            print(f"  Error: {task.error}")
```

3. **Natural Language to ROS Action Mapping**:
```python
# nl_to_ros_mapper.py
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json

@dataclass
class ParsedCommand:
    action: str
    parameters: Dict[str, any]
    confidence: float

class NaturalLanguageMapper:
    """Maps natural language commands to ROS actions"""

    def __init__(self):
        # Define action patterns
        self.action_patterns = {
            "navigate_to": [
                r"navigate to the (\w+)",
                r"go to the (\w+)",
                r"move to the (\w+)",
                r"walk to the (\w+)",
                r"head to the (\w+)",
                r"travel to the (\w+)"
            ],
            "grasp_object": [
                r"pick up the (\w+)",
                r"grab the (\w+)",
                r"take the (\w+)",
                r"get the (\w+)",
                r"lift the (\w+)",
                r"collect the (\w+)"
            ],
            "place_object": [
                r"place the (\w+) on the (\w+)",
                r"put the (\w+) on the (\w+)",
                r"set the (\w+) on the (\w+)"
            ],
            "follow_person": [
                r"follow the (\w+)",
                r"follow (\w+)",
                r"accompany the (\w+)",
                r"go with the (\w+)"
            ],
            "find_object": [
                r"find the (\w+)",
                r"locate the (\w+)",
                r"search for the (\w+)",
                r"look for the (\w+)"
            ]
        }

        # Location mappings
        self.location_mappings = {
            "kitchen": "kitchen_area",
            "living room": "living_room_area",
            "bedroom": "bedroom_area",
            "bathroom": "bathroom_area",
            "office": "office_area",
            "dining room": "dining_room_area",
            "hallway": "hallway_area",
            "entrance": "entrance_area",
            "livingroom": "living_room_area"
        }

        # Object mappings
        self.object_mappings = {
            "cup": "cup_01",
            "bottle": "bottle_01",
            "book": "book_01",
            "phone": "phone_01",
            "keys": "keys_01",
            "plate": "plate_01",
            "fork": "fork_01",
            "spoon": "spoon_01",
            "bowl": "bowl_01"
        }

    def parse_command(self, text: str) -> Optional[ParsedCommand]:
        """Parse natural language command into structured action"""
        text = text.lower().strip()

        for action, patterns in self.action_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    if action == "navigate_to":
                        location = match.group(1)
                        mapped_location = self.location_mappings.get(location, location)
                        return ParsedCommand(
                            action=action,
                            parameters={"location": mapped_location},
                            confidence=0.9
                        )
                    elif action == "grasp_object":
                        obj = match.group(1)
                        mapped_obj = self.object_mappings.get(obj, obj)
                        return ParsedCommand(
                            action=action,
                            parameters={"object_id": mapped_obj},
                            confidence=0.9
                        )
                    elif action == "place_object":
                        obj = match.group(1)
                        location = match.group(2)
                        mapped_obj = self.object_mappings.get(obj, obj)
                        mapped_location = self.location_mappings.get(location, location)
                        return ParsedCommand(
                            action=action,
                            parameters={
                                "object_id": mapped_obj,
                                "location": mapped_location
                            },
                            confidence=0.9
                        )
                    elif action == "follow_person":
                        person = match.group(1)
                        return ParsedCommand(
                            action=action,
                            parameters={"target": person},
                            confidence=0.9
                        )
                    elif action == "find_object":
                        obj = match.group(1)
                        mapped_obj = self.object_mappings.get(obj, obj)
                        return ParsedCommand(
                            action=action,
                            parameters={"object_type": mapped_obj},
                            confidence=0.9
                        )

        # If no specific pattern matched, try general movement
        movement_cmd = self._parse_movement(text)
        if movement_cmd:
            return movement_cmd

        return None

    def _parse_movement(self, text: str) -> Optional[ParsedCommand]:
        """Parse simple movement commands"""
        movement_patterns = {
            "move_forward": [r"go forward", r"move forward", r"go straight", r"move straight"],
            "move_backward": [r"go backward", r"move backward", r"go back", r"move back"],
            "turn_left": [r"turn left", r"turn to the left"],
            "turn_right": [r"turn right", r"turn to the right"],
            "stop": [r"stop", r"halt", r"pause"]
        }

        for action, patterns in movement_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return ParsedCommand(
                        action=action,
                        parameters={},
                        confidence=0.8
                    )

        return None

    def generate_ros_action(self, parsed_command: ParsedCommand) -> Dict[str, any]:
        """Generate ROS action call from parsed command"""
        action_map = {
            "navigate_to": {
                "action_type": "nav2_msgs/action/NavigateToPose",
                "goal": {
                    "pose": {
                        "header": {"frame_id": "map"},
                        "pose": {"position": {"x": 0.0, "y": 0.0, "z": 0.0}}
                    }
                }
            },
            "grasp_object": {
                "action_type": "manipulation_msgs/action/GraspObject",
                "goal": {
                    "object_id": parsed_command.parameters.get("object_id", "")
                }
            },
            "place_object": {
                "action_type": "manipulation_msgs/action/PlaceObject",
                "goal": {
                    "object_id": parsed_command.parameters.get("object_id", ""),
                    "location": parsed_command.parameters.get("location", "")
                }
            },
            "follow_person": {
                "action_type": "tracking_msgs/action/FollowTarget",
                "goal": {
                    "target_id": parsed_command.parameters.get("target", "")
                }
            }
        }

        if parsed_command.action in action_map:
            ros_action = action_map[parsed_command.action].copy()

            # Update position for navigation based on location
            if parsed_command.action == "navigate_to":
                # In practice, this would look up coordinates from a map
                # For now, use dummy coordinates based on location
                location = parsed_command.parameters.get("location", "default")
                if "kitchen" in location:
                    ros_action["goal"]["pose"]["pose"]["position"]["x"] = 2.0
                    ros_action["goal"]["pose"]["pose"]["position"]["y"] = 1.0
                elif "bedroom" in location:
                    ros_action["goal"]["pose"]["pose"]["position"]["x"] = -1.0
                    ros_action["goal"]["pose"]["pose"]["position"]["y"] = 2.0
                # Add more location mappings as needed

            return ros_action
        else:
            return {
                "action_type": "unknown",
                "goal": parsed_command.parameters
            }

# Example usage
if __name__ == "__main__":
    mapper = NaturalLanguageMapper()

    test_commands = [
        "Navigate to the kitchen",
        "Pick up the cup",
        "Place the cup on the table",
        "Follow the person",
        "Find the keys"
    ]

    for cmd in test_commands:
        parsed = mapper.parse_command(cmd)
        if parsed:
            print(f"Command: '{cmd}'")
            print(f"  -> Action: {parsed.action}")
            print(f"  -> Parameters: {parsed.parameters}")
            print(f"  -> Confidence: {parsed.confidence}")

            ros_action = mapper.generate_ros_action(parsed)
            print(f"  -> ROS Action: {json.dumps(ros_action, indent=2)}")
            print()
        else:
            print(f"Command '{cmd}' could not be parsed")
```

## Exercises
1. Implement a more sophisticated task decomposition system that can handle concurrent tasks and resource conflicts.
2. Create a feedback loop where the robot can ask for clarification when natural language commands are ambiguous.
3. Design a system that learns from execution failures to improve future task planning.

## Summary
This chapter explored LLM-driven cognitive planning for humanoid robots, focusing on translating natural language tasks into executable ROS 2 action sequences. We examined cognitive planning architectures, LLM integration patterns, task decomposition techniques, and execution monitoring systems. The hands-on examples demonstrated how to create intelligent planning systems that enable robots to understand and execute complex tasks expressed in natural language, bridging the gap between human communication and robotic action execution.

## References
 1. Achiam, J., et al. (2023). *GPT-4 Technical Report*. OpenAI.
 2. Brohan, A., et al. (2022). *RT-1: Robotics Transformer for Real-World Control at Scale*. arXiv preprint arXiv:2208.01874.
 3. Huang, W., et al. (2022). *Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents*. International Conference on Machine Learning.