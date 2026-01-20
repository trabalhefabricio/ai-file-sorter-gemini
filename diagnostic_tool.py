#!/usr/bin/env python3
"""
AI File Sorter - Comprehensive Diagnostic Tool
Analyzes code for the 12 identified bugs and provides actionable reports
"""

import os
import re
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class BugFinding:
    """Represents a single bug detection result"""
    bug_id: str
    severity: str
    file_path: str
    line_number: int
    description: str
    code_snippet: str
    found: bool
    recommendation: str

class DiagnosticTool:
    """Comprehensive diagnostic tool for AI File Sorter bugs"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.app_path = self.repo_path / "app"
        self.findings: List[BugFinding] = []
        
    def run_all_checks(self) -> Dict:
        """Run all diagnostic checks"""
        print("=" * 80)
        print("AI File Sorter - Comprehensive Diagnostic Tool")
        print("=" * 80)
        print(f"Repository: {self.repo_path}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 80)
        
        checks = [
            self.check_bug_1_detached_thread,
            self.check_bug_2_null_pointer,
            self.check_bug_3_stol_exception,
            self.check_bug_4_data_race,
            self.check_bug_5_memory_leak,
            self.check_bug_6_silent_db_failure,
            self.check_bug_7_sql_leak,
            self.check_bug_8_static_state,
            self.check_bug_9_optimize_ui,
            self.check_bug_10_null_item_to_node,
            self.check_bug_11_file_preview_error,
            self.check_bug_12_bare_catch,
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                print(f"ERROR running {check.__name__}: {e}")
        
        return self.generate_report()
    
    def check_bug_1_detached_thread(self):
        """Bug #1: Detached thread with dangling pointer"""
        print("\n[BUG #1] Checking for detached thread with dangling pointer...")
        
        file_path = self.app_path / "lib" / "GeminiClient.cpp"
        if not file_path.exists():
            print(f"  ⚠️  File not found: {file_path}")
            return
        
        content = file_path.read_text()
        
        # Look for the pattern: flag_ptr = &save_pending_ ... .detach()
        pattern = r'(std::atomic<bool>\*\s+\w+\s*=\s*&\w+;.*?\.detach\(\);)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        found = len(matches) > 0
        
        if found:
            # Find line number
            lines = content.split('\n')
            line_num = None
            for i, line in enumerate(lines, 1):
                if 'detach()' in line and 'flag_ptr' in content[max(0, content.find(line)-200):content.find(line)]:
                    line_num = i
                    break
            
            snippet = matches[0][:200] + "..." if len(matches[0]) > 200 else matches[0]
            
            self.findings.append(BugFinding(
                bug_id="BUG-001",
                severity="CRITICAL",
                file_path=str(file_path),
                line_number=line_num or 0,
                description="Detached thread captures member variable address. Use-after-free if object destroyed before thread completes.",
                code_snippet=snippet,
                found=True,
                recommendation="Use std::shared_ptr or make thread joinable. Store thread in member variable and join in destructor."
            ))
            print(f"  ❌ FOUND at line {line_num}: Detached thread with dangling pointer")
        else:
            print(f"  ✅ Not found (or already fixed)")
    
    def check_bug_2_null_pointer(self):
        """Bug #2: Null pointer dereference from topLevelItem()"""
        print("\n[BUG #2] Checking for null pointer dereferences in tree operations...")
        
        file_path = self.app_path / "lib" / "WhitelistTreeEditor.cpp"
        if not file_path.exists():
            print(f"  ⚠️  File not found: {file_path}")
            return
        
        content = file_path.read_text()
        lines = content.split('\n')
        
        # Look for topLevelItem() calls without null checks
        pattern = r'topLevelItem\(\w+\)->(?!.*if\s*\()'
        
        found_lines = []
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                # Check if there's a null check within 3 lines before
                has_null_check = False
                for j in range(max(0, i-3), i):
                    if 'if' in lines[j-1] and ('nullptr' in lines[j-1] or '!item' in lines[j-1]):
                        has_null_check = True
                        break
                
                if not has_null_check:
                    found_lines.append((i, line.strip()))
        
        if found_lines:
            for line_num, line in found_lines:
                self.findings.append(BugFinding(
                    bug_id="BUG-002",
                    severity="CRITICAL",
                    file_path=str(file_path),
                    line_number=line_num,
                    description="topLevelItem() can return nullptr but code dereferences without checking",
                    code_snippet=line,
                    found=True,
                    recommendation="Add null check: if (item) { ... } before dereferencing"
                ))
            print(f"  ❌ FOUND {len(found_lines)} instances without null checks")
        else:
            print(f"  ✅ All topLevelItem() calls have null checks")
    
    def check_bug_3_stol_exception(self):
        """Bug #3: Unhandled std::stol exception"""
        print("\n[BUG #3] Checking for unhandled std::stol exceptions...")
        
        file_path = self.app_path / "lib" / "GeminiClient.cpp"
        if not file_path.exists():
            print(f"  ⚠️  File not found: {file_path}")
            return
        
        content = file_path.read_text()
        lines = content.split('\n')
        
        # Look for std::stol with bare catch(...)
        pattern = r'std::stol\('
        
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                # Check if it's in a try block with catch(...)
                # Look ahead for catch block
                has_bare_catch = False
                for j in range(i, min(i+10, len(lines))):
                    if 'catch' in lines[j] and '...' in lines[j]:
                        has_bare_catch = True
                        break
                
                if has_bare_catch:
                    self.findings.append(BugFinding(
                        bug_id="BUG-003",
                        severity="HIGH",
                        file_path=str(file_path),
                        line_number=i,
                        description="std::stol can throw exceptions but uses bare catch(...) that swallows all errors",
                        code_snippet=line.strip(),
                        found=True,
                        recommendation="Catch specific exceptions: catch(const std::invalid_argument&) and catch(const std::out_of_range&). Log errors."
                    ))
                    print(f"  ❌ FOUND at line {i}: std::stol with bare catch(...)")
    
    def check_bug_4_data_race(self):
        """Bug #4: Data race in progress callback"""
        print("\n[BUG #4] Checking for data race in progress callback...")
        
        file_path = self.app_path / "lib" / "GeminiClient.cpp"
        if not file_path.exists():
            print(f"  ⚠️  File not found: {file_path}")
            return
        
        content = file_path.read_text()
        
        # Look for ProgressData struct with non-atomic last_activity_ms
        if 'struct ProgressData' in content:
            # Check if last_activity_ms is atomic
            if 'last_activity_ms' in content and 'std::atomic<uint64_t>' not in content:
                lines = content.split('\n')
                line_num = None
                for i, line in enumerate(lines, 1):
                    if 'last_activity_ms' in line and 'struct ProgressData' in '\n'.join(lines[max(0,i-5):i]):
                        line_num = i
                        break
                
                self.findings.append(BugFinding(
                    bug_id="BUG-004",
                    severity="HIGH",
                    file_path=str(file_path),
                    line_number=line_num or 0,
                    description="ProgressData::last_activity_ms accessed from multiple threads without synchronization (data race)",
                    code_snippet="uint64_t last_activity_ms = 0;  // Not atomic!",
                    found=True,
                    recommendation="Change to: std::atomic<uint64_t> last_activity_ms{0};"
                ))
                print(f"  ❌ FOUND: Non-atomic last_activity_ms in multi-threaded context")
            else:
                print(f"  ✅ last_activity_ms is properly atomic")
    
    def check_bug_5_memory_leak(self):
        """Bug #5: Memory leak in on_remove_item"""
        print("\n[BUG #5] Checking for memory leak in WhitelistTreeEditor...")
        
        file_path = self.app_path / "lib" / "WhitelistTreeEditor.cpp"
        if not file_path.exists():
            print(f"  ⚠️  File not found: {file_path}")
            return
        
        content = file_path.read_text()
        
        # Look for: delete tree_widget_->takeTopLevelItem(...)
        pattern = r'delete\s+tree_widget_->takeTopLevelItem'
        
        if re.search(pattern, content):
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    self.findings.append(BugFinding(
                        bug_id="BUG-005",
                        severity="HIGH",
                        file_path=str(file_path),
                        line_number=i,
                        description="Manual delete of Qt-owned tree item. Can cause double-free or memory leak.",
                        code_snippet=line.strip(),
                        found=True,
                        recommendation="Let Qt manage lifetime. Either don't delete, or ensure item ownership is properly transferred."
                    ))
                    print(f"  ❌ FOUND at line {i}: Manual delete of Qt tree item")
        else:
            print(f"  ✅ No manual delete of tree items found")
    
    def check_bug_6_silent_db_failure(self):
        """Bug #6: Silent database operation failure"""
        print("\n[BUG #6] Checking for ignored database operation return values...")
        
        file_path = self.app_path / "lib" / "FileTinderDialog.cpp"
        if not file_path.exists():
            print(f"  ⚠️  File not found: {file_path}")
            return
        
        content = file_path.read_text()
        lines = content.split('\n')
        
        # Look for db_. method calls where return value is ignored
        pattern = r'^\s*db_\.\w+\([^;]+\);\s*$'
        
        found_lines = []
        for i, line in enumerate(lines, 1):
            if re.match(pattern, line):
                # Check if it's not in an if statement
                if i > 1 and 'if' not in lines[i-2]:
                    found_lines.append((i, line.strip()))
        
        if found_lines:
            for line_num, line in found_lines[:3]:  # Report first 3
                self.findings.append(BugFinding(
                    bug_id="BUG-006",
                    severity="MEDIUM",
                    file_path=str(file_path),
                    line_number=line_num,
                    description="Database operation return value ignored. Failures go undetected.",
                    code_snippet=line,
                    found=True,
                    recommendation="Check return value: if (!db_.method(...)) { /* handle error */ }"
                ))
            print(f"  ❌ FOUND {len(found_lines)} unchecked database operations")
        else:
            print(f"  ✅ All database operations check return values")
    
    def check_bug_7_sql_leak(self):
        """Bug #7: SQL statement resource leak"""
        print("\n[BUG #7] Checking for SQL statement resource leaks...")
        
        file_path = self.app_path / "lib" / "DatabaseManager.cpp"
        if not file_path.exists():
            print(f"  ⚠️  File not found: {file_path}")
            return
        
        content = file_path.read_text()
        
        # Look for sqlite3_prepare_v2 without finalize on error path
        if 'sqlite3_prepare_v2' in content and 'prepare_statement' in content:
            # Check if error path finalizes
            has_finalize_on_error = 'if (raw) sqlite3_finalize(raw)' in content or \
                                   'sqlite3_finalize(raw)' in content
            
            if not has_finalize_on_error:
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if 'sqlite3_prepare_v2' in line:
                        self.findings.append(BugFinding(
                            bug_id="BUG-007",
                            severity="MEDIUM",
                            file_path=str(file_path),
                            line_number=i,
                            description="sqlite3_prepare_v2 may partially allocate statement on error. Not finalized on error path.",
                            code_snippet=line.strip(),
                            found=True,
                            recommendation="Add: if (raw) sqlite3_finalize(raw); before returning on error"
                        ))
                        print(f"  ❌ FOUND at line {i}: Missing finalize on error path")
                        break
            else:
                print(f"  ✅ Error path properly finalizes statements")
    
    def check_bug_8_static_state(self):
        """Bug #8: Thread safety of static PersistentState"""
        print("\n[BUG #8] Checking for thread-unsafe static state...")
        
        file_path = self.app_path / "lib" / "GeminiClient.cpp"
        if not file_path.exists():
            print(f"  ⚠️  File not found: {file_path}")
            return
        
        content = file_path.read_text()
        
        if 'static PersistentState' in content:
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if 'static PersistentState' in line:
                    self.findings.append(BugFinding(
                        bug_id="BUG-008",
                        severity="MEDIUM",
                        file_path=str(file_path),
                        line_number=i,
                        description="Static PersistentState shared across all GeminiClient instances. Thread safety concerns with detached threads.",
                        code_snippet=line.strip(),
                        found=True,
                        recommendation="Make PersistentState a member variable or use thread-safe singleton with proper lifetime management"
                    ))
                    print(f"  ❌ FOUND at line {i}: Static shared state")
                    break
        else:
            print(f"  ✅ No static shared state found")
    
    def check_bug_9_optimize_ui(self):
        """Bug #9: Optimize operation UI shows success before checking"""
        print("\n[BUG #9] Checking for premature success message...")
        
        file_path = self.app_path / "lib" / "CacheManagerDialog.cpp"
        if not file_path.exists():
            print(f"  ⚠️  File not found: {file_path}")
            return
        
        content = file_path.read_text()
        
        if 'on_optimize_clicked' in content:
            # Check if success message comes before operation check
            lines = content.split('\n')
            in_optimize = False
            for i, line in enumerate(lines, 1):
                if 'on_optimize_clicked' in line:
                    in_optimize = True
                if in_optimize and 'QMessageBox::information' in line:
                    # Check if this comes before the actual db operation check
                    next_lines = '\n'.join(lines[i:min(i+10, len(lines))])
                    if 'optimize_database()' in next_lines and 'if' not in line:
                        self.findings.append(BugFinding(
                            bug_id="BUG-009",
                            severity="MEDIUM",
                            file_path=str(file_path),
                            line_number=i,
                            description="Success message shown before checking if optimize_database() succeeds",
                            code_snippet=line.strip(),
                            found=True,
                            recommendation="Check operation result before showing success message"
                        ))
                        print(f"  ❌ FOUND at line {i}: Premature success message")
                        break
                if in_optimize and line.strip() == '}':
                    break
    
    def check_bug_10_null_item_to_node(self):
        """Bug #10: Null check in item_to_node()"""
        print("\n[BUG #10] Checking for missing null check in item_to_node...")
        
        file_path = self.app_path / "lib" / "WhitelistTreeEditor.cpp"
        if not file_path.exists():
            print(f"  ⚠️  File not found: {file_path}")
            return
        
        content = file_path.read_text()
        
        if 'item_to_node' in content:
            # Check if child() is called without null check
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if 'item->child(' in line and 'item_to_node' in line:
                    # Check for null check nearby
                    context = '\n'.join(lines[max(0,i-3):min(i+3,len(lines))])
                    if 'if' not in context or 'nullptr' not in context:
                        self.findings.append(BugFinding(
                            bug_id="BUG-010",
                            severity="MEDIUM",
                            file_path=str(file_path),
                            line_number=i,
                            description="item->child(i) can return nullptr but passed to item_to_node without check",
                            code_snippet=line.strip(),
                            found=True,
                            recommendation="Check if child is null before recursive call"
                        ))
                        print(f"  ❌ FOUND at line {i}: Missing null check before recursive call")
                        break
    
    def check_bug_11_file_preview_error(self):
        """Bug #11: Generic file error message"""
        print("\n[BUG #11] Checking for generic file error messages...")
        
        file_path = self.app_path / "lib" / "FileTinderDialog.cpp"
        if not file_path.exists():
            print(f"  ⚠️  File not found: {file_path}")
            return
        
        content = file_path.read_text()
        
        if 'preview_file' in content and 'Unable to read file' in content:
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if 'Unable to read file' in line:
                    # Check if error reason is logged
                    context = '\n'.join(lines[max(0,i-5):i])
                    if 'errorString' not in context and 'error()' not in context:
                        self.findings.append(BugFinding(
                            bug_id="BUG-011",
                            severity="LOW",
                            file_path=str(file_path),
                            line_number=i,
                            description="Generic error message without logging specific failure reason",
                            code_snippet=line.strip(),
                            found=True,
                            recommendation="Log file.errorString() or specific error reason for debugging"
                        ))
                        print(f"  ❌ FOUND at line {i}: Generic error without details")
                        break
    
    def check_bug_12_bare_catch(self):
        """Bug #12: Bare catch(...) anti-pattern"""
        print("\n[BUG #12] Checking for bare catch(...) blocks...")
        
        file_path = self.app_path / "lib" / "GeminiClient.cpp"
        if not file_path.exists():
            print(f"  ⚠️  File not found: {file_path}")
            return
        
        content = file_path.read_text()
        lines = content.split('\n')
        
        # Look for catch(...) that's completely empty or just has {}
        pattern = r'catch\s*\(\s*\.\.\.\s*\)\s*\{\s*\}'
        
        for i, line in enumerate(lines, 1):
            if 'catch' in line and '...' in line:
                # Check if next line is just }
                if i < len(lines) and lines[i].strip() == '}':
                    self.findings.append(BugFinding(
                        bug_id="BUG-012",
                        severity="LOW",
                        file_path=str(file_path),
                        line_number=i,
                        description="Bare catch(...) swallows all exceptions including system errors",
                        code_snippet=line.strip(),
                        found=True,
                        recommendation="Catch specific exceptions: catch(const std::exception& e) and log error"
                    ))
                    print(f"  ❌ FOUND at line {i}: Bare catch(...) {{}} block")
    
    def generate_report(self) -> Dict:
        """Generate comprehensive diagnostic report"""
        print("\n" + "=" * 80)
        print("DIAGNOSTIC REPORT SUMMARY")
        print("=" * 80)
        
        critical = [f for f in self.findings if f.severity == "CRITICAL"]
        high = [f for f in self.findings if f.severity == "HIGH"]
        medium = [f for f in self.findings if f.severity == "MEDIUM"]
        low = [f for f in self.findings if f.severity == "LOW"]
        
        print(f"\n📊 Results:")
        print(f"  CRITICAL: {len(critical)} issues")
        print(f"  HIGH:     {len(high)} issues")
        print(f"  MEDIUM:   {len(medium)} issues")
        print(f"  LOW:      {len(low)} issues")
        print(f"  TOTAL:    {len(self.findings)} issues found")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "repository": str(self.repo_path),
            "total_issues": len(self.findings),
            "by_severity": {
                "critical": len(critical),
                "high": len(high),
                "medium": len(medium),
                "low": len(low)
            },
            "findings": [asdict(f) for f in self.findings]
        }
        
        # Save report
        report_path = self.repo_path / "diagnostic_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_path}")
        
        # Print critical issues
        if critical:
            print("\n🚨 CRITICAL ISSUES (fix immediately):")
            for f in critical:
                print(f"  - {f.bug_id}: {f.description}")
                print(f"    File: {f.file_path}:{f.line_number}")
                print(f"    Fix: {f.recommendation}")
        
        print("\n" + "=" * 80)
        print("For detailed analysis, see: BUG_ANALYSIS_REPORT.md")
        print("=" * 80)
        
        return report

def main():
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = os.getcwd()
    
    tool = DiagnosticTool(repo_path)
    report = tool.run_all_checks()
    
    # Exit with error code if critical/high issues found
    critical_high = report['by_severity']['critical'] + report['by_severity']['high']
    sys.exit(1 if critical_high > 0 else 0)

if __name__ == "__main__":
    main()
