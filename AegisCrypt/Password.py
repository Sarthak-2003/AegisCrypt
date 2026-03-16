def check_password_strength(pwd):
    score = 0
    if len(pwd) >= 8: 
        score += 1
    if any(c.islower() for c in pwd): 
        score += 1
    if any(c.isupper() for c in pwd): 
        score += 1
    if any(c.isdigit() for c in pwd): 
        score += 1
    if any(c in "!@#$%^&*()-_+=" for c in pwd): 
        score += 1
    if score <= 2:
        return "Weak", "red"
    elif score == 3:
        return "Medium", "orange"
    else:
        return "Strong", "green"
