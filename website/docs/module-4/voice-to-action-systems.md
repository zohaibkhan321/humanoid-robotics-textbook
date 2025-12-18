---
title: 'Voice-to-Action Systems'
tags: [voice-recognition, whisper, intent-parsing, ros2-actions, human-robot-interaction]
difficulty: intermediate
time: '55 minutes'
learningObjectives:
  - 'Implement voice recognition systems for robot control'
  - 'Parse natural language intents and map to ROS 2 actions'
  - 'Create voice-controlled interfaces for humanoid robots'
---

# Voice-to-Action Systems

## Learning Objectives
After completing this chapter, you will be able to:
- Set up voice recognition systems using Whisper or similar technologies
- Parse natural language intents from voice commands
- Map parsed intents to ROS 2 actions for robot control
- Create voice-controlled interfaces for humanoid robots

## Introduction
Voice-to-action systems enable natural human-robot interaction by allowing users to control robots using spoken commands. This chapter explores the implementation of voice recognition systems that convert speech to text, parse the intent from natural language, and execute corresponding ROS 2 actions. We'll focus on creating intuitive voice interfaces for humanoid robots that can understand and respond to human commands.

## Core Concepts

### Voice Recognition Pipeline
The voice-to-action pipeline consists of several stages:
1. Audio capture and preprocessing
2. Speech-to-text conversion
3. Natural language understanding
4. Intent parsing and entity extraction
5. Action mapping to ROS 2 services/actions
6. Execution and feedback

### Whisper for Speech Recognition
OpenAI's Whisper is a state-of-the-art speech recognition model that can transcribe speech to text with high accuracy. It supports multiple languages and can be fine-tuned for specific domains or accents.

### Natural Language Understanding (NLU)
NLU is the process of extracting meaning from natural language. For voice-to-action systems, this involves:
- Intent classification (what the user wants to do)
- Entity extraction (specific parameters like locations, objects, or values)
- Context awareness (understanding references based on conversation history)

### ROS 2 Actions and Services
ROS 2 provides two main mechanisms for robot control:
- **Services**: Synchronous request-response communication
- **Actions**: Asynchronous goal-oriented communication with feedback and status updates

## Hands-on Lab

### Implementing a Voice-to-Action System

1. **Voice Recognition and Intent Parsing Node**:
```python
# voice_control_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from action_msgs.msg import GoalStatus
from rclpy.action import ActionClient
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor
import openai
import json
import threading
import queue
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import pyaudio

class VoiceControlNode(Node):
    def __init__(self):
        super().__init__('voice_control_node')

        # Publishers for robot commands
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Publisher for voice feedback
        self.feedback_pub = self.create_publisher(String, '/voice_feedback', 10)

        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Initialize VOSK model (alternative to Whisper for local processing)
        # Note: You would need to download a VOSK model file
        # self.vosk_model = Model("path/to/vosk-model")
        # self.vosk_rec = KaldiRecognizer(self.vosk_model, 16000)

        # Audio stream for VOSK
        # self.audio_stream = pyaudio.PyAudio().open(
        #     format=pyaudio.paInt16,
        #     channels=1,
        #     rate=16000,
        #     input=True,
        #     frames_per_buffer=8000
        # )

        # Command queue for processing
        self.command_queue = queue.Queue()

        # Start voice recognition thread
        self.voice_thread = threading.Thread(target=self.voice_recognition_loop)
        self.voice_thread.daemon = True
        self.voice_thread.start()

        # Timer to process commands
        self.timer = self.create_timer(0.1, self.process_commands)

        self.get_logger().info('Voice Control Node initialized')

    def voice_recognition_loop(self):
        """Continuously listen for voice commands"""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        while rclpy.ok():
            try:
                self.get_logger().info("Listening for voice command...")
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=5.0, phrase_time_limit=5.0)

                # Using Google Speech Recognition (alternative to Whisper)
                try:
                    text = self.recognizer.recognize_google(audio)
                    self.get_logger().info(f"Heard: {text}")
                    self.command_queue.put(text.lower())
                except sr.UnknownValueError:
                    self.get_logger().info("Could not understand audio")
                except sr.RequestError as e:
                    self.get_logger().error(f"Could not request results; {e}")

            except sr.WaitTimeoutError:
                # Continue listening
                continue
            except Exception as e:
                self.get_logger().error(f"Error in voice recognition: {e}")

    def process_commands(self):
        """Process commands from the queue"""
        while not self.command_queue.empty():
            command = self.command_queue.get()
            self.parse_and_execute_command(command)

    def parse_and_execute_command(self, command_text):
        """Parse natural language command and execute corresponding action"""
        self.get_logger().info(f"Parsing command: {command_text}")

        # Simple intent parsing (in practice, use more sophisticated NLU)
        intent = self.classify_intent(command_text)

        if intent == "move_forward":
            self.execute_move_forward()
        elif intent == "move_backward":
            self.execute_move_backward()
        elif intent == "turn_left":
            self.execute_turn_left()
        elif intent == "turn_right":
            self.execute_turn_right()
        elif intent == "stop":
            self.execute_stop()
        elif intent == "unknown":
            self.send_feedback(f"Unknown command: {command_text}")
        else:
            self.send_feedback(f"Command not implemented: {intent}")

    def classify_intent(self, text):
        """Simple intent classification"""
        text = text.lower()

        # Movement commands
        if any(word in text for word in ["forward", "straight", "ahead", "go"]):
            return "move_forward"
        elif any(word in text for word in ["backward", "back", "reverse"]):
            return "move_backward"
        elif any(word in text for word in ["left", "turn left"]):
            return "turn_left"
        elif any(word in text for word in ["right", "turn right"]):
            return "turn_right"
        elif any(word in text for word in ["stop", "halt", "pause"]):
            return "stop"
        else:
            return "unknown"

    def execute_move_forward(self):
        """Execute forward movement command"""
        msg = Twist()
        msg.linear.x = 0.5  # Move forward at 0.5 m/s
        msg.angular.z = 0.0
        self.cmd_vel_pub.publish(msg)
        self.send_feedback("Moving forward")

    def execute_move_backward(self):
        """Execute backward movement command"""
        msg = Twist()
        msg.linear.x = -0.5  # Move backward at 0.5 m/s
        msg.angular.z = 0.0
        self.cmd_vel_pub.publish(msg)
        self.send_feedback("Moving backward")

    def execute_turn_left(self):
        """Execute left turn command"""
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.5  # Turn left at 0.5 rad/s
        self.cmd_vel_pub.publish(msg)
        self.send_feedback("Turning left")

    def execute_turn_right(self):
        """Execute right turn command"""
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = -0.5  # Turn right at 0.5 rad/s
        self.cmd_vel_pub.publish(msg)
        self.send_feedback("Turning right")

    def execute_stop(self):
        """Execute stop command"""
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.cmd_vel_pub.publish(msg)
        self.send_feedback("Stopping")

    def send_feedback(self, message):
        """Send feedback to user"""
        feedback_msg = String()
        feedback_msg.data = message
        self.feedback_pub.publish(feedback_msg)
        self.get_logger().info(f"Feedback: {message}")


def main(args=None):
    rclpy.init(args=args)
    voice_control_node = VoiceControlNode()

    try:
        # Use multi-threaded executor to handle both timer and voice recognition
        executor = MultiThreadedExecutor()
        executor.add_node(voice_control_node)
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        voice_control_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

2. **Advanced Intent Parser with Entity Extraction**:
```python
# intent_parser.py
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class IntentResult:
    intent: str
    entities: Dict[str, str]
    confidence: float

class AdvancedIntentParser:
    """Advanced intent parser with entity extraction"""

    def __init__(self):
        # Define patterns for different intents
        self.patterns = {
            "move_to_location": [
                r"move to the (\w+)",
                r"go to the (\w+)",
                r"navigate to the (\w+)",
                r"walk to the (\w+)"
            ],
            "pick_up_object": [
                r"pick up the (\w+)",
                r"grab the (\w+)",
                r"take the (\w+)",
                r"get the (\w+)"
            ],
            "follow_person": [
                r"follow the (\w+)",
                r"follow (\w+)",
                r"go after the (\w+)"
            ],
            "wait_for": [
                r"wait for (\w+)",
                r"wait until (\w+)",
                r"stop until (\w+)"
            ]
        }

        # Location entities
        self.locations = {
            "kitchen", "living room", "bedroom", "bathroom", "office",
            "dining room", "hallway", "garage", "garden", "entrance"
        }

        # Object entities
        self.objects = {
            "cup", "book", "phone", "keys", "bottle", "plate",
            "fork", "spoon", "bowl", "toy", "remote", "newspaper"
        }

        # Person entities
        self.people = {
            "person", "man", "woman", "child", "adult", "elderly",
            "john", "mary", "sarah", "tom", "anna", "mike"
        }

    def parse(self, text: str) -> Optional[IntentResult]:
        """Parse text and extract intent and entities"""
        text = text.lower().strip()

        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    # Extract the entity
                    entity = match.group(1)

                    # Validate entity based on intent type
                    if intent == "move_to_location" and entity in self.locations:
                        return IntentResult(
                            intent=intent,
                            entities={"location": entity},
                            confidence=0.9
                        )
                    elif intent == "pick_up_object" and entity in self.objects:
                        return IntentResult(
                            intent=intent,
                            entities={"object": entity},
                            confidence=0.9
                        )
                    elif intent == "follow_person" and (entity in self.people or entity in self.locations):
                        return IntentResult(
                            intent=intent,
                            entities={"target": entity},
                            confidence=0.9
                        )
                    elif intent == "wait_for" and entity in self.people:
                        return IntentResult(
                            intent=intent,
                            entities={"target": entity},
                            confidence=0.9
                        )

        # If no specific intent matched, try general movement commands
        movement_intents = self.parse_movement_commands(text)
        if movement_intents:
            return movement_intents

        return None

    def parse_movement_commands(self, text: str) -> Optional[IntentResult]:
        """Parse simple movement commands"""
        movement_patterns = {
            "move_forward": [r"go forward", r"move forward", r"go straight", r"move straight", r"go ahead"],
            "move_backward": [r"go backward", r"move backward", r"go back", r"move back"],
            "turn_left": [r"turn left", r"turn to the left", r"rotate left"],
            "turn_right": [r"turn right", r"turn to the right", r"rotate right"],
            "stop": [r"stop", r"halt", r"pause", r"stand still"]
        }

        for intent, patterns in movement_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return IntentResult(
                        intent=intent,
                        entities={},
                        confidence=0.8
                    )

        return None

# Example usage
if __name__ == "__main__":
    parser = AdvancedIntentParser()

    test_commands = [
        "move to the kitchen",
        "pick up the cup",
        "follow the person",
        "wait for mary",
        "go forward",
        "turn left"
    ]

    for cmd in test_commands:
        result = parser.parse(cmd)
        if result:
            print(f"Command: '{cmd}' -> Intent: {result.intent}, Entities: {result.entities}")
        else:
            print(f"Command: '{cmd}' -> Unknown")
```

3. **ROS 2 Action Client for Voice-Controlled Navigation**:
```python
# voice_navigation_action_client.py
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose

class VoiceNavigationActionClient(Node):
    def __init__(self):
        super().__init__('voice_navigation_action_client')
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def send_goal(self, x, y, theta=0.0):
        """Send navigation goal to Nav2"""
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.position.z = 0.0

        # Convert theta to quaternion (simplified)
        import math
        goal_msg.pose.pose.orientation.z = math.sin(theta / 2.0)
        goal_msg.pose.pose.orientation.w = math.cos(theta / 2.0)

        self.get_logger().info(f'Waiting for action server...')
        self._action_client.wait_for_server()

        self.get_logger().info(f'Sending navigation goal to ({x}, {y})')
        send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result}')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Received feedback: {feedback}')
```

## Exercises
1. Implement a more sophisticated intent parser using machine learning techniques or NLP libraries like spaCy or NLTK.
2. Create a voice command system that can handle complex multi-step instructions (e.g., "Go to the kitchen and pick up the red cup").
3. Design a voice feedback system that can provide natural language responses to the user about the robot's status.

## Summary
This chapter covered the implementation of voice-to-action systems for humanoid robots, focusing on converting speech to text, parsing natural language intents, and mapping those intents to ROS 2 actions. We explored the voice recognition pipeline, natural language understanding concepts, and practical implementations of voice-controlled robot interfaces. The hands-on examples demonstrated how to create responsive voice control systems that enable natural human-robot interaction.

## References
1. Radford, A., et al. (2022). *Robust Speech Recognition via Large-Scale Weak Supervision*. arXiv preprint arXiv:2212.04356.
2. ROS Navigation. (2023). *Navigation2 (Nav2) Action Interface*. https://navigation.ros.org/
3. Chen, G., et al. (2020). *Voice-controlled robotics: A survey*. IEEE Transactions on Human-Machine Systems, 50(6), 457-468.