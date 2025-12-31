# GitHub Actions Caching Strategy

This document explains the caching strategy implemented in the GitHub Actions workflows to make builds faster.

## Overview

The workflows implement a multi-layered caching approach that significantly speeds up subsequent builds by avoiding redundant downloads, installations, and compilations. On a cache hit, build times can be reduced from 30-60 minutes to 5-10 minutes.

## Linux Build Workflow (`build.yml`)

### 1. Qt Installation Cache
- **Built-in caching**: Uses `jurplel/install-qt-action@v3` with `cache: true`
- **Purpose**: Qt is ~1GB and takes several minutes to download and install
- **Managed by**: The Qt action handles caching automatically
- **Impact**: Saves 3-5 minutes per build

### 2. ccache (Compiler Cache)
- **Cache Key**: `ccache-{os}-{source-hash}`
- **Cache Location**: `~/.cache/ccache`
- **Purpose**: Caches compiled object files to avoid recompiling unchanged source
- **Configuration**: 500MB max size, compression enabled
- **Invalidation**: Changes to source files (.cpp/.h)
- **Impact**: Saves 10-20 minutes on incremental builds (most significant speedup)

### 3. CMake Build Cache
- **Cache Key**: `cmake-build-{os}-{cmake-hash}-{source-hash}`
- **Purpose**: Preserves build artifacts for incremental compilation
- **Paths Cached**:
  - `build/` - Main application build directory
  - `app/include/external/llama.cpp/build/` - llama.cpp build artifacts
- **Invalidation**: Changes to CMakeLists.txt or source files
- **Fallback Keys**: Progressive fallback to less specific cache keys
- **Impact**: Combined with ccache, enables very fast incremental builds

## Windows Build Workflow (`get_my_exe.yml`)

### 1. vcpkg Installation Cache
- **Cache Key**: `vcpkg-{os}-{vcpkg-json-hash}`
- **Purpose**: Caches vcpkg tool installation (clone + bootstrap)
- **Invalidation**: Changes to vcpkg.json
- **Impact**: Saves 2-3 minutes per build

### 2. vcpkg Binary Cache
- **Cache Key**: `vcpkg-binary-{os}-{vcpkg-json-hash}`
- **Purpose**: Caches pre-built binary packages (most important cache)
- **Packages**: curl[ssl], fmt, spdlog, jsoncpp, sqlite3
- **Configuration**: Uses GitHub Actions cache as binary source
- **Invalidation**: Changes to vcpkg.json
- **Impact**: Saves 15-30 minutes per build (each package takes 5-30 min to build)

### 3. Llama.cpp Build Cache
- **Cache Key**: `llama-build-{os}-{llama-source-hash}`
- **Purpose**: Caches llama.cpp build artifacts (most time-consuming single step)
- **Paths Cached**:
  - `app/include/external/llama.cpp/build/` - Build directory
  - `app/lib/precompiled/cpu/` - Compiled libraries
  - `app/lib/ggml/` - GGML libraries
  - `app/include/llama/` - Headers
- **Invalidation**: Changes to llama.cpp source files
- **Impact**: Saves 15-30 minutes when cache hits

### 4. CMake Build Cache
- **Cache Key**: `cmake-build-{os}-{cmake-hash}-{git-sha}`
- **Purpose**: Enables incremental compilation of the main application
- **Paths Cached**: `build/` directory
- **Invalidation**: Git SHA for precise versioning, with fallback to CMakeLists.txt
- **Impact**: Saves 5-10 minutes on incremental builds

## Cache Hierarchy and Fallback

Both workflows use progressive cache key fallback:

```yaml
key: specific-key-with-all-hashes
restore-keys: |
  less-specific-key-with-fewer-hashes
  most-general-key
```

This ensures that even if an exact match isn't found, a recent cache can still provide significant speedup.

## Cache Invalidation Strategy

Caches are invalidated when:
1. **Dependency files change** (vcpkg.json, workflow files)
2. **Source code changes** (CMakeLists.txt, .cpp/.h files)
3. **Git SHA changes** (for exact build reproducibility)

The fallback keys ensure that even with source changes, dependency caches can be reused.

## Expected Build Times

### Linux Build
- **First build (no cache)**: 15-25 minutes
- **Full cache hit**: 3-5 minutes
- **Partial cache hit**: 8-12 minutes

### Windows Build
- **First build (no cache)**: 45-60 minutes
- **Full cache hit**: 8-12 minutes
- **Partial cache hit**: 20-30 minutes

## Cache Size Limits

GitHub Actions provides 10GB of cache storage per repository. Current cache sizes:
- **Qt Linux**: ~1.5GB
- **vcpkg binaries**: ~500MB-1GB
- **Llama build**: ~200-500MB
- **CMake builds**: ~100-300MB
- **ccache**: ~500MB (configured limit)

Total: ~3-4GB (well within limits)

## Maintenance

Caches are automatically evicted based on:
1. **Age**: Not accessed for 7 days
2. **Size**: LRU when approaching the 10GB limit

No manual maintenance required.

## Monitoring Cache Effectiveness

The Linux workflow includes a "Show ccache statistics" step that reports:
- Cache hit rate
- Number of cached files
- Cache size

Monitor these stats to ensure caching is working effectively.

## Future Improvements

Potential enhancements:
1. Add sccache for Windows (similar to ccache)
2. Cache Qt installation on Windows (currently using built-in action cache)
3. Implement cache warming on main branch to benefit PRs
4. Add cache analytics dashboard
