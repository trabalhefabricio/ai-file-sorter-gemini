# Error Reporting for Non-Coders / Copilot Users

## Overview

AI File Sorter now has **Copilot-friendly error reporting** designed specifically for users who rely on GitHub Copilot for troubleshooting.

## How It Works

When an error occurs, the application automatically creates a **special error report file** that you can copy and paste directly into GitHub Copilot Chat to get help.

## Finding Your Error Reports

### Location

Error reports are saved to:
- **Windows:** `C:\Users\YourName\AppData\Roaming\aifilesorter\logs\COPILOT_ERROR_*.md`
- **Linux:** `~/.cache/aifilesorter/logs/COPILOT_ERROR_*.md`
- **macOS:** `~/Library/Application Support/aifilesorter/logs/COPILOT_ERROR_*.md`

### File Names

Look for files like:
- `COPILOT_ERROR_ERR-1736003456789-4523.md`
- The most recent file is usually the error you just encountered

## Using the Error Report with Copilot

### Step 1: Find the Error File

1. Open the logs directory (see location above)
2. Find the most recent `COPILOT_ERROR_*.md` file
3. The file with the newest timestamp is your latest error

### Step 2: Open the File

- Use any text editor (Notepad, Visual Studio Code, etc.)
- Or right-click → "Open with" → Choose your editor

### Step 3: Copy Everything

- Press `Ctrl+A` (select all)
- Press `Ctrl+C` (copy)
- The entire contents are now in your clipboard

### Step 4: Paste into Copilot Chat

1. Open GitHub Copilot Chat in VS Code or your IDE
2. Press `Ctrl+V` (paste)
3. Press Enter to send

### Step 5: Ask for Help

Copilot will see:
- Exactly where the error occurred (file, line, function)
- The code around the error
- Your system information
- What went wrong and why
- Troubleshooting steps already tried

You can then ask:
- "How do I fix this error?"
- "What's causing this problem?"
- "Can you explain this in simple terms?"
- "What should I do step by step?"

## What's in the Error Report?

Each error report contains:

### 1. Error Summary
```
Error ID: ERR-1736003456789-4523
Category: DLL_LOADING
Severity: CRITICAL
Error Code: DLL_DROPEVENT_NOT_FOUND
Message: QTableView::dropEvent symbol not found in Qt6Widgets.dll
```

### 2. Where It Happened
```
File: app/lib/CategorizationDialog.cpp
Line: 223
Function: CategorizationDialog::setup_ui()
```

### 3. Code Context
```cpp
 >>> 223 | table_view = new QTableView(this);
     224 | table_view->setModel(model);
     225 | table_view->setSelectionBehavior(QAbstractItemView::SelectRows);
```
*The `>>>` shows the exact line where the error occurred*

### 4. System Information
```
OS: Windows 10
App Version: 1.5.0
Qt Compile Version: 6.5.3
Qt Runtime Version: 6.7.0  ← MISMATCH!
```

### 5. Troubleshooting Steps
- Category-specific steps already tried
- What to check next
- How to fix common causes

### 6. Ready-Made Copilot Question
The file ends with a formatted question for Copilot that provides all context needed.

## Example Workflow

### Scenario: Application crashes at startup

**You See:**
```
Error dialog: "Critical DLL Setup Error"
Message mentions COPILOT_ERROR_*.md file
```

**You Do:**
1. Note the error message (or take screenshot)
2. Open logs directory
3. Find newest `COPILOT_ERROR_*.md` file
4. Open it in text editor
5. Copy all contents (`Ctrl+A`, `Ctrl+C`)
6. Open Copilot Chat
7. Paste (`Ctrl+V`)
8. Ask: "How do I fix this? I followed the troubleshooting steps but still have issues."

**Copilot Sees:**
- Your exact error with full context
- Your system configuration
- What's already been tried
- Code location and snippet

**Copilot Responds:**
- Identifies root cause (e.g., Qt version mismatch)
- Provides step-by-step fix instructions
- Explains what each step does
- Offers alternatives if first solution doesn't work

## Tips for Best Results

### 1. Always Copy the Entire File
Don't try to summarize or extract parts - Copilot needs all the context.

### 2. Mention What You've Tried
After pasting, add:
```
I already tried:
- Running as Administrator
- Checking system PATH
- Reinstalling the application
```

### 3. Ask Specific Follow-ups
- "Can you explain step 2 in more detail?"
- "I don't understand what PATH means"
- "Where do I find Environment Variables?"
- "Show me exactly what to click"

### 4. Share Results
Tell Copilot what happened:
- "That worked! But now I have a different error"
- "Step 3 didn't work - it says access denied"
- "I can't find the file you mentioned"

## Common Error Categories

### DLL_LOADING
**What it means:** Windows can't find the right DLL files
**What to do:** Copy COPILOT_ERROR file, paste to Copilot, focus on PATH and Qt installation issues

### QT_INITIALIZATION
**What it means:** Qt framework failed to start
**What to do:** Check Qt DLLs, plugins, run as Administrator

### MODEL_LOADING (Future)
**What it means:** AI model failed to load
**What to do:** Check model file, VRAM, quantization format

### LLM_API (Future)
**What it means:** API call to OpenAI/Gemini failed
**What to do:** Check API key, rate limits, internet connection

## Troubleshooting the Error Reporter Itself

### "I can't find the logs directory"

**Windows:**
1. Press `Win+R`
2. Type: `%APPDATA%\aifilesorter\logs`
3. Press Enter

**Alternative:**
1. Open File Explorer
2. Type in address bar: `%APPDATA%\aifilesorter\logs`
3. Press Enter

### "The COPILOT_ERROR file is empty"

This means the error occurred before the error reporter was initialized.
Check the regular `errors.log` file instead and copy its contents.

### "There are multiple COPILOT_ERROR files"

Use the most recent one (highest timestamp number in filename).
Or check Windows "Date modified" column and use newest.

### "I get an error when trying to paste into Copilot"

The file might be too large. Try:
1. Copy just the "Error Summary" and "Where It Happened" sections
2. Paste those first
3. Then add more context if Copilot asks

## Benefits of This System

### For You
- ✅ No need to understand code
- ✅ No need to parse technical logs
- ✅ Everything formatted for Copilot
- ✅ One copy-paste gets you help
- ✅ Includes troubleshooting steps
- ✅ Shows exact error location

### For Copilot
- ✅ Sees exact code context
- ✅ Knows your system setup
- ✅ Understands error category
- ✅ Can provide precise solutions
- ✅ Knows what you've already tried

### For Developers (if you share with them)
- ✅ Complete diagnostic information
- ✅ Reproducible error context
- ✅ System configuration details
- ✅ Easy to identify patterns

## Privacy Note

Error reports contain:
- File paths on your system
- Your Windows username (in paths)
- System PATH directories
- Qt installation locations
- Working directory

They do NOT contain:
- API keys or passwords
- File contents
- Personal data
- Your files or documents

**Safe to share** with Copilot or developers for troubleshooting.

## Advanced: Using with GitHub Issues

If Copilot can't solve your issue and you need to report a bug:

1. Copy COPILOT_ERROR file contents
2. Create GitHub issue
3. Paste contents in issue description
4. Add screenshots of error dialogs
5. Mention what Copilot suggested and what happened

This gives developers everything they need to help you.

## Questions?

If you have questions about the error reporting system itself:

1. Copy a COPILOT_ERROR file
2. Paste into Copilot Chat
3. Ask: "Can you explain what each section of this error report means?"

Copilot can help you understand the error reporting system too!
