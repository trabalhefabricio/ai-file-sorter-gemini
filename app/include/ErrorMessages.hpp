#ifndef ERRORMESSAGES_H
#define ERRORMESSAGES_H

#include <libintl.h>

#define _(String) gettext(String)

// Improved error messages with actionable context
#define ERR_NO_FILES_TO_CATEGORIZE _("There are no files or directories to categorize.\n\n" \
                                     "💡 Check that:\n" \
                                     "• The selected folder contains files\n" \
                                     "• You have permission to access the folder\n" \
                                     "• Files are not already categorized")

#define ERR_INVALID_PATH _("Invalid directory path.\n\n" \
                           "💡 Please:\n" \
                           "• Verify the path exists\n" \
                           "• Check you have permission to access it\n" \
                           "• Ensure the path is not a file")

#define ERR_NO_INTERNET_CONNECTION _("No internet connection detected.\n\n" \
                                     "💡 To use remote models:\n" \
                                     "• Check your network connection\n" \
                                     "• Verify firewall settings\n" \
                                     "• Try using a local LLM instead (Settings → Select LLM)")

// New error messages for better context
#define ERR_DATABASE_ERROR _("Database operation failed.\n\n" \
                             "💡 Troubleshooting:\n" \
                             "• Check log files for details\n" \
                             "• Verify disk space is available\n" \
                             "• Restart the application")

#define ERR_LLM_INITIALIZATION _("Failed to initialize language model.\n\n" \
                                 "💡 Possible solutions:\n" \
                                 "• Check log files for specific errors\n" \
                                 "• Verify model files are not corrupted\n" \
                                 "• Try selecting a different model\n" \
                                 "• Check disk space availability")

#define ERR_API_KEY_INVALID _("API key validation failed.\n\n" \
                              "💡 Please:\n" \
                              "• Verify your API key is correct\n" \
                              "• Check the API key hasn't expired\n" \
                              "• Ensure you have available quota\n" \
                              "• Visit your API provider's dashboard")

#define INFO_LOG_LOCATION _("For more information, check the log files at:\n%1")

#endif