"""
Password Generator - Python CLI

Instructions:
1. Save all files in the same folder: main.py, generator.py, strength.py, utils.py
2. pip install -r requirements.txt
3. Run: python main.py

Features:
- Generate secure passwords with selectable categories
- Generate multiple passwords at once
- Assess the strength of existing passwords (entropy + recommendations)
- Save generated passwords to file
- Copy to clipboard (if pyperclip is installed)

Error Handling:
- Invalid numbers are caught
- Length is checked against mandatory character categories
- File errors are caught when saving

Suggestions for Improvement:
- Add password policies (e.g. NIST or company rules)
- Support JSON/CSV export
- Integrate a secure keyring (OS-specific)
"""


