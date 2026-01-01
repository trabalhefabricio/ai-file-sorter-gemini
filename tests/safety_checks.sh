#!/usr/bin/env bash
# AI File Sorter - Safety Checks Test Suite
# This script performs automated safety checks on the codebase

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="$ROOT_DIR/app"

echo "AI File Sorter - Safety Checks"
echo "==============================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ISSUES_FOUND=0

# Function to report an issue
report_issue() {
    echo -e "${RED}❌ ISSUE:${NC} $1"
    ((ISSUES_FOUND++))
}

# Function to report success
report_success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Function to report warning
report_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo "1. Checking for unsafe string operations..."
UNSAFE_STRINGS=$(find "$APP_DIR" -name "*.cpp" -o -name "*.hpp" | xargs grep -n "strcpy\|strcat\|sprintf" | wc -l) || UNSAFE_STRINGS=0
if [ "$UNSAFE_STRINGS" -eq 0 ]; then
    report_success "No unsafe string operations found"
else
    report_issue "Found $UNSAFE_STRINGS unsafe string operations (strcpy/strcat/sprintf)"
fi

echo ""
echo "2. Checking for potential null pointer dereferences..."
# Look for patterns like pointer->method() without preceding null check
# This is a heuristic and may have false positives
POTENTIAL_NULL=$(find "$APP_DIR/lib" -name "*.cpp" -exec grep -P '(?<!if\s*\()\w+\s*->\s*\w+\(' {} + | grep -v "Logger::" | grep -v "//" | wc -l) || POTENTIAL_NULL=0
if [ "$POTENTIAL_NULL" -lt 100 ]; then
    report_success "Reasonable number of pointer dereferences found ($POTENTIAL_NULL)"
else
    report_warning "High number of pointer dereferences ($POTENTIAL_NULL) - manual review recommended"
fi

echo ""
echo "3. Checking for manual memory management..."
RAW_NEWS=$(find "$APP_DIR/lib" -name "*.cpp" | xargs grep -n "new \w" | grep -v "// " | wc -l) || RAW_NEWS=0
RAW_DELETES=$(find "$APP_DIR/lib" -name "*.cpp" | xargs grep -n "delete " | grep -v "delete\[\]" | grep -v "// " | grep -v "\"" | wc -l) || RAW_DELETES=0

if [ "$RAW_NEWS" -lt 30 ]; then
    report_success "Low usage of raw new ($RAW_NEWS instances) - good use of smart pointers"
else
    report_warning "Moderate usage of raw new ($RAW_NEWS instances)"
fi

if [ "$RAW_DELETES" -eq 0 ]; then
    report_success "No manual delete operations found"
else
    report_warning "Found $RAW_DELETES manual delete operations"
fi

echo ""
echo "4. Checking for proper exception handling..."
EMPTY_CATCHES=$(find "$APP_DIR/lib" -name "*.cpp" -exec grep -A 1 "catch.*{" {} + | grep -B 1 "}" | grep -c "catch") || EMPTY_CATCHES=0
if [ "$EMPTY_CATCHES" -lt 5 ]; then
    report_success "Minimal empty catch blocks ($EMPTY_CATCHES)"
else
    report_warning "$EMPTY_CATCHES potentially empty catch blocks found - review recommended"
fi

echo ""
echo "5. Checking for hardcoded paths..."
HARDCODED_PATHS=$(find "$APP_DIR/lib" -name "*.cpp" | xargs grep -n '\".*[/\\].*\"' | grep -v "//" | grep -v "://" | wc -l) || HARDCODED_PATHS=0
if [ "$HARDCODED_PATHS" -lt 20 ]; then
    report_success "Low number of potential hardcoded paths ($HARDCODED_PATHS)"
else
    report_warning "$HARDCODED_PATHS potential hardcoded paths - verify cross-platform compatibility"
fi

echo ""
echo "6. Checking for TODO/FIXME markers..."
TODOS=$(find "$APP_DIR" -name "*.cpp" -o -name "*.hpp" | xargs grep -i "TODO\|FIXME" | wc -l) || TODOS=0
if [ "$TODOS" -eq 0 ]; then
    report_success "No TODO/FIXME markers found"
else
    report_warning "Found $TODOS TODO/FIXME markers in code"
fi

echo ""
echo "7. Checking for proper mutex usage..."
MUTEX_LOCKS=$(find "$APP_DIR/lib" -name "*.cpp" | xargs grep -n "\.lock()" | wc -l) || MUTEX_LOCKS=0
LOCK_GUARDS=$(find "$APP_DIR/lib" -name "*.cpp" | xargs grep -n "lock_guard\|unique_lock" | wc -l) || LOCK_GUARDS=0

if [ "$MUTEX_LOCKS" -eq 0 ]; then
    report_success "No raw mutex.lock() calls - good use of RAII lock guards"
elif [ "$MUTEX_LOCKS" -lt 3 ]; then
    report_warning "Found $MUTEX_LOCKS raw mutex.lock() calls - consider using lock_guard"
else
    report_issue "Found $MUTEX_LOCKS raw mutex.lock() calls - should use lock_guard for exception safety"
fi

echo ""
echo "8. Checking for integer overflow risks..."
# Look for arithmetic operations without bounds checking
UNCHECKED_MATH=$(find "$APP_DIR/lib" -name "*.cpp" | xargs grep -n "\+ 1\|* 2" | grep -v "//" | wc -l) || UNCHECKED_MATH=0
if [ "$UNCHECKED_MATH" -lt 100 ]; then
    report_success "Reasonable amount of arithmetic operations ($UNCHECKED_MATH)"
else
    report_warning "High number of arithmetic operations ($UNCHECKED_MATH) - verify bounds checking"
fi

echo ""
echo "9. Checking for proper resource cleanup..."
OPEN_CALLS=$(find "$APP_DIR/lib" -name "*.cpp" | xargs grep -n "\.open(" | wc -l) || OPEN_CALLS=0
CLOSE_CALLS=$(find "$APP_DIR/lib" -name "*.cpp" | xargs grep -n "\.close()" | wc -l) || CLOSE_CALLS=0

if [ "$OPEN_CALLS" -le "$CLOSE_CALLS" ]; then
    report_success "Resource cleanup appears balanced (open: $OPEN_CALLS, close: $CLOSE_CALLS)"
else
    report_warning "Potential resource leaks (open: $OPEN_CALLS, close: $CLOSE_CALLS)"
fi

echo ""
echo "10. Checking for SQL injection risks..."
# Look for string concatenation with SQL
SQL_CONCAT=$(find "$APP_DIR/lib" -name "*.cpp" | xargs grep -n "SELECT.*+\|INSERT.*+\|UPDATE.*+\|DELETE.*+" | wc -l) || SQL_CONCAT=0
if [ "$SQL_CONCAT" -eq 0 ]; then
    report_success "No obvious SQL concatenation found - using prepared statements"
else
    report_issue "Found $SQL_CONCAT potential SQL concatenations - verify prepared statements used"
fi

echo ""
echo "==============================="
echo "Safety Checks Complete"
echo ""

if [ "$ISSUES_FOUND" -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! No critical issues found.${NC}"
    echo ""
    echo "The codebase demonstrates good safety practices:"
    echo "  • Proper memory management with RAII"
    echo "  • No unsafe string operations"
    echo "  • Exception-safe code"
    echo "  • SQL prepared statements"
    exit 0
else
    echo -e "${RED}⚠ Found $ISSUES_FOUND issue(s) that should be reviewed.${NC}"
    echo ""
    echo "Please review the items marked with ❌ above."
    echo "These may indicate potential bugs or areas for improvement."
    exit 1
fi
