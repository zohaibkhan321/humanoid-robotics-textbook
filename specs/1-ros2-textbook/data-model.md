# Data Model: Module 1 — The Robotic Nervous System (ROS 2)

**Feature**: 1-ros2-textbook
**Created**: 2025-12-16

## Chapter Entity

**Definition**: Educational content unit with learning objectives, theory, labs, exercises, and references

**Fields**:
- `id`: string (unique identifier for the chapter)
- `title`: string (chapter title for navigation and display)
- `path`: string (URL path in the documentation site)
- `tags`: array of strings (for categorization and search functionality)
- `difficulty`: string (enum: beginner, intermediate, advanced)
- `time`: string (estimated completion time in minutes)
- `learningObjectives`: array of strings (specific learning outcomes)
- `theory`: string (core concepts and explanations)
- `lab_code`: string (executable Python code example)
- `exercises`: array of strings (practice problems with solutions)
- `references`: array of reference objects (APA format citations)
- `createdAt`: datetime (creation timestamp)
- `updatedAt`: datetime (last modification timestamp)

**Validation Rules**:
- Title must be 5-100 characters
- Difficulty must be one of the allowed values
- Learning objectives must be an array of 2-5 items
- References must follow APA format

## Reference Entity

**Definition**: Academic citation in APA format

**Fields**:
- `id`: string (unique identifier)
- `author`: string (author name)
- `year`: number (publication year)
- `title`: string (publication title)
- `source`: string (journal, book, or website)
- `url`: string (optional URL)
- `type`: string (enum: book, journal, website, documentation)

**Validation Rules**:
- All fields except URL are required
- Year must be a valid year (1900-2030)
- Type must be one of the allowed values

## Chapter Metadata Entity

**Definition**: Metadata for RAG indexing and content management

**Fields**:
- `chapter_id`: string (reference to the chapter)
- `title`: string (chapter title)
- `path`: string (file path in docs structure)
- `chunk_ids`: array of strings (IDs for RAG chunking)
- `related_chapters`: array of strings (navigation suggestions)
- `word_count`: number (total word count for reading time estimation)
- `token_count`: number (total token count for RAG processing)
- `last_indexed`: datetime (timestamp of last RAG indexing)

**Validation Rules**:
- Chapter_id must reference an existing chapter
- Chunk_ids must be an array of valid IDs
- Word count and token count must be positive numbers

## Lab Exercise Entity

**Definition**: Practical coding exercise within a chapter

**Fields**:
- `id`: string (unique identifier)
- `chapter_id`: string (reference to parent chapter)
- `title`: string (exercise title)
- `description`: string (detailed exercise description)
- `difficulty`: string (enum: beginner, intermediate, advanced)
- `prerequisites`: array of strings (required knowledge/skills)
- `steps`: array of step objects (detailed implementation steps)
- `expected_output`: string (what the solution should produce)
- `solution`: string (optional reference solution)

**Validation Rules**:
- All fields except solution are required
- Difficulty must be one of the allowed values
- Steps must be an array of at least one item

## Step Entity (nested in Lab Exercise)

**Fields**:
- `step_number`: number (sequential step number)
- `description`: string (what to do in this step)
- `code`: string (code to implement or modify)
- `explanation`: string (why this step is important)

**Validation Rules**:
- Step number must be positive
- Description is required