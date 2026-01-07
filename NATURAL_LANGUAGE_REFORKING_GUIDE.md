# Natural Language Reforking Guide
## A Conversational Approach to Migrating Your Custom Features

**Created:** January 7, 2026  
**Style:** Natural language, narrative format  
**Purpose:** Guide you through re-forking in plain English without overwhelming technical details

---

## 🎯 What This Document Is

This is a **friendly, conversational guide** that walks you through re-forking the original `hyperfield/ai-file-sorter` repository while keeping all your custom work. 

**Think of it as:** Having a knowledgeable friend explain the process over coffee, not a technical manual.

**If you want technical details:** See [REFORKING_STRATEGY.md](REFORKING_STRATEGY.md) or [AI_PROMPTS_BY_IMPLEMENTATION_ORDER.md](AI_PROMPTS_BY_IMPLEMENTATION_ORDER.md)

---

## 📖 The Story So Far

You've been working on a fork of AI File Sorter and added some really cool features:
- A user profiling system that learns from your file organization habits
- Google Gemini API support with smart free-tier handling
- API usage tracking so you can monitor costs
- A "File Tinder" tool for quick file cleanup
- Cache management, better undo, dry run previews
- And more...

That's about **6,000 lines of custom code** across 7 major features. Good work!

But now you want to start fresh from the original repository. Why? Because:
- The original keeps getting updates
- Your fork has drifted too far to merge easily
- You want a clean git history
- Future maintenance will be much easier

**The challenge:** How do you start fresh without losing all that work?

**The answer:** You migrate your features one at a time to a new fork. And this guide shows you how.

---

## 🤔 Understanding the Big Picture

### What You're Actually Doing

Imagine you have a house (your current fork) that's been heavily remodeled. Now you want to move to a new house (fresh fork) and bring all your custom furniture and decorations with you.

**The process:**
1. **Look around your current house** and catalog what you've added
2. **Get the keys to the new house** (fork the original repo)
3. **Move your stuff room by room** (migrate features one at a time)
4. **Test each room after moving** (make sure features work)
5. **Enjoy your new house** (clean fork with all your features)

**Time investment:** About 6-8 weeks if you work on it part-time.

**Is it worth it?** Absolutely. Your future self will thank you when upstream updates are easy to merge.

---

## 🗺️ The Journey: A Week-by-Week Overview

### Week 1: Setting Up Your New Home

**What you'll do:** Get organized and build the foundation.

**Day 1:** Take inventory of what you have
- Go through your current fork
- List all the custom features
- Note which files belong to which feature
- Extract the database schemas you've added

**Day 2-3:** Set up the new fork and database
- Fork the original repository on GitHub
- Clone it to your computer
- Add all your custom database tables
- Test that the database creates properly

**Day 4-5:** Add helper methods
- Create utility functions for your database operations
- These are the "plumbing" that your features will use
- Test each helper function

**By end of Week 1:** You have a fresh fork with a solid foundation. No features yet, but the groundwork is laid.

---

### Week 2: The Easy Wins

**What you'll do:** Start with the simpler features to build confidence.

**Why start here:** These features are straightforward and will give you momentum.

**Day 6-7: Enhanced Undo System**
- Take your existing UndoManager code
- Enhance it to save undo plans to the database
- Now undo works even after closing the app
- **What this gives you:** Better user experience, minimal effort

**Day 8-9: Dry Run Preview**
- Add a checkbox to the categorization dialog
- When checked, show a preview instead of moving files
- **What this gives you:** Safety net for users, low risk to implement

**Day 10-12: Cache Manager Dialog**
- Create a simple settings dialog
- Show cache statistics
- Add buttons to clear cache or optimize database
- **What this gives you:** A complete feature, good confidence builder

**By end of Week 2:** You have 3 working features in your new fork. You're on a roll!

---

### Week 3: The API Features

**What you'll do:** Add Google Gemini support and API tracking.

**Day 13-17: Google Gemini API Client**
- This is moderately complex but well-documented
- Implement the client with rate limiting
- Add progressive timeouts for free tier users
- Integrate with the LLM selection dialog

**What makes this special:**
- Smart rate limiting (15 requests per minute for free tier)
- Timeout handling that adapts if requests are slow
- Retry logic that doesn't give up too easily

**What this gives you:** A third AI provider option for users

**Day 18-20: API Usage Tracking**
- Create a system to record every API call
- Track tokens used and costs
- Build a statistics dialog showing daily/monthly usage
- Add quota warnings

**What this gives you:** Cost awareness for users, professional feature

**By end of Week 3:** You have significant new capabilities added to your fork.

---

### Weeks 4-5: The Crown Jewel - User Profiling

**What you'll do:** Implement the most complex and valuable feature.

**Why this takes longer:** It's sophisticated and has multiple parts.

**Week 4, Days 21-25: Core Profiling System**

The user profiling manager analyzes files and infers things about the user:
- What hobbies they have (based on file categories)
- Their work patterns (office documents, projects, etc.)
- Their organization style (minimalist, detailed, etc.)

**How it works (conceptually):**
1. Every time files are categorized, the system looks at patterns
2. If you have lots of photography files, it infers you're into photography
3. It builds confidence scores over time
4. This context gets sent to the AI for better categorization

**Week 5, Days 26-28: User Interface Dialogs**

Create two dialogs:
1. **View Profile Dialog:** Shows what the system has learned about you
   - Your characteristics with confidence levels
   - Folder analysis history
   - Organizational templates it's discovered

2. **Folder Learning Dialog:** Configure learning per folder
   - Full learning: Use profile and store data
   - Partial learning: Store data but don't use profile
   - No learning: Keep this folder private

**Days 29-30: Integration**

Connect the profiling system to categorization:
- Add a checkbox in the main window: "Learn from my organization patterns"
- Add a settings button next to folder paths
- Inject user context into AI prompts
- Add menu item: Help → View User Profile

**By end of Week 5:** You have a complete, intelligent user profiling system. This is your signature feature.

---

### Week 6: The Utilities

**What you'll do:** Add helpful tools.

**Day 31-33: File Tinder**

This is a fun one. It's like Tinder but for files:
- Show files one at a time
- Arrow keys: → keep, ← delete, ↓ skip, ↑ back
- Preview images and text files
- Review decisions before actually deleting
- Save session so you can resume later

**Why users will love it:** Quick way to clean up messy folders

**Day 34-36: Error Reporting System (Optional)**

If you want professional error handling:
- Auto-generate detailed error reports
- Create COPILOT_ERROR_*.md files for easy bug reporting
- User-friendly error messages
- Diagnostic information collection

**By end of Week 6:** All major features are implemented!

---

### Week 7-8: Polish and Ship

**What you'll do:** Final touches and release.

**Week 7: Documentation and Testing**
- Copy all your documentation files
- Update README with new features
- Test each feature thoroughly
- Fix any bugs you find

**Week 8: Release Preparation**
- Final end-to-end testing
- Update version number
- Create release notes
- Tag the release
- Celebrate! 🎉

---

## 💡 Key Principles for Success

### 1. **One Feature at a Time**

Don't try to migrate everything at once. That's overwhelming and error-prone.

**Do this:** Pick one feature, migrate it completely, test it, commit it, then move to the next.

**Why it works:** You can track progress, each feature works before moving on, easier to debug problems.

### 2. **Test After Every Feature**

Don't wait until the end to test. Test immediately after each feature.

**What to test:**
- Does the feature work as expected?
- Does it break any existing functionality?
- Can you build the project?
- Any compiler warnings?

**Why it works:** Catches problems early when they're easy to fix.

### 3. **Commit with Meaningful Messages**

Each feature gets its own commit with a clear message.

**Good commit messages:**
- "Add Google Gemini API integration with rate limiting"
- "Implement user profiling core system"
- "Add cache manager dialog to Settings menu"

**Why it works:** Clear history, easy to understand what changed, can revert individual features if needed.

### 4. **Use AI Assistance Wisely**

You have detailed prompts in [AI_PROMPTS_BY_IMPLEMENTATION_ORDER.md](AI_PROMPTS_BY_IMPLEMENTATION_ORDER.md) if you want AI help.

**How to use them:**
- Copy the entire prompt for a feature
- Give it to your AI assistant (GitHub Copilot, Claude, etc.)
- Review the generated code carefully
- Test before committing

**Why it works:** Speeds up implementation, but you stay in control.

### 5. **Don't Panic If Something Doesn't Work**

You will hit issues. That's normal.

**When something breaks:**
1. Read the error message carefully
2. Check if you missed a step
3. Look at the reference implementation in your old fork
4. Search for similar errors online
5. Take a break and come back with fresh eyes

**Remember:** You have working code in your old fork. You can always look at how it works there.

---

## 🔍 Detailed Walkthroughs

### Example: Migrating Cache Manager (The Easy One)

Let me walk through one feature in detail so you understand the process.

**Situation:** You want to add the Cache Manager dialog to your new fork.

**Step 1: Locate the Files**

In your old fork, the Cache Manager consists of:
- `app/include/CacheManagerDialog.hpp` (header file)
- `app/lib/CacheManagerDialog.cpp` (implementation)

**Step 2: Copy Files to New Fork**

```bash
cp old-fork/app/include/CacheManagerDialog.hpp new-fork/app/include/
cp old-fork/app/lib/CacheManagerDialog.cpp new-fork/app/lib/
```

**Step 3: Add to Build System**

Edit `new-fork/app/CMakeLists.txt` and add:
```
app/lib/CacheManagerDialog.cpp
```

**Step 4: Integrate with Main Application**

Edit `new-fork/app/lib/MainApp.cpp`:

Find the part where menus are created, and add:
```cpp
#include "CacheManagerDialog.hpp"

// In the Settings menu creation:
QAction* cache_action = settings_menu->addAction(tr("Manage Cache..."));
connect(cache_action, &QAction::triggered, this, [this]() {
    CacheManagerDialog dialog(*db_manager_, this);
    dialog.exec();
});
```

**Step 5: Build and Test**

```bash
cd new-fork/app
make clean
make -j4
./bin/aifilesorter
```

Click Settings → Manage Cache. Does it open? Can you see statistics? Do the buttons work?

**Step 6: Commit**

```bash
git add .
git commit -m "Add cache manager dialog

- View cache statistics (entries, size, dates)
- Clear all cache with confirmation
- Clear cache older than X days
- Optimize database (VACUUM)
- Integrated into Settings menu
"
```

**Done!** One feature migrated. 12 more to go (but they follow the same pattern).

---

### Example: The Harder One - User Profiling

This one is more complex because it has multiple parts that work together.

**The Big Picture:**

User Profiling has three layers:
1. **Core Engine:** UserProfileManager class (the brain)
2. **User Interface:** Two dialogs (the face)
3. **Integration:** Hooks into categorization (the connections)

**Strategy:** Build layer by layer, test each layer before moving on.

**Layer 1: The Core Engine (UserProfileManager)**

This is the logic that analyzes files and builds the user profile.

**What it does:**
- When you categorize files, it looks at the categories
- Infers characteristics (hobbies, work patterns, style)
- Builds confidence scores
- Stores everything in the database

**How to migrate it:**
1. Copy `UserProfileManager.hpp` and `.cpp`
2. Add to build system
3. Create a simple test to make sure it compiles
4. Don't integrate with anything yet, just make sure the class exists

**Layer 2: The User Interface**

Two dialogs to create:

**UserProfileDialog:** Shows the learned profile
- Three tabs: Overview, Characteristics, Folder Insights
- Displays data in readable format
- Read-only, just for viewing

**FolderLearningDialog:** Configures per-folder settings
- Simple dialog with radio buttons
- Full / Partial / No learning options
- Saves to database

**How to migrate:**
1. Copy dialog files
2. Add to build system
3. Test by manually opening each dialog
4. Make sure they display data correctly

**Layer 3: Integration**

Now connect everything:

**In MainApp:**
- Add "Learn from my organization patterns" checkbox
- Add settings button next to folder path
- Connect to UserProfileManager
- Add Help → View User Profile menu item

**In CategorizationService:**
- When categorizing, check if learning is enabled
- Call UserProfileManager to analyze files
- Get user context from profile
- Include context in AI prompts

**How to migrate:**
1. Update MainApp with UI elements
2. Connect buttons and checkboxes to profile manager
3. Update categorization to use profile
4. Test end-to-end

**Testing the Whole Thing:**

1. Enable learning checkbox
2. Categorize a folder with photography files
3. Check Help → View User Profile
4. You should see "Photography" as a hobby
5. Categorize more folders
6. Watch confidence scores increase
7. Verify AI gets better suggestions over time

**This takes 2 weeks** because there's a lot of code, but it's very rewarding when it works!

---

## 🎓 Learning from the Process

### What You'll Gain

By doing this migration, you're not just moving code. You're:

**1. Understanding Your Own Code Better**

Going through each feature again helps you remember why you built things the way you did.

**2. Improving Your Implementation**

As you migrate, you'll notice things you could do better. Feel free to improve as you go!

**3. Building Confidence**

Each successfully migrated feature proves you can do this. By week 3, you'll be flying.

**4. Creating Documentation**

The commit messages and notes you make become documentation for future you.

### Common Pitfalls and How to Avoid Them

**Pitfall #1: Trying to rush**
- **Symptom:** Copying many features at once without testing
- **Result:** Everything breaks and you don't know why
- **Solution:** One feature at a time, test each one

**Pitfall #2: Forgetting dependencies**
- **Symptom:** Feature won't compile because it needs something else first
- **Result:** Frustration and wasted time
- **Solution:** Follow the order in this guide, it accounts for dependencies

**Pitfall #3: Not testing edge cases**
- **Symptom:** Feature works in happy path but crashes in unusual situations
- **Result:** Users encounter bugs, you lose trust
- **Solution:** Test with weird inputs, empty folders, large files, etc.

**Pitfall #4: Skipping documentation**
- **Symptom:** Finish migration but forgot what you changed
- **Result:** Confusion when you need to update something later
- **Solution:** Write clear commit messages, keep notes

---

## 🔮 The Yet-to-be-Implemented Features

You have database tables ready for features you haven't built yet:

### 1. Confidence Scoring System

**What it would do:** Show how confident the AI is about each categorization.

**Why it's useful:** Users can focus manual review on low-confidence items.

**Status:** Database table exists, no code yet.

**If you want to add it later:** You have the foundation, just need to implement the scoring logic and UI.

### 2. Content Analysis Cache

**What it would do:** Analyze file contents (not just names) for better categorization.

**Why it's useful:** Text documents could be categorized by their content, not just filename.

**Status:** Database table exists, no code yet.

**If you want to add it later:** Would need content extraction, keyword detection, caching logic.

### 3. Session Management

**What it would do:** Save categorization sessions and resume them later.

**Why it's useful:** Large folders could be categorized in multiple sittings.

**Status:** Database table exists, no code yet.

**If you want to add it later:** Need session state serialization and resume logic.

### 4. User Corrections Learning

**What it would do:** Learn when users manually change categories and improve suggestions.

**Why it's useful:** The system gets smarter from corrections.

**Status:** Database table exists, no code yet, but pairs well with User Profiling.

**If you want to add it later:** Easier to add once User Profiling is working.

### 5. Multi-level Undo/Redo

**What it would do:** Multiple undo levels, not just the last operation.

**Why it's useful:** More flexible undo, redo support, undo timeline.

**Status:** Enhanced undo table exists, basic undo works, can be extended.

**If you want to add it later:** Build on the enhanced undo you'll migrate.

---

## 💪 Staying Motivated

This is a long project (6-8 weeks). Here's how to stay on track:

### Break It Into Milestones

**Milestone 1:** Foundation complete (end of Week 1)
- **Reward:** Treat yourself to your favorite snack

**Milestone 2:** Three features working (end of Week 2)
- **Reward:** Take a day off, do something fun

**Milestone 3:** API features done (end of Week 3)
- **Reward:** Share progress on social media, celebrate!

**Milestone 4:** User Profiling working (end of Week 5)
- **Reward:** This is huge, take the weekend off

**Milestone 5:** All features migrated (end of Week 6)
- **Reward:** You're almost done, push through!

**Milestone 6:** Released! (end of Week 8)
- **Reward:** You did it! 🎉 Celebrate properly

### Track Your Progress

Create a simple checklist:
```
Week 1: Foundation
  [✓] Day 1: Inventory
  [✓] Day 2-3: Database
  [✓] Day 4-5: Helpers
  
Week 2: Easy Wins
  [✓] Day 6-7: Enhanced Undo
  [✓] Day 8-9: Dry Run
  [✓] Day 10-12: Cache Manager
  
Week 3: API Features
  [✓] Day 13-17: Gemini
  [✓] Day 18-20: API Tracking
  
...
```

Checking off items feels great and shows progress!

### When You Feel Stuck

**Remember:**
- You've already built these features once
- You have working code to reference
- The hard part (designing the features) is done
- This is just moving things, not inventing from scratch
- Future you will love present you for doing this

---

## 🎯 The Finish Line

After 6-8 weeks, you'll have:

✅ A **clean fork** of the original repository  
✅ All **7 custom features** working perfectly  
✅ **6,000 lines** of your code in the new fork  
✅ A **professional git history** that makes sense  
✅ The ability to **easily merge upstream updates**  
✅ **No technical debt** from the old fork  
✅ **Pride** in your accomplishment  

And most importantly: **You'll never have to do this again** because your fork can now easily sync with upstream.

---

## 📚 Additional Resources

**For more details:**
- [REFORKING_STRATEGY.md](REFORKING_STRATEGY.md) - Complete technical strategy
- [AI_PROMPTS_BY_IMPLEMENTATION_ORDER.md](AI_PROMPTS_BY_IMPLEMENTATION_ORDER.md) - AI-ready prompts
- [QUICK_START_REFORKING.md](QUICK_START_REFORKING.md) - Quick commands reference

**For understanding features:**
- [FEATURE_ANALYSIS.md](FEATURE_ANALYSIS.md) - Detailed feature documentation
- [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) - Original implementation plans

---

## 🤝 Final Thoughts

Migrating a fork is like moving houses. It's work, but it's worth it for the fresh start and clean foundation.

**You've got this!** 

Take it one week at a time, one feature at a time, one commit at a time. Before you know it, you'll be done and you'll have a fork you're proud of.

**Good luck on your reforking journey!** 🚀

---

**Document Version:** 1.0  
**Last Updated:** January 7, 2026  
**Style:** Natural language, conversational  
**Next Steps:** Start with Week 1, Day 1 - take inventory of your features
