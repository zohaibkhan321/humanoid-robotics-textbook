#!/usr/bin/env node

/**
 * Chapter Validation Script
 * Validates ROS 2 textbook chapter structure and content
 */

const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

// Check if a file path is provided
if (process.argv.length < 3) {
  console.error('Usage: node validate-chapter.js <chapter-file.md>');
  process.exit(1);
}

const chapterPath = process.argv[2];

// Check if file exists
if (!fs.existsSync(chapterPath)) {
  console.error(`Error: File does not exist: ${chapterPath}`);
  process.exit(1);
}

// Read and parse the chapter file
const fileContent = fs.readFileSync(chapterPath, 'utf8');
const parsed = matter(fileContent);

// Validation checks
const errors = [];

// Check frontmatter exists
if (!parsed.data) {
  errors.push('Missing frontmatter in chapter file');
} else {
  // Check required frontmatter fields
  const requiredFields = ['title', 'tags', 'difficulty', 'time', 'learningObjectives'];
  for (const field of requiredFields) {
    if (!parsed.data[field]) {
      errors.push(`Missing required frontmatter field: ${field}`);
    }
  }

  // Check learningObjectives is an array with at least 2 items
  if (parsed.data.learningObjectives &&
      (!Array.isArray(parsed.data.learningObjectives) || parsed.data.learningObjectives.length < 2)) {
    errors.push('learningObjectives must be an array with at least 2 items');
  }

  // Check difficulty is valid
  const validDifficulties = ['beginner', 'intermediate', 'advanced'];
  if (parsed.data.difficulty && !validDifficulties.includes(parsed.data.difficulty)) {
    errors.push(`difficulty must be one of: ${validDifficulties.join(', ')}`);
  }

  // Check tags is an array
  if (parsed.data.tags && !Array.isArray(parsed.data.tags)) {
    errors.push('tags must be an array');
  }
}

// Check for required sections in content
const requiredSections = ['Learning Objectives', 'Core Concepts', 'Summary', 'References'];
for (const section of requiredSections) {
  if (!fileContent.includes(`## ${section}`)) {
    errors.push(`Missing required section: ${section}`);
  }
}

// Check for hands-on lab section
if (!fileContent.includes('## Hands-on Lab')) {
  errors.push('Missing required section: Hands-on Lab');
}

// Check for exercises section
if (!fileContent.includes('## Exercises')) {
  errors.push('Missing required section: Exercises');
}

// Output results
if (errors.length > 0) {
  console.error('Validation failed with the following errors:');
  errors.forEach((error, index) => {
    console.error(`  ${index + 1}. ${error}`);
  });
  process.exit(1);
} else {
  console.log('✓ Chapter validation passed successfully!');
  process.exit(0);
}