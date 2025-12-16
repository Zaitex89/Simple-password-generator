import secrets 
import string

MIN_PASSWORD_LENGTH = 1
MAX_PASSWORD_LENGTH = 50
DEFAULT_PASSWORD_LENGTH = 16

# Character sets
SYMBOLS = "!@#$%&*()-_+=~[]{}<>?"

def build_charset(use_upper=True, use_lower=True, use_digits=True, use_symbols=True):
    charset = ""
    if use_lower:
        charset += string.ascii_lowercase
    if use_upper:
        charset += string.ascii_uppercase
    if use_digits:
        charset += string.digits
    if use_symbols:
        charset += SYMBOLS
    return charset

def generate_password(
    length=DEFAULT_PASSWORD_LENGTH, 
    use_upper=True, 
    use_lower=True, 
    use_digits=True, 
    use_symbols=True
):
    
    """
    Generate a secure random password.
    
    Args:
        length: Password length (1-50 characters)
        use_upper: Include uppercase letters
        use_lower: Include lowercase letters
        use_digits: Include digits
        use_symbols: Include special symbols
        
    Returns:
        Generated password string
        
    Raises:
        ValueError: If length is invalid or no character types selected
    """
    # Validate length
    if not isinstance(length, int):
        raise ValueError("Length must be an integer")
    
    if length < MIN_PASSWORD_LENGTH:
        raise ValueError(f"Length must be at least {MIN_PASSWORD_LENGTH}")
    
    if length > MAX_PASSWORD_LENGTH:
        raise ValueError(f"Length cannot exceed {MAX_PASSWORD_LENGTH} characters")
    
    # Build character set
    charset = build_charset(use_upper, use_lower, use_digits, use_symbols)
    if not charset:
        raise ValueError("At least one character type must be selected")
    
    # Build mandatory characters (ensure at least one from each selected category)
    mandatory = []
    if use_lower:
        mandatory.append(secrets.choice(string.ascii_lowercase))
    if use_upper:
        mandatory.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        mandatory.append(secrets.choice(string.digits))
    if use_symbols:
        mandatory.append(secrets.choice(SYMBOLS))
    
    # Validate that length can accommodate mandatory characters
    if length < len(mandatory):
        raise ValueError(
            f"Length {length} is too short for the selected categories "
            f"({len(mandatory)} characters required minimum)"
        )
    
    # Generate remaining random characters
    remaining = [secrets.choice(charset) for _ in range(length - len(mandatory))]
    
    # Combine and shuffle
    password_list = mandatory + remaining
    secrets.SystemRandom().shuffle(password_list)
    
    return "".join(password_list)

def generate_multiple_passwords(
    count=5,
    length=DEFAULT_PASSWORD_LENGTH,
    use_upper=True,
    use_lower=True,
    use_digits=True,
    use_symbols=True
):
    """
    Generate multiple passwords at once.
    
    Args:
        count: Number of passwords to generate (1-100)
        length: Password length
        use_upper: Include uppercase letters
        use_lower: Include lowercase letters
        use_digits: Include digits
        use_symbols: Include special symbols
        
    Returns:
        List of generated passwords
        
    Raises:
        ValueError: If count is invalid
    """
    if not isinstance(count, int) or count < 1:
        raise ValueError("Count must be a positive integer")
    
    if count > 100:
        raise ValueError("Cannot generate more than 100 passwords at once")
    
    return [
        generate_password(length, use_upper, use_lower, use_digits, use_symbols)
        for _ in range(count)
    ]