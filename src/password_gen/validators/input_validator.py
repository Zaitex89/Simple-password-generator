"""Input validation module."""
from typing import Optional
import re


class InputValidator:
    """Class for validating user input with security measures."""
    
    MAX_INPUT_LENGTH = 100
    MAX_INTEGER_LENGTH = 15

    @staticmethod
    def clear_input(value: str, max_length: int = MAX_INPUT_LENGTH) -> Optional[str]:
        """
        clear input string to prevent DoS attacks.

        Args: Value: Input string to clear
        max_length: Max allowed length

        returns: clear string or none if invalid
        """
        if not isinstance(value, str):
            return None
        
        if len(value) > max_length:
            print(f"Input too long (max {max_length} chars)")
            return None
        
        # Stripping whitespace
        return value.strip()
    

    @staticmethod
    def validate_integer(
        value: str, 
        min_val: Optional[int] = None, 
        max_val: Optional[int] = None
    ) -> Optional[int]:
        """
        Validate and convert input to integer with security checks.
        
        Args:
            value: Input string to validate
            min_val: Min allowed value
            max_val: Max allowed value
            
        Returns:
            Integer if valid, None otherwise
        """
        # Clear input first
        clean_value = InputValidator.clear_input(value, max_length=InputValidator.MAX_INTEGER_LENGTH)
        if clean_value is None:
            return None
        
        # Check if input contains valid chars 
        if not re.match(r'^-?\d+$', clean_value):
            print(f"'{value}' is not a valid integer")
            return None

        try:
            num = int(clean_value)

            if abs(num) > 2**10:
                print("Number is too large")
                return None
            
            if min_val is not None and num < min_val:
                print(f"Value must be at least {min_val}")
                return None
            
            if max_val is not None and num > max_val:
                print(f"Value must be at most {max_val}")
                return None
            
            return num
        
        except ValueError:
            print(f"'{value}' is not a valid integer")
            return None
    
    @staticmethod
    def validate_boolean(value: str) -> Optional[bool]:
        """
        Convert input to boolean with security checks.
        
        Args:
            value: Input string (y/n, yes/no, true/false)
            
        Returns:
            Boolean if valid, None otherwise
        """

        # clear input first
        clean_value = InputValidator.clear_input(value, max_length=10)
        if clean_value is None:
            return None
        
        clean_value = clean_value.lower()


        if clean_value in ['y', 'yes', 'true', '1']:
            return True
        elif clean_value in ['n', 'no', 'false', '0']:
            return False
        else:
            print("Invalid value. Use y/n or yes/no")
            return None
        
    @staticmethod
    def validate_string(
        value: str,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        allow_empty: bool = False,
        allowed_chars: Optional[str] = None
    ) -> Optional[str]:
        """
        Validate string input with security checks.
        
        Args:
            value: String to validate
            min_length: Min string length
            max_length: Max string length (default 1000)
            allow_empty: Whether empty strings are allowed
            allowed_chars: Regex pattern of allowed characters
            
        Returns:
            String if valid, None otherwise
        """
        # Set default max if not specified
        if max_length is None:
            max_length = 1000
        
        # Sanitize
        clean_value = InputValidator.clear_input(value, max_length=max_length)
        if clean_value is None:
            return None
        
        # Empty check
        if not allow_empty and not clean_value:
            print("Value cannot be empty")
            return None
        
        # Length checks
        if min_length is not None and len(clean_value) < min_length:
            print(f"Value must be at least {min_length} characters")
            return None
        
        if max_length is not None and len(clean_value) > max_length:
            print(f"Value must be at most {max_length} characters")
            return None
        
        # Character validation
        if allowed_chars is not None:
            if not re.match(allowed_chars, clean_value):
                print(f"Value contains invalid characters")
                return None
        
        return clean_value
    
    @staticmethod
    def validate_filename(value: str) -> Optional[str]:
        """
        Validate filename to prevent path traversal attacks.
        
        Args:
            value: Filename to validate
            
        Returns:
            Sanitized filename or None if invalid
        """
        # Sanitize
        clean_value = InputValidator.clear_input(value, max_length=255)
        if clean_value is None:
            return None
        
        # Prevent path traversal
        if '..' in clean_value or '/' in clean_value or '\\' in clean_value:
            print("Invalid filename: path traversal not allowed")
            return None
        
        # Check for valid filename characters
        # Allow alphanumeric, dash, underscore, dot
        if not re.match(r'^[\w\-. ]+$', clean_value):
            print("Invalid filename: contains illegal characters")
            return None
        
        return clean_value
