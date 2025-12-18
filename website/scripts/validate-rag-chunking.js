#!/usr/bin/env node

/**
 * RAG Chunking Validation Script
 * Validates that chapters meet the 200-400 token requirement for RAG indexing
 */

const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

// Calculate approximate token count (1 token ≈ 4 characters for English text)
function calculateTokenCount(text) {
  // Simple estimation: divide character count by 4
  // This is a rough approximation - real tokenizers may vary
  return Math.floor(text.length / 4);
}

// Split content into semantic chunks that meet token requirements
function splitIntoChunks(content, maxTokens = 400, minTokens = 200) {
  const chunks = [];
  const lines = content.split('\n');
  let currentChunk = '';
  let currentTokenCount = 0;

  for (const line of lines) {
    const lineTokenCount = calculateTokenCount(line);

    // If adding this line would exceed max tokens, and we have enough tokens for a valid chunk
    if (currentTokenCount + lineTokenCount > maxTokens && currentTokenCount >= minTokens) {
      chunks.push(currentChunk.trim());
      currentChunk = line + '\n';
      currentTokenCount = lineTokenCount;
    } else {
      // Add line to current chunk
      currentChunk += line + '\n';
      currentTokenCount += lineTokenCount;

      // If current chunk is getting too large but hasn't reached minimum yet,
      // we'll break it anyway to avoid infinite loops
      if (currentTokenCount > maxTokens && currentTokenCount < minTokens) {
        chunks.push(currentChunk.trim());
        currentChunk = '';
        currentTokenCount = 0;
      }
    }
  }

  // Add the last chunk if it has content
  if (currentChunk.trim()) {
    chunks.push(currentChunk.trim());
  }

  return chunks;
}

// Validate a single chapter file
function validateChapter(chapterPath) {
  if (!fs.existsSync(chapterPath)) {
    console.error(`Error: File does not exist: ${chapterPath}`);
    return false;
  }

  const fileContent = fs.readFileSync(chapterPath, 'utf8');
  const parsed = matter(fileContent);
  const bodyContent = parsed.content;

  // Calculate token count for the entire chapter
  const totalTokenCount = calculateTokenCount(bodyContent);
  const totalWordCount = bodyContent.split(/\s+/).filter(word => word.length > 0).length;

  console.log(`Chapter: ${path.basename(chapterPath)}`);
  console.log(`  Total words: ${totalWordCount}`);
  console.log(`  Estimated tokens: ${totalTokenCount}`);
  console.log(`  RAG requirement: 200-400 tokens per chunk`);

  // Check if chapter meets RAG chunking requirements
  if (totalTokenCount <= 400) {
    console.log(`  ✓ Chapter meets RAG chunking requirements (single chunk)`);
    return { valid: true, totalTokens: totalTokenCount, chunks: 1 };
  } else {
    console.log(`  ✗ Chapter exceeds RAG chunking requirements`);
    console.log(`  - Current size: ${totalTokenCount} tokens`);
    console.log(`  - Needs to be split into smaller chunks`);

    // Show how it could be split
    const chunks = splitIntoChunks(bodyContent);
    console.log(`  - Could be split into ${chunks.length} chunks:`);
    chunks.forEach((chunk, index) => {
      const chunkTokens = calculateTokenCount(chunk);
      console.log(`    Chunk ${index + 1}: ~${chunkTokens} tokens`);
    });

    return { valid: false, totalTokens: totalTokenCount, chunks: chunks.length, suggestedChunks: chunks };
  }
}

// Validate all ROS 2 chapters
function validateAllChapters() {
  const docsDir = './docs/ros2';
  const chapterFiles = fs.readdirSync(docsDir).filter(file =>
    file.endsWith('.md') && !file.startsWith('_') && file !== 'tags-taxonomy.md' && file !== 'content-guidelines.md'
  );

  console.log('RAG Chunking Validation for ROS 2 Textbook');
  console.log('==========================================\n');

  let allValid = true;
  const results = [];

  for (const file of chapterFiles) {
    const chapterPath = path.join(docsDir, file);
    const result = validateChapter(chapterPath);
    results.push({ file, ...result });
    if (!result.valid) {
      allValid = false;
    }
    console.log('');
  }

  console.log('Summary:');
  console.log('========');
  results.forEach(result => {
    const status = result.valid ? '✓' : '✗';
    console.log(`${status} ${result.file}: ${result.totalTokens} tokens (${result.chunks} chunk${result.chunks > 1 ? 's' : ''})`);
  });

  console.log(`\nOverall: ${allValid ? 'All chapters meet RAG chunking requirements' : 'Some chapters need to be restructured for RAG chunking'}`);

  return { allValid, results };
}

// Run validation
if (require.main === module) {
  validateAllChapters();
}

module.exports = { calculateTokenCount, splitIntoChunks, validateChapter, validateAllChapters };