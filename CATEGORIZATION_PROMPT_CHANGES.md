# Categorization Prompt Changes - The Core Sorting Logic Difference

**Created:** January 7, 2026  
**Importance:** ⚠️ **CRITICAL** - This is THE MOST IMPORTANT change  
**Files Affected:** `app/lib/LLMClient.cpp`, `app/lib/GeminiClient.cpp`

---

## Executive Summary

The **main categorization prompt** is what tells the AI how to sort files. This is the single most important difference between the original fork and your custom version. Without implementing this change, the re-forked repository will categorize files differently and lose the improved accuracy.

**Priority:** This must be Feature #0 - implement BEFORE all other features.

---

## What Changed

### Original Fork (hyperfield/ai-file-sorter)

**System Prompt:**
```
"Categorize this file: [filename]"
```

**Characteristics:**
- Simple instruction
- Filename only
- No guidance on analysis approach
- Always expects a category response
- No confidence handling

**Result:** Basic categorization based purely on filename string matching.

---

### Custom Fork (trabalhefabricio/ai-file-sorter-iconic)

**System Prompt:**
```cpp
"You are an intelligent file categorization assistant. "
"Analyze the file name, extension, and context to understand what the file represents. "
"Consider the purpose, content type, and intended use of the file.\n\n"
"IMPORTANT: If you are uncertain about the categorization (confidence < 70%), "
"respond with: UNCERTAIN : [filename]\n"
"Otherwise, respond ONLY with: Category : Subcategory\n"
"No explanations, no additional text."
```

**User Prompt Enhancement:**
```cpp
"File to categorize:\n"
"Type: " + to_string(file_type) + "\n"  // NEW: File type awareness
"Name: " + file_name + "\n"
"Path: " + file_path + "\n"  // NEW: Path context

"\nAnalyze this file based on:\n"  // NEW: Structured analysis
"- What this file type (." + extension + ") is typically used for\n"
"- The semantic meaning of the filename\n"
"- Common purposes and applications for this file format\n"
```

**Characteristics:**
- Intelligent assistant persona
- Multi-factor analysis (name + extension + path + type)
- Explicit analysis framework
- Confidence threshold (70%)
- UNCERTAIN response handling
- Purpose-based reasoning

**Result:** Smart categorization based on file type, extension semantics, context, and purpose.

---

## The 5 Key Enhancements

### 1. File Type Awareness
**Original:** No file type information  
**Custom:** Includes `FileType` enum (FILE, DIRECTORY, etc.)

**Why it matters:** Directories and files have different categorization needs.

### 2. Extension Analysis
**Original:** Extension ignored  
**Custom:** Explicit instruction to analyze what the extension means

**Example:**
```
.psd → Photoshop Document → Design Work
.py → Python Script → Development/Scripts
.pdf → PDF Document → Documents/Reports (context-dependent)
```

**Why it matters:** Extensions are the strongest signal for file purpose.

### 3. Confidence Threshold
**Original:** Always returns a category (even if wrong)  
**Custom:** Returns "UNCERTAIN" if confidence < 70%

**Why it matters:** Prevents bad guesses. Better to be uncertain than wrong.

### 4. Path Context
**Original:** Filename only  
**Custom:** Includes full path when available

**Example:**
```
projects/web-dev/styles.css → Web Development
personal/budget.css → Personal/Finance (CSS for styling a finance tracker)
```

**Why it matters:** Path provides critical context for ambiguous filenames.

### 5. Structured Analysis Framework
**Original:** No guidance on how to think  
**Custom:** Three-point analysis framework

**Framework:**
1. What is this file type typically used for?
2. What does the filename mean semantically?
3. What are common applications for this format?

**Why it matters:** Consistent reasoning process → consistent results.

---

## Impact on Categorization Quality

### Accuracy Improvement Examples

**File:** `report.txt`

**Original Logic:**
- "Categorize: report.txt"
- Guess: "Documents : Reports" (might be right)

**Custom Logic:**
- File type: FILE
- Extension: .txt (plain text file for notes, logs, configs)
- Filename: "report" (suggests documentation)
- Analysis: Plain text + "report" name → Documentation
- Result: "Documents : Reports" (high confidence)

---

**File:** `config.json`

**Original Logic:**
- "Categorize: config.json"
- Guess: "Documents : Data" (wrong - not a document)

**Custom Logic:**
- File type: FILE
- Extension: .json (configuration file, data exchange format)
- Filename: "config" (configuration settings)
- Analysis: JSON + "config" name → Application configuration
- Result: "Development : Configuration" (correct)

---

**File:** `photo.dat`

**Original Logic:**
- "Categorize: photo.dat"
- Guess: "Images : Photos" (wrong - .dat is not an image)

**Custom Logic:**
- File type: FILE
- Extension: .dat (generic binary data)
- Filename: "photo" (suggests image content)
- Analysis: Uncertain - .dat could be anything
- Result: "UNCERTAIN : photo.dat" (correct - avoids misclassification)

---

## Code Implementation

### Location 1: LLMClient.cpp (OpenAI)

**File:** `app/lib/LLMClient.cpp`  
**Function:** `make_categorization_payload()`  
**Lines:** 396-438

```cpp
// System message with enhanced prompt
Json::Value system_msg;
system_msg["role"] = "system";
std::string system_content = "You are an intelligent file categorization assistant. "
    "Analyze the file name, extension, and context to understand what the file represents. "
    "Consider the purpose, content type, and intended use of the file.\n\n"
    "IMPORTANT: If you are uncertain about the categorization (confidence < 70%), "
    "respond with: UNCERTAIN : [filename]\n"
    "Otherwise, respond ONLY with: Category : Subcategory\n"
    "No explanations, no additional text.";

if (!consistency_context.empty()) {
    system_content += "\n\nContext and constraints:\n" + consistency_context;
}
system_msg["content"] = system_content;
messages.append(system_msg);

// User message with file analysis
Json::Value user_msg;
user_msg["role"] = "user";

std::string user_content = "File to categorize:\n";
user_content += "Type: " + to_string(file_type) + "\n";
user_content += "Name: " + file_name + "\n";
if (!file_path.empty() && file_path != file_name) {
    user_content += "Path: " + file_path + "\n";
}

// Extension analysis
size_t dot_pos = file_name.find_last_of('.');
if (dot_pos != std::string::npos && dot_pos < file_name.length() - 1) {
    std::string extension = file_name.substr(dot_pos + 1);
    user_content += "\nAnalyze this file based on:\n";
    user_content += "- What this file type (." + extension + ") is typically used for\n";
    user_content += "- The semantic meaning of the filename\n";
    user_content += "- Common purposes and applications for this file format\n";
}

user_msg["content"] = user_content;
messages.append(user_msg);
```

### Location 2: GeminiClient.cpp (Google Gemini)

**File:** `app/lib/GeminiClient.cpp`  
**Function:** `make_categorization_payload()`  
**Lines:** 629-677

```cpp
// Gemini combines system and user prompts into one
std::string prompt = "You are an intelligent file categorization assistant. "
    "Analyze the file name, extension, and context to understand what the file represents. "
    "Consider the purpose, content type, and intended use of the file.\n\n"
    "IMPORTANT: If you are uncertain about the categorization (confidence < 70%), "
    "respond with: UNCERTAIN : [filename]\n"
    "Otherwise, respond ONLY with: Category : Subcategory\n"
    "No explanations, no additional text.\n\n";

if (!consistency_context.empty()) {
    prompt += "Context and constraints:\n" + consistency_context + "\n\n";
}

// File analysis
prompt += "File to categorize:\n";
prompt += "Type: " + to_string(file_type) + "\n";
prompt += "Name: " + file_name + "\n";
if (!file_path.empty() && file_path != file_name) {
    prompt += "Path: " + file_path + "\n";
}

// Extension analysis
size_t dot_pos = file_name.find_last_of('.');
if (dot_pos != std::string::npos && dot_pos < file_name.length() - 1) {
    std::string extension = file_name.substr(dot_pos + 1);
    prompt += "\nAnalyze this file based on:\n";
    prompt += "- What this file type (." + extension + ") is typically used for\n";
    prompt += "- The semantic meaning of the filename\n";
    prompt += "- Common purposes and applications for this file format\n";
}
```

---

## Implementation Priority

### ⚠️ THIS IS FEATURE #0

**Why it comes first:**
1. It's the foundation - everything else builds on correct categorization
2. Affects every file processed
3. Simple to implement but massive impact
4. No dependencies on other features
5. Can be tested immediately

**Implementation order:**
```
0. Enhanced Categorization Prompt ← START HERE
   ↓
1. Database Schema (if needed)
   ↓
2. Enhanced Undo System
   ↓
3. Dry Run Preview
   ↓
... (all other features)
```

---

## Testing the Prompt Changes

### Test Cases

**Test 1: Extension Analysis**
```
Input: project_plan.xlsx
Expected: Analyzes .xlsx as spreadsheet → Business/Planning
Original: Might guess Documents/General
```

**Test 2: Confidence Threshold**
```
Input: data.bin
Expected: UNCERTAIN (binary files are ambiguous)
Original: Guesses randomly, might be wrong
```

**Test 3: Path Context**
```
Input: photos/vacation/IMG_001.jpg with path
Expected: Uses "photos/vacation" context → Personal/Photos
Original: Only sees filename, might categorize differently
```

**Test 4: Purpose Analysis**
```
Input: README.md
Expected: Analyzes .md as documentation → Development/Docs
Original: Might not recognize Markdown significance
```

---

## Migration Checklist

When re-forking, you must:

- [ ] Copy enhanced system prompt to `LLMClient.cpp` lines 396-407
- [ ] Copy enhanced user prompt logic to `LLMClient.cpp` lines 414-431
- [ ] Copy enhanced system prompt to `GeminiClient.cpp` lines 629-635
- [ ] Copy enhanced user prompt logic to `GeminiClient.cpp` lines 642-657
- [ ] Ensure `FileType` enum is available (should be in original)
- [ ] Test with diverse file types
- [ ] Verify UNCERTAIN responses work correctly
- [ ] Confirm extension analysis runs for all files
- [ ] Test path context with nested directories

---

## Why This Was Forgotten

This change is "invisible" in the feature list because:
1. It's code-level, not UI/feature-level
2. No new files were added
3. It's embedded in existing categorization flow
4. The improvement is subtle but pervasive

**But it's the MOST important change** because it determines the quality of every categorization operation.

---

## Summary

**What:** Enhanced AI prompts with file type analysis, extension semantics, path context, and confidence thresholds.

**Where:** `LLMClient.cpp` and `GeminiClient.cpp` in `make_categorization_payload()` functions.

**Why:** Dramatically improves categorization accuracy and prevents bad guesses.

**When to implement:** FIRST - before all other features.

**Time to implement:** 30 minutes to 1 hour (copy prompt text, test)

**Impact:** Foundation for all file sorting quality improvements.

---

## Next Steps

1. **Read this document** - Understand why this is critical
2. **Review the code** - See exactly what changed
3. **Implement Feature #0** - Copy the enhanced prompts first
4. **Test thoroughly** - Verify improved categorization
5. **Move to Feature #1** - Then implement other features

**Remember:** Without this change, your re-fork will sort files like the original (less accurately). With this change, you maintain the improved sorting intelligence that makes your fork valuable.
