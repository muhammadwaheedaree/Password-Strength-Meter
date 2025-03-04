import re
import streamlit as st
import string
import random
from typing import Tuple

def check_length(password: str) -> Tuple[bool, str]:
    """Check if password meets minimum length requirement."""
    is_valid = len(password) >= 8
    message = "✅ Length is good" if is_valid else "❌ Password should be at least 8 characters long"
    return is_valid, message

def check_case(password: str) -> Tuple[bool, str]:
    """Check if password contains both upper and lowercase letters."""
    is_valid = bool(re.search(r"[A-Z]", password) and re.search(r"[a-z]", password))
    message = "✅ Good mix of cases" if is_valid else "❌ Include both uppercase and lowercase letters"
    return is_valid, message

def check_digits(password: str) -> Tuple[bool, str]:
    """Check if password contains at least one digit."""
    is_valid = bool(re.search(r"\d", password))
    message = "✅ Contains numbers" if is_valid else "❌ Add at least one number (0-9)"
    return is_valid, message

def check_special_chars(password: str) -> Tuple[bool, str]:
    """Check if password contains special characters."""
    is_valid = bool(re.search(r"[!@#$%^&*]", password))
    message = "✅ Has special characters" if is_valid else "❌ Include at least one special character (!@#$%^&*)"
    return is_valid, message

def generate_strong_password() -> str:
    """Generate a strong password that meets all criteria."""
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*"
    
    # Ensure at least one character from each set
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special)
    ]
    
    # Add additional random characters
    all_chars = lowercase + uppercase + digits + special
    password.extend(random.choice(all_chars) for _ in range(8))
    
    # Shuffle the password
    random.shuffle(password)
    return ''.join(password)

def check_password_strength(password: str) -> int:
    """
    Check password strength and provide feedback.
    Returns score from 0-4.
    """
    checks = [
        check_length(password),
        check_case(password),
        check_digits(password),
        check_special_chars(password)
    ]
    
    # Calculate score and collect messages
    score = sum(passed for passed, _ in checks)
    messages = [message for _, message in checks]
    
    return score, messages

def main():
    st.set_page_config(page_title="Password Strength Meter", page_icon="🔒")
    
    st.title("🔒 Password Strength Meter")
    st.write("Check how strong your password is!")
    
    # Create two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Password input with toggle visibility
        password = st.text_input(
            "Enter your password",
            type="password",
            help="Your password should be at least 8 characters long and contain uppercase, lowercase, numbers, and special characters."
        )
    
    with col2:
        # Toggle password visibility
        show_password = st.toggle("Show password")
        if show_password and password:
            st.text(password)
    
    if password:
        score, messages = check_password_strength(password)
        
        # Display messages with appropriate styling
        for message in messages:
            if "✅" in message:
                st.success(message)
            elif "❌" in message:
                st.error(message)
        
        # Display strength meter
        st.write("\n**Password Strength:**")
        if score == 4:
            st.success("✅ Strong Password!")
            progress_color = "green"
        elif score == 3:
            st.warning("⚠️ Moderate Password - Consider adding more security features")
            progress_color = "yellow"
        else:
            st.error("❌ Weak Password - Please improve it using the suggestions above")
            progress_color = "red"
        
        # Progress bar
        st.progress(score/4, text=f"Strength: {score}/4")
        
        # Generate password button
        if score < 4:
            if st.button("Generate Strong Password"):
                strong_password = generate_strong_password()
                st.code(strong_password, language=None)
                st.info("👆 Copy this password and keep it safe!")

if __name__ == "__main__":
    main()
