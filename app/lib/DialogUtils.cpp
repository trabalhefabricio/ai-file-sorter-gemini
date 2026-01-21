#include "DialogUtils.hpp"
#include "ErrorHandler.hpp"
#include "Logger.hpp"

#include <QMessageBox>
#include <QObject>
#include <QString>

void DialogUtils::show_error_dialog(QWidget* parent, const std::string& message)
{
    QMessageBox::critical(parent, QObject::tr("Error"), QString::fromStdString(message));
}

void DialogUtils::show_error_with_logs(QWidget* parent, 
                                       const std::string& message,
                                       bool include_log_info)
{
    ErrorHandler::show_error_with_context(
        parent,
        QObject::tr("Error"),
        QString::fromStdString(message),
        QString(),
        include_log_info
    );
}

void DialogUtils::show_detailed_error(QWidget* parent,
                                      const std::string& message,
                                      const std::string& details)
{
    ErrorHandler::show_error_with_log_access(
        parent,
        QObject::tr("Error"),
        QString::fromStdString(message),
        QString::fromStdString(details)
    );
}
