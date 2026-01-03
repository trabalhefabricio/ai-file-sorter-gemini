# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Release")
  file(REMOVE_RECURSE
  "CMakeFiles/aifilesorter_autogen.dir/AutogenUsed.txt"
  "CMakeFiles/aifilesorter_autogen.dir/ParseCache.txt"
  "aifilesorter_autogen"
  "llama-build/ggml/src/CMakeFiles/ggml-base_autogen.dir/AutogenUsed.txt"
  "llama-build/ggml/src/CMakeFiles/ggml-base_autogen.dir/ParseCache.txt"
  "llama-build/ggml/src/CMakeFiles/ggml-cpu_autogen.dir/AutogenUsed.txt"
  "llama-build/ggml/src/CMakeFiles/ggml-cpu_autogen.dir/ParseCache.txt"
  "llama-build/ggml/src/CMakeFiles/ggml_autogen.dir/AutogenUsed.txt"
  "llama-build/ggml/src/CMakeFiles/ggml_autogen.dir/ParseCache.txt"
  "llama-build/ggml/src/ggml-base_autogen"
  "llama-build/ggml/src/ggml-cpu_autogen"
  "llama-build/ggml/src/ggml_autogen"
  "llama-build/src/CMakeFiles/llama_autogen.dir/AutogenUsed.txt"
  "llama-build/src/CMakeFiles/llama_autogen.dir/ParseCache.txt"
  "llama-build/src/llama_autogen"
  )
endif()
