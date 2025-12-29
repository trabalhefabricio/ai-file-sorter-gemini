# AI File Sorter - Comprehensive Feature Analysis

## Document Overview
This document provides a detailed analysis of all features in AI File Sorter, with special focus on customized features developed over time. Each feature includes a description of what it does, how it works in the context of the application, and suggestions for improvement.

**Analysis Date:** December 28, 2025  
**Repository:** trabalhefabricio/ai-file-sorter-gemini  
**Version Context:** v1.5.0+ with User Profiling (Unreleased)

---

## Table of Contents
1. [Core Features](#core-features)
2. [AI & LLM Integration Features](#ai--llm-integration-features)
3. [User Profiling & Adaptive Learning](#user-profiling--adaptive-learning)
4. [Categorization Features](#categorization-features)
5. [File Management Features](#file-management-features)
6. [UI/UX Features](#uiux-features)
7. [Platform & Performance Features](#platform--performance-features)
8. [Developer & Configuration Features](#developer--configuration-features)

---

## 1. Core Features

### 1.1 AI-Powered File Categorization
**What it is:**  
The primary feature that analyzes file names, extensions, paths, and directory context to automatically assign categories and optional subcategories to files.

**How it works:**
- Uses `CategorizationService` class to orchestrate the entire categorization pipeline
- Scans files using `FileScanner` which generates `FileEntry` objects containing file metadata
- Each file is processed through either a local LLM or remote API (OpenAI/Gemini)
- Results are cached in SQLite database (`DatabaseManager`) to avoid re-processing
- Categories can be hierarchical (category + subcategory) if enabled
- Supports batch processing with progress callbacks

**Implementation Details:**
```cpp
// Located in: app/lib/CategorizationService.cpp
std::vector<CategorizedFile> categorize_entries(
    const std::vector<FileEntry>& files,
    bool is_local_llm,
    std::atomic<bool>& stop_flag,
    const ProgressCallback& progress_callback,
    ...)
```

**How it could be improved:**
1. **Content-based analysis**: Currently only uses file name/extension. Could analyze file content for better accuracy (partially planned per README)
2. **Parallel processing**: Process multiple files concurrently to speed up large batches
3. **Confidence scoring**: Add confidence levels to categorizations so users can prioritize manual review
4. **Smart batching**: Group similar files together for more efficient LLM prompts
5. **Learning from corrections**: When users manually change categories, learn from these corrections

### 1.2 Taxonomy-Based System
**What it is:**  
A hierarchical reference system that maintains consistency in category assignments across different categorization sessions.

**How it works:**
- Database stores a taxonomy table mapping categories to subcategories
- When categorizing files, the system references this taxonomy to prefer existing categories
- Helps reduce the proliferation of similar but differently-named categories (e.g., "Documents" vs "Document" vs "Docs")
- Used in conjunction with consistency hints for "More Consistent" mode

**Implementation Details:**
- Stored in SQLite database managed by `DatabaseManager`
- Taxonomy entries are created/updated during categorization
- `ConsistencyPassService` uses taxonomy to harmonize categories in bulk

**How it could be improved:**
1. **User-editable taxonomy**: Allow users to merge/rename categories in the taxonomy
2. **Taxonomy import/export**: Share taxonomies between users or machines
3. **Smart taxonomy suggestions**: Automatically detect and suggest merging similar categories
4. **Hierarchical visualization**: Show taxonomy as a tree structure for better understanding
5. **Category aliases**: Support multiple names for the same category (e.g., "Photos" = "Images")

---

## 2. AI & LLM Integration Features

### 2.1 Google Gemini API Integration (v1.5.0 - CUSTOMIZED)
**What it is:**  
Full integration with Google's Gemini API as an alternative to OpenAI and local LLMs, with extensive optimizations for the free tier.

**How it works:**
- `GeminiClient` class implements `ILLMClient` interface
- Uses REST API to send requests to Gemini's `generateContent` endpoint
- Implements sophisticated rate limiting and retry logic specifically tuned for free tier limits

**Key Features:**
1. **Intelligent Rate Limiting (15 RPM)**
   - Token bucket algorithm with dynamic refill rate
   - Per-model state tracking in static map
   - Persistent state across application sessions
   - Adaptive capacity adjustment based on API performance

2. **Progressive Timeout Extension**
   - Starts with 20-second timeout
   - Doubles timeout on each timeout failure up to 240 seconds
   - Gradually reduces timeout on successful requests
   - Payload-aware timeout scaling (larger prompts get more time)

3. **Circuit Breaker Pattern**
   - Opens after 3 consecutive failures
   - 60-second cooldown period
   - Prevents overwhelming degraded API
   - Automatic reset when service recovers

4. **Decorrelated Jitter Backoff**
   - AWS-recommended backoff algorithm
   - Prevents request clustering
   - Better distribution than simple exponential backoff
   - Random jitter prevents thundering herd

**Implementation Details:**
```cpp
// Located in: app/lib/GeminiClient.cpp
struct ModelState {
    double tokens = 3.0;            // current tokens in bucket
    double capacity = 5.0;          // max tokens (conservative for free tier)
    double refill_per_sec = 0.25;   // ~15 per minute for free tier
    uint64_t retry_after_until_ms = 0;
    double ewma_ms = 15000.0;       // EWMA of response duration
    int consecutive_failures = 0;
    uint64_t circuit_open_until_ms = 0;
    int timeout_extensions = 0;
    // ...
};
```

**How it could be improved:**
1. **Model-specific optimization**: Different timeout/rate strategies per Gemini model (flash vs pro)
2. **Cost tracking**: Show estimated API costs/usage to users
3. **Fallback chain**: Automatically fall back to local LLM if API repeatedly fails
4. **Streaming responses**: Use Gemini's streaming API for real-time feedback
5. **Batch API support**: Use Gemini's batch API for processing many files at once
6. **Regional optimization**: Adjust timeouts based on user's geographic location

### 2.2 Local LLM Support (llama.cpp Integration)
**What it is:**  
Ability to run file categorization completely offline using local LLMs like LLaMa 3B and Mistral 7B.

**How it works:**
- Integrates llama.cpp library for LLM inference
- `LocalLLMClient` class wraps llama.cpp API
- Models are GGUF format, optimized for CPU/GPU inference
- Supports multiple backends: CPU (OpenBLAS), CUDA, Vulkan, Metal (macOS)
- Models downloaded on-demand via `LLMDownloader`
- Backend auto-detection at runtime via launcher scripts

**Implementation Details:**
- Models stored in: `~/.local/share/aifilesorter/llms` (Linux) or `~/Library/Application Support/aifilesorter/llms` (macOS)
- Backend selection priority: Vulkan → CUDA → CPU
- Command-line flags: `--cuda={on|off}`, `--vulkan={on|off}`

**How it could be improved:**
1. **Model fine-tuning**: Allow users to fine-tune models on their file naming patterns
2. **Model marketplace**: Community-shared fine-tuned models for specific domains
3. **Automatic model selection**: Choose best model based on available RAM/VRAM
4. **Quantization options**: Offer different quantization levels (Q4, Q5, Q8) for size/quality tradeoff
5. **Multi-model ensemble**: Use multiple models and vote on categorizations
6. **Progress indicators**: Show model loading progress and inference speed

### 2.3 OpenAI API Integration (BYOK - Bring Your Own Key)
**What it is:**  
Support for using ChatGPT models via user's own OpenAI API key.

**How it works:**
- `LLMClient` class implements OpenAI API integration
- API key stored locally in config.ini
- Supports any ChatGPT model (gpt-4o-mini, gpt-4.1, o3-mini, etc.)
- Similar retry and error handling as Gemini, but simpler rate limiting

**How it could be improved:**
1. **Usage analytics**: Track token usage and estimated costs
2. **Budget limits**: Set spending caps to prevent runaway costs
3. **Model recommendations**: Suggest optimal model for user's needs
4. **Batch processing**: Use OpenAI's batch API for 50% cost reduction
5. **Fine-tuning support**: Allow users to fine-tune OpenAI models on their data

### 2.4 Custom Local LLM Support
**What it is:**  
Users can register their own GGUF models for categorization.

**How it works:**
- `CustomLLMDialog` allows adding custom models
- Models stored in Settings with ID, name, description, and path
- Custom models selectable in LLM selection dialog
- Same inference path as bundled local models

**Implementation Details:**
```cpp
// Located in: app/include/Types.hpp
struct CustomLLM {
    std::string id;
    std::string name;
    std::string description;
    std::string path;
};
```

**How it could be improved:**
1. **Model validation**: Check GGUF format validity before adding
2. **Automatic metadata extraction**: Read model name/size from GGUF file
3. **Model benchmarking**: Test performance and suggest optimal settings
4. **Model presets**: Share recommended settings for popular models
5. **HuggingFace integration**: Browse and download models directly from HuggingFace

---

## 3. User Profiling & Adaptive Learning (Unreleased - HEAVILY CUSTOMIZED)

### 3.1 User Profile Building
**What it is:**  
An intelligent system that learns from user's file organization patterns over time to provide increasingly personalized categorization suggestions.

**How it works:**
- `UserProfileManager` analyzes categorized files to infer user characteristics
- Profile contains: characteristics (traits), folder insights, and organizational templates
- Characteristics include hobbies, work patterns, and organizational style
- Each characteristic has a confidence level (0.0 to 1.0) that grows with evidence
- Profile data stored locally in SQLite database

**Implementation Details:**
```cpp
// Located in: app/include/UserProfileManager.hpp
struct UserProfile {
    std::string user_id;
    std::vector<UserCharacteristic> characteristics;
    std::vector<FolderInsight> folder_insights;
    std::vector<OrganizationalTemplate> learned_templates;
    std::string created_at;
    std::string last_updated;
};

struct UserCharacteristic {
    std::string trait_name;
    std::string value;
    float confidence;  // 0.0 to 1.0
    std::string evidence;
    std::string timestamp;
};
```

**Analysis Process:**
1. **Hobby Detection**: Analyzes dominant categories (music, photos, games) to infer interests
2. **Work Pattern Detection**: Identifies professional files (documents, spreadsheets, code)
3. **Organization Style Analysis**: Determines if user prefers minimalist, balanced, detailed, or power-user organization

**How it could be improved:**
1. **Time-based patterns**: Learn when certain types of files are typically organized
2. **Project detection**: Identify projects and suggest project-specific categorization
3. **Context awareness**: Different profiles for work vs personal computers
4. **Profile sharing**: Export/import profiles across devices
5. **AI-driven insights**: Use LLM to generate natural language insights about organization style
6. **Habit tracking**: Track and visualize organization habits over time

### 3.2 Folder Insights
**What it is:**  
Per-folder analysis tracking dominant categories, file counts, and usage patterns.

**How it works:**
- After each folder analysis, system generates `FolderInsight` object
- Tracks: folder path, description, dominant categories, file count, last analyzed time, usage pattern
- Usage patterns: "work", "personal", "archive", etc.
- Insights stored in profile and viewable in User Profile dialog

**Implementation Details:**
```cpp
// Located in: app/lib/UserProfileManager.cpp
void analyze_and_update_from_folder(
    const std::string& folder_path,
    const std::vector<CategorizedFile>& files)
{
    // Calculate category distribution
    auto cat_dist = calculate_category_distribution(files);
    // Determine usage pattern
    std::string usage_pattern = determine_usage_pattern(files);
    // Generate description
    std::string description = generate_folder_description(folder_path, files);
    // ...
}
```

**How it could be improved:**
1. **Trend analysis**: Show how folder contents change over time
2. **Anomaly detection**: Alert when unusual files appear in a folder
3. **Folder recommendations**: Suggest new folder structures based on insights
4. **Cleanup suggestions**: Identify folders that need organization
5. **Comparison tools**: Compare folders to find duplicates or similar content

### 3.3 Organizational Templates
**What it is:**  
Learned patterns of how users organize similar types of content, stored as reusable templates.

**How it works:**
- System observes categorization patterns across folders
- Creates templates with suggested categories and subcategories
- Templates have confidence scores based on usage frequency
- Can be applied to new folders for consistent organization

**Implementation Details:**
```cpp
// Located in: app/include/Types.hpp
struct OrganizationalTemplate {
    std::string template_name;
    std::string description;
    std::vector<std::string> suggested_categories;
    std::vector<std::string> suggested_subcategories;
    float confidence;
    std::string based_on_folders;
    int usage_count;
};
```

**How it could be improved:**
1. **Template marketplace**: Share templates with community
2. **Template recommendations**: Suggest templates based on folder content
3. **Template customization**: Easy editing and refinement of templates
4. **Template versioning**: Track template evolution over time
5. **Industry templates**: Pre-built templates for different professions/industries

### 3.4 Per-Folder Learning Control (CUSTOMIZED)
**What it is:**  
Granular control over how the profiling system learns from each folder.

**How it works:**
- Three levels of learning: Full, Partial, None
- **Full Learning**: Uses profile for AI categorization AND stores folder information
- **Partial Learning**: Doesn't use profile for categorization but STILL stores folder information
- **None**: Doesn't use profile AND doesn't store any folder information
- Configurable via `FolderLearningDialog` (gear icon next to folder path)
- Settings stored in database per folder path

**Implementation Details:**
```cpp
// Located in: app/include/FolderLearningDialog.hpp
class FolderLearningDialog : public QDialog {
    std::string get_selected_level() const;
    // Returns: "full", "partial", or "none"
};

// Database stores folder inclusion level
std::string get_folder_inclusion_level(const std::string& folder_path);
```

**Use Cases:**
- **Full**: Trusted folders (personal documents, photos)
- **Partial**: Gather data without affecting categorization (testing new organization)
- **None**: Sensitive folders (private, temporary, client data)

**How it could be improved:**
1. **Folder hierarchies**: Apply learning level to entire directory trees
2. **Pattern matching**: Set learning level based on folder name patterns
3. **Time-based rules**: Automatically exclude old/inactive folders
4. **Visual indicators**: Show learning level in UI with icons/colors
5. **Bulk configuration**: Set learning levels for multiple folders at once
6. **Smart defaults**: Suggest learning level based on folder location/name

### 3.5 Profile Visualization (User Profile Dialog)
**What it is:**  
A dialog showing all learned information about the user's organization patterns.

**How it works:**
- Accessible via Help → View User Profile menu
- Three tabs: Overview, Characteristics, Folder Insights
- **Overview Tab**: Summary statistics and top characteristics
- **Characteristics Tab**: All traits organized by category with confidence levels and evidence
- **Folder Insights Tab**: Per-folder analysis and patterns

**How it could be improved:**
1. **Interactive visualizations**: Charts and graphs showing trends
2. **Timeline view**: See how profile evolved over time
3. **Export functionality**: Export profile as JSON/PDF report
4. **Comparison mode**: Compare profiles across time periods
5. **Recommendations panel**: Actionable suggestions based on profile
6. **Search and filter**: Find specific characteristics or folders

---

## 4. Categorization Features

### 4.1 Two Categorization Modes (CUSTOMIZED)
**What it is:**  
Two distinct approaches to file categorization: "More Refined" and "More Consistent".

**How it works:**

**More Refined Mode:**
- Flexibility-focused approach
- Consistency hints DISABLED
- Model picks most specific category/subcategory for each file independently
- Best for diverse/mixed folders
- Results in more varied but precise categorizations

**More Consistent Mode:**
- Uniformity-focused approach
- Consistency hints ENABLED
- Model receives context from prior assignments in current session
- Files with similar names/extensions trend toward same categories
- Best for batches where uniformity is desired

**Implementation Details:**
```cpp
// Located in: app/lib/CategorizationService.cpp
std::vector<CategoryPair> collect_consistency_hints(
    const std::string& signature,
    const SessionHistoryMap& session_history,
    const std::string& extension,
    FileType file_type) const;

// Hints are formatted and injected into LLM prompt
std::string build_combined_context(const std::string& hint_block) const;
```

**Consistency Hint Example:**
```
Previous similar files in this session:
- report.pdf → Documents : Reports
- invoice.pdf → Documents : Invoices
```

**How it could be improved:**
1. **Hybrid mode**: Automatically switch between modes based on file similarity
2. **Consistency strength slider**: Adjust how strongly hints influence decisions
3. **Session management**: Save/load sessions to maintain consistency across app restarts
4. **Visual feedback**: Show when consistency hints were used in results
5. **Learning mode**: Learn optimal mode per folder type

### 4.2 Category Whitelists (CUSTOMIZED)
**What it is:**  
Named lists of allowed categories and subcategories that constrain LLM output.

**How it works:**
- Managed via Settings → Manage category whitelists
- Multiple named whitelists can be stored
- Each whitelist contains categories, subcategories, context, and settings
- When enabled, whitelist is injected into LLM prompt
- Model constrained to choose only from allowed categories
- Works in both categorization modes

**Implementation Details:**
```cpp
// Located in: app/include/WhitelistStore.hpp
struct WhitelistEntry {
    std::vector<std::string> categories;
    std::vector<std::string> subcategories;
    std::string context;  // User-provided context
    bool enable_advanced_subcategories;  // Generate subcats dynamically
};

class WhitelistStore {
    std::vector<std::string> list_names() const;
    std::optional<WhitelistEntry> get(const std::string& name) const;
    void set(const std::string& name, WhitelistEntry entry);
    void remove(const std::string& name);
};
```

**Use Cases:**
- **Project-specific**: Different whitelists for different projects
- **Client work**: Enforce client's categorization scheme
- **Simplified organization**: Limit to 10-15 main categories
- **Language-specific**: Different whitelists per language

**Best Practices (from README):**
- Keep each whitelist to 15-20 categories to avoid overlong prompts
- Use several narrow lists instead of one very long one
- Pair with "More Consistent" for strongest adherence

**How it could be improved:**
1. **Hierarchical whitelists**: Define category hierarchies in whitelists
2. **Smart suggestions**: Auto-generate whitelist from existing folders
3. **Whitelist templates**: Pre-built whitelists for common scenarios
4. **Regex patterns**: Allow pattern matching for categories (e.g., "Project-*")
5. **Conditional whitelists**: Different whitelists based on file type or folder
6. **Whitelist inheritance**: Base whitelists that extend parent lists

### 4.3 Multilingual Categorization
**What it is:**  
Ability to have LLM assign categories in different languages.

**How it works:**
- Settings → Category Language menu
- Supported languages: Dutch, English, French, German, Italian, Polish, Portuguese, Spanish, Turkish
- Language context injected into LLM prompt
- Independent from UI language setting

**Implementation Details:**
```cpp
// Located in: app/lib/CategorizationService.cpp
std::string build_category_language_context() const {
    const auto lang = settings.get_category_language();
    if (lang == CategoryLanguage::English) return "";
    // Return language-specific prompt instruction
}
```

**How it could be improved:**
1. **Auto-detection**: Detect system language and suggest category language
2. **Mixed-language support**: Allow multiple languages in same categorization
3. **Translation mode**: Translate existing categories between languages
4. **Language confidence**: Show confidence in non-English categorizations
5. **Custom language prompts**: User-editable language instructions

### 4.4 Consistency Pass (Development Feature)
**What it is:**  
A post-processing step that harmonizes all categories in a batch for maximum consistency.

**How it works:**
- Development menu → Run consistency pass
- `ConsistencyPassService` processes categorized files
- Sends batches of files to LLM with current taxonomy
- LLM suggests harmonized categories for entire batch
- Updates all categories to be consistent

**Implementation Details:**
```cpp
// Located in: app/lib/ConsistencyPassService.cpp
void run(std::vector<CategorizedFile>& categorized_files,
         std::vector<CategorizedFile>& newly_categorized_files,
         std::function<std::unique_ptr<ILLMClient>()> llm_factory,
         std::atomic<bool>& stop_flag,
         const ProgressCallback& progress_callback) const;
```

**How it could be improved:**
1. **Automatic triggering**: Run automatically after large categorizations
2. **Selective consistency**: Only harmonize specific category groups
3. **Diff preview**: Show before/after comparison of changes
4. **Undo support**: Allow reverting consistency pass
5. **Integration with modes**: Make this a third categorization mode

### 4.5 Subcategory Support
**What it is:**  
Optional hierarchical categorization with category + subcategory.

**How it works:**
- Toggle via checkbox on main window
- When enabled, LLM assigns both category and subcategory
- Subcategory typically more specific than category
- Creates nested folder structure: `/Category/Subcategory/`

**Examples:**
- Documents : Reports
- Photos : Vacation
- Music : Rock

**How it could be improved:**
1. **Multi-level hierarchies**: Support more than 2 levels (Category/Sub1/Sub2)
2. **Smart flattening**: Automatically combine category+subcat when redundant
3. **Subcategory suggestions**: Suggest common subcategories based on category
4. **Custom separators**: Choose folder structure separator (slash, underscore, etc.)
5. **Conditional subcategories**: Only use subcategories for certain file types

---

## 5. File Management Features

### 5.1 Dry Run / Preview Mode (v1.4.0 - CUSTOMIZED)
**What it is:**  
Preview planned file moves without actually moving any files.

**How it works:**
- Checkbox in categorization results dialog: "Dry run (preview only, do not move files)"
- When enabled, shows `DryRunPreviewDialog` with From→To table
- No files are moved until dry run is disabled and confirmed
- Allows reviewing entire organization before committing

**Implementation Details:**
```cpp
// Located in: app/include/DryRunPreviewDialog.hpp
struct Entry {
    std::string from_label;
    std::string to_label;
    std::string source_tooltip;
    std::string destination_tooltip;
};
```

**How it could be improved:**
1. **Conflict detection**: Highlight potential file conflicts before moving
2. **Size analysis**: Show total size to be moved per category
3. **Export preview**: Export move plan as CSV/Excel for review
4. **Selective execution**: Choose which moves to execute from preview
5. **Impact analysis**: Show before/after folder structure diagrams
6. **Simulation mode**: Show what folder structure would look like after move

### 5.2 Persistent Undo (v1.4.0 - CUSTOMIZED)
**What it is:**  
Ability to revert file moves even after closing the application.

**How it works:**
- Every sort operation saves an undo plan to JSON file
- Plan includes: source, destination, file size, modification time
- Accessible via Edit → "Undo last run" even after app restart
- `UndoManager` handles plan storage and restoration
- Plans stored in undo directory with timestamps

**Implementation Details:**
```cpp
// Located in: app/include/UndoManager.hpp
struct Entry {
    std::string source;
    std::string destination;
    std::uintmax_t size_bytes;
    std::time_t mtime;
};

struct UndoResult {
    int restored;
    int skipped;
    QStringList details;
};
```

**Undo Logic:**
- Checks if destination file still exists
- Verifies file size and mtime match plan
- Skips files that have been modified or moved
- Reports success/skip counts

**How it could be improved:**
1. **Undo history**: Keep multiple undo points, not just last one
2. **Partial undo**: Undo specific files or categories
3. **Undo preview**: Show what would be undone before executing
4. **Automatic cleanup**: Delete old undo plans after X days
5. **Redo support**: Allow re-doing undone operations
6. **Conflict resolution**: Better handling of modified files during undo
7. **Undo chains**: Track sequences of operations for multi-step undo

### 5.3 Sortable Review Table
**What it is:**  
Results table that can be sorted by different columns for easier review.

**How it works:**
- Click column headers in categorization review dialog
- Sort by: file name, category, subcategory
- Helps quickly find files in specific categories
- Useful for reviewing consistency

**How it could be improved:**
1. **Multi-column sort**: Sort by multiple columns (category, then name)
2. **Filter options**: Filter by category, file type, or source folder
3. **Search functionality**: Quick search to find specific files
4. **Group by category**: Collapsible groups for each category
5. **Statistics panel**: Show count and size per category
6. **Bulk editing**: Select multiple files and change category at once

### 5.4 Local Database Caching
**What it is:**  
SQLite database that caches categorization results to avoid re-processing.

**How it works:**
- `DatabaseManager` handles all database operations
- Cache key: item name, path, file type
- Stores: category, subcategory, taxonomy ID, timestamp
- Cache checked before calling LLM
- Significantly speeds up re-categorization
- Reduces API costs for remote LLMs

**Implementation Details:**
```cpp
// Located in: app/include/DatabaseManager.hpp
struct ResolvedCategory {
    std::string category;
    std::string subcategory;
    int taxonomy_id;
    bool from_cache;
};
```

**How it could be improved:**
1. **Cache expiration**: Automatically expire old cache entries
2. **Cache statistics**: Show hit rate and cache size
3. **Smart invalidation**: Invalidate cache when settings change
4. **Cache export/import**: Share cache between machines
5. **Selective cache clearing**: Clear cache for specific folders only
6. **Cache compression**: Reduce database size for large caches

---

## 6. UI/UX Features

### 6.1 Qt6 Interface
**What it is:**  
Native Qt6 desktop interface replacing the old GTK/Glade UI.

**How it works:**
- `MainApp` class extends `QMainWindow`
- `MainAppUiBuilder` handles UI construction
- Modern Qt widgets: QTreeView, QTableWidget, QDockWidget
- Cross-platform native look and feel
- Responsive and lightweight

**Key Components:**
- Main window with path selection and options
- Categorization review dialog
- Progress dialog during analysis
- Various settings dialogs
- File explorer dock

**How it could be improved:**
1. **Dark mode**: Native dark theme support
2. **Custom themes**: User-selectable color schemes
3. **Layout customization**: Drag-and-drop UI customization
4. **Keyboard shortcuts**: More keyboard navigation options
5. **Accessibility**: Better screen reader support
6. **Tablet mode**: Touch-friendly interface for tablet devices

### 6.2 File Explorer Dock
**What it is:**  
Integrated file system browser in the main window.

**How it works:**
- Dockable side panel showing file system
- QTreeView with QFileSystemModel
- Click folder to set as sort target
- View → Toggle File Explorer to show/hide
- Persistent state across sessions

**How it could be improved:**
1. **Favorites/bookmarks**: Quick access to common folders
2. **Recent folders**: History of recently analyzed folders
3. **Folder preview**: Show folder stats (file count, size) on hover
4. **Custom icons**: Show preview thumbnails for image folders
5. **Multi-select**: Select multiple folders for batch processing
6. **Context menu**: Right-click operations (open, properties, etc.)

### 6.3 Multilingual UI (Internationalization)
**What it is:**  
User interface available in multiple languages.

**How it works:**
- Gettext-based translation system
- `TranslationManager` and `UiTranslator` classes
- Supported UI languages: Dutch, English, French, German, Italian, Polish, Portuguese, Spanish, Turkish
- Settings → Language menu
- Translations stored in PO files
- Runtime language switching

**Implementation Details:**
```cpp
// Located in: app/include/UiTranslator.hpp
class UiTranslator {
    void set_language(Language lang);
    void retranslate_ui(MainApp& app);
};
```

**How it could be improved:**
1. **Community translations**: Easy contribution of new translations
2. **Translation completeness**: Show % translated for each language
3. **Context help**: Show original English text as tooltip
4. **Automatic language detection**: Use system language by default
5. **Custom terminology**: Allow users to customize translations
6. **Fallback chains**: Fallback to similar language if translation missing

### 6.4 Progress Reporting
**What it is:**  
Real-time feedback during file categorization.

**How it works:**
- `CategorizationProgressDialog` shows progress
- Progress callbacks from `CategorizationService`
- Shows: current file being processed, cached vs LLM categorizations
- Queue display shows pending files
- Stop button to cancel analysis

**How it could be improved:**
1. **Time estimates**: Show estimated time remaining
2. **Detailed stats**: Show processing speed (files/sec)
3. **Pause button**: Pause analysis instead of just stopping
4. **Background processing**: Minimize to system tray while processing
5. **Notification**: Desktop notification when complete
6. **Detailed log**: Expandable log showing all operations

### 6.5 Error Handling System (HEAVILY CUSTOMIZED)
**What it is:**  
Comprehensive error code system with user-friendly messages and resolution steps.

**How it works:**
- 100+ unique error codes organized by category
- `ErrorCode.hpp` defines error catalog
- `AppException` class for structured exceptions
- Enhanced error dialogs with "Copy Error Details" button
- Each error includes: code, message, resolution steps, technical details

**Error Categories:**
- 1000-1099: Network errors
- 1100-1199: API errors
- 1200-1299: File system errors
- 1300-1399: Database errors
- 1400-1499: LLM errors
- 1500-1599: Configuration errors
- 1600-1699: Validation errors
- 1700-1799: System errors
- 1800-1899: Categorization errors
- 1900-1999: Download errors

**Implementation Details:**
```cpp
// Located in: app/include/ErrorCode.hpp
struct ErrorInfo {
    std::string message;
    std::string resolution;
};

class ErrorCatalog {
    static const ErrorInfo& get_info(Code code);
};

// Located in: app/include/AppException.hpp
class AppException : public std::runtime_error {
    AppException(Code code, const std::string& context = "");
    int get_error_code_int() const;
    std::string get_full_details() const;
};
```

**Error Dialog Features:**
- Shows error code (e.g., "Error 1401")
- User-friendly message
- Step-by-step resolution instructions
- Technical details for developers/support
- Copy button for bug reports

**How it could be improved:**
1. **Error analytics**: Track which errors occur most frequently
2. **Smart suggestions**: AI-powered problem resolution
3. **Automatic recovery**: Auto-retry for transient errors
4. **Error documentation**: Link to online help for each error code
5. **Community solutions**: User-submitted fixes for common errors
6. **Telemetry**: Optional anonymous error reporting to improve app

---

## 7. Platform & Performance Features

### 7.1 Multi-Backend GPU Acceleration
**What it is:**  
Support for multiple GPU acceleration backends for local LLM inference.

**How it works:**
- Three backends: Vulkan, CUDA, CPU (OpenBLAS)
- Runtime auto-detection in launcher scripts
- Priority order: Vulkan → CUDA → CPU
- Command-line override flags available
- Separate llama.cpp builds per backend

**Supported Platforms:**
- **Vulkan**: Cross-platform (Linux, Windows, macOS)
- **CUDA**: NVIDIA GPUs only (Linux, Windows)
- **Metal**: macOS Apple Silicon
- **CPU**: Universal fallback with OpenBLAS

**Build Process:**
- Linux: `build_llama_linux.sh` with cuda/vulkan flags
- Windows: `build_llama_windows.ps1` with cuda/vulkan flags
- macOS: `build_llama_macos.sh` (Metal automatic)

**How it could be improved:**
1. **Automatic benchmark**: Test all backends and choose fastest
2. **Hybrid execution**: Use multiple GPUs simultaneously
3. **ROCm support**: Add AMD GPU support on Linux
4. **oneAPI support**: Intel GPU acceleration
5. **Power management**: Reduce GPU usage on battery power
6. **Performance stats**: Show inference speed per backend

### 7.2 Cross-Platform Support
**What it is:**  
Native builds for Windows, macOS, and Linux.

**Platform-Specific Features:**

**Linux:**
- Debian/Ubuntu packages (.deb)
- RPM support (Fedora/RHEL)
- AUR support (Arch/Manjaro)
- Build from source support
- Multiple init systems supported

**macOS:**
- Apple Silicon (M1/M2/M3) native
- Intel Mac support
- .app bundle packaging
- Homebrew integration
- Metal acceleration

**Windows:**
- Native MSVC build
- MSI installer
- Portable version available
- CUDA/Vulkan support
- Windows 10/11 compatible

**How it could be improved:**
1. **Flatpak/Snap**: Universal Linux packaging
2. **Microsoft Store**: Windows Store distribution
3. **Mac App Store**: macOS App Store distribution
4. **Auto-updates**: Built-in update mechanism
5. **Portable mode**: Run from USB drive without installation
6. **Server mode**: Command-line server for remote categorization

### 7.3 Update Notifications
**What it is:**  
System that notifies users about new versions.

**How it works:**
- `Updater` class checks for updates
- Optional vs required update flows
- Version comparison with current version
- Skippable version tracking
- GitHub releases integration

**How it could be improved:**
1. **Automatic download**: Download updates in background
2. **Change highlights**: Show what's new in update
3. **Beta channel**: Opt-in to beta releases
4. **Rollback support**: Easy downgrade if update causes issues
5. **Update scheduling**: Schedule updates for convenient time
6. **Selective updates**: Choose which components to update

---

## 8. Developer & Configuration Features

### 8.1 Development Mode Features
**What it is:**  
Special features for developers and advanced users.

**Features:**
- **Prompt Logging**: Log all LLM prompts and responses
- **Consistency Pass**: Manual consistency harmonization
- **Cache Management**: Clear categorization cache
- **Development Menu**: Hidden menu with advanced tools

**How it works:**
- Enabled via Settings → Development menu
- Prompt logging stores prompts to log files
- Helps debug categorization issues
- Useful for model fine-tuning

**How it could be improved:**
1. **Debug console**: Live console for running commands
2. **API playground**: Test LLM prompts interactively
3. **Performance profiler**: Profile CPU/memory usage
4. **Network inspector**: Monitor API calls
5. **Database browser**: Browse/edit database directly
6. **Testing mode**: Automated testing features

### 8.2 Configuration Management
**What it is:**  
Settings system for persistent configuration.

**How it works:**
- `Settings` class manages configuration
- `IniConfig` wrapper around QSettings
- Config file: `config.ini` in app data folder
- Stores: LLM choice, API keys, UI preferences, file scan options
- Automatic save on changes

**Configuration Locations:**
- **Linux**: `~/.config/aifilesorter/config.ini`
- **macOS**: `~/Library/Preferences/aifilesorter/config.ini`
- **Windows**: `%APPDATA%\aifilesorter\config.ini`

**How it could be improved:**
1. **Config profiles**: Multiple configuration profiles
2. **Import/export**: Share configs between machines
3. **Cloud sync**: Sync settings via cloud service
4. **Config validation**: Detect and fix corrupted configs
5. **Reset to defaults**: Easy reset of all settings
6. **Config encryption**: Encrypt sensitive settings (API keys)

### 8.3 Testing Infrastructure
**What it is:**  
Catch2-based unit test suite for quality assurance.

**How it works:**
- Optional CMake flag: `AI_FILE_SORTER_BUILD_TESTS=ON`
- Tests in `tests/unit/` directory
- CTest integration for running tests
- Test utilities for core functionality
- Continuous integration ready

**Current Coverage:**
- Core utilities
- File scanning
- Categorization logic
- Database operations

**How it could be improved:**
1. **Integration tests**: Test full workflows end-to-end
2. **UI tests**: Automated UI testing with Qt Test
3. **Performance tests**: Benchmark critical operations
4. **Regression tests**: Prevent re-introduction of bugs
5. **Code coverage**: Measure and improve test coverage
6. **Mock LLM**: Test without actual LLM calls

---

## Summary of Key Customizations

The following features show significant custom development beyond standard file organization:

1. **Google Gemini Integration** (v1.5.0) - Sophisticated rate limiting, timeout handling, circuit breaker, and retry logic specifically optimized for free tier
2. **User Profiling System** (Unreleased) - Complete adaptive learning system with characteristics, folder insights, and organizational templates
3. **Per-Folder Learning Control** - Granular privacy control with three learning levels
4. **Two Categorization Modes** - "More Refined" vs "More Consistent" with session-based consistency hints
5. **Category Whitelists** - Named, reusable category constraints with multiple whitelist management
6. **Dry Run/Preview Mode** (v1.4.0) - Safe preview before committing file moves
7. **Persistent Undo** (v1.4.0) - Restore file moves even after app restart
8. **Error Code System** - Comprehensive 100+ error codes with user-friendly messages and resolution steps
9. **Multi-Backend GPU Support** - Vulkan, CUDA, Metal support with auto-detection and fallback
10. **Consistency Pass Service** - Post-processing harmonization for maximum category consistency

---

## Overall Recommendations for Improvement

### High Priority
1. **Performance Optimization**: Parallel file processing for faster categorization
2. **Content Analysis**: Add actual file content analysis (not just name/extension)
3. **Undo History**: Multiple undo points instead of just one
4. **Profile Insights**: Better visualization and actionable recommendations
5. **Error Recovery**: Automatic retry and recovery for transient failures

### Medium Priority
1. **Batch Operations**: Process multiple folders simultaneously
2. **Template Marketplace**: Share organization templates with community
3. **Advanced Filtering**: Better search and filter in results
4. **Cloud Integration**: Optional cloud sync for settings and profiles
5. **Mobile Companion**: Mobile app for remote monitoring/control

### Low Priority
1. **Plugin System**: Allow community-developed extensions
2. **Scripting API**: Automate tasks with Python/JavaScript
3. **Server Mode**: Network API for remote categorization
4. **Advanced Analytics**: Detailed statistics and insights
5. **Integration Hooks**: Connect with other file management tools

---

## Conclusion

AI File Sorter is a sophisticated, well-architected application with extensive customization in several key areas. The codebase shows strong software engineering practices including:

- Clean separation of concerns (UI, business logic, data access)
- Comprehensive error handling with user-friendly messaging
- Flexible architecture supporting multiple LLM backends
- Thoughtful privacy controls (per-folder learning levels)
- Performance optimizations (caching, GPU acceleration)
- Extensibility (custom LLMs, whitelists, templates)

The recent additions (Gemini integration, user profiling, dry run/undo) represent substantial enhancements that significantly improve both functionality and user experience. The error code system in particular shows excellent attention to user experience and supportability.

The most innovative customizations are:
1. The intelligent rate limiting and retry logic for Gemini's free tier
2. The user profiling system that learns organization patterns
3. The dual categorization modes with consistency hints
4. The granular per-folder privacy controls

These features demonstrate deep understanding of both the problem domain (file organization) and the technical constraints (API limits, privacy concerns, user preferences).
