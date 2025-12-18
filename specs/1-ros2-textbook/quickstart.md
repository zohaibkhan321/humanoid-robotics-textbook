# Quickstart Guide: ROS 2 Textbook Development

**Feature**: 1-ros2-textbook
**Created**: 2025-12-16

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Git for version control
- Basic knowledge of ROS 2 concepts
- Python 3.8+ for ROS 2 examples

## Setup Docusaurus Project

1. **Initialize the project:**
   ```bash
   npx create-docusaurus@latest website classic
   cd website
   ```

2. **Install additional dependencies:**
   ```bash
   npm install @docusaurus/module-type-aliases @docusaurus/types
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

## Create Textbook Structure

1. **Create the docs directory structure:**
   ```bash
   mkdir -p docs/ros2
   ```

2. **Create the 5 chapters in the docs/ros2/ directory:**
   - `01-fundamentals.md` - ROS 2 Fundamentals
   - `02-rclpy-agents.md` - rclpy Python Agents
   - `03-agent-controller-bridge.md` - Agent ↔ Controller Bridge
   - `04-urdf-humanoids.md` - URDF for Humanoids
   - `05-testing-deployment.md` - Testing & Deployment

## Chapter Template

Use this template for each chapter:

```markdown
---
title: 'Chapter Title'
tags: [tag1, tag2, tag3]
difficulty: 'intermediate'
time: '45 minutes'
learningObjectives:
  - 'Understand key concept 1'
  - 'Implement technique 2'
  - 'Apply method 3'
---

# Chapter Title

## Learning Objectives

After completing this chapter, you will be able to:
- Objective 1
- Objective 2
- Objective 3

## Introduction

Brief introduction to the chapter topic and its importance in ROS 2.

## Core Concepts

Detailed explanation of the main concepts covered in this chapter.

## Hands-on Lab

### Setup
Instructions to set up the environment for the lab.

### Implementation
Step-by-step implementation guide with code examples:

```python
# Python code example
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        # Implementation here
```

### Testing
Instructions to test the implementation.

## Exercises

1. **Exercise 1**: Description of the first exercise
2. **Exercise 2**: Description of the second exercise

## Summary

Recap of key points covered in the chapter.

## References

1. Author, A. A. (Year). *Title of work*. Publisher.
2. Author, B. B. (Year). Title of article. *Title of Periodical*, volume(issue), pages. URL
```

## Configure Sidebar

Update `sidebars.js` to include your textbook chapters:

```javascript
module.exports = {
  docs: [
    {
      type: 'category',
      label: 'ROS 2 Textbook',
      items: [
        'ros2/fundamentals',
        'ros2/rclpy-agents',
        'ros2/agent-controller-bridge',
        'ros2/urdf-humanoids',
        'ros2/testing-deployment',
      ],
    },
  ],
};
```

## Create Chapter Metadata

For each chapter, create a corresponding metadata file:

`docs/ros2/fundamentals-metadata.json`:
```json
{
  "chapter_id": "ros2-fundamentals",
  "title": "ROS 2 Fundamentals",
  "path": "/docs/ros2/fundamentals",
  "chunk_ids": ["fundamentals-001", "fundamentals-002"],
  "related_chapters": ["rclpy-agents", "agent-controller-bridge"],
  "word_count": 1200,
  "token_count": 950
}
```

## Build and Test

1. **Build the site:**
   ```bash
   npm run build
   ```

2. **Serve the built site:**
   ```bash
   npm run serve
   ```

## Validate Requirements

1. Check that all code examples run in Ubuntu environment
2. Verify all chapters have proper frontmatter
3. Confirm metadata files exist for RAG indexing
4. Test that navigation works correctly
5. Validate that content meets academic rigor standards