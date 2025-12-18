# Content API Contracts: Simulation, AI-Robot Brain & VLA Modules

## Chapter Content API

### Get Chapter Content
```
GET /api/chapters/{chapterId}
```

**Description**: Retrieve the content of a specific chapter

**Path Parameters**:
- `chapterId`: string - The unique identifier for the chapter (e.g., "module-2/gazebo-physics-simulation")

**Response**:
```json
{
  "id": "module-2/gazebo-physics-simulation",
  "title": "Gazebo Physics Simulation",
  "content": "# Chapter Title\n\n## Learning Objectives\n...",
  "metadata": {
    "tags": ["gazebo", "physics", "simulation", "humanoid"],
    "difficulty": "intermediate",
    "time": "45 minutes",
    "learningObjectives": [
      "Understand gravity configuration in Gazebo",
      "Configure collision properties for humanoid models",
      "Set up joint constraints and world files"
    ]
  },
  "references": [
    {
      "id": "gazebo-docs-2023",
      "title": "Gazebo Classic Documentation",
      "authors": ["Open Robotics"],
      "year": 2023,
      "url": "https://classic.gazebosim.org/tutorials",
      "apa_citation": "Open Robotics. (2023). Gazebo Classic Documentation. https://classic.gazebosim.org/tutorials"
    }
  ]
}
```

**Success Response**:
- Code: `200 OK`
- Content: Chapter content with metadata

**Error Responses**:
- Code: `404 Not Found` - Chapter does not exist
- Code: `500 Internal Server Error` - Server error retrieving content

### Search Chapters
```
GET /api/chapters/search?q={query}&module={module}
```

**Description**: Search for chapters based on query and/or module

**Query Parameters**:
- `q`: string (optional) - Search query term
- `module`: string (optional) - Module filter (module-2, module-3, module-4)

**Response**:
```json
{
  "results": [
    {
      "id": "module-2/gazebo-physics-simulation",
      "title": "Gazebo Physics Simulation",
      "module": "module-2",
      "difficulty": "intermediate",
      "tags": ["gazebo", "physics", "simulation"]
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10
}
```

## Module Navigation API

### Get Module Structure
```
GET /api/modules/{moduleId}
```

**Description**: Retrieve the structure and contents of a specific module

**Path Parameters**:
- `moduleId`: string - The module identifier (module-2, module-3, or module-4)

**Response**:
```json
{
  "id": "module-2",
  "title": "The Digital Twin (Simulation)",
  "description": "Physics simulation using Gazebo",
  "chapters": [
    {
      "id": "module-2/gazebo-physics-simulation",
      "title": "Gazebo Physics Simulation",
      "path": "/docs/module-2/gazebo-physics-simulation"
    },
    {
      "id": "module-2/sensors-environments",
      "title": "Sensors & Environments",
      "path": "/docs/module-2/sensors-environments"
    }
  ],
  "prerequisites": ["ros2-fundamentals"]
}
```

## Validation Rules

### Content Validation
- Chapter titles must be 5-100 characters
- Tags array must contain 3-8 tags
- Difficulty must be one of: "beginner", "intermediate", "advanced"
- Learning objectives array must contain 2-5 items
- Time must be in format: "X minutes" where X is 15-120

### Search Validation
- Query string must be 2-50 characters
- Module parameter must be one of: "module-2", "module-3", "module-4"
- Page number must be >= 1
- Limit must be between 1-50