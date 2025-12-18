#!/usr/bin/env node

/**
 * Proofreading and Consistency Check Script
 * Checks for consistency across all textbook chapters
 */

const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

// Check if a chapter has all required sections
function checkRequiredSections(content) {
  const requiredSections = [
    'Learning Objectives',
    'Introduction',
    'Core Concepts',
    'Hands-on Lab',
    'Exercises',
    'Summary',
    'References'
  ];

  const missingSections = [];
  for (const section of requiredSections) {
    if (!content.includes(`## ${section}`) && !content.includes(`### ${section}`)) {
      missingSections.push(section);
    }
  }

  return missingSections;
}

// Check if a chapter follows the required frontmatter structure
function checkFrontmatterConsistency(frontmatter) {
  const errors = [];

  // Check required fields
  const requiredFields = ['title', 'tags', 'difficulty', 'time', 'learningObjectives'];
  for (const field of requiredFields) {
    if (!frontmatter[field]) {
      errors.push(`Missing required frontmatter field: ${field}`);
    }
  }

  // Check learningObjectives is an array with at least 2 items
  if (frontmatter.learningObjectives) {
    if (!Array.isArray(frontmatter.learningObjectives) || frontmatter.learningObjectives.length < 2) {
      errors.push('learningObjectives must be an array with at least 2 items');
    }
  }

  // Check difficulty is valid
  const validDifficulties = ['beginner', 'intermediate', 'advanced'];
  if (frontmatter.difficulty && !validDifficulties.includes(frontmatter.difficulty)) {
    errors.push(`difficulty must be one of: ${validDifficulties.join(', ')}`);
  }

  // Check tags is an array
  if (frontmatter.tags && !Array.isArray(frontmatter.tags)) {
    errors.push('tags must be an array');
  }

  // Check time format
  if (frontmatter.time && typeof frontmatter.time !== 'string') {
    errors.push('time must be a string');
  }

  return errors;
}

// Check for common writing issues
function checkWritingIssues(content) {
  const issues = [];

  // Check for placeholder text
  const placeholderRegex = /\[.*?\]|\{\{.*?\}\}|NEEDS CLARIFICATION|TBD|TODO/gi;
  const placeholders = content.match(placeholderRegex);
  if (placeholders) {
    issues.push(`Found placeholder text: ${placeholders.join(', ')}`);
  }

  // Check for broken links
  const brokenLinkRegex = /\[([^\]]+)\]\(\)/g;
  const brokenLinks = content.match(brokenLinkRegex);
  if (brokenLinks) {
    issues.push(`Found broken links: ${brokenLinks.join(', ')}`);
  }

  // Check for double spaces
  const doubleSpaceRegex = / {2,}/g;
  const doubleSpaces = content.match(doubleSpaceRegex);
  if (doubleSpaces && doubleSpaces.length > 5) { // Only report if there are many
    issues.push(`Found multiple instances of double/triple spaces`);
  }

  // Check for missing alt text in images
  const imgWithoutAlt = /!\[\s*\](\(.+\)|\s+("|').+("|'))/g;
  const imagesWithoutAlt = content.match(imgWithoutAlt);
  if (imagesWithoutAlt) {
    issues.push(`Found images without alt text: ${imagesWithoutAlt.length} instances`);
  }

  return issues;
}

// Analyze a single chapter
function analyzeChapter(chapterPath) {
  if (!fs.existsSync(chapterPath)) {
    console.error(`Error: File does not exist: ${chapterPath}`);
    return null;
  }

  const fileContent = fs.readFileSync(chapterPath, 'utf8');
  const parsed = matter(fileContent);

  const frontmatterErrors = checkFrontmatterConsistency(parsed.data);
  const missingSections = checkRequiredSections(parsed.content);
  const writingIssues = checkWritingIssues(parsed.content);

  const fileName = path.basename(chapterPath);

  console.log(`Analyzing: ${fileName}`);
  console.log(`  Frontmatter: ${frontmatterErrors.length === 0 ? '✓ Valid' : `✗ ${frontmatterErrors.length} errors`}`);
  if (frontmatterErrors.length > 0) {
    frontmatterErrors.forEach(error => console.log(`    - ${error}`));
  }

  console.log(`  Required sections: ${missingSections.length === 0 ? '✓ All present' : `✗ Missing ${missingSections.length}`}`);
  if (missingSections.length > 0) {
    missingSections.forEach(section => console.log(`    - Missing: ${section}`));
  }

  console.log(`  Writing issues: ${writingIssues.length === 0 ? '✓ None found' : `✗ ${writingIssues.length} issues`}`);
  if (writingIssues.length > 0) {
    writingIssues.forEach(issue => console.log(`    - ${issue}`));
  }

  const hasIssues = frontmatterErrors.length > 0 || missingSections.length > 0 || writingIssues.length > 0;
  console.log(`  Status: ${hasIssues ? '✗ Needs review' : '✓ Good'}`);
  console.log('');

  return {
    fileName,
    hasIssues,
    frontmatterErrors,
    missingSections,
    writingIssues
  };
}

// Run consistency check across all chapters
function runConsistencyCheck() {
  const docsDir = './docs/ros2';
  const chapterFiles = fs.readdirSync(docsDir).filter(file =>
    file.endsWith('.md') && !file.startsWith('_') && file !== 'tags-taxonomy.md' && file !== 'content-guidelines.md'
  );

  console.log('Proofreading and Consistency Check for ROS 2 Textbook');
  console.log('====================================================\n');

  const results = [];

  for (const file of chapterFiles) {
    const chapterPath = path.join(docsDir, file);
    const result = analyzeChapter(chapterPath);
    if (result) {
      results.push(result);
    }
  }

  console.log('Summary:');
  console.log('========');
  results.forEach(result => {
    const status = result.hasIssues ? '✗' : '✓';
    const totalIssues = result.frontmatterErrors.length + result.missingSections.length + result.writingIssues.length;
    console.log(`${status} ${result.fileName}: ${totalIssues} total issues`);
  });

  const issuesCount = results.reduce((sum, r) => sum + (r.frontmatterErrors.length + r.missingSections.length + r.writingIssues.length), 0);
  const chaptersWithIssues = results.filter(r => r.hasIssues).length;

  console.log(`\nOverall: ${chaptersWithIssues}/${results.length} chapters have issues (${issuesCount} total issues found)`);

  return { results, issuesCount, chaptersWithIssues };
}

// Run consistency check
if (require.main === module) {
  runConsistencyCheck();
}

module.exports = {
  checkRequiredSections,
  checkFrontmatterConsistency,
  checkWritingIssues,
  analyzeChapter,
  runConsistencyCheck
};