import re

def check_password_strength(password):

    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Password should be at least 8 characters long")

    if re.search("[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add an uppercase letter")

    if re.search("[a-z]", password):
        score += 1
    else:
        suggestions.append("Add a lowercase letter")

    if re.search("[0-9]", password):
        score += 1
    else:
        suggestions.append("Add a number")

    if re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        suggestions.append("Add a special character")

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    print(f"\nPassword Strength: {strength}")

    if suggestions:
        print("\nSuggestions:")
        for s in suggestions:
            print("-", s)


password = input("Enter password: ")
check_password_strength(password)