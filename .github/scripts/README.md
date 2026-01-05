# GitHub Scripts

This directory contains automation scripts for issue triage and bug analysis.

## parse_bug_report.py

An "agents agent" - a tool that parses and analyzes bug reports to provide structured analysis for AI assistants and developers.

### Purpose

This script:
- Parses structured data from GitHub issue templates
- Detects known bug patterns automatically
- Calculates priority using the priority matrix
- Generates triage analysis comments
- Provides user-facing troubleshooting steps
- Identifies affected code components

### Usage

**Analyze a bug report from JSON:**
```bash
python3 parse_bug_report.py --from-file issue_data.json
```

**Analyze a COPILOT_ERROR file:**
```bash
python3 parse_bug_report.py --analyze-copilot-error COPILOT_ERROR_12345.md
```

**Output as JSON:**
```bash
python3 parse_bug_report.py --from-file issue_data.json --output json
```

### Example Output

```markdown
## 🔍 Initial Triage Analysis

**Priority:** P0 - Critical - Fix immediately
**Category:** DLL/Library Loading Error
**Pattern Detected:** dll_version_mismatch (confidence: 75%)

### Quick Summary
DLL/Library Loading Error on Windows 11 (v1.5.0): Application crashes with QTableView::dropEvent error

### Root Cause Analysis
This appears to match a known pattern: **Dll Version Mismatch**

**Hypothesis:** DLL version mismatch - check StartAiFileSorter.exe usage and PATH

**Reference Documentation:** [QTABLEVIEW_DROPEVENT_FIX.md](QTABLEVIEW_DROPEVENT_FIX.md)

### Immediate Actions (For User)
Please try the following and report back:
1. Verify you're launching `StartAiFileSorter.exe`, NOT `aifilesorter.exe` directly
2. Check your system PATH for multiple Qt installations
3. Review the DLL search path setup in error logs

### For Developers
**Affected Components:**
- startapp_windows.cpp
- DLL loading

**Complexity Estimate:** Low-Medium (known pattern)
```

### Integration with GitHub Actions

This script can be integrated into GitHub Actions workflows to automatically triage new issues:

```yaml
name: Auto-Triage Issues
on:
  issues:
    types: [opened]

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Analyze Issue
        run: |
          python3 .github/scripts/parse_bug_report.py \
            --from-file issue.json --output markdown > triage.md
      - name: Post Comment
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const triage = fs.readFileSync('triage.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: triage
            });
```

### Known Bug Patterns

The script recognizes these patterns:

1. **dll_version_mismatch**: Qt DLL version mismatches
2. **ggml_function_missing**: GGML library out of date
3. **permission_denied**: File permission issues
4. **api_rate_limit**: API rate limiting issues
5. **local_llm_load_fail**: Local LLM loading failures

### Adding New Patterns

Edit the `PATTERNS` dictionary in `parse_bug_report.py`:

```python
PATTERNS = {
    'new_pattern_name': {
        'keywords': ['keyword1', 'keyword2', 'keyword3'],
        'confidence_threshold': 0.7,  # 70% keyword match required
        'solution': 'Description of the solution',
        'reference': 'DOCUMENTATION.md'
    }
}
```

### Dependencies

- Python 3.7+
- No external packages required (uses standard library only)

### Related Documentation

- [ISSUE_TRIAGE_GUIDE.md](../../ISSUE_TRIAGE_GUIDE.md) - Manual for issue triage process
- [BUGFIXING_GUIDE.md](../../BUGFIXING_GUIDE.md) - Bug prevention and fixing guide
- [ERROR_REPORTING_FOR_COPILOT_USERS.md](../../ERROR_REPORTING_FOR_COPILOT_USERS.md) - User guide for error reporting
