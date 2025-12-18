# Data Model: Simulation, AI-Robot Brain & VLA Modules

## Chapter Entity

**Chapter**:
- `title`: string (chapter title for navigation)
- `tags`: array of strings (for categorization and search)
- `difficulty`: string (beginner/intermediate/advanced)
- `time`: string (estimated completion time)
- `learning_objectives`: array of strings (what student will learn)
- `theory`: string (core concepts explanation)
- `practical_example`: string (executable example or configuration)
- `exercises`: array of strings (practice problems)
- `references`: array of objects (APA format citations)

## Module Entity

**Module**:
- `id`: string (unique identifier for the module: module-2, module-3, module-4)
- `title`: string (module title)
- `description`: string (brief description of the module)
- `chapters`: array of Chapter entities (the chapters included in this module)
- `prerequisites`: array of strings (knowledge required before starting this module)

## Learning Objective Entity

**LearningObjective**:
- `id`: string (unique identifier)
- `text`: string (the specific learning objective)
- `module_id`: string (which module this objective belongs to)
- `chapter_id`: string (which chapter this objective belongs to)
- `difficulty_level`: string (beginner/intermediate/advanced)

## Reference Entity

**Reference**:
- `id`: string (unique identifier)
- `type`: string (book, journal, website, documentation)
- `title`: string (title of the reference)
- `authors`: array of strings (authors of the reference)
- `year`: number (publication year)
- `url`: string (URL if applicable)
- `apa_citation`: string (proper APA format citation)
- `used_in`: array of strings (chapters where this reference is used)

## Navigation Entity

**NavigationItem**:
- `id`: string (unique identifier)
- `label`: string (display name in navigation)
- `type`: string (category or doc)
- `items`: array of NavigationItem or string (path to doc)
- `module_id`: string (which module this navigation item belongs to)

## Validation Rules

- Chapter titles must be unique across all modules
- Learning objectives must be specific, measurable, and achievable
- References must follow APA format standards
- Difficulty levels must be consistent with content complexity
- Time estimates must be realistic based on content length and complexity
- Tags must be from the predefined taxonomy to ensure searchability

## Relationships

- Module contains multiple Chapters
- Chapter contains multiple LearningObjectives
- Chapter contains multiple References
- NavigationItem links to multiple Chapters