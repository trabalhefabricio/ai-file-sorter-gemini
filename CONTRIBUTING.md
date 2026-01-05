# Contributing to AI File Sorter

Thank you for your interest in contributing to AI File Sorter! This document explains how to report bugs, request features, and contribute code.

## Table of Contents

- [Reporting Bugs](#reporting-bugs)
- [Requesting Features](#requesting-features)
- [Contributing Code](#contributing-code)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)

## Reporting Bugs

We've made bug reporting as easy as possible! Here's the process:

### Quick Start: Using Issue Templates

1. Go to [Issues](../../issues)
2. Click "New Issue"
3. Select "🐛 Bug Report" template
4. Fill out the form (most fields are required)
5. Submit!

### What Makes a Good Bug Report?

A good bug report includes:

✅ **Clear title**: `[Bug]: Application crashes when clicking Analyze button`  
✅ **Steps to reproduce**: Detailed, numbered steps  
✅ **Expected vs Actual behavior**: What should happen vs what actually happens  
✅ **System information**: OS, version, installation method  
✅ **Error messages**: Copy any error dialogs or console output  
✅ **Log files**: Attach or paste from error logs  

❌ **Poor**: "App doesn't work"  
✅ **Good**: "Application crashes with QTableView error when analyzing folders with 1000+ files on Windows 11"

### Finding Log Files

Error logs are located at:

- **Windows**: `%APPDATA%\aifilesorter\logs\errors.log`
- **Linux**: `~/.cache/aifilesorter/logs/errors.log`
- **macOS**: `~/Library/Application Support/aifilesorter/logs/errors.log`

### For Copilot Users

If the application created a `COPILOT_ERROR_*.md` file (same logs directory), please paste its contents in the "Copilot Error File" section of the bug report. This file contains detailed context that helps diagnose issues quickly.

See [ERROR_REPORTING_FOR_COPILOT_USERS.md](ERROR_REPORTING_FOR_COPILOT_USERS.md) for details.

### What Happens After You Report?

1. **Automated Triage** (within 24 hours): An AI assistant or developer will analyze your report and:
   - Classify the bug (priority, category)
   - Check for duplicates
   - Suggest initial diagnosis
   - Request additional information if needed

2. **Investigation**: If it's a new bug, a developer will:
   - Attempt to reproduce
   - Identify root cause
   - Propose a fix

3. **Fix**: The bug will be fixed in:
   - **Hotfix release** (within days) for critical bugs
   - **Next regular release** (within weeks) for normal bugs
   - **Future release** (when convenient) for minor issues

4. **Notification**: You'll be notified when:
   - The bug is confirmed
   - A fix is in progress
   - A fix is released

## Requesting Features

Have an idea for improvement? We'd love to hear it!

### Using the Feature Request Template

1. Go to [Issues](../../issues)
2. Click "New Issue"
3. Select "✨ Feature Request" template
4. Fill out the form
5. Submit!

### What Makes a Good Feature Request?

✅ **Problem statement**: What need does this address?  
✅ **Proposed solution**: How should it work?  
✅ **Use cases**: When would this be useful?  
✅ **Alternatives**: What else have you considered?  

### Feature Request Process

1. **Community Feedback** (1-2 weeks): Other users can comment and vote (👍)
2. **Feasibility Analysis**: Maintainers evaluate technical feasibility
3. **Roadmap Decision**: If approved, added to roadmap
4. **Implementation**: Implemented based on priority

Check [FUTURE_IMPROVEMENTS.md](FUTURE_IMPROVEMENTS.md) to see planned features.

## Contributing Code

We welcome code contributions! Here's how:

### Before You Start

1. **Check for existing issues**: Look for related issues or feature requests
2. **Discuss first**: For major changes, create an issue to discuss the approach
3. **Read the code**: Familiarize yourself with the codebase structure

### Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/ai-file-sorter-iconic.git
cd ai-file-sorter-iconic
git submodule update --init --recursive
```

### Create a Branch

```bash
# Create a descriptive branch name
git checkout -b feature/add-batch-processing
# or
git checkout -b fix/qtableview-crash
```

### Make Your Changes

Follow the [Code Style](#code-style) guidelines below.

### Test Your Changes

```bash
# Build
cd app
make -j4

# Run tests (if applicable)
cd ../tests
./run_tests.sh

# Test manually
cd ../app/bin
./aifilesorter  # or StartAiFileSorter.exe on Windows
```

### Commit Your Changes

```bash
git add .
git commit -m "Add batch processing for large directories

- Implement batch size setting (default 500 files)
- Add progress tracking across batches
- Add pause/resume functionality
- Update UI to show current batch

Fixes #123"
```

**Commit message guidelines:**
- First line: Brief summary (50 chars or less)
- Blank line
- Detailed description of changes
- Reference related issues: `Fixes #123`, `Related to #456`

### Push and Create Pull Request

```bash
git push origin feature/add-batch-processing
```

Then:
1. Go to your fork on GitHub
2. Click "Pull Request"
3. Fill out the PR template
4. Submit!

### Pull Request Review

A maintainer will:
1. Review your code
2. Suggest changes if needed
3. Merge when approved

## Development Setup

### Prerequisites

See [README.md - Requirements](README.md#requirements) for full list.

**Essential:**
- C++20 compiler (GCC 11+, Clang 13+, MSVC 2022+)
- Qt 6.5+ (Core, Gui, Widgets)
- CMake 3.21+

**Recommended:**
- IDE: Visual Studio Code with C++ extensions, Qt Creator, or Visual Studio
- Debugger: GDB, LLDB, or MSVC debugger
- Git GUI: GitKraken, GitHub Desktop, or command line

### Building from Source

**Linux:**
```bash
# Install dependencies (Ubuntu/Debian)
sudo apt install -y build-essential cmake git \
  qt6-base-dev qt6-tools-dev-tools \
  libcurl4-openssl-dev libjsoncpp-dev libsqlite3-dev \
  libssl-dev libfmt-dev libspdlog-dev

# Clone and build
git clone https://github.com/trabalhefabricio/ai-file-sorter-iconic.git
cd ai-file-sorter-iconic
git submodule update --init --recursive

# Build llama.cpp
./app/scripts/build_llama_linux.sh cuda=off vulkan=off

# Build application
cd app
make -j4
```

**Windows:**
```powershell
# Prerequisites: Visual Studio 2022, vcpkg

# Clone and build
git clone https://github.com/trabalhefabricio/ai-file-sorter-iconic.git
cd ai-file-sorter-iconic
git submodule update --init --recursive

# Build llama.cpp
app\scripts\build_llama_windows.ps1 cuda=off vulkan=off vcpkgroot=C:\dev\vcpkg

# Build application
app\build_windows.ps1 -Configuration Release -VcpkgRoot C:\dev\vcpkg
```

**macOS:**
```bash
# Install dependencies
brew install qt curl jsoncpp sqlite openssl fmt spdlog cmake git

# Clone and build
git clone https://github.com/trabalhefabricio/ai-file-sorter-iconic.git
cd ai-file-sorter-iconic
git submodule update --init --recursive

# Build llama.cpp
./app/scripts/build_llama_macos.sh

# Build application
cd app
make -j4
```

See [README.md - Installation](README.md#installation) for full instructions.

## Code Style

### General Principles

- **Modern C++**: Use C++20 features where appropriate
- **RAII**: Prefer smart pointers and RAII patterns
- **Const correctness**: Use `const` liberally
- **Naming**: Follow existing conventions

### Naming Conventions

```cpp
// Classes: PascalCase
class FileProcessor { };

// Functions/methods: snake_case
void process_file();

// Variables: snake_case
std::string file_path;
int file_count;

// Constants: UPPER_SNAKE_CASE
constexpr int MAX_FILES = 1000;

// Namespaces: lowercase
namespace file_utils { }

// Private members: trailing underscore (optional)
class MyClass {
private:
    int count_;
    std::string name_;
};
```

### Code Formatting

We use `.clang-format` in the repository root. Before committing:

```bash
# Format all changed files
clang-format -i app/lib/MyFile.cpp app/include/MyFile.hpp
```

### Best Practices

See [BUGFIXING_GUIDE.md](BUGFIXING_GUIDE.md) for comprehensive guidelines on:
- Memory safety
- Thread safety
- Error handling
- Resource management
- Qt-specific patterns

**Key principles:**
- ✅ Use smart pointers (`unique_ptr`, `shared_ptr`)
- ✅ Check optional values before accessing
- ✅ Use `std::lock_guard` instead of manual locking
- ✅ Handle all error cases
- ✅ Validate user input
- ✅ Log errors with context

## Testing

### Running Tests

```bash
# Build tests
cd tests
cmake -S . -B build -DAI_FILE_SORTER_BUILD_TESTS=ON
cmake --build build

# Run tests
ctest --test-dir build --output-on-failure
```

### Writing Tests

We use Catch2 for unit tests:

```cpp
#include <catch2/catch_test_macros.hpp>
#include "MyClass.hpp"

TEST_CASE("MyClass processes files correctly", "[file-processing]") {
    MyClass processor;
    
    SECTION("handles empty input") {
        auto result = processor.process({});
        REQUIRE(result.empty());
    }
    
    SECTION("processes single file") {
        auto result = processor.process({"file.txt"});
        REQUIRE(result.size() == 1);
    }
}
```

### Manual Testing

For UI changes, please:
1. Test on your primary platform
2. Take screenshots of changes
3. Include screenshots in PR description
4. Test with different window sizes
5. Test with different themes (if applicable)

## Documentation

### Code Comments

- **Do**: Explain WHY, not WHAT
- **Don't**: State the obvious

```cpp
// ❌ Bad: States the obvious
// Increment the counter
counter++;

// ✅ Good: Explains the reason
// Skip first item as it's the header row
counter++;
```

### API Documentation

Use Doxygen-style comments for public APIs:

```cpp
/**
 * @brief Processes a batch of files for categorization
 * 
 * @param files Vector of file paths to process
 * @param batch_size Maximum files to process at once (default: 500)
 * @return ProcessingResult containing categorized files and any errors
 * 
 * @throws FileNotFoundException if any input file doesn't exist
 * @throws OutOfMemoryException if batch_size too large
 */
ProcessingResult process_batch(
    const std::vector<std::string>& files,
    size_t batch_size = 500
);
```

### User-Facing Documentation

When adding features:
- Update README.md with usage instructions
- Add examples
- Update CHANGELOG.md
- Consider adding a guide (like ERROR_REPORTER_GUIDE.md)

## Questions?

- **General questions**: Use [GitHub Discussions](../../discussions)
- **Bug questions**: Comment on the relevant issue
- **Contributing questions**: Create a [discussion](../../discussions/new?category=q-a)

## Code of Conduct

Be respectful, constructive, and professional. We're all here to make AI File Sorter better!

## License

By contributing, you agree that your contributions will be licensed under the GNU AGPL v3 license. See [LICENSE](LICENSE) for details.

---

**Thank you for contributing to AI File Sorter!** 🎉

Your contributions help make file organization easier for everyone.
