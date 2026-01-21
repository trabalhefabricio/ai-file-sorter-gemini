#ifndef DIALOGUTILS_HPP
#define DIALOGUTILS_HPP

#include <string>

class QWidget;

class DialogUtils {
public:
    /**
     * @brief Shows a basic error dialog
     * @param parent Parent widget
     * @param message Error message to display
     */
    static void show_error_dialog(QWidget* parent, const std::string& message);

    /**
     * @brief Shows an error dialog with log file information
     * @param parent Parent widget
     * @param message Error message to display
     * @param include_log_info Whether to include log file location
     */
    static void show_error_with_logs(QWidget* parent, 
                                     const std::string& message,
                                     bool include_log_info = true);

    /**
     * @brief Shows an error dialog with detailed information and log access
     * @param parent Parent widget
     * @param message Main error message
     * @param details Detailed error information
     */
    static void show_detailed_error(QWidget* parent,
                                   const std::string& message,
                                   const std::string& details);
};

#endif // DIALOGUTILS_HPP
