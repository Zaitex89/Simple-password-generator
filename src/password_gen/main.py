"""main.py
Main program for password generator. Interactive with CLI.
"""

import sys
import logging
from typing import Optional
from .generator import generate_password
from .strength import assess_password
from . import utils
from .logging_config import setup_logging
from .validators import PasswordValidator

# Clipboard handling
CLIPBOARD_AVAILABLE = False
try:
    import pyperclip as _pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    _pyperclip = None


def copy_to_clipboard(text: str) -> bool:
    """
    Copy text to clipboard if available.
    
    Args:
        text: Text to copy
        
    Returns:
        True if successful, False otherwise
    """
    if not CLIPBOARD_AVAILABLE or _pyperclip is None:
        return False
    
    try:
        _pyperclip.copy(text)
        return True
    except Exception as e:
        print(f"Could not copy to clipboard: {e}")
        return False


MENU = '''
=== PASSWORD GENERATOR ===
1) Generate one password
2) Generate multiple passwords
3) Analyze existing password
4) Save password (latest generated)
5) Quit
Pick a number: '''


def prompt_options():
    """Ask the user which categories to use."""
    use_lower = utils.ask_yes_no("Include lowercase letters (a-z)?", default=True)
    use_upper = utils.ask_yes_no("Include uppercase letters (A-Z)?", default=True)
    use_digits = utils.ask_yes_no("Include digits (0-9)?", default=True)
    use_symbols = utils.ask_yes_no("Include symbols (e.g. !@#)?", default=False)
    return use_upper, use_lower, use_digits, use_symbols


setup_logging()
logger = logging.getLogger(__name__)


def main():
    logger.info("Programme started")
    latest = []  # list of most recently generated passwords
    validator = PasswordValidator(min_length=8)
    
    while True:
        try:
            choice = input(MENU).strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            sys.exit(0)

        if choice == "1":
            length = utils.ask_int("Password length (default 16): ", min_value=1, default=16)
            try:
                use_upper, use_lower, use_digits, use_symbols = prompt_options()
                pwd = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
                print(f"\nGenerated password: {pwd}")
                
                # Validate the generated password
                validation = validator.validate_strength(pwd)
                entropy_report = assess_password(pwd)
                
                print(f"\nPassword Analysis:")
                print(f"   Validation Score: {validation['score']}/5")
                print(f"   Entropy: {entropy_report['entropy_bits']} bits")
                print(f"   Strength: {entropy_report['label']}")
                
                if validation['issues']:
                    print("\n  Note:")
                    for issue in validation['issues']:
                        print(f"   - {issue}")
                
                # Check for common patterns
                if validator.check_common_patterns(pwd):
                    print("\n  Warning: Password contains common patterns!")
                
                # Offer copy to clipboard
                if CLIPBOARD_AVAILABLE and utils.ask_yes_no("\nCopy password to clipboard?", default=True):
                    if copy_to_clipboard(pwd):
                        print(" Copied to clipboard.")
                    else:
                        print(" Could not copy to clipboard.")
                
                latest = [pwd]
                logger.info(f"Generated password with length {length}, score: {validation['score']}, entropy: {entropy_report['entropy_bits']}")
            except ValueError as e:
                print(f"Error: {e}")
                logger.error(f"Error generating password: {e}")

        elif choice == "2":
            n = utils.ask_int("Number of passwords to generate: ", min_value=1, default=5)
            length = utils.ask_int("Length of each password (default 16): ", min_value=1, default=16)
            try:
                use_upper, use_lower, use_digits, use_symbols = prompt_options()
                results = []
                for _ in range(n):
                    pwd = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
                    results.append(pwd)
                
                print("\nGenerated passwords:")
                for i, p in enumerate(results, 1):
                    val = validator.validate_strength(p)
                    entropy = assess_password(p)
                    print(f"{i}: {p}")
                    print(f"   Score: {val['score']}/5 | Entropy: {entropy['entropy_bits']} bits | {entropy['label']}")
                
                latest = results
                
                if CLIPBOARD_AVAILABLE and utils.ask_yes_no("\nCopy the first password to clipboard?", default=False):
                    if copy_to_clipboard(results[0]):
                        print(" Copied first password to clipboard.")
                    else:
                        print(" Could not copy to clipboard.")
                
                logger.info(f"Generated {n} passwords")
            except ValueError as e:
                print(f"Error: {e}")
                logger.error(f"Error generating passwords: {e}")

        elif choice == "3":
            # Combined password analysis - both validation and entropy
            pwd = input("Paste or type the password to analyze: ")
            if not pwd:
                print("No password provided.")
                continue
            
            # Get both validation and entropy results
            validation = validator.validate_strength(pwd)
            entropy_report = assess_password(pwd)
            
            print(f"\n{'='*60}")
            print("PASSWORD ANALYSIS")
            print(f"{'='*60}")
            print(f"Password: {pwd}")
            print(f"Length: {len(pwd)} characters")
            
            # Quick summary
            print(f"\nOverall Assessment:")
            print(f"   Validation Score: {validation['score']}/5")
            print(f"   Entropy: {entropy_report['entropy_bits']} bits")
            print(f"   Strength Rating: {entropy_report['label']}")
            print(f"   Status: {' VALID' if validation['valid'] else ' INVALID'}")
            
            # Common patterns check
            has_patterns = validator.check_common_patterns(pwd)
            if has_patterns:
                print(f"   Pattern Check:   Contains common patterns")
            else:
                print(f"   Pattern Check:  No common patterns")
            
            # Detailed issues if any exist
            all_issues = []
            
            if validation['issues']:
                all_issues.extend(validation['issues'])
            
            if entropy_report['recommendations']:
                all_issues.extend(entropy_report['recommendations'])
            
            if all_issues:
                print(f"\nRecommendations for Improvement:")
                # Remove duplicates while preserving order
                seen = set()
                for issue in all_issues:
                    if issue not in seen:
                        seen.add(issue)
                        print(f"   - {issue}")
            else:
                print(f"\n Excellent! No issues found.")
            
            if has_patterns:
                print(f"\n  WARNING: Password contains common patterns")
                print(f"   (e.g., '123', 'password', 'qwerty', 'abc123')")
                print(f"   Consider using a completely random password for better security.")
            
            print(f"{'='*60}")
            logger.info(f"Analyzed password - Score: {validation['score']}, Entropy: {entropy_report['entropy_bits']}, Patterns: {has_patterns}")

        elif choice == "4":
            if not latest:
                print("No recently generated passwords to save.")
                continue
            path = input("File to save to (default passwords.txt): ").strip() or "passwords.txt"
            append = utils.ask_yes_no("Append to file?", default=True)
            ok = utils.save_to_file(path, latest, append=append)
            if ok:
                print(f" Saved {len(latest)} password(s) to {path}")
                logger.info(f"Saved {len(latest)} passwords to {path}")

        elif choice == "5":
            print("\nGoodbye!")
            logger.info("Programme ended")
            sys.exit(0)

        else:
            print(" Invalid choice — choose a number between 1 and 5.")


if __name__ == "__main__":
    main()