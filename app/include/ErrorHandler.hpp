#ifndef ERRORHANDLER_HPP
#define ERRORHANDLER_HPP

#include <QWidget>
#include <QString>
#include <string>

/**
 * @brief Enhanced error handling utility with context and logging integration
 * 
 * This class provides improved error dialogs that include:
 * - Actionable error messages
 * - Log file location information
 * - Quick access to logs
 * - Copy error details functionality
 */
class ErrorHandler
{
public:
    /**
     * @brief Shows an enhanced error dialog with log file context
     * @param parent Parent widget
     * @param title Dialog title
     * @param message Main error message
     * @param details Optional detailed error information
     * @param include_log_info Whether to include log file location in the message
     */
    static void show_error_with_context(QWidget* parent,
                                       const QString& title,
                                       const QString& message,
                                       const QString& details = QString(),
                                       bool include_log_info = true);

    /**
     * @brief Shows an error dialog with option to open log directory
     * @param parent Parent widget
     * @param title Dialog title
     * @param message Main error message
     * @param details Optional detailed error information
     */
    static void show_error_with_log_access(QWidget* parent,
                                          const QString& title,
                                          const QString& message,
                                          const QString& details = QString());

    /**
     * @brief Logs an error and shows a user-friendly dialog
     * @param parent Parent widget
     * @param logger_name Name of the logger to use (e.g., "core_logger")
     * @param title Dialog title
     * @param user_message Message shown to user
     * @param technical_details Technical details logged to file
     */
    static void log_and_show_error(QWidget* parent,
                                   const std::string& logger_name,
                                   const QString& title,
                                   const QString& user_message,
                                   const std::string& technical_details);

    /**
     * @brief Gets a formatted string with log directory information
     * @return Formatted log location message
     */
    static QString get_log_location_message();

    /**
     * @brief Opens the log directory in the system file explorer
     * @param parent Parent widget for error dialogs
     * @return true if successful, false otherwise
     */
    static bool open_log_directory(QWidget* parent = nullptr);

private:
    ErrorHandler() = delete;  // Static utility class
};

#endif // ERRORHANDLER_HPP
