#ifndef APP_EXCEPTION_HPP
#define APP_EXCEPTION_HPP

#include <stdexcept>
#include <string>
#include "ErrorCode.hpp"

class AppException : public std::runtime_error {
public:
    AppException(ErrorCodes::Code code, const std::string& message)
        : std::runtime_error(message), error_code_(code) {}

    ErrorCodes::Code error_code() const { return error_code_; }

private:
    ErrorCodes::Code error_code_;
};

#endif // APP_EXCEPTION_HPP
