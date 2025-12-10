#Help functions for CLI
import sys

def ask_int(prompt, min_value=None, max_value=None, default=None):
    """Ask user for integer, handle wrong input."""
    while True:
        try:
            raw = input(prompt)
            if raw.strip() == "" and default is not None:
                return default
            value = int(raw)
            if min_value is not None and value < min_value:
                print(f"Value must be >= {min_value}")
                continue
            if max_value is not None and value > max_value:
                print(f"Value must be <= {max_value}")
                continue
            return value
        except ValueError:
            print("Invalid number - try again.")
        except (KeyboardInterrupt, EOFError):
            print("\nEnded by user.")
            sys.exit(1)

def ask_yes_no(prompt, default=True):
    """Ask yes/no. Returns True/False. Default if Enter."""
    default_str = "Y/n" if default else "y/N"
    while True:
        try:
            raw = input(f"{prompt} [{default_str}]: ")
            if raw.strip() == "":
                return default
            r = raw.strip().lower()
            if r in ("y", "yes", "ja", "j"):
                return True
            if r in ("n", "no", "nej"):
                return False
            print("answer 'y' or 'n'.")
        except (KeyboardInterrupt, EOFError):
            print("\nEnded by user.")
            sys.exit(1)




def save_to_file(path, passwords, append=True):
    """Save a list with password to file.
    """
    mode = "a" if append else "w"
    try:
        with open(path, mode, encoding="utf-8") as f:
            if isinstance(passwords, (list, tuple)):
                for p in passwords:
                    f.write(p + "\n")
            else:
                f.write(str(passwords) + "\n")
    except Exception as e:
        print(f"Kunde inte spara till fil: {e}")
        return False
    return True