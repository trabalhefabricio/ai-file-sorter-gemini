#ifndef STARTUPERRORDIALOG_HPP
#define STARTUPERRORDIALOG_HPP

#include <QDialog>
#include <QString>
#include <string>

class QTextEdit;
class QPushButton;

/**
 * @brief Dialog to display detailed startup error information
 * 
 * This dialog shows comprehensive error information including:
 * - Error message
 * - Log file locations
 * - System information
 * - Actionable steps for users
 * 
 * Users can copy all information to clipboard for bug reports.
 */
class StartupErrorDialog : public QDialog
{
    Q_OBJECT

public:
    explicit StartupErrorDialog(const std::string& error_message,
                                const std::string& error_details,
                                QWidget* parent = nullptr);
    ~StartupErrorDialog() override = default;

    /**
     * @brief Shows a startup error dialog with the given error information
     * @param error_message The main error message
     * @param error_details Additional error details (e.g., exception.what())
     * @param parent Parent widget
     */
    static void show_startup_error(const std::string& error_message,
                                   const std::string& error_details,
                                   QWidget* parent = nullptr);

private slots:
    void copy_to_clipboard();
    void open_log_directory();

private:
    void setup_ui();
    QString generate_error_report() const;
    QString get_system_info() const;

    QString error_message_;
    QString error_details_;
    QString log_directory_;
    
    QTextEdit* text_display_{nullptr};
    QPushButton* copy_button_{nullptr};
    QPushButton* open_logs_button_{nullptr};
    QPushButton* close_button_{nullptr};
};

#endif // STARTUPERRORDIALOG_HPP
