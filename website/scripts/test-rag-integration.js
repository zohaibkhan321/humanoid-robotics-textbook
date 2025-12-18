#!/usr/bin/env node

/**
 * RAG System Integration Test Script
 * Tests that chapter metadata files are properly structured for RAG indexing
 */

const fs = require('fs');
const path = require('path');

// Validate a single metadata file
function validateMetadataFile(metadataPath) {
  if (!fs.existsSync(metadataPath)) {
    console.error(`Error: File does not exist: ${metadataPath}`);
    return { valid: false, errors: ['File does not exist'] };
  }

  try {
    const content = fs.readFileSync(metadataPath, 'utf8');
    const metadata = JSON.parse(content);

    const errors = [];

    // Validate required fields
    const requiredFields = ['chapter_id', 'title', 'path', 'chunk_ids'];
    for (const field of requiredFields) {
      if (metadata[field] === undefined) {
        errors.push(`Missing required field: ${field}`);
      }
    }

    // Validate field types
    if (metadata.chapter_id && typeof metadata.chapter_id !== 'string') {
      errors.push('chapter_id must be a string');
    }

    if (metadata.title && typeof metadata.title !== 'string') {
      errors.push('title must be a string');
    }

    if (metadata.path && typeof metadata.path !== 'string') {
      errors.push('path must be a string');
    }

    if (metadata.chunk_ids && !Array.isArray(metadata.chunk_ids)) {
      errors.push('chunk_ids must be an array');
    }

    if (metadata.related_chapters && !Array.isArray(metadata.related_chapters)) {
      errors.push('related_chapters must be an array');
    }

    if (metadata.word_count && typeof metadata.word_count !== 'number') {
      errors.push('word_count must be a number');
    }

    if (metadata.token_count && typeof metadata.token_count !== 'number') {
      errors.push('token_count must be a number');
    }

    if (metadata.last_indexed && typeof metadata.last_indexed !== 'string') {
      errors.push('last_indexed must be a string');
    }

    // Validate chapter_id format (should be lowercase with hyphens only)
    if (metadata.chapter_id && !/^[a-z0-9-]+$/.test(metadata.chapter_id)) {
      errors.push('chapter_id must contain only lowercase letters, numbers, and hyphens');
    }

    // Validate path format
    if (metadata.path && !metadata.path.startsWith('/')) {
      errors.push('path should start with /');
    }

    // Validate chunk_ids are properly formatted
    if (Array.isArray(metadata.chunk_ids)) {
      for (const chunkId of metadata.chunk_ids) {
        if (typeof chunkId !== 'string') {
          errors.push('All chunk_ids must be strings');
          break;
        }
        if (!/^[a-z0-9-]+$/.test(chunkId)) {
          errors.push(`Invalid chunk_id format: ${chunkId}. Must contain only lowercase letters, numbers, and hyphens`);
        }
      }
    }

    // Check if the associated chapter file exists
    if (metadata.path) {
      // Convert path like "/docs/ros2/fundamentals" to "docs/ros2/fundamentals.md"
      let chapterPath = metadata.path.substring(1) + '.md'; // Remove leading slash and add .md
      if (!fs.existsSync(chapterPath)) {
        errors.push(`Associated chapter file does not exist: ${chapterPath}`);
      }
    }

    return {
      valid: errors.length === 0,
      errors,
      metadata
    };
  } catch (error) {
    return {
      valid: false,
      errors: [`Invalid JSON: ${error.message}`]
    };
  }
}

// Test RAG integration for all metadata files
function testRAGIntegration() {
  const docsDir = './docs/ros2';
  const metadataFiles = fs.readdirSync(docsDir).filter(file =>
    file.endsWith('-metadata.json') && file !== 'chapter-metadata-schema.json' && file !== 'example-metadata.json'
  );

  console.log('RAG System Integration Test');
  console.log('===========================\n');

  let allValid = true;
  const results = [];

  for (const file of metadataFiles) {
    const metadataPath = path.join(docsDir, file);
    console.log(`Testing: ${file}`);

    const result = validateMetadataFile(metadataPath);
    results.push({ file, ...result });

    if (result.valid) {
      console.log('  ✓ Valid metadata structure');
      console.log(`  - Chapter ID: ${result.metadata.chapter_id}`);
      console.log(`  - Title: ${result.metadata.title}`);
      console.log(`  - Path: ${result.metadata.path}`);
      console.log(`  - Chunk IDs: ${result.metadata.chunk_ids.length} chunks`);
      if (result.metadata.related_chapters) {
        console.log(`  - Related chapters: ${result.metadata.related_chapters.length}`);
      }
      if (result.metadata.token_count) {
        console.log(`  - Token count: ${result.metadata.token_count}`);
      }
      if (result.metadata.word_count) {
        console.log(`  - Word count: ${result.metadata.word_count}`);
      }
    } else {
      console.log('  ✗ Invalid metadata:');
      result.errors.forEach(error => {
        console.log(`    - ${error}`);
      });
      allValid = false;
    }
    console.log('');
  }

  console.log('Summary:');
  console.log('========');
  results.forEach(result => {
    const status = result.valid ? '✓' : '✗';
    console.log(`${status} ${result.file}`);
  });

  console.log(`\nOverall: ${allValid ? 'All metadata files are properly structured for RAG integration' : 'Some metadata files have issues that need to be fixed'}`);

  return { allValid, results };
}

// Run RAG integration test
if (require.main === module) {
  testRAGIntegration();
}

module.exports = {
  validateMetadataFile,
  testRAGIntegration
};