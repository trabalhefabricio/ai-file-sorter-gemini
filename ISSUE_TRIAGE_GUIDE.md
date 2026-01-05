# Issue Triage Guide for AI Assistants & Developers

## Overview

This guide explains how to triage, analyze, and route bug reports and feature requests in the AI File Sorter project. It serves as a **systematic intake system** for issues, ensuring bugs are properly understood, categorized, and fixed efficiently.

## Purpose: The "Agents Agent"

This document is designed to be:
- **For AI Assistants (like GitHub Copilot)**: A structured protocol for parsing user issues and providing actionable analysis
- **For Developers**: A standardized workflow for handling incoming issues
- **For Users**: Transparency into how their bug reports are processed

## When a Bug Report Arrives

### 1. Initial Assessment (Automated by AI)

When a new bug report is filed using the bug_report.yml template, perform this analysis:

#### A. Extract Key Information

```markdown
ISSUE INTAKE ANALYSIS
======================
Issue #: [number]
Title: [title]
Category: [bug-category from template]
Severity: [severity from template]
OS: [operating system]
Version: [app-version]
LLM Type: [llm-type]

Quick Summary:
[1-2 sentence summary of the problem]

Reproducibility: [Always/Sometimes/Once/Cannot Reproduce]
```

#### B. Classification Matrix

Cross-reference bug category and severity to determine priority:

| Category | Critical | High | Medium | Low |
|----------|----------|------|--------|-----|
| Application Crash/Won't Start | P0 | P0 | P1 | P2 |
| DLL/Library Loading | P0 | P1 | P1 | P2 |
| Qt/UI Issue | P1 | P1 | P2 | P3 |
| Categorization/AI | P1 | P2 | P2 | P3 |
| File Operations | P0 | P1 | P2 | P3 |
| Database/Cache | P1 | P2 | P2 | P3 |
| API Integration | P1 | P2 | P2 | P3 |
| Performance | P2 | P2 | P3 | P3 |
| Cosmetic | P3 | P3 | P3 | P3 |

**Priority Definitions:**
- **P0 (Critical)**: Drop everything, fix immediately. App unusable for affected users.
- **P1 (High)**: Fix in next release/hotfix. Major functionality broken.
- **P2 (Medium)**: Fix in upcoming releases. Minor functionality affected.
- **P3 (Low)**: Fix when convenient. Nice to have.

#### C. Check for Duplicates/Patterns

```markdown
PATTERN ANALYSIS
================
Related Issues: [list issue numbers]
Known Bug: [Yes/No - check BUGFIXING_GUIDE.md and BUG_FIXING_RESULTS.md]
Previous Occurrences: [link to previous similar issues]
Root Cause (if known): [from previous analysis]
```

### 2. Deep Analysis (AI-Assisted)

If the issue contains a `COPILOT_ERROR_*.md` file or detailed logs, perform deeper analysis:

#### A. Parse Error Context

Extract from COPILOT_ERROR file or logs:
```markdown
ERROR CONTEXT EXTRACTION
========================
Error ID: [from log]
Error Code: [from log]
Source Location: [file:line:function]
Stack Trace: [if available]

System Context:
- Qt Compile Version: [version]
- Qt Runtime Version: [version]
- OS Version: [details]
- System PATH: [first 5 entries]

DLL Context (if applicable):
- DLL Name: [name]
- DLL Path: [path]
- Missing Symbol: [symbol]

Root Cause Hypothesis:
[Based on error context and patterns]
```

#### B. Cross-Reference with Known Issues

Check against:
1. **BUGFIXING_GUIDE.md** - Known patterns and solutions
2. **BUG_FIXING_RESULTS.md** - Previously fixed bugs
3. **STARTUP_ERROR_FIXES_SUMMARY.md** - Startup-specific issues
4. **QTABLEVIEW_DROPEVENT_FIX.md** - Qt/DLL issues
5. **ERROR_CODES.md** - Error code definitions

#### C. Suggest Initial Diagnosis

```markdown
INITIAL DIAGNOSIS
=================
Likely Cause: [best guess based on all context]

Evidence Supporting This:
1. [evidence point 1]
2. [evidence point 2]
3. [evidence point 3]

Confidence Level: [High/Medium/Low]

Recommended Next Steps:
1. [step 1 for user to try]
2. [step 2 for user to try]
3. [information to gather]
```

### 3. Response Template (Post as Comment)

When posting initial triage analysis, use this format:

```markdown
## 🔍 Initial Triage Analysis

**Priority:** P[0-3] - [Critical/High/Medium/Low]
**Category:** [refined category if different from initial]
**Estimated Complexity:** [Simple/Medium/Complex]

### Quick Summary
[1-2 sentence summary in plain language]

### Root Cause Analysis
[Hypothesis about what's causing this issue]

### Immediate Actions (For User)
Please try the following and report back:
1. [specific step 1]
2. [specific step 2]
3. [specific step 3]

### For Developers
**Affected Components:**
- File(s): [source files affected]
- Subsystem: [which part of codebase]

**Similar Issues:**
- [link to related issues]

**Potential Fix Approach:**
[High-level description of how to fix]

**Complexity Estimate:** [hours/days]

---
*This analysis was performed using the Issue Triage Guide. If you need clarification or have additional information, please comment below.*
```

## Pattern Recognition (AI-Assisted)

### Common Bug Patterns and Solutions

#### Pattern 1: DLL Version Mismatch
**Symptoms:**
- Error mentions `QTableView::dropEvent` or similar Qt function
- COPILOT_ERROR shows Qt runtime ≠ compile version
- Windows system PATH has multiple Qt installations

**Root Cause:** System PATH pointing to wrong Qt DLL version

**Solution:**
1. Check `StartAiFileSorter.exe` is being used (not `aifilesorter.exe` directly)
2. Verify application directory DLLs match expected version
3. Guide user through PATH cleanup

**Reference:** QTABLEVIEW_DROPEVENT_FIX.md

#### Pattern 2: GGML Function Missing
**Symptoms:**
- Error: `ggml_xielu` or other GGML function not found
- Happens after updating submodules

**Root Cause:** llama.cpp library outdated vs application

**Solution:**
1. Rebuild llama.cpp library first
2. Then rebuild application
3. Clean build directories if needed

**Reference:** README.md Troubleshooting section

#### Pattern 3: Permission Denied on File Operations
**Symptoms:**
- File move/copy fails
- Error accessing directories
- Happens on specific folders only

**Root Cause:** File permissions or antivirus blocking

**Solution:**
1. Check file/folder permissions
2. Try running as administrator (Windows)
3. Check antivirus logs
4. Verify user has write access to destination

**Reference:** BUGFIXING_GUIDE.md - Filesystem section

#### Pattern 4: API Rate Limiting (Gemini/OpenAI)
**Symptoms:**
- Errors after batch of successful API calls
- "Rate limit exceeded" or timeout messages
- Happens with free-tier API keys

**Root Cause:** API rate limits hit

**Solution:**
1. Verify rate limiting is enabled (should be automatic)
2. Check ApiUsageStatistics.cpp for tracking
3. Suggest batch size reduction or delay between batches

**Reference:** README.md - Gemini API section

#### Pattern 5: Local LLM Won't Load
**Symptoms:**
- Model file not found
- Out of memory errors
- Quantization format errors

**Root Cause:** Model file issues or insufficient RAM/VRAM

**Solution:**
1. Verify model file exists and is valid GGUF format
2. Check available RAM/VRAM vs model requirements
3. Suggest smaller quantization (Q4 instead of Q8)
4. Check LLMDownloader.cpp for supported formats

**Reference:** README.md - Local LLM section

### Pattern Detection Algorithm

When analyzing a new issue:

1. **Extract keywords** from description and error messages
2. **Match against known patterns** above
3. **Calculate confidence score** (0-100%)
4. **If confidence > 70%**, suggest pattern-based solution
5. **If confidence < 70%**, perform deep analysis
6. **Always** provide reasoning for your conclusion

## Feature Request Handling

### 1. Initial Assessment

```markdown
FEATURE REQUEST ANALYSIS
========================
Issue #: [number]
Title: [title]
Category: [category]
Priority: [priority]
Breaking Changes: [Yes/No/Maybe]

Problem Statement:
[Clear summary of problem being solved]

Proposed Solution:
[High-level approach]

Feasibility Assessment: [High/Medium/Low]
```

### 2. Check Against Roadmap

Cross-reference with:
- **FUTURE_IMPROVEMENTS.md** - Planned features
- **IMPLEMENTATION_PLAN.md** - Scheduled work
- **NON_AI_FEATURES_SUMMARY.md** - Feature matrix

Is this already planned? Link to relevant section.

### 3. Technical Feasibility Analysis

```markdown
TECHNICAL FEASIBILITY
=====================
Estimated Complexity: [Simple/Medium/Complex/Very Complex]

Dependencies:
- [external library X]
- [system capability Y]

Affected Components:
- [component 1]
- [component 2]

Implementation Approach:
[High-level technical approach]

Estimated Effort: [hours/days/weeks]

Risks/Challenges:
- [risk 1]
- [risk 2]
```

### 4. Community Feedback Request

```markdown
## 🎯 Feature Request Triage

**Feasibility:** [High/Medium/Low]
**Estimated Effort:** [XYZ hours/days]
**Conflicts with existing features:** [Yes/No]

### Summary
[Plain language summary]

### Implementation Approach
[How this could be built]

### Questions for Community
1. [question 1 for other users]
2. [question 2 for other users]

### Next Steps
- [ ] Gather community feedback (1 week)
- [ ] Create technical design document (if feasible)
- [ ] Add to roadmap (if approved)

**Vote:** 👍 if you want this feature, 👎 if not needed
```

## Automated Actions

### Labels to Apply

Based on triage analysis, apply appropriate labels:

**Priority:**
- `priority-p0-critical`
- `priority-p1-high`
- `priority-p2-medium`
- `priority-p3-low`

**Component:**
- `component-ui`
- `component-ai-llm`
- `component-file-ops`
- `component-database`
- `component-api`
- `component-build`

**Status:**
- `status-needs-info` - Waiting for user response
- `status-reproducing` - Attempting to reproduce
- `status-confirmed` - Bug confirmed
- `status-in-progress` - Fix being worked on
- `status-testing` - Fix awaiting testing
- `status-blocked` - Blocked by external factor

**Type:**
- `bug`
- `enhancement`
- `documentation`
- `question`
- `duplicate`
- `wontfix`

### Assignments

**P0 (Critical):**
- Assign to maintainer immediately
- Set milestone to "Next Hotfix"

**P1 (High):**
- Assign to maintainer within 24 hours
- Set milestone to "Next Release"

**P2/P3:**
- Add to backlog
- Let maintainer prioritize

## Communication Templates

### Requesting More Information

```markdown
## 📋 Additional Information Needed

Thank you for reporting this issue! To help us diagnose and fix it, we need a bit more information:

### Required:
1. **[specific info needed]**
   - Why: [explanation]
   - How to find: [instructions]

2. **[another piece of info]**
   - Why: [explanation]
   - How to find: [instructions]

### Optional (But Helpful):
- [optional info 1]
- [optional info 2]

**How to provide this:**
You can edit your original issue description or add a comment with the information.

Once we have this information, we can proceed with diagnosis and resolution.
```

### Bug Confirmed

```markdown
## ✅ Bug Confirmed

Thank you for the detailed report! We've confirmed this is a genuine bug.

**Root Cause:** [explanation]

**Affected Users:** [scope of impact]

**Fix Approach:** [how we'll fix it]

**Timeline:** [when fix expected]

We'll update this issue as we make progress. You can track the fix by watching this issue or checking the linked PR.
```

### Duplicate Issue

```markdown
## 🔄 Duplicate Issue

Thank you for reporting! This issue is a duplicate of #[number].

**Related Issue:** #[number]
**Status:** [status of original issue]

We're consolidating discussion and work on the original issue. Please:
1. Review the original issue thread
2. Add any unique information there if different from what's already reported
3. Subscribe to the original issue for updates

Closing this as duplicate.
```

### Cannot Reproduce

```markdown
## ❓ Cannot Reproduce

Thank you for reporting this issue. We've attempted to reproduce it but haven't been successful yet.

**What we tried:**
1. [step 1 we tried]
2. [step 2 we tried]
3. [result]

**To help us reproduce:**
- Could you provide [specific info]?
- Does this happen every time or intermittently?
- Any special configuration or circumstances?

If we can reproduce it, we can fix it! Please provide any additional details that might help.

Adding `status-needs-info` label.
```

## Quality Checks

Before posting triage analysis, verify:

- [ ] All extracted information is accurate
- [ ] Pattern matching was performed
- [ ] Known issues were checked
- [ ] Priority assignment follows matrix
- [ ] Response is clear and actionable
- [ ] User is given specific next steps
- [ ] Developer information is technical enough to start work
- [ ] Tone is helpful and professional
- [ ] No sensitive information exposed (API keys, passwords, etc.)

## Metrics to Track

For continuous improvement:

- **Time to First Response:** How long before triage analysis posted
- **Time to Resolution:** How long to close issue
- **Accuracy of Initial Diagnosis:** % of correct root cause identification
- **Duplicate Detection Rate:** % of duplicates caught early
- **User Satisfaction:** Based on feedback/reactions

## Special Cases

### Security Issues

If an issue mentions security vulnerabilities:

1. **Do NOT discuss in public issue**
2. Post comment: "Thank you for reporting. This appears to be a security concern. Please email [security-email] with details."
3. Apply `security` label (private)
4. Close issue immediately
5. Follow up privately

### Toxic/Abusive Reports

1. Apply `invalid` label
2. Post: "This issue does not meet our code of conduct standards. Closing."
3. Close and lock thread
4. Report to GitHub if needed

### Questions (Not Bugs)

If someone files a bug that's actually a question:

```markdown
## 💬 Discussion Topic

Thanks for reaching out! This seems like a question rather than a bug report.

**Answer:** [provide answer if simple]

**For future questions:**
Please use [GitHub Discussions](link) for questions rather than Issues. Issues are for bugs and feature requests.

Closing this issue but feel free to:
- Ask follow-up questions in Discussions
- Check the [Documentation](link)

Converting to Discussion...
```

## Continuous Improvement

This guide should evolve based on:
- New bug patterns discovered
- Changes to codebase architecture
- User feedback on issue templates
- Effectiveness of triage responses

**Review Schedule:** Monthly
**Owner:** Maintainer team
**Last Updated:** 2026-01-05

---

## For AI Assistants: Quick Reference

When triaging an issue, follow this checklist:

1. ✅ Extract all structured information from issue template
2. ✅ Classify using Priority Matrix
3. ✅ Check for duplicates and patterns
4. ✅ Parse error logs/COPILOT_ERROR files if present
5. ✅ Cross-reference with known issues documentation
6. ✅ Generate diagnosis with confidence level
7. ✅ Provide user-facing next steps
8. ✅ Provide developer-facing technical analysis
9. ✅ Apply appropriate labels
10. ✅ Post triage comment using template

**Remember:** Your goal is to help users get their issues resolved quickly while providing developers with actionable information to fix bugs efficiently.
