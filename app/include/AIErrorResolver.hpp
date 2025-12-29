#ifndef AI_ERROR_RESOLVER_HPP
#define AI_ERROR_RESOLVER_HPP

#include "ErrorCode.hpp"
#include "ILLMClient.hpp"
#include "DatabaseManager.hpp"
#include <string>
#include <vector>
#include <memory>
#include <optional>
#include <functional>

/**
 * @brief AI-powered error analysis and resolution system
 * 
 * This class provides natural language error understanding, diagnosis,
 * and automated resolution capabilities integrated with the existing
 * ErrorCode system.
 */
class AIErrorResolver {
public:
    /**
     * @brief Error category identified by AI analysis
     */
    enum class ErrorCategory {
        Network,
        API,
        FileSystem,
        Database,
        LLM,
        Configuration,
        Validation,
        System,
        Categorization,
        Download,
        Unknown
    };

    /**
     * @brief Resolution step with description and optional automated action
     */
    struct ResolutionStep {
        std::string description;
        std::string technical_detail;
        bool can_auto_fix;
        std::function<bool()> auto_fix_action;  // Returns true if fix succeeded
        
        ResolutionStep(const std::string& desc, 
                      const std::string& tech = "",
                      bool auto_fixable = false)
            : description(desc)
            , technical_detail(tech)
            , can_auto_fix(auto_fixable)
            , auto_fix_action(nullptr) {}
    };

    /**
     * @brief Complete error analysis result
     */
    struct ErrorAnalysis {
        ErrorCodes::Code error_code;
        ErrorCategory category;
        std::string ai_diagnosis;
        std::string user_friendly_explanation;
        std::vector<ResolutionStep> resolution_steps;
        float confidence_score;  // 0.0 to 1.0
        
        ErrorAnalysis()
            : error_code(ErrorCodes::Code::UNKNOWN_ERROR)
            , category(ErrorCategory::Unknown)
            , confidence_score(0.0f) {}
    };

    /**
     * @brief Resolution attempt result
     */
    struct ResolutionResult {
        bool success;
        std::string message;
        std::vector<std::string> steps_taken;
        std::string error_detail;
        
        ResolutionResult(bool succeeded = false, const std::string& msg = "")
            : success(succeeded), message(msg) {}
    };

    /**
     * @brief Construct AIErrorResolver
     * @param llm_client LLM client for natural language understanding
     * @param db_manager Database for storing resolution history
     */
    explicit AIErrorResolver(std::shared_ptr<ILLMClient> llm_client,
                            DatabaseManager& db_manager);

    /**
     * @brief Analyze error using AI
     * @param error_code The error code to analyze
     * @param context Additional context about the error
     * @param user_description Optional user description in natural language
     * @return Complete error analysis with suggested resolutions
     */
    ErrorAnalysis analyze_error(ErrorCodes::Code error_code,
                               const std::string& context = "",
                               const std::string& user_description = "");

    /**
     * @brief Parse natural language error description to identify error category
     * @param user_description User's description of the problem
     * @return Identified error category and potential error codes
     */
    std::pair<ErrorCategory, std::vector<ErrorCodes::Code>> 
        parse_natural_language_error(const std::string& user_description);

    /**
     * @brief Attempt automated resolution
     * @param analysis The error analysis containing resolution steps
     * @return Result of the resolution attempt
     */
    ResolutionResult attempt_auto_resolution(const ErrorAnalysis& analysis);

    /**
     * @brief Check if automated resolution is available for this error
     * @param error_code The error code to check
     * @return True if auto-fix is available
     */
    bool has_auto_fix(ErrorCodes::Code error_code) const;

    /**
     * @brief Get resolution history for learning
     * @param error_code Optional filter by error code
     * @param limit Maximum number of records to return
     * @return Vector of past resolution attempts
     */
    std::vector<ResolutionResult> get_resolution_history(
        std::optional<ErrorCodes::Code> error_code = std::nullopt,
        int limit = 10);

private:
    std::shared_ptr<ILLMClient> llm_client_;
    DatabaseManager& db_manager_;

    // Helper methods
    ErrorCategory categorize_error_code(ErrorCodes::Code code) const;
    std::string generate_ai_prompt(ErrorCodes::Code error_code,
                                   const std::string& context,
                                   const std::string& user_description);
    std::vector<ResolutionStep> extract_steps_from_ai_response(
        const std::string& ai_response,
        ErrorCategory category);
    void add_auto_fix_actions(ErrorAnalysis& analysis);
    bool validate_api_key(const std::string& api_key);
    bool reset_rate_limiter();
    bool check_network_connectivity();
    bool check_file_permissions(const std::string& path);
    bool attempt_database_repair();
    void log_resolution_attempt(const ErrorAnalysis& analysis,
                               const ResolutionResult& result);
};

#endif // AI_ERROR_RESOLVER_HPP
