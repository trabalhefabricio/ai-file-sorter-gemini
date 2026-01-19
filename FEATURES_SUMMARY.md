# AI File Sorter - Features Summary (Original Repository)

This document provides a comprehensive overview of features in the **original hyperfield/ai-file-sorter repository**.

For **custom features added in this fork (trabalhefabricio/ai-file-sorter-iconic)**, see [FORK_FEATURES.md](FORK_FEATURES.md).

---

## Currently Implemented Features

### Version 1.4.5 (Latest - December 2025)
- ✅ **Gemini API Support** - Added support for Google's Gemini LLM as a remote model option
  - Users can bring their own Gemini API key
  - Supports models like `gemini-2.5-flash-lite`, `gemini-2.5-flash`, and `gemini-2.5-pro`
- ✅ **Arch Linux Compatibility** - Fixed compilation issues on Arch Linux

### Version 1.4.0 (December 2025)
- ✅ **Dry Run / Preview Mode** - Preview file moves without actually performing them
  - Shows From→To table of planned moves
  - Files are not moved until "Dry run" is unchecked
- ✅ **Persistent Undo** - Undo file sorting operations even after closing dialogs
  - Latest sort saves a plan file
  - Access via Edit → "Undo last run"
  - Best-effort restoration (skips conflicts/changes)
- ✅ **UI Improvements**
  - Name column auto-resizes
  - New translations for dry run/undo strings
  - Undo moved to top of Edit menu
- ✅ **Bring Your Own API Key** - Users now provide their own OpenAI API key
  - Removed bundled remote key
  - Supports any ChatGPT model (gpt-4o-mini, gpt-4.1, o3-mini, etc.)

### Version 1.3.0 (November 2025)
- ✅ **Dual Categorization Modes**
  - **More Refined** - Flexible, detail-oriented categorization with specific categories
  - **More Consistent** - Uniform categorization with consistency hints for batch processing
- ✅ **Category Whitelists** - Constrain LLM output to predefined categories
  - Create and manage named whitelists under Settings → Manage category whitelists
  - Support for multiple named lists for different projects
  - Can enable/disable whitelists per session
- ✅ **Sortable Review Table** - Sort files by name, category, or subcategory in review dialog
- ✅ **Custom Local LLM Support** - Register your own local GGUF models directly from Select LLM dialog
- ✅ **Multilingual Categorization** - Categories can be assigned in multiple languages:
  - Dutch, French, German, Italian, Polish, Portuguese, Spanish, Turkish
  - Model-dependent feature
- ✅ **Multilingual UI** - Interface translations for:
  - Dutch, French, German, Italian, Polish, Portuguese, Spanish, Turkish

### Version 1.1.0 (November 2025)
- ✅ **Vulkan Support** - GPU acceleration for non-NVIDIA graphics cards
  - Works with AMD, Intel, and other Vulkan 1.2+ compatible GPUs
- ✅ **Subcategory Toggle** - Enable/disable subcategories in categorization review dialog
- ✅ **Undo File Sort** - Basic undo functionality for recent file sort operations
- ✅ **CTest Integration** - Added CTest-integrated test suite with expanded coverage
- ✅ **Code Optimization** - Various refactors for better stability

### Version 1.0.0 (October 2025)
- ✅ **Qt6 Migration** - Complete UI rewrite from GTK/Glade to native Qt6
- ✅ **File Selection Checkboxes** - Select individual files in categorization review dialog
- ✅ **Internationalization Framework** - i18n support with French translation
- ✅ **Refreshed UI**
  - New menu icons
  - Mnemonic behavior
  - Persistent File Explorer settings
- ✅ **Simplified Cross-Platform Builds** - Unified build system for Linux/macOS around Qt6
- ✅ **CMake for Windows** - Modernized Windows build pipeline with CMake

### Version 0.9.7 (October 2025)
- ✅ **Enhanced Context** - File paths included in LLM requests for better context
- ✅ **Taxonomy System** - Improved consistency in category assignments
  - Narrows down the number of categories and subcategories
  - Builds smarter internal reference for file types and naming patterns
- ✅ **Improved CUDA Stability** - Better CUDA detection and interaction
- ✅ **Enhanced Logging** - Increased logging coverage throughout codebase

### Version 0.9.0 (July 2025)
- ✅ **Local LLM Support** - Integration with llama.cpp for offline file categorization
  - Supports LLaMa 3B, Mistral 7B, and other GGUF models
  - No internet connection required for local models
- ✅ **LLM Selection Dialog** - Download and manage local language models
- ✅ **Improved Build System** - Hassle-free Makefile for build and installation

### Core Features (Present Since Early Versions)
- ✅ **AI-Powered Categorization** - Intelligent file classification using LLMs
- ✅ **Offline-Friendly** - Complete functionality without internet (using local LLMs)
- ✅ **Multiple LLM Backends**
  - Local models (LLaMa, Mistral via llama.cpp)
  - Remote models (ChatGPT with OpenAI API, Gemini with Google AI Studio API)
- ✅ **Cross-Platform Support** - Windows, macOS, and Linux
- ✅ **GPU Acceleration** - Multiple backend support:
  - CUDA for NVIDIA cards
  - Vulkan for AMD/Intel/other cards
  - Apple Metal for macOS
  - Automatic fallback to CPU/OpenBLAS
- ✅ **Local Database Caching** - Speeds up repeated categorization
- ✅ **Customizable Rules** - Automatic category and subcategory assignment
- ✅ **Update Notifications** - Optional or required update flows

## Features In Development / Planned

### Actively In Development
- 🔨 **Content-Based Sorting** - Sort files based on their actual content (not just filenames)
  - Status: "in development" per README line 34
  - Applies to certain file types
  - Will enable more accurate categorization for files with generic or unclear names
  - See prototype code in `prototypes/constrained_taxonomy/`

### Planned Features
- 📋 **Native Windows Build Instructions** - Complete documentation for native Qt/MSVC builds on Windows
  - Status: "planned" per README line 130
  - Currently Windows builds are provided as binaries
  - Documentation will enable users to build from source on Windows

### Prototype/Experimental Features
- 🧪 **Constrained Taxonomy Pipeline** - Advanced controlled vocabulary system
  - Location: `prototypes/constrained_taxonomy/`
  - Goal: Map file types to curated (category, subcategory) pairs
  - Features:
    - Template lists for known file type fingerprints
    - Constrained LLM prompts that only expose relevant templates
    - Lightweight type detection using extensions and file command output
  - Status: Experimental, not yet integrated into main application
  - Next steps per prototype README:
    - Flesh out templates map with real production taxonomy data
    - Integrate type detection (extensions + file command)
    - Transplant logic into CategorizationService behind feature flag

## Feature Evolution Timeline

### Major Milestones
1. **July 2025** - Local LLM support (v0.9.0) - Made app fully offline-capable
2. **October 2025** - Qt6 migration (v1.0.0) - Complete UI modernization
3. **November 2025** - Vulkan support (v1.1.0) - Expanded GPU compatibility beyond NVIDIA
4. **November 2025** - Dual categorization modes (v1.3.0) - Flexible vs. consistent sorting
5. **December 2025** - Dry run & persistent undo (v1.4.0) - Safe preview and rollback
6. **December 2025** - Gemini support (v1.4.5) - Additional remote LLM option

### Feature Categories

#### Categorization Intelligence
- ✅ Taxonomy-based system
- ✅ Consistency hints (More Consistent mode)
- ✅ Flexibility (More Refined mode)
- ✅ Category whitelists
- ✅ Multilingual categories
- 🔨 Content-based analysis (in development)

#### User Experience
- ✅ Qt6 interface
- ✅ Multilingual UI (8 languages)
- ✅ Sortable review tables
- ✅ File selection checkboxes
- ✅ Dry run/preview mode
- ✅ Persistent undo

#### AI/LLM Features
- ✅ Local LLM support (llama.cpp)
- ✅ Custom local model registration
- ✅ OpenAI ChatGPT support (BYOK)
- ✅ Google Gemini support (BYOK)
- ✅ Local database caching

#### Performance & Compatibility
- ✅ CUDA acceleration (NVIDIA)
- ✅ Vulkan acceleration (AMD/Intel/others)
- ✅ Apple Metal acceleration (macOS)
- ✅ CPU/OpenBLAS fallback
- ✅ Cross-platform (Windows/macOS/Linux)
- ✅ Runtime backend detection

#### Developer Features
- ✅ CMake build system
- ✅ CTest integration
- ✅ Enhanced logging with spdlog
- 📋 Native Windows build docs (planned)

## Summary

**Total Implemented Features:** 40+ major features across 8 versions
**Features In Development:** 1 (Content-based sorting)
**Planned Features:** 1+ (Native Windows build documentation)
**Experimental Prototypes:** 1 (Constrained taxonomy pipeline)

The project has shown consistent development with major releases every 1-3 months, focusing on:
- Enhanced AI capabilities (multiple LLMs, modes, languages)
- Improved user experience (undo, preview, multilingual UI)
- Broader hardware support (Vulkan, Metal, CUDA)
- Modern development practices (Qt6, CMake, testing)

The primary feature still in active development is **content-based sorting**, which will analyze file contents rather than just names for more accurate categorization.
