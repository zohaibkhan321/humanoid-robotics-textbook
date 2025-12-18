# Implementation Plan: Module 1 — The Robotic Nervous System (ROS 2)

**Feature**: 1-ros2-textbook
**Created**: 2025-12-16
**Status**: Draft
**Plan Version**: 1.0.0

## Technical Context

This plan outlines the implementation of a Docusaurus-based textbook for teaching ROS 2 concepts. The implementation will include:
- Setting up a Docusaurus project with proper configuration
- Creating 5 markdown chapters covering ROS 2 fundamentals through testing & deployment
- Configuring sidebar navigation for the textbook
- Implementing proper frontmatter, learning objectives, runnable labs, exercises, and APA references
- Creating chapter metadata files for RAG indexing
- Updating the spec-kit manifest

**Technology Stack**:
- Docusaurus v3.x (static site generator)
- Node.js 18+ (runtime environment)
- npm/yarn (package management)
- Markdown (content format)
- ROS 2 Humble Hawksbill (target ROS 2 distribution)

**Architecture**:
- Static site architecture with client-side search
- Content organized in /docs directory
- Custom sidebar configuration for textbook navigation
- Integration-ready for future RAG system

**Known Unknowns**: None (all resolved in research.md)

## Constitution Check

This implementation plan aligns with the project constitution:

✅ **Accuracy and Verifiability**: All ROS 2 concepts will be verified against official documentation and runnable code examples will be tested

✅ **Reproducibility**: All code labs will include complete setup instructions and be tested in Ubuntu CI environment

✅ **Provenance-First RAG**: Chapter metadata will support source attribution for the RAG system

✅ **Selected-Text-Only Integrity**: Implementation will support the RAG system requirements for text selection

✅ **Accessibility and Open Standards**: Docusaurus provides accessibility features and content will use CC BY-SA 4.0 license

✅ **Academic Rigor**: Content will target appropriate academic level with learning objectives and exercises

**Gates**:
- [ ] All code examples must run successfully in Ubuntu CI environment
- [ ] All chapters must include proper frontmatter and metadata
- [ ] RAG indexing requirements must be satisfied with metadata files
- [ ] Content must meet readability standards (FK grade 12-14)

## Phase 0: Outline & Research

### Research Tasks

#### Decision: Docusaurus Theme Configuration
**Rationale**: Need to determine the best Docusaurus theme configuration for textbook content
**Alternatives considered**:
- Standard docs-only theme
- Blog + docs combination
- Custom textbook theme with enhanced features
**Chosen approach**: Standard docs theme with custom sidebar for textbook navigation

#### Decision: ROS 2 Simulation Environment
**Rationale**: Need to select appropriate simulation environment for runnable labs
**Alternatives considered**:
- Gazebo Classic
- Ignition Gazebo (now called Fortress)
- Webots
- Simple unit testing without simulation
**Chosen approach**: Use basic ROS 2 tools with potential integration with Gazebo Fortress for advanced examples

#### Decision: Content Format
**Rationale**: User requested .md format instead of MDX
**Alternatives considered**:
- Keep MDX format as specified in constitution
- Use MD format as requested by user
**Chosen approach**: Use .md format as requested by user, noting this differs from constitution requirement

## Phase 1: Design & Contracts

### Data Model: Chapter Structure

**Chapter Entity**:
- `title`: string (chapter title for navigation)
- `tags`: array of strings (for categorization and search)
- `difficulty`: string (beginner/intermediate/advanced)
- `time`: string (estimated completion time)
- `learning_objectives`: array of strings (what student will learn)
- `theory`: string (core concepts explanation)
- `lab_code`: string (executable Python code example)
- `exercises`: array of strings (practice problems)
- `references`: array of objects (APA format citations)

**Chapter Metadata Entity**:
- `chapter_id`: string (unique identifier for RAG)
- `title`: string (chapter title)
- `path`: string (file path in docs structure)
- `chunk_ids`: array of strings (for RAG chunking)
- `related_chapters`: array of strings (navigation suggestions)

### API Contracts (Internal)

**Chapter Creation Interface**:
- Input: Chapter content with frontmatter
- Output: Validated chapter file at correct path
- Validation: Frontmatter completeness, content structure, reference format

**Metadata Generation Interface**:
- Input: Chapter file path
- Output: Chapter metadata JSON file
- Validation: Proper structure for RAG indexing

## Phase 2: Implementation Approach

### Task Breakdown

**Task 1: Initialize Docusaurus Project**
- Set up new Docusaurus project
- Configure basic site settings
- Install necessary dependencies
- Set up proper directory structure

**Task 2: Configure Docusaurus for Textbook**
- Customize sidebar to include all 5 chapters
- Configure navigation structure
- Set up proper URL routing
- Configure search and indexing

**Task 3: Create Chapter 1 - ROS 2 Fundamentals**
- Create markdown file with proper frontmatter
- Include learning objectives
- Add theoretical content about nodes, topics, services, actions, QoS
- Include runnable publisher/subscriber Python lab
- Add exercises and APA references
- Generate chapter metadata

**Task 4: Create Chapter 2 - rclpy Python Agents**
- Create markdown file with proper frontmatter
- Include learning objectives
- Add theoretical content about rclpy, parameters, lifecycle nodes, launch files
- Include runnable Python agent lab
- Add exercises and APA references
- Generate chapter metadata

**Task 5: Create Chapter 3 - Agent ↔ Controller Bridge**
- Create markdown file with proper frontmatter
- Include learning objectives
- Add theoretical content about ros2_control, controller manager, control loops
- Include runnable agent-controller bridge lab
- Add exercises and APA references
- Generate chapter metadata

**Task 6: Create Chapter 4 - URDF for Humanoids**
- Create markdown file with proper frontmatter
- Include learning objectives
- Add theoretical content about URDF, links, joints, sensors, XACRO
- Include simple humanoid model example
- Add exercises and APA references
- Generate chapter metadata

**Task 7: Create Chapter 5 - Testing & Deployment**
- Create markdown file with proper frontmatter
- Include learning objectives
- Add theoretical content about ROS 2 testing, CI, Docker, debugging
- Include runnable testing and deployment examples
- Add exercises and APA references
- Generate chapter metadata

**Task 8: Update Manifest and Finalize**
- Update spec-kit-manifest.json with new chapters
- Verify all chapters are properly linked
- Test site build process
- Validate RAG chunking requirements (200-400 tokens)

## Success Criteria

- [ ] Docusaurus site builds without errors
- [ ] All 5 chapters are accessible via navigation
- [ ] Each chapter includes proper frontmatter, objectives, theory, labs, exercises, and references
- [ ] All code examples run successfully in Ubuntu environment
- [ ] Chapter metadata files are generated for RAG indexing
- [ ] spec-kit-manifest.json includes all new chapters
- [ ] Content chunking meets 200-400 token requirements