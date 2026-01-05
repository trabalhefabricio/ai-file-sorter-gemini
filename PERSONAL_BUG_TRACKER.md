# Personal Bug Tracker

**For:** Power user personal tracking  
**Purpose:** Keep track of bugs found, prevent AI dismissal, track fixes

## Active Bugs

### [Date] - Brief Description
**Status:** Open/In Progress/Fixed  
**Severity:** Critical/High/Medium/Low  
**Found in:** [version/commit]  
**Component:** [which part of app]

**Description:**
[What's wrong]

**How to Reproduce:**
1. Step 1
2. Step 2
3. Bug occurs

**Evidence:**
- Error log: [path to log or paste excerpt]
- COPILOT_ERROR file: [if exists]
- Screenshots: [if applicable]

**Why this is NOT "no bug":**
[Your argument for why this is real]

**AI Assistant Notes:**
[Space for AI to respond - prevents dismissal]

**Fix Applied:** [when fixed]
**Verified:** [date verified]

---

### Example Entry

### 2026-01-05 - QTableView crash on large folders
**Status:** Open  
**Severity:** High  
**Found in:** v1.5.0  
**Component:** UI/Categorization Dialog

**Description:**
App crashes when analyzing folders with 5000+ files. QTableView::dropEvent error.

**How to Reproduce:**
1. Point app at Downloads folder (6000 files)
2. Click Analyze
3. Crashes immediately with DLL error

**Evidence:**
- Error log: `%APPDATA%\aifilesorter\logs\errors.log` shows DLL_DROPEVENT_NOT_FOUND
- Qt Runtime: 6.7.0 vs Compile: 6.5.3 (VERSION MISMATCH)
- System PATH has multiple Qt installs

**Why this is NOT "no bug":**
- Reproducible 100% of the time
- Error logs clearly show DLL mismatch
- Worked fine in v1.4.0
- Other users report same issue (if applicable)

**AI Assistant Notes:**
Pattern: DLL version mismatch
Root cause: StartAiFileSorter.exe not being used OR system PATH has wrong Qt version
Solution: Use StartAiFileSorter.exe, clean PATH, verify DLL versions match

**Fix Applied:** [pending]
**Verified:** [pending]

---

## Fixed Bugs

### [Date] - Brief Description
**Fixed in:** [commit/version]
**Fix:** [what was done]
**Verified:** [date]

---

## False Alarms / Not Bugs

### [Date] - What I thought was a bug
**Actually was:** [explanation]
**Lesson learned:** [what to check next time]

---

## Patterns Detected

### Pattern: DLL Version Mismatch
**Symptoms:** QTableView errors, entry point not found
**Root cause:** Multiple Qt installations, wrong PATH
**Solution:** Use StartAiFileSorter.exe, check PATH
**Frequency:** Common on fresh installs

### Pattern: [Another pattern you notice]
**Symptoms:**
**Root cause:**
**Solution:**
**Frequency:**

---

## Quick Checklist Before Reporting to AI

When you find a bug and want AI help:

- [ ] Bug is reproducible (can you make it happen again?)
- [ ] You have error logs or COPILOT_ERROR files
- [ ] You can describe exact steps to reproduce
- [ ] You checked if it worked in previous version
- [ ] You have evidence (logs, screenshots, error messages)

**Then:** Copy the bug entry above and paste it to AI assistant with:
> "I have a bug. This is NOT a 'no bug' situation. Here's the evidence:"
> [paste bug entry]

This format makes it harder for AI to dismiss because you've pre-addressed the "why it's real" question.

---

## Tips for Working with AI Assistants on Your Fork

### When AI says "no bugs found":

**Don't accept it.** Instead, respond:
```
I found a specific bug. Please analyze THIS evidence:
- Error log excerpt: [paste]
- Reproduction steps: [paste]
- Expected vs actual: [paste]

This is reproducible. Please don't dismiss it. What's the root cause?
```

### When AI suggests "check documentation":

**If you already did that:**
```
I already read [doc]. The bug persists. Here's what I tried:
1. [step]
2. [step]
3. Still broken

Next suggestion?
```

### When AI suggests "update to latest version":

**If you're on latest:**
```
I'm on the latest commit [hash]. Bug still exists. 
Git log shows: [recent commits]
This bug is present in current code. Let's fix it.
```

---

## Personal Notes

**My Setup:**
- OS: [your OS]
- Build method: [how you build]
- Common workflows: [what you do most]
- Pain points: [recurring issues]

**My Conventions:**
- How I report bugs: [your style]
- How I test fixes: [your process]
- How I track versions: [your method]

---

**Last Updated:** [date]
