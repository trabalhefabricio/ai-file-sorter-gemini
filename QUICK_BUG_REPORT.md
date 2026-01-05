# Quick Bug Reporter for Power Users

This is a **lightweight, personal tool** for you to quickly capture and communicate bugs to AI assistants without them being dismissed.

## The Problem This Solves

You: "There's a bug where X happens"  
AI: "I don't see any bugs in the code"  
You: 😤

## The Solution

A simple markdown template you fill out when you find a bug, then paste to AI assistants. The structured format forces them to actually analyze instead of dismissing.

## Usage

### Step 1: Copy This Template

```markdown
## BUG REPORT - DO NOT DISMISS

**Date:** [today's date]
**Component:** [UI/File Operations/Database/AI/etc]
**Severity:** [Critical/High/Medium/Low]

### The Bug
[One sentence: what's broken]

### How to Reproduce
1. [specific step]
2. [specific step]
3. [what happens - the bug]

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happens]

### Evidence
```
[paste error log excerpt, or screenshot description]
```

### Why This is NOT "No Bug":
- [ ] Reproducible (I can make it happen every time)
- [ ] Have error logs/evidence
- [ ] Worked before (version: ___)
- [ ] Breaks expected functionality
- [ ] Specific error message: "___"

### System Context
- Version/Commit: [your version]
- OS: [your OS]
- Build: [source/binary]

### What I Already Tried
1. [thing you tried]
2. [thing you tried]
3. [result]

---

**AI Assistant:** Please analyze the evidence above and identify the root cause. This is a real bug with reproducible steps and evidence.
```

### Step 2: Fill It Out

When you hit a bug:
1. Copy template above
2. Fill in the blanks (takes 2 minutes)
3. Attach error logs or COPILOT_ERROR_*.md file

### Step 3: Paste to AI

Open Copilot Chat or your AI assistant and paste the filled template.

The key phrase at the bottom tells the AI: "This is real, analyze it."

## Examples

### Example 1: Clear Bug with Evidence

```markdown
## BUG REPORT - DO NOT DISMISS

**Date:** 2026-01-05
**Component:** UI/Categorization Dialog
**Severity:** Critical

### The Bug
Application crashes when clicking Analyze button on folders with 5000+ files

### How to Reproduce
1. Open AI File Sorter
2. Select Downloads folder (contains 6000 files)
3. Click "Analyze" button
4. Application crashes with "Critical DLL Setup Error" dialog

### Expected Behavior
Application should analyze files and show categorization dialog

### Actual Behavior
Immediate crash with error message:
"Could not locate entry point QTableView::dropEvent in Qt6Widgets.dll"

### Evidence
```
[2026-01-05 10:30:45] [ERROR] DLL_DROPEVENT_NOT_FOUND
[2026-01-05 10:30:45] [ERROR] Qt Runtime Version: 6.7.0
[2026-01-05 10:30:45] [ERROR] Qt Compile Version: 6.5.3 ← MISMATCH
[2026-01-05 10:30:45] [ERROR] System PATH: C:\Program Files\Qt\6.7.0\bin;...
```

### Why This is NOT "No Bug":
- [x] Reproducible (happens every single time)
- [x] Have error logs showing DLL mismatch
- [x] Worked before (v1.4.0 was fine)
- [x] Breaks core functionality (can't analyze anything)
- [x] Specific error message: "QTableView::dropEvent not found"

### System Context
- Version/Commit: v1.5.0 / commit abc123
- OS: Windows 11 22H2
- Build: Downloaded release binary

### What I Already Tried
1. Reinstalled application - still crashes
2. Checked system PATH - has multiple Qt versions
3. Read troubleshooting docs - suggests using StartAiFileSorter.exe
4. Launched StartAiFileSorter.exe - still crashes
5. Checked error logs - confirms Qt version mismatch

---

**AI Assistant:** Please analyze the evidence above and identify the root cause. This is a real bug with reproducible steps and evidence. The Qt version mismatch is clear from the logs.
```

**Result:** AI can't dismiss this. The evidence is right there.

### Example 2: Performance Bug

```markdown
## BUG REPORT - DO NOT DISMISS

**Date:** 2026-01-05
**Component:** File Operations
**Severity:** Medium

### The Bug
File sorting takes 10+ minutes for 100 files when it should take seconds

### How to Reproduce
1. Open AI File Sorter
2. Select test folder with 100 small files (1KB each)
3. Click Analyze
4. Click "Confirm & Sort"
5. Watch progress - takes 10+ minutes

### Expected Behavior
100 small files should sort in under 10 seconds (it's just file moves)

### Actual Behavior
Takes 10+ minutes. Progress bar advances very slowly. No errors.

### Evidence
- Timed it: 12 minutes 34 seconds for 100 files
- Task Manager shows high disk usage but low CPU
- Previous version (v1.4.0) sorted same folder in 8 seconds
- Log shows: "Moving file 1/100... Moving file 2/100..." with 7-8 second gaps

### Why This is NOT "No Bug":
- [x] Reproducible (happens every time with this folder)
- [x] Have timing data
- [x] Worked before (v1.4.0: 8 seconds, v1.5.0: 12+ minutes)
- [x] Breaks usability (unusably slow)
- [x] Regression from previous version

### System Context
- Version/Commit: v1.5.0 / commit xyz789
- OS: Ubuntu 24.04
- Build: Built from source

### What I Already Tried
1. Different folders - same slow behavior
2. Checked disk space - plenty available
3. Ran with debug logging - shows long pauses between file moves
4. Compared with v1.4.0 - v1.4.0 is fast, v1.5.0 is slow
5. Checked git diff between versions - file operation code changed

---

**AI Assistant:** Please analyze the evidence above and identify the root cause. This is a clear performance regression - something changed between v1.4.0 and v1.5.0 that made file operations 90x slower.
```

## When AI Still Dismisses

If AI still says "no bug" after your detailed report, try:

### Response 1: Point to Evidence
```
I provided detailed evidence:
- Reproducible steps
- Error logs showing [specific error]
- Timing data showing [specific regression]
- Version comparison showing it worked before

Which part of this evidence are you questioning?
```

### Response 2: Ask for Code Review
```
I've shown this is reproducible. Please review the code in [component] 
and identify what could cause [symptom]. Don't tell me there's no bug - 
help me find WHERE the bug is.
```

### Response 3: Escalate
```
This bug is blocking my use of the application. I need a fix, not a dismissal.
Let's work together:
1. You review the code
2. I'll test changes
3. We'll iterate until fixed

Where should we start?
```

## Integration with Existing Tools

Your app already has excellent error reporting:
- `COPILOT_ERROR_*.md` files in logs directory
- Detailed error logs with context
- System information capture

**Use these together:**

1. Hit a bug
2. Find the `COPILOT_ERROR_*.md` file
3. Fill out the quick template above
4. Paste BOTH to AI: template + COPILOT_ERROR contents

This gives AI everything needed to fix the bug, not dismiss it.

## Local Bug Tracking

Keep your own `BUGS.md` file:

```markdown
# My Active Bugs

## 2026-01-05: QTableView crash
Status: Open
[paste your bug report here]
AI response: [paste what AI said]
Fix attempt 1: [what you tried]
Result: [did it work?]

## 2026-01-03: Slow file operations
Status: Fixed in commit abc123
[bug details]
Solution: [what fixed it]
```

This way YOU have the record, independent of AI memory.

## Summary

**For power user personal use:**
1. ✅ Quick template (2 minutes to fill)
2. ✅ Structured to prevent AI dismissal
3. ✅ Works with existing error reporting
4. ✅ Local tracking (BUGS.md file)
5. ✅ No complex system needed
6. ✅ Just YOU and your fork

**Not needed:**
- ❌ GitHub Issue templates (overkill for one user)
- ❌ Public triage system
- ❌ Multi-user workflows

Keep it simple, keep it effective, keep it YOURS.

---

**Save this file as:** `QUICK_BUG_REPORT.md` in your repository
