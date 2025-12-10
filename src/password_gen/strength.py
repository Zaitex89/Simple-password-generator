import math
import string

def charset_size(password):
    """Estimates size of characters used in pw
    This is a heuristic: checks if the password contains characters from given groups
    """
    size = 0
    if any(c.islower() for c in password):
        size += 26
    if any(c.isupper() for c in password):
        size += 26
    if any(c.isdigit() for c in password):
        size += 10
        
    symbols = set(string.punctuation)
    if any(c in symbols for c in password):
        size += 20
    return size

def entropy_bits(password):
    if not password:
        return 0.0
    size = charset_size(password)
    if size <= 0:
        return 0.0
    return len(password) * math.log2(size)

def strength_label(entropy):
    if entropy < 28:
        return "Weak"
    if entropy < 36:
        return "Fair"
    if entropy < 60:
        return "Strong"
    return "Very strong"

def assess_password(password):
    e = entropy_bits(password)
    label = strength_label(e)
    recs = []
    if len(password) < 8:
        recs.append("Make password longer (at least 8 characters).")
    if not any(c.islower() for c in password):
        recs.append("Include lowercase letters (a-z).")
    if not any(c.isupper() for c in password):
        recs.append("Include uppercase letters (A-Z).")
    if not any(c.isdigit() for c in password):
        recs.append("Include digits (0-9).")
    if not any(c in string.punctuation for c in password):
        recs.append("Include symbols (e.g. !@#).")



    return {"entropy_bits": round(e, 2), "label": label, "recommendations": recs}