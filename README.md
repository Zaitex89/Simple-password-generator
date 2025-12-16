# Password Generator

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

A secure, feature-rich command-line password generator with validation, strength analysis, and logging capabilities.

## Features

- **Secure Random Generation**: Uses Python's `secrets` module for cryptographically secure password generation
- **Customizable Passwords**: Configure length (1-50 characters) and character types
- **Password Analysis**: Comprehensive validation and entropy-based strength assessment
- **Pattern Detection**: Identifies common weak patterns like "password123" or "qwerty"
- **Clipboard Support**: Copy passwords directly to clipboard
- **File Export**: Save generated passwords to file
- **Detailed Logging**: All operations logged with configurable levels
- **Interactive CLI**: User-friendly command-line interface

## Project Structure

```
Simple-password-generator/
├── src/
│   ├── password_gen/           # Main package
│   │   ├── __init__.py
│   │   ├── main.py             # Entry point and CLI
│   │   ├── generator.py        # Password generation logic
│   │   ├── strength.py         # Entropy and strength assessment
│   │   ├── utils.py            # Utility functions
│   │   └── validators/         # Validation sub-package
│   │       ├── __init__.py
│   │       ├── password_validator.py    # Password strength validation
│   │       └── input_validator.py       # Secure input validation
│   └── logging_config/         # Logging package
│       ├── __init__.py
│       └── logger.py           # Custom logging configuration
├── logs/                       # Log files directory
├── .venv/                      # Virtual environment
├── .gitignore
├── pyproject.toml             # Project configuration
└── README.md
```

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Zaitex89/Simple-password-generator.git
cd Simple-password-generator
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install the Package

```bash
pip install -e .
```

This installs the package in "editable" mode, allowing you to make changes without reinstalling.

## Usage

### Running the Program

After installation, simply run:

```bash
passwordgen
```

### Menu Options

```
=== PASSWORD GENERATOR ===
1) Generate one password
2) Generate multiple passwords
3) Analyze existing password
4) Save password (latest generated)
5) Quit
```

### Example: Generate a Password

```
Pick a number: 1
Password length (default 16): 20
Include lowercase letters (a-z)? [Y/n]: y
Include uppercase letters (A-Z)? [Y/n]: y
Include digits (0-9)? [Y/n]: y
Include symbols (e.g. !@#)? [y/N]: y

Generated password: Xk9$mPq2#vL5rTnW4bGh

Password Analysis:
   Validation Score: 5/5
   Entropy: 118.63 bits
   Strength: Very strong

Copy password to clipboard? [Y/n]: y
Copied to clipboard.
```

### Example: Analyze a Password

```
Pick a number: 3
Paste or type the password to analyze: password123

============================================================
PASSWORD ANALYSIS
============================================================
Password: password123
Length: 13 characters

Overall Assessment:
   Validation Score: 2/5
   Entropy: 60.11 bits
   Strength Rating: Strong
   Status: INVALID
   Pattern Check:  Contains common patterns

Recommendations for Improvement:
   - Missing uppercase (A-Z)
   - Missing special chars
   - Include uppercase letters (A-Z).
   - Include symbols (e.g. !@#).

 WARNING: Password contains common patterns
   (e.g., '123', 'password', 'qwerty', 'abc123')
   Consider using a completely random password for better security.
============================================================
```

## Configuration

### Password Length

- **Minimum**: 1 character
- **Maximum**: 50 characters
- **Default**: 16 characters

### Character Sets

- **Lowercase**: a-z (26 characters)
- **Uppercase**: A-Z (26 characters)
- **Digits**: 0-9 (10 characters)
- **Symbols**: !@#$%&*()-_+=~[]{}<>? (20 characters)

### Logging

Logs are stored in `logs/password_gen.log` with the following levels:

- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages
- **ERROR**: Error messages
- **CRITICAL**: Critical issues

View logs:
```bash
cat logs/password_gen.log
tail -f logs/password_gen.log  # Follow in real-time
```

## Security Features

### Password Generation

- Uses `secrets` module for cryptographically secure random generation
- Ensures at least one character from each selected category
- Shuffles characters using `secrets.SystemRandom()`

### Input Validation

- Length limits (1-50 characters)
- Type checking and sanitization
- Prevention of common attacks:
  - Memory exhaustion
  - Path traversal (for file saves)
  - Invalid input injection

### Pattern Detection

Detects common weak patterns:
- Sequential numbers (123, 456)
- Common words (password, qwerty)
- Simple substitutions (abc123)

## Testing

Run the test suite:

```bash
# Test password generation
python -m password_gen.generator

# Test validation
python -c "from password_gen.validators import PasswordValidator; v = PasswordValidator(); print(v.validate_strength('Test123!'))"

# Test logging
python -c "from logging_config import setup_logging, get_logger; logger = setup_logging(); logger.info('Test')"
```

## Dependencies

- **pyperclip** (≥1.8.2): Clipboard functionality (optional)

All dependencies are automatically installed with `pip install -e .`

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**YZaitex89**
- GitHub: [@Zaitex89](https://github.com/Zaitex89)

## Acknowledgments

- Built as a Python learning project
- Uses industry-standard security practices
- Follows PEP 8 style guidelines

## Support

If you encounter any issues or have questions:

1. Check the logs in `logs/password_gen.log`
2. Open an issue on GitHub
3. Contact the maintainer

## Version History

- **0.1.0** (2025-12-04)
  - Initial release
  - Basic password generation
  - Validation and strength analysis
  - Logging functionality
  - CLI interface

---

**Made with Python**