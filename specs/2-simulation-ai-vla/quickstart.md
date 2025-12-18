# Quickstart: Simulation, AI-Robot Brain & VLA Modules

## Overview
This guide helps you set up and work with the Simulation, AI-Robot Brain, and Vision-Language-Action modules for the Physical AI & Humanoid Robotics textbook.

## Prerequisites
- Node.js 18+ installed
- Basic understanding of ROS 2 concepts (covered in Module 1)
- Familiarity with Docusaurus documentation framework

## Setup Process

### 1. Create Module Directories
```bash
cd website/docs
mkdir -p module-2 module-3 module-4
```

### 2. Create Chapter Files
Create the following files in their respective directories:

**Module 2 - The Digital Twin (Simulation):**
- `website/docs/module-2/gazebo-physics-simulation.md`
- `website/docs/module-2/sensors-environments.md`

**Module 3 - The AI-Robot Brain (NVIDIA Isaac):**
- `website/docs/module-3/nvidia-isaac-sim.md`
- `website/docs/module-3/isaac-ros-navigation.md`

**Module 4 - Vision-Language-Action (VLA):**
- `website/docs/module-4/voice-to-action-systems.md`
- `website/docs/module-4/llm-cognitive-planning.md`

### 3. Update Sidebar Navigation
Add the new modules and chapters to `website/sidebars.js`:

```javascript
// In the tutorialSidebar array, add:
{
  type: 'category',
  label: 'Module 2 — The Digital Twin (Simulation)',
  items: [
    'module-2/gazebo-physics-simulation',
    'module-2/sensors-environments'
  ],
},
{
  type: 'category',
  label: 'Module 3 — The AI-Robot Brain (NVIDIA Isaac)',
  items: [
    'module-3/nvidia-isaac-sim',
    'module-3/isaac-ros-navigation'
  ],
},
{
  type: 'category',
  label: 'Module 4 — Vision-Language-Action (VLA)',
  items: [
    'module-4/voice-to-action-systems',
    'module-4/llm-cognitive-planning'
  ],
},
```

### 4. Content Standards
Each chapter file must include:
- Frontmatter with title, tags, difficulty, time, and learningObjectives
- Learning Objectives section
- Introduction and Core Concepts sections
- Hands-on Lab section with practical example
- Exercises section
- Summary section
- References section with APA citations

### 5. Build and Test
```bash
cd website
npm install
npm run build
npm run start  # To test locally
```

## Chapter Template
Use this template for each chapter:

```markdown
---
title: 'Chapter Title'
tags: [tag1, tag2, tag3]
difficulty: intermediate
time: '45 minutes'
learningObjectives:
  - 'Objective 1'
  - 'Objective 2'
  - 'Objective 3'
---

# Chapter Title

## Learning Objectives
After completing this chapter, you will be able to:
- Objective 1
- Objective 2
- Objective 3

## Introduction
[Chapter introduction]

## Core Concepts
[Main theoretical content]

## Hands-on Lab
[Practical example or exercise]

## Exercises
[Practice problems]

## Summary
[Chapter summary]

## References
[APA format citations]
```

## Validation Checklist
- [ ] All chapters have proper frontmatter
- [ ] All chapters follow academic rigor standards
- [ ] All chapters have learning objectives and exercises
- [ ] All chapters include APA format references
- [ ] Sidebar navigation includes all new chapters
- [ ] Site builds without errors
- [ ] Content meets readability standards (Grade 12-14)