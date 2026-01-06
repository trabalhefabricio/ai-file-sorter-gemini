@echo off
REM AI File Sorter - Emergency Diagnostic Script
REM Run this if the application won't start
REM This script collects diagnostic information and attempts basic fixes

echo ========================================
echo AI File Sorter Emergency Diagnostics
echo ========================================
echo.

REM Get script directory
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo Current directory: %CD%
echo.

REM Create diagnostic output file
set DIAG_FILE=emergency_diagnostic_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt
set DIAG_FILE=%DIAG_FILE: =0%
echo Writing diagnostic information to: %DIAG_FILE%
echo.

REM Start diagnostic file
echo AI File Sorter Emergency Diagnostic Report > %DIAG_FILE%
echo Generated: %date% %time% >> %DIAG_FILE%
echo Directory: %CD% >> %DIAG_FILE%
echo. >> %DIAG_FILE%

REM Check for critical executables
echo [1/8] Checking for executables...
echo ========================================  >> %DIAG_FILE%
echo EXECUTABLE CHECK >> %DIAG_FILE%
echo ========================================  >> %DIAG_FILE%

if exist "aifilesorter.exe" (
    echo   [OK] aifilesorter.exe found
    echo [OK] aifilesorter.exe found >> %DIAG_FILE%
) else (
    echo   [FAIL] aifilesorter.exe MISSING
    echo [FAIL] aifilesorter.exe MISSING >> %DIAG_FILE%
)

if exist "StartAiFileSorter.exe" (
    echo   [OK] StartAiFileSorter.exe found
    echo [OK] StartAiFileSorter.exe found >> %DIAG_FILE%
) else (
    echo   [FAIL] StartAiFileSorter.exe MISSING
    echo [FAIL] StartAiFileSorter.exe MISSING >> %DIAG_FILE%
)
echo.
echo. >> %DIAG_FILE%

REM Check for critical DLLs
echo [2/8] Checking for critical DLLs...
echo ========================================  >> %DIAG_FILE%
echo DLL CHECK >> %DIAG_FILE%
echo ========================================  >> %DIAG_FILE%

set DLL_MISSING=0

for %%D in (Qt6Core.dll Qt6Gui.dll Qt6Widgets.dll) do (
    if exist "%%D" (
        echo   [OK] %%D
        echo [OK] %%D >> %DIAG_FILE%
    ) else (
        echo   [FAIL] %%D MISSING
        echo [FAIL] %%D MISSING >> %DIAG_FILE%
        set DLL_MISSING=1
    )
)
echo.
echo. >> %DIAG_FILE%

REM Check GGML directories
echo [3/8] Checking GGML directories...
echo ========================================  >> %DIAG_FILE%
echo GGML DIRECTORIES >> %DIAG_FILE%
echo ========================================  >> %DIAG_FILE%

if exist "lib\ggml\wocuda" (
    echo   [OK] lib\ggml\wocuda exists
    echo [OK] lib\ggml\wocuda exists >> %DIAG_FILE%
    dir lib\ggml\wocuda\*.dll >> %DIAG_FILE% 2>&1
) else (
    echo   [FAIL] lib\ggml\wocuda MISSING
    echo [FAIL] lib\ggml\wocuda MISSING >> %DIAG_FILE%
)

if exist "lib\ggml\wcuda" (
    echo   [OK] lib\ggml\wcuda exists
    echo [OK] lib\ggml\wcuda exists >> %DIAG_FILE%
) else (
    echo   [INFO] lib\ggml\wcuda not found (optional)
    echo [INFO] lib\ggml\wcuda not found >> %DIAG_FILE%
)

if exist "lib\ggml\wvulkan" (
    echo   [OK] lib\ggml\wvulkan exists
    echo [OK] lib\ggml\wvulkan exists >> %DIAG_FILE%
) else (
    echo   [INFO] lib\ggml\wvulkan not found (optional)
    echo [INFO] lib\ggml\wvulkan not found >> %DIAG_FILE%
)
echo.
echo. >> %DIAG_FILE%

REM Check Qt in PATH
echo [4/8] Checking for Qt conflicts in PATH...
echo ========================================  >> %DIAG_FILE%
echo PATH CHECK >> %DIAG_FILE%
echo ========================================  >> %DIAG_FILE%
echo %PATH% | findstr /i "qt" > nul
if %ERRORLEVEL% EQU 0 (
    echo   [WARN] Qt found in system PATH - may cause conflicts
    echo [WARN] Qt found in system PATH: >> %DIAG_FILE%
    echo %PATH% | findstr /i "qt" >> %DIAG_FILE%
) else (
    echo   [OK] No Qt in system PATH
    echo [OK] No Qt in system PATH >> %DIAG_FILE%
)
echo.
echo. >> %DIAG_FILE%

REM Check for log files
echo [5/8] Checking for existing log files...
echo ========================================  >> %DIAG_FILE%
echo LOG FILES >> %DIAG_FILE%
echo ========================================  >> %DIAG_FILE%

if exist "startup_log.txt" (
    echo   [INFO] Found startup_log.txt
    echo [INFO] Found startup_log.txt >> %DIAG_FILE%
    echo. >> %DIAG_FILE%
    echo *** Last 20 lines of startup_log.txt: *** >> %DIAG_FILE%
    powershell -Command "Get-Content startup_log.txt -Tail 20" >> %DIAG_FILE% 2>&1
    echo. >> %DIAG_FILE%
) else (
    echo   [INFO] No startup_log.txt found
    echo [INFO] No startup_log.txt found >> %DIAG_FILE%
)

if exist "logs\errors.log" (
    echo   [INFO] Found logs\errors.log
    echo [INFO] Found logs\errors.log >> %DIAG_FILE%
    echo. >> %DIAG_FILE%
    echo *** Last 20 lines of errors.log: *** >> %DIAG_FILE%
    powershell -Command "Get-Content logs\errors.log -Tail 20" >> %DIAG_FILE% 2>&1
    echo. >> %DIAG_FILE%
) else (
    echo   [INFO] No logs\errors.log found
    echo [INFO] No logs\errors.log found >> %DIAG_FILE%
)
echo.
echo. >> %DIAG_FILE%

REM Check Windows version
echo [6/8] Checking Windows version...
echo ========================================  >> %DIAG_FILE%
echo SYSTEM INFORMATION >> %DIAG_FILE%
echo ========================================  >> %DIAG_FILE%
ver >> %DIAG_FILE%
echo. >> %DIAG_FILE%

REM Check if running as admin
echo [7/8] Checking administrator privileges...
net session >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Running as Administrator
    echo [OK] Running as Administrator >> %DIAG_FILE%
) else (
    echo   [WARN] NOT running as Administrator
    echo [WARN] NOT running as Administrator >> %DIAG_FILE%
    echo   TIP: Right-click StartAiFileSorter.exe and select "Run as Administrator"
)
echo.
echo. >> %DIAG_FILE%

REM Try to run diagnostic tool if it exists
echo [8/8] Running diagnostic tool (if available)...
if exist "diagnose_startup.exe" (
    echo   Running diagnose_startup.exe...
    echo. >> %DIAG_FILE%
    echo ========================================  >> %DIAG_FILE%
    echo DIAGNOSTIC TOOL OUTPUT >> %DIAG_FILE%
    echo ========================================  >> %DIAG_FILE%
    diagnose_startup.exe >> %DIAG_FILE% 2>&1
) else (
    echo   [INFO] diagnose_startup.exe not found (not critical)
    echo [INFO] diagnose_startup.exe not found >> %DIAG_FILE%
)
echo.
echo. >> %DIAG_FILE%

REM Summary
echo ========================================  >> %DIAG_FILE%
echo RECOMMENDATIONS >> %DIAG_FILE%
echo ========================================  >> %DIAG_FILE%

echo.
echo ========================================
echo Summary
echo ========================================

if %DLL_MISSING% EQU 1 (
    echo.
    echo [CRITICAL] Missing DLLs detected!
    echo.
    echo SOLUTION: Reinstall the application or copy missing DLLs
    echo. >> %DIAG_FILE%
    echo [CRITICAL] Missing DLLs - reinstall required >> %DIAG_FILE%
)

if not exist "StartAiFileSorter.exe" (
    echo.
    echo [CRITICAL] StartAiFileSorter.exe is missing!
    echo.
    echo SOLUTION: Reinstall the application
    echo. >> %DIAG_FILE%
    echo [CRITICAL] StartAiFileSorter.exe missing - reinstall required >> %DIAG_FILE%
)

echo.
echo Diagnostic information saved to:
echo %DIAG_FILE%
echo.
echo NEXT STEPS:
echo 1. Review the diagnostic file: %DIAG_FILE%
echo 2. Try running: StartAiFileSorter.exe (right-click, Run as Administrator)
echo 3. If still failing, read TROUBLESHOOTING_STARTUP.md
echo 4. Submit bug report with diagnostic file attached
echo.

echo. >> %DIAG_FILE%
echo END OF DIAGNOSTIC REPORT >> %DIAG_FILE%

echo Press any key to open the diagnostic file...
pause > nul
notepad %DIAG_FILE%
