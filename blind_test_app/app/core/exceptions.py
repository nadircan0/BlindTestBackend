from fastapi import HTTPException, status


class BlindTestException(Exception):
    """Base exception class for Blind Test application"""
    pass


class UserNotFoundError(BlindTestException):
    """Raised when user is not found"""
    pass


class InvalidCredentialsError(BlindTestException):
    """Invalid credentials"""
    pass


class InsufficientPermissionsError(BlindTestException):
    """Insufficient permissions"""
    pass


class ModelNotFoundError(BlindTestException):
    """Raised when model is not found"""
    pass


class TestNotFoundError(BlindTestException):
    """Raised when test is not found"""
    pass


class InputPoolNotFoundError(BlindTestException):
    """Raised when input pool is not found"""
    pass


class QuestionNotFoundError(BlindTestException):
    """Raised when question is not found"""
    pass


# HTTP Exceptions
def raise_user_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


def raise_invalid_credentials():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def raise_insufficient_permissions():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient permissions for this operation"
    )


def raise_model_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Model not found"
    )


def raise_test_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Test not found"
    )


def raise_input_pool_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Input pool not found"
    )


def raise_question_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Question not found"
    )


def raise_email_already_exists():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email address already registered"
    )


def raise_inactive_user():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User account is inactive"
    )


def raise_foreign_key_violation(resource: str):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Referenced {resource} does not exist"
    )


def raise_validation_error(message: str):
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=f"Validation error: {message}"
    )


def raise_server_error(message: str = "Internal server error"):
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=message
    )
