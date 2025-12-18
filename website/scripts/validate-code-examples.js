#!/usr/bin/env node

/**
 * Code Example Validation Script
 * Validates that all code examples in the textbook chapters are syntactically correct
 */

const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

// Extract Python code blocks from markdown content
function extractPythonCodeBlocks(content) {
  const pythonRegex = /```python\n([\s\S]*?)\n```/g;
  const matches = [];
  let match;

  while ((match = pythonRegex.exec(content)) !== null) {
    matches.push(match[1].trim());
  }

  return matches;
}

// Extract shell/command code blocks from markdown content
function extractShellCodeBlocks(content) {
  const shellRegex = /```bash\n([\s\S]*?)\n```|```\n([\s\S]*?command.*?|.*?source.*?|.*?ros2.*?|.*?colcon.*?|.*?apt.*?|.*?pip.*?|.*?npm.*?|.*?python.*?|.*?cd.*?|.*?ls.*?|.*?cat.*?)\n```/g;
  const matches = [];
  let match;

  while ((match = shellRegex.exec(content)) !== null) {
    const code = match[1] || match[2];
    if (code) {
      matches.push(code.trim());
    }
  }

  return matches;
}

// Validate Python code syntax by writing to temp file and checking for syntax errors
function validatePythonCode(code) {
  const { spawnSync } = require('child_process');
  const { writeFileSync, unlinkSync } = require('fs');
  const { join } = require('path');
  const { tmpdir } = require('os');

  // Write code to temporary file
  const tempFile = join(tmpdir(), `temp_${Date.now()}.py`);
  try {
    writeFileSync(tempFile, code);

    // Check syntax with Python
    const result = spawnSync('python3', ['-m', 'py_compile', tempFile], {
      stdio: ['pipe', 'pipe', 'pipe']
    });

    const isValid = result.status === 0;
    const error = !isValid ? result.stderr.toString() : null;

    return { isValid, error };
  } catch (error) {
    return { isValid: false, error: error.message };
  } finally {
    // Clean up temp file
    try {
      unlinkSync(tempFile);
    } catch (e) {
      // Ignore cleanup errors
    }
  }
}

// Validate a single chapter file
function validateChapterCodeExamples(chapterPath) {
  if (!fs.existsSync(chapterPath)) {
    console.error(`Error: File does not exist: ${chapterPath}`);
    return false;
  }

  const fileContent = fs.readFileSync(chapterPath, 'utf8');
  const parsed = matter(fileContent);
  const bodyContent = parsed.content;

  // Extract Python code blocks
  const pythonCodeBlocks = extractPythonCodeBlocks(bodyContent);
  const shellCodeBlocks = extractShellCodeBlocks(bodyContent);

  console.log(`Validating code examples in: ${path.basename(chapterPath)}`);

  let pythonErrors = 0;
  let shellExamples = 0;

  // Validate Python code blocks
  if (pythonCodeBlocks.length > 0) {
    console.log(`  Found ${pythonCodeBlocks.length} Python code blocks`);
    for (let i = 0; i < pythonCodeBlocks.length; i++) {
      const code = pythonCodeBlocks[i];
      const validation = validatePythonCode(code);

      if (!validation.isValid) {
        console.log(`    ✗ Python block ${i + 1}: Syntax error`);
        console.log(`      Error: ${validation.error}`);
        pythonErrors++;
      } else {
        console.log(`    ✓ Python block ${i + 1}: Valid syntax`);
      }
    }
  } else {
    console.log('  No Python code blocks found');
  }

  // Count shell/command examples
  if (shellCodeBlocks.length > 0) {
    console.log(`  Found ${shellCodeBlocks.length} shell/command examples`);
    shellExamples = shellCodeBlocks.length;
    shellCodeBlocks.forEach((code, i) => {
      console.log(`    Shell example ${i + 1}: ${code.split('\n')[0].substring(0, 50)}...`);
    });
  } else {
    console.log('  No shell/command examples found');
  }

  const hasErrors = pythonErrors > 0;
  console.log(`  Status: ${hasErrors ? '✗ Has errors' : '✓ Validated successfully'}`);
  console.log('');

  return {
    isValid: !hasErrors,
    pythonBlocks: pythonCodeBlocks.length,
    pythonErrors,
    shellExamples
  };
}

// Validate all ROS 2 chapters
function validateAllChapters() {
  const docsDir = './docs/ros2';
  const chapterFiles = fs.readdirSync(docsDir).filter(file =>
    file.endsWith('.md') && !file.startsWith('_') && file !== 'tags-taxonomy.md' && file !== 'content-guidelines.md'
  );

  console.log('Code Example Validation for ROS 2 Textbook');
  console.log('============================================\n');

  let allValid = true;
  const results = [];

  for (const file of chapterFiles) {
    const chapterPath = path.join(docsDir, file);
    const result = validateChapterCodeExamples(chapterPath);
    results.push({ file, ...result });
    if (!result.isValid) {
      allValid = false;
    }
  }

  console.log('Summary:');
  console.log('========');
  results.forEach(result => {
    const status = result.isValid ? '✓' : '✗';
    console.log(`${status} ${result.file}: ${result.pythonBlocks} Python blocks (${result.pythonErrors} errors), ${result.shellExamples} shell examples`);
  });

  console.log(`\nOverall: ${allValid ? 'All code examples are syntactically valid' : 'Some code examples have syntax errors'}`);

  return { allValid, results };
}

// Run validation
if (require.main === module) {
  validateAllChapters();
}

module.exports = {
  extractPythonCodeBlocks,
  extractShellCodeBlocks,
  validatePythonCode,
  validateChapterCodeExamples,
  validateAllChapters
};