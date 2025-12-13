"""
Password validation module.
Validates password strength and safety.
"""
from typing import Dict, Any
import re


class PasswordValidator:
    """Class to validate password strength."""
    
    def __init__(self, min_length: int = 8):
        self.min_length = min_length
    
    def validate_strength(self, password: str) -> Dict[str, Any]:
        """
        Validates password strength.
        
        Args:
            password: Password to validate
            
        Returns:
            Dict with validation results
        """
        results = {
            "valid": True,
            "score": 0,
            "issues": []
        }
        
        # Length check
        if len(password) < self.min_length:
            results["valid"] = False
            results["issues"].append(f"Password must be at least {self.min_length} chars")
        else:
            results["score"] += 1
        
        # Content checks
        if not re.search(r"[a-z]", password):
            results["issues"].append("Missing lowercase (a-z)")
        else:
            results["score"] += 1
        
        if not re.search(r"[A-Z]", password):
            results["issues"].append("Missing uppercase (A-Z)")
        else:
            results["score"] += 1
        
        if not re.search(r"\d", password):
            results["issues"].append("Missing numbers (0-9)")
        else:
            results["score"] += 1
        
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]", password):
            results["issues"].append("Missing special chars")
        else:
            results["score"] += 1
        
        return results
    
    def check_common_patterns(self, password: str) -> bool:
        """
        Checks if password contains common patterns.
        
        Args:
            password: Password to check
            
        Returns:
            True if common pattern found, False otherwise
        """
        common_patterns = [
            r"^123",
            r"password",
            r"qwerty",
            r"abc123"
        ]
        
        for pattern in common_patterns:
            if re.search(pattern, password.lower()):
                return True
        return False