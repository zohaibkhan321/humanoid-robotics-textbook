#!/usr/bin/env node

/**
 * Readability Analysis Script
 * Analyzes the readability of textbook chapters using the Flesch-Kincaid Grade Level formula
 */

const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

// Count sentences in text
function countSentences(text) {
  // Count sentence-ending punctuation marks
  const sentences = text.match(/[.!?]+/g);
  return sentences ? sentences.length : 0;
}

// Count words in text
function countWords(text) {
  // Split on whitespace and remove empty strings
  const words = text.split(/\s+/).filter(word => word.length > 0);
  return words.length;
}

// Count syllables in a word
function countSyllables(word) {
  // Convert to lowercase and remove non-alphabetic characters
  word = word.toLowerCase().replace(/[^a-z]/g, '');

  if (word.length <= 3) return 1;

  // Count vowel groups as syllables
  const vowels = word.match(/[aeiouy]+/g);
  let count = vowels ? vowels.length : 0;

  // Subtract 1 for silent 'e' at the end
  if (word.endsWith('e')) {
    count--;
  }

  // Every word has at least one syllable
  return Math.max(1, count);
}

// Count total syllables in text
function countTotalSyllables(text) {
  const words = text.split(/\s+/).filter(word => word.length > 0);
  return words.reduce((total, word) => total + countSyllables(word), 0);
}

// Calculate Flesch-Kincaid Grade Level
function calculateFleschKincaidGradeLevel(text) {
  const sentences = countSentences(text);
  const words = countWords(text);
  const syllables = countTotalSyllables(text);

  if (sentences === 0 || words === 0) return 0;

  // Flesch-Kincaid Grade Level formula:
  // 0.39 * (total words / total sentences) + 11.8 * (total syllables / total words) - 15.59
  const avgWordsPerSentence = words / sentences;
  const avgSyllablesPerWord = syllables / words;

  const gradeLevel = (0.39 * avgWordsPerSentence) + (11.8 * avgSyllablesPerWord) - 15.59;

  return Math.max(0, gradeLevel); // Don't return negative values
}

// Clean content by removing code blocks, frontmatter, and non-text elements
function cleanContent(content) {
  // Remove frontmatter
  let cleaned = content.replace(/^---\n[\s\S]*?\n---\n/, '');

  // Remove code blocks (```...```)
  cleaned = cleaned.replace(/```[\s\S]*?```/g, '');

  // Remove inline code (`...`)
  cleaned = cleaned.replace(/`[^`]*`/g, '');

  // Remove markdown links [text](url) but keep the text
  cleaned = cleaned.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');

  // Remove markdown headers, bold, italic formatting
  cleaned = cleaned.replace(/^[#\s]+|[*_]{1,3}|[*_]{1,3}/gm, '');

  return cleaned;
}

// Analyze readability of a single chapter
function analyzeChapterReadability(chapterPath) {
  if (!fs.existsSync(chapterPath)) {
    console.error(`Error: File does not exist: ${chapterPath}`);
    return null;
  }

  const fileContent = fs.readFileSync(chapterPath, 'utf8');
  const parsed = matter(fileContent);
  const bodyContent = parsed.content;

  // Clean content to get just the text
  const cleanedContent = cleanContent(bodyContent);

  // Calculate readability metrics
  const sentences = countSentences(cleanedContent);
  const words = countWords(cleanedContent);
  const syllables = countTotalSyllables(cleanedContent);
  const gradeLevel = calculateFleschKincaidGradeLevel(cleanedContent);

  console.log(`Analyzing readability of: ${path.basename(chapterPath)}`);
  console.log(`  Words: ${words}`);
  console.log(`  Sentences: ${sentences}`);
  console.log(`  Syllables: ${syllables}`);
  console.log(`  Flesch-Kincaid Grade Level: ${gradeLevel.toFixed(2)}`);

  const meetsRequirement = gradeLevel >= 12 && gradeLevel <= 14;
  console.log(`  Target: Grade 12-14 | Status: ${meetsRequirement ? '✓ Meets requirement' : '✗ Does not meet requirement'}`);
  console.log('');

  return {
    fileName: path.basename(chapterPath),
    wordCount: words,
    sentenceCount: sentences,
    syllableCount: syllables,
    gradeLevel: gradeLevel,
    meetsTarget: meetsRequirement
  };
}

// Analyze readability of all ROS 2 chapters
function analyzeAllChapters() {
  const docsDir = './docs/ros2';
  const chapterFiles = fs.readdirSync(docsDir).filter(file =>
    file.endsWith('.md') && !file.startsWith('_') && file !== 'tags-taxonomy.md' && file !== 'content-guidelines.md'
  );

  console.log('Readability Analysis for ROS 2 Textbook');
  console.log('========================================\n');

  const results = [];

  for (const file of chapterFiles) {
    const chapterPath = path.join(docsDir, file);
    const result = analyzeChapterReadability(chapterPath);
    if (result) {
      results.push(result);
    }
  }

  console.log('Summary:');
  console.log('========');
  results.forEach(result => {
    const status = result.meetsTarget ? '✓' : '✗';
    console.log(`${status} ${result.fileName}: Grade ${result.gradeLevel.toFixed(2)} (${result.wordCount} words)`);
  });

  const compliantCount = results.filter(r => r.meetsTarget).length;
  const total = results.length;
  const percentage = total > 0 ? (compliantCount / total * 100).toFixed(1) : 0;

  console.log(`\nOverall: ${compliantCount}/${total} chapters (${percentage}%) meet the Grade 12-14 target`);

  return { results, compliantCount, total, percentage };
}

// Run analysis
if (require.main === module) {
  analyzeAllChapters();
}

module.exports = {
  countSentences,
  countWords,
  countSyllables,
  countTotalSyllables,
  calculateFleschKincaidGradeLevel,
  cleanContent,
  analyzeChapterReadability,
  analyzeAllChapters
};