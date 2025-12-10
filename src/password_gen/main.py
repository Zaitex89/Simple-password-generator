"""main.py
Main program for password generator. Interactive with CLI.
"""

import sys
from .generator import generate_password
from .strength import assess_password
from . import utils
from .logging_config import setup_logging
import logging

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except Exception:
    CLIPBOARD_AVAILABLE = False


MENU = '''
=== PASSWORD GENERATOR ===
1) Generate one password
2) Generate multiple passwords
3) Try strength on a password
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
                # offer copy to clipboard
                if CLIPBOARD_AVAILABLE and utils.ask_yes_no("Copy password to clipboard?", default=True):
                    try:
                        pyperclip.copy(pwd) # type: ignore
                        print("Copied to clipboard.")
                    except Exception as e:
                        print(f"Could not copy: {e}")
                latest = [pwd]
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            n = utils.ask_int("Number of passwords to generate: ", min_value=1, default=5)
            length = utils.ask_int("Length of each password (default 16): ", min_value=1, default=16)
            try:
                use_upper, use_lower, use_digits, use_symbols = prompt_options()
                results = []
                for _ in range(n):
                    results.append(generate_password(length, use_upper, use_lower, use_digits, use_symbols))
                print("\nGenerated passwords:")
                for i, p in enumerate(results, 1):
                    print(f"{i}: {p}")
                latest = results
                if CLIPBOARD_AVAILABLE and utils.ask_yes_no("Copy the first password to clipboard?", default=False):
                    try:
                        pyperclip.copy(results[0]) # type: ignore
                        print("Copied first password to clipboard.")
                    except Exception as e:
                        print(f"Could not copy: {e}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            pwd = input("Paste or type the password to assess: ")
            if not pwd:
                print("No password provided.")
                continue
            report = assess_password(pwd)
            print(f"\nEntropy: {report['entropy_bits']} bits")
            print(f"Strength: {report['label']}")
            if report['recommendations']:
                print("Recommendations:")
                for r in report['recommendations']:
                    print(f" - {r}")

        elif choice == "4":
            if not latest:
                print("No recently generated passwords to save.")
                continue
            path = input("File to save to (default passwords.txt): ").strip() or "passwords.txt"
            append = utils.ask_yes_no("Append to file?", default=True)
            ok = utils.save_to_file(path, latest, append=append)
            if ok:
                print(f"Saved to {path}")

        elif choice == "5":
            print("Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice — choose a number between 1 and 5.")




if __name__ == "__main__":
    main()