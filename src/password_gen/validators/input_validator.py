"""Input validation module."""
from typing import Optional


class InputValidator:
    """Class for validating user input."""
    
    @staticmethod
    def validate_integer(value: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> Optional[int]:
        """Validate and convert input to integer."""
        try:
            num = int(value)
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
        """Convert input to boolean."""
        value = value.lower().strip()
        if value in ['y', 'yes', 'true', '1']:
            return True
        elif value in ['n', 'no', 'false', '0']:
            return False
        else:
            print("Invalid value. Use y/n or yes/no")
            return None