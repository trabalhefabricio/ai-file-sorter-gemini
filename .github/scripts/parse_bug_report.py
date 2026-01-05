#!/usr/bin/env python3
"""
Bug Report Parser and Analyzer

This script parses GitHub issue data and provides structured analysis
to help AI assistants and developers triage bugs more efficiently.

Usage:
    python3 parse_bug_report.py <issue_number>
    python3 parse_bug_report.py --from-file bug_report.json
    python3 parse_bug_report.py --analyze-copilot-error error_file.md
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class BugReportParser:
    """Parses and analyzes bug reports from GitHub issues"""

    # Known bug patterns from ISSUE_TRIAGE_GUIDE.md
    PATTERNS = {
        'dll_version_mismatch': {
            'keywords': ['QTableView::dropEvent', 'Qt runtime', 'Qt compile', 'DLL'],
            'confidence_threshold': 0.7,
            'solution': 'DLL version mismatch - check StartAiFileSorter.exe usage and PATH',
            'reference': 'QTABLEVIEW_DROPEVENT_FIX.md'
        },
        'ggml_function_missing': {
            'keywords': ['ggml_xielu', 'llama.dll', 'entry point', 'procedure'],
            'confidence_threshold': 0.7,
            'solution': 'GGML library outdated - rebuild llama.cpp then application',
            'reference': 'README.md - Troubleshooting'
        },
        'permission_denied': {
            'keywords': ['permission denied', 'access denied', 'cannot write', 'read-only'],
            'confidence_threshold': 0.6,
            'solution': 'File permission issue - check permissions, antivirus, run as admin',
            'reference': 'BUGFIXING_GUIDE.md - Filesystem'
        },
        'api_rate_limit': {
            'keywords': ['rate limit', 'quota exceeded', 'too many requests', 'Gemini', 'OpenAI'],
            'confidence_threshold': 0.7,
            'solution': 'API rate limiting - verify rate limiter is enabled, reduce batch size',
            'reference': 'README.md - Gemini API'
        },
        'local_llm_load_fail': {
            'keywords': ['model not found', 'out of memory', 'GGUF', 'quantization'],
            'confidence_threshold': 0.6,
            'solution': 'LLM loading issue - verify model file, check RAM/VRAM, try smaller quantization',
            'reference': 'README.md - Local LLM'
        }
    }

    # Priority matrix from ISSUE_TRIAGE_GUIDE.md
    PRIORITY_MATRIX = {
        'Application Crash/Won\'t Start': {'Critical': 'P0', 'High': 'P0', 'Medium': 'P1', 'Low': 'P2'},
        'DLL/Library Loading Error': {'Critical': 'P0', 'High': 'P1', 'Medium': 'P1', 'Low': 'P2'},
        'Qt/UI Issue': {'Critical': 'P1', 'High': 'P1', 'Medium': 'P2', 'Low': 'P3'},
        'Categorization/AI Model Issue': {'Critical': 'P1', 'High': 'P2', 'Medium': 'P2', 'Low': 'P3'},
        'File Sorting/Moving Error': {'Critical': 'P0', 'High': 'P1', 'Medium': 'P2', 'Low': 'P3'},
        'Database/Cache Issue': {'Critical': 'P1', 'High': 'P2', 'Medium': 'P2', 'Low': 'P3'},
        'API Integration (OpenAI/Gemini)': {'Critical': 'P1', 'High': 'P2', 'Medium': 'P2', 'Low': 'P3'},
        'Performance/Slow Operation': {'Critical': 'P2', 'High': 'P2', 'Medium': 'P3', 'Low': 'P3'},
    }

    def __init__(self, data: Dict):
        self.data = data
        self.analysis = {}

    def extract_fields(self) -> Dict:
        """Extract structured fields from issue template"""
        body = self.data.get('body', '')
        title = self.data.get('title', '')

        fields = {
            'title': title,
            'bug_category': self._extract_field(body, 'Bug Category'),
            'severity': self._extract_field(body, 'Severity'),
            'description': self._extract_field(body, 'Bug Description'),
            'steps_to_reproduce': self._extract_field(body, 'Steps to Reproduce'),
            'expected_behavior': self._extract_field(body, 'Expected Behavior'),
            'actual_behavior': self._extract_field(body, 'Actual Behavior'),
            'os': self._extract_field(body, 'Operating System'),
            'app_version': self._extract_field(body, 'AI File Sorter Version'),
            'error_message': self._extract_field(body, 'Error Messages'),
            'log_files': self._extract_field(body, 'Log Files'),
            'copilot_error': self._extract_field(body, 'Copilot Error File'),
        }

        return fields

    def _extract_field(self, body: str, field_name: str) -> Optional[str]:
        """Extract a specific field from issue body"""
        # Match GitHub issue template format
        pattern = rf'### {re.escape(field_name)}\s*\n\s*\n(.*?)(?=\n###|\Z)'
        match = re.search(pattern, body, re.DOTALL)
        if match:
            value = match.group(1).strip()
            return value if value and value != '_No response_' else None
        return None

    def calculate_priority(self, category: str, severity: str) -> str:
        """Calculate priority using priority matrix"""
        if category in self.PRIORITY_MATRIX:
            return self.PRIORITY_MATRIX[category].get(severity, 'P3')
        return 'P3'

    def detect_pattern(self, text: str) -> Tuple[Optional[str], float]:
        """Detect known bug patterns in text"""
        text_lower = text.lower()
        best_match = None
        best_confidence = 0.0

        for pattern_name, pattern_data in self.PATTERNS.items():
            matches = sum(1 for keyword in pattern_data['keywords'] 
                         if keyword.lower() in text_lower)
            confidence = matches / len(pattern_data['keywords'])

            if confidence > best_confidence and confidence >= pattern_data['confidence_threshold']:
                best_confidence = confidence
                best_match = pattern_name

        return best_match, best_confidence

    def analyze(self) -> Dict:
        """Perform full analysis of bug report"""
        fields = self.extract_fields()

        # Calculate priority
        priority = self.calculate_priority(
            fields.get('bug_category', ''),
            fields.get('severity', '')
        )

        # Combine all text for pattern detection
        all_text = ' '.join(filter(None, [
            fields.get('title', ''),
            fields.get('description', ''),
            fields.get('error_message', ''),
            fields.get('actual_behavior', ''),
            fields.get('log_files', ''),
        ]))

        # Detect pattern
        pattern, confidence = self.detect_pattern(all_text)

        analysis = {
            'fields': fields,
            'priority': priority,
            'pattern_detected': pattern,
            'pattern_confidence': confidence,
            'has_copilot_error': bool(fields.get('copilot_error')),
            'has_logs': bool(fields.get('log_files')),
        }

        if pattern:
            pattern_data = self.PATTERNS[pattern]
            analysis['suggested_solution'] = pattern_data['solution']
            analysis['reference_doc'] = pattern_data['reference']

        self.analysis = analysis
        return analysis

    def generate_triage_comment(self) -> str:
        """Generate a triage comment for posting on GitHub"""
        if not self.analysis:
            self.analyze()

        fields = self.analysis['fields']
        priority = self.analysis['priority']
        pattern = self.analysis.get('pattern_detected')
        confidence = self.analysis.get('pattern_confidence', 0)

        comment = f"""## 🔍 Initial Triage Analysis

**Priority:** {priority} - {self._priority_description(priority)}
**Category:** {fields.get('bug_category', 'Unknown')}
**Pattern Detected:** {pattern or 'None'} (confidence: {confidence:.0%})

### Quick Summary
{self._generate_summary(fields)}

"""

        if pattern:
            solution = self.analysis.get('suggested_solution', '')
            reference = self.analysis.get('reference_doc', '')
            comment += f"""### Root Cause Analysis
This appears to match a known pattern: **{pattern.replace('_', ' ').title()}**

**Hypothesis:** {solution}

**Reference Documentation:** [{reference}]({reference})

"""

        comment += f"""### Immediate Actions (For User)
Please try the following and report back:
{self._generate_user_steps(pattern, fields)}

### For Developers
**Affected Components:**
{self._identify_components(fields)}

**Complexity Estimate:** {self._estimate_complexity(pattern, fields)}

---
*This analysis was performed using the Issue Triage Guide. If you need clarification or have additional information, please comment below.*
"""

        return comment

    def _priority_description(self, priority: str) -> str:
        descriptions = {
            'P0': 'Critical - Fix immediately',
            'P1': 'High - Fix in next release',
            'P2': 'Medium - Fix in upcoming releases',
            'P3': 'Low - Fix when convenient'
        }
        return descriptions.get(priority, 'Unknown')

    def _generate_summary(self, fields: Dict) -> str:
        """Generate a plain-language summary"""
        category = fields.get('bug_category', 'Unknown')
        os = fields.get('os', 'Unknown OS')
        version = fields.get('app_version', 'unknown version')

        desc = fields.get('description', 'No description provided')
        # Truncate to first sentence or 100 chars
        summary = desc.split('.')[0][:100]

        return f"{category} on {os} (v{version}): {summary}"

    def _generate_user_steps(self, pattern: Optional[str], fields: Dict) -> str:
        """Generate specific troubleshooting steps for user"""
        steps = []

        if pattern == 'dll_version_mismatch':
            steps = [
                "1. Verify you're launching `StartAiFileSorter.exe`, NOT `aifilesorter.exe` directly",
                "2. Check your system PATH for multiple Qt installations",
                "3. Review the DLL search path setup in error logs",
            ]
        elif pattern == 'ggml_function_missing':
            steps = [
                "1. Update to the latest release version",
                "2. If building from source, rebuild llama.cpp: `./app/scripts/build_llama_*.sh`",
                "3. Then rebuild the application",
            ]
        elif pattern == 'permission_denied':
            steps = [
                "1. Check file and folder permissions on the target directory",
                "2. Try running the application as Administrator (Windows) or with sudo (Linux)",
                "3. Check if antivirus is blocking file operations",
            ]
        elif pattern == 'api_rate_limit':
            steps = [
                "1. Verify you're using a valid API key",
                "2. Check Tools → API Usage Statistics for quota information",
                "3. Reduce the number of files per batch",
            ]
        else:
            # Generic steps
            steps = [
                "1. Verify you're using the latest version of AI File Sorter",
                "2. Check the logs directory for detailed error information",
                "3. Try the operation with a smaller set of files to isolate the issue",
            ]

        return '\n'.join(steps)

    def _identify_components(self, fields: Dict) -> str:
        """Identify which code components are likely affected"""
        category = fields.get('bug_category', '')
        components = []

        component_map = {
            'Application Crash': ['main.cpp', 'StartupManager'],
            'DLL/Library Loading': ['startapp_windows.cpp', 'DLL loading'],
            'Qt/UI Issue': ['Qt widgets', 'UI dialogs'],
            'Categorization': ['LLMClient', 'ConsistencyPassService'],
            'File Sorting': ['FileOperations', 'MovableCategorizedFile'],
            'Database': ['DatabaseManager', 'SQLite operations'],
            'API Integration': ['OpenAIClient', 'GeminiClient', 'ApiUsageStatistics'],
        }

        for key, comps in component_map.items():
            if key.lower() in category.lower():
                components.extend(comps)
                break

        return '\n'.join(f'- {comp}' for comp in components) if components else '- To be determined'

    def _estimate_complexity(self, pattern: Optional[str], fields: Dict) -> str:
        """Estimate fix complexity"""
        if pattern:
            # Known patterns are usually simpler
            return "Low-Medium (known pattern)"

        severity = fields.get('severity', '')
        if 'Critical' in severity or 'High' in severity:
            return "Medium-High (high severity issue)"

        return "To be determined after investigation"


def parse_copilot_error_file(filepath: Path) -> Dict:
    """Parse a COPILOT_ERROR_*.md file"""
    content = filepath.read_text()

    # Extract structured information
    data = {
        'error_id': re.search(r'Error ID: (.+)', content),
        'category': re.search(r'Category: (.+)', content),
        'severity': re.search(r'Severity: (.+)', content),
        'error_code': re.search(r'Error Code: (.+)', content),
        'message': re.search(r'Message: (.+)', content),
        'source_file': re.search(r'File: (.+)', content),
        'source_line': re.search(r'Line: (\d+)', content),
        'function': re.search(r'Function: (.+)', content),
    }

    # Extract match groups
    return {key: (match.group(1) if match else None) for key, match in data.items()}


def main():
    parser = argparse.ArgumentParser(description='Parse and analyze bug reports')
    parser.add_argument('issue_number', nargs='?', help='GitHub issue number')
    parser.add_argument('--from-file', help='Parse from JSON file')
    parser.add_argument('--analyze-copilot-error', help='Parse COPILOT_ERROR_*.md file')
    parser.add_argument('--output', choices=['json', 'markdown'], default='markdown',
                        help='Output format')

    args = parser.parse_args()

    if args.analyze_copilot_error:
        # Parse Copilot error file
        filepath = Path(args.analyze_copilot_error)
        if not filepath.exists():
            print(f"Error: File not found: {filepath}", file=sys.stderr)
            return 1

        data = parse_copilot_error_file(filepath)
        print(json.dumps(data, indent=2))
        return 0

    # Load issue data
    if args.from_file:
        filepath = Path(args.from_file)
        if not filepath.exists():
            print(f"Error: File not found: {filepath}", file=sys.stderr)
            return 1
        with open(filepath) as f:
            issue_data = json.load(f)
    elif args.issue_number:
        # In real usage, this would fetch from GitHub API
        print("Note: Fetching from GitHub API not implemented in this demo.")
        print("Use --from-file to provide issue data as JSON.")
        return 1
    else:
        parser.print_help()
        return 1

    # Analyze
    analyzer = BugReportParser(issue_data)
    analysis = analyzer.analyze()

    # Output
    if args.output == 'json':
        print(json.dumps(analysis, indent=2))
    else:
        comment = analyzer.generate_triage_comment()
        print(comment)

    return 0


if __name__ == '__main__':
    sys.exit(main())
