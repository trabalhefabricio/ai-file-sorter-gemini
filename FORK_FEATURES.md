# AI File Sorter "Iconic" Fork - Custom Features

This document lists features and improvements added by @trabalhefabricio to the `ai-file-sorter-iconic` fork of the original `hyperfield/ai-file-sorter` repository.

## Repository Context

- **Original Repository**: [hyperfield/ai-file-sorter](https://github.com/hyperfield/ai-file-sorter)
- **Fork Repository**: [trabalhefabricio/ai-file-sorter-iconic](https://github.com/trabalhefabricio/ai-file-sorter-iconic)
- **Development Branch**: `newstuff`
- **Analysis Date**: January 19, 2026

---

## ✅ Implemented Custom Features (in `newstuff` branch)

### 1. **Enhanced Gemini API Integration with Advanced Rate Limiting**
**Status**: ✅ Implemented  
**Location**: `app/lib/GeminiClient.cpp`, `app/include/GeminiClient.hpp`

**Features:**
- Intelligent rate limiting specifically tuned for Gemini free tier (15 RPM)
- Token bucket algorithm with dynamic refill rate
- Per-model state tracking with persistent state across sessions
- Progressive timeout extension (20s → 240s with exponential backoff)
- Circuit breaker pattern for service degradation handling
- Advanced jitter implementation for retry scheduling
- Adaptive capacity adjustment based on API performance

**Why it's valuable**: Maximizes free tier usage while preventing rate limit errors

---

### 2. **User Profiling and Adaptive Learning System**
**Status**: ✅ Implemented  
**Location**: `app/include/UserProfileManager.hpp`, `app/lib/UserProfileManager.cpp`, `app/include/UserProfileDialog.hpp`

**Features:**
- Multiple user profile support
- Learning from user corrections to categories
- Profile-specific categorization patterns
- Adaptive behavior based on user habits
- Profile switching capability
- Timeline view of profile evolution

**Database Tables Added:**
- `user_profiles` - Store multiple user profiles
- `profile_characteristics` - Track user-specific traits and preferences
- `user_corrections` - Learn from manual category corrections

---

### 3. **File Tinder Tool**
**Status**: ✅ Implemented  
**Location**: `app/include/FileTinderDialog.hpp`, `app/lib/FileTinderDialog.cpp`

**Features:**
- Swipe-style file cleanup interface
- Arrow key navigation:
  - ← Left Arrow: Mark file for deletion
  - → Right Arrow: Keep file
  - ↑ Up Arrow: Send to back of queue
  - ↓ Down Arrow: Ignore for this session
- File preview (images, text, metadata)
- Review marked files before deletion
- Save and resume sessions
- Session state persistence

**Database Tables Added:**
- `file_tinder_state` - Persist File Tinder decisions

**Why it's valuable**: Unique, fun way to quickly triage large numbers of files

---

### 4. **API Usage Tracking and Cost Monitoring**
**Status**: ✅ Implemented  
**Location**: `app/include/APIUsageTracker.hpp`, `app/include/UsageStatsDialog.hpp`, `app/lib/UsageStatsDialog.cpp`

**Features:**
- Track OpenAI and Gemini API usage
- Monitor token consumption
- Estimate API costs
- Daily/monthly usage statistics
- Free tier quota tracking (Gemini 15 RPM limit)
- Historical usage graphs
- Export usage data

**Database Tables Added:**
- `api_usage_tracking` - Track API calls, tokens, costs, and limits

---

### 5. **Enhanced Whitelist Tree Editor**
**Status**: ✅ Implemented  
**Location**: `app/lib/WhitelistTreeEditor.cpp`, `app/include/WhitelistStore.hpp` (enhanced)

**Features:**
- Hierarchical tree-based category structure
- Visual whitelist editing
- Drag-and-drop category organization
- Keyboard shortcuts for quick editing
- Category/subcategory relationship management
- Import/export whitelist configurations

---

### 6. **Confidence Scoring System**
**Status**: ✅ Implemented  
**Location**: Enhanced in `CategorizationService.cpp`

**Features:**
- Track confidence levels for categorizations
- Confidence-based uncertainty detection
- Highlight low-confidence categorizations for review
- Trigger category suggestion wizard for uncertain files
- Model version tracking for confidence scores

**Database Tables Added:**
- `confidence_scores` - Store confidence levels per file

---

### 7. **Category Suggestion Wizard**
**Status**: ✅ Implemented  
**Location**: `app/include/CategorySuggestionWizard.hpp`, `app/lib/CategorySuggestionWizard.cpp`

**Features:**
- Dynamic category suggestion for uncertain files
- Confidence-based triggering
- Interactive category selection
- Integration with whitelist system
- Smart category recommendations based on file analysis

---

### 8. **Enhanced Cache Management Dialog**
**Status**: ✅ Implemented  
**Location**: `app/include/CacheManagerDialog.hpp`

**Features:**
- View cache statistics (entry count, size, dates)
- Clear all cache with confirmation
- Clear cache older than N days (configurable)
- Optimize database (VACUUM) to reclaim space
- Real-time statistics refresh
- Cache performance metrics

**UI Location**: Settings → Manage Cache...

---

### 9. **Comprehensive Error Code System**
**Status**: ✅ Implemented  
**Location**: `app/include/ErrorCode.hpp`, `app/include/ErrorMessages.hpp`, `app/include/ErrorReporter.hpp`

**Features:**
- Structured error codes with categories
- User-friendly error messages
- Copyable error dialogs
- Comprehensive error tracking
- Error reporting system for debugging
- Step-by-step guidance for common errors

**Documentation**: `ERROR_CODES.md`, `ERROR_REPORTER_GUIDE.md`

---

### 10. **Enhanced Categorization Session Management**
**Status**: ✅ Implemented (Database infrastructure ready)  
**Location**: Database schema additions

**Features:**
- Save categorization sessions
- Resume interrupted sessions
- Session templates
- Historical session tracking
- Per-session consistency mode settings

**Database Tables Added:**
- `categorization_sessions` - Track and resume sessions

---

### 11. **Enhanced Undo/Redo System**
**Status**: ✅ Enhanced (Database infrastructure ready)  
**Location**: Database schema additions

**Features:**
- Multiple undo history (not just last operation)
- Persistent undo chains
- Undo operation tracking
- Better recovery from mistakes

**Database Tables Added:**
- `undo_history` (enhanced) - Multi-level undo support

---

### 12. **Content Analysis Infrastructure**
**Status**: ✅ Database schema ready  
**Location**: Database schema additions

**Features (Planned):**
- Cache for file content analysis
- Content hash tracking
- MIME type detection
- Analysis result caching

**Database Tables Added:**
- `content_analysis_cache` - Ready for content-based sorting implementation

---

### 13. **Diagnostic and Testing Tools**
**Status**: ✅ Implemented  
**Location**: `diagnostic_tool.py`, `thorough_diagnostic.py`, `emergency_diagnostic.bat`

**Features:**
- Comprehensive diagnostic tools for debugging
- Automated artifact testing framework
- Test result aggregation
- Safety checks and bug prevention tests
- HTML and JSON diagnostic reports
- Feature validation scripts

**Documentation**: 
- `DIAGNOSTIC_TOOLS_COMPARISON.md`
- `THOROUGH_DIAGNOSTIC_README.md`
- `TESTING_TOOLS_README.md`
- `MANUAL_TESTING_GUIDE.md`

---

### 14. **DLL Version Checking (Windows)**
**Status**: ✅ Implemented  
**Location**: `app/include/DllVersionChecker.hpp`, `app/startapp_windows.cpp` (enhanced)

**Features:**
- Automatic DLL version compatibility checking
- ggml library version validation
- Qt DLL compatibility checking
- Comprehensive DLL loading order fixes
- Early PATH setup for DLL resolution
- Prevent QTableView::dropEvent errors

---

### 15. **Folder Learning Dialog**
**Status**: ✅ Implemented  
**Location**: `app/include/FolderLearningDialog.hpp`

**Features:**
- Learn from folder structure
- Pattern recognition in existing organization
- Apply learned patterns to new folders
- Folder-specific categorization rules

---

### 16. **User Categorization Dialog**
**Status**: ✅ Implemented  
**Location**: `app/include/UserCategorizationDialog.hpp`, `app/lib/UserCategorizationDialog.cpp`

**Features:**
- Custom category definition interface
- User-driven categorization workflows
- Integration with learning system
- Profile-specific categories

---

### 17. **Enhanced Whitelist Management**
**Status**: ✅ Enhanced  
**Location**: `app/lib/WhitelistStore.cpp` (significantly enhanced), `app/lib/WhitelistManagerDialog.cpp` (enhanced)

**Features:**
- Advanced whitelist storage and retrieval
- Hierarchical category support
- Whitelist validation
- Import/export functionality improvements
- Profile-specific whitelists

**Documentation**: `WHITELIST_IMPROVEMENTS.md`

---

## 🔨 In Development / Planned Features (in `newstuff` branch)

### 1. **Content-Based File Sorting**
**Status**: 🔨 Database schema ready, implementation planned  
**Priority**: High

**Planned Features:**
- Analyze actual file contents (not just names)
- PDF text extraction and analysis
- Image content recognition
- Code file semantic analysis
- Document keyword extraction
- Language detection

**Why it's valuable**: Much more accurate categorization for files with generic names

---

### 2. **Advanced User Profiling with AI Questionnaires**
**Status**: 📋 Planned (detailed in IMPLEMENTATION_PLAN.md Phase 3)  
**Priority**: Medium

**Planned Features:**
- AI-generated dynamic questionnaires
- Natural language profile understanding
- Adaptive question generation based on responses
- Timeline view of profile evolution
- Log-based learning from user behavior

---

### 3. **Smart Taxonomy Suggestions**
**Status**: 📋 Planned (IMPLEMENTATION_PLAN.md Phase 4.2)  
**Priority**: Medium

**Planned Features:**
- Automatic similarity detection (e.g., "Document" ≈ "Docs")
- Merge suggestions with confidence scores
- Taxonomy optimization
- Category alias support
- Learning from corrections

---

### 4. **Hybrid Categorization Mode**
**Status**: 📋 Planned (IMPLEMENTATION_PLAN.md Phase 4)  
**Priority**: Medium

**Planned Features:**
- Third mode between "More Refined" and "More Consistent"
- Auto-detect file clusters
- Apply consistency within clusters
- Consistency strength slider
- Smart balance based on file similarity

---

### 5. **Enhanced Simulation Mode**
**Status**: 📋 Planned (IMPLEMENTATION_PLAN.md Phase 5)  
**Priority**: Medium

**Planned Features:**
- Before/After folder structure visualization
- Tree view and graph view modes
- File count and size per category
- Conflict highlighting
- Searchable preview
- Export preview as report

---

### 6. **Parallel File Processing**
**Status**: 📋 Planned (FUTURE_IMPROVEMENTS.md)  
**Priority**: High

**Planned Features:**
- Multi-threaded file categorization
- Thread pool management
- 3-5x faster processing for large batches
- Better CPU utilization

---

### 7. **Easy Mode / Wizard Interface**
**Status**: 📋 Planned (IMPLEMENTATION_PLAN.md Phase 6.2)  
**Priority**: Low

**Planned Features:**
- Simplified wizard for beginners
- Smart defaults and presets
- Guided step-by-step experience
- Progressive disclosure of advanced features
- Auto-detection of optimal settings

---

### 8. **Trend Analysis and Recommendations**
**Status**: 📋 Planned (IMPLEMENTATION_PLAN.md Phase 3.2)  
**Priority**: Medium

**Planned Features:**
- Category usage trends over time
- Folder recommendations based on patterns
- Folder hierarchy analysis
- Cleanup suggestions
- Storage optimization recommendations

---

### 9. **Natural Language Error Resolution**
**Status**: 📋 Planned (IMPLEMENTATION_PLAN.md Phase 1.2)  
**Priority**: Low

**Planned Features:**
- Describe problems in natural language
- AI-powered problem diagnosis
- Automatic resolution suggestions
- Integration with existing error code system

---

### 10. **Conflict Detection and Resolution with AI**
**Status**: 📋 Planned (IMPLEMENTATION_PLAN.md Phase 5.2)  
**Priority**: Medium

**Planned Features:**
- Comprehensive conflict type detection
- Natural language resolution interface
- Batch conflict resolution
- Smart suggestions based on learning
- Duplicate file detection and handling

---

## 📊 Development Statistics

### Code Changes (main → newstuff)
- **Total Files Changed**: 155+
- **Lines Added**: 38,000+
- **Lines Removed**: 1,600+
- **New Classes/Dialogs**: 15+
- **New Database Tables**: 8
- **New Documentation Files**: 35+

### Feature Breakdown
- **✅ Fully Implemented**: 17 features
- **🔨 In Development**: 1 feature (Content-based sorting)
- **📋 Planned**: 9 features
- **Total**: 27 custom features/enhancements

### Implementation Phases (from IMPLEMENTATION_PLAN.md)
- **Phase 1**: Foundation & Infrastructure (Mostly Complete)
- **Phase 2**: Core Feature Enhancements (In Progress)
- **Phase 3**: Advanced User Profiling (Partially Complete)
- **Phase 4**: Enhanced Categorization (Partially Complete)
- **Phase 5**: File Management & UX (In Progress)
- **Phase 6**: Auxiliary Tools & Polish (Mostly Complete)

---

## 🎯 Key Differentiators from Original Repository

1. **Advanced Gemini Integration**: Sophisticated rate limiting and retry logic specifically for free tier
2. **User Profiling System**: Learn and adapt to individual user preferences
3. **File Tinder**: Unique swipe-style interface for file cleanup
4. **API Cost Tracking**: Monitor and optimize API usage costs
5. **Comprehensive Diagnostic Tools**: Extensive testing and debugging framework
6. **Enhanced Error System**: Structured error codes with user-friendly messages
7. **Confidence Scoring**: Highlight uncertain categorizations for review
8. **Category Suggestion Wizard**: Interactive help for difficult categorizations
9. **Cache Management UI**: User-friendly cache control interface
10. **Enhanced Whitelist Editor**: Tree-based hierarchical editing

---

## 📚 Documentation Created

Over 35 comprehensive documentation files including:
- `FEATURE_ANALYSIS.md` - Detailed analysis of all features
- `IMPLEMENTATION_PLAN.md` - 6-phase roadmap with 30+ features
- `FUTURE_IMPROVEMENTS.md` - Performance and UX enhancement ideas
- `NON_AI_FEATURES_SUMMARY.md` - Features implementable without AI
- `DIAGNOSTIC_TOOLS_COMPARISON.md` - Testing tools guide
- `ERROR_CODES.md` - Complete error code reference
- `WHITELIST_IMPROVEMENTS.md` - Whitelist system enhancements
- `PATH_BASED_CATEGORIZATION.md` - Advanced categorization strategies
- Multiple testing and debugging guides

---

## 🚀 Future Roadmap

Based on `IMPLEMENTATION_PLAN.md`, the fork aims to add:

1. **Smart AI Features**: Content analysis, confidence scoring, learning from corrections
2. **Enhanced UX**: Better progress feedback, simulation modes, visual editors
3. **Performance**: Parallel processing, smart caching, incremental categorization
4. **Personalization**: Advanced profiling, trend analysis, recommendations
5. **Usability**: Easy mode, wizards, conflict resolution
6. **Developer Tools**: Comprehensive testing, debugging, and diagnostic tools

**Estimated Timeline**: 12-16 weeks for full implementation of planned features

---

## Summary

The `ai-file-sorter-iconic` fork by @trabalhefabricio represents a significant enhancement of the original AI File Sorter, with **17 fully implemented custom features** and **10 additional features in development or planning**. The fork focuses on:

- **Enhanced AI integration** with sophisticated Gemini API handling
- **User personalization** through profiling and adaptive learning
- **Developer experience** with comprehensive diagnostic tools
- **Unique features** like File Tinder and interactive wizards
- **Future-ready infrastructure** with extensive database schema for planned features

All features maintain the core principles of the original project: cross-platform compatibility, offline operation support, and user privacy.
