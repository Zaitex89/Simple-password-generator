import secrets 
import string

def build_charset(use_upper=True, use_lower=True, use_digits=True, use_symbols=True):
    charset = ""
    if use_lower:
        charset += string.ascii_lowercase
    if use_upper:
        charset += string.ascii_uppercase
    if use_digits:
        charset += string.digits
    if use_symbols:
        charset += "!@#$%&*()-_+=~[]{}<>?"
    return charset

def generate_password(lenght=16, use_upper=True, use_lower=True, use_digits=True, use_symbols=True):
    if lenght < 1:
        raise ValueError("Lenght must be atleast 1")
    charset = build_charset(use_upper, use_lower, use_digits, use_symbols)
    if not charset:
        raise ValueError("No category chosen")
    
    mandatory = []
    if use_lower:
        mandatory.append(secrets.choice(string.ascii_lowercase))
    if use_upper:
        mandatory.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        mandatory.append(secrets.choice(string.digits))
    if use_symbols:
        mandatory.append(secrets.choice("!@#$%&*()-_+=~[]{}<>?"))
    
    if lenght < len(mandatory):
        raise ValueError(f"The length {lenght} is to short for the chosen categories ({len(mandatory)}) necessary symbols")
    
    remaining = [secrets.choice(charset) for _ in range(lenght - len(mandatory))]

    password_list = mandatory + remaining
    secrets.SystemRandom().shuffle(password_list)
    return "".join(password_list)