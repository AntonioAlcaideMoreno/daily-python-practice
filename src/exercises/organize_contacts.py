def valid_email(email):
    """
    Validates if a string is a properly formatted email address.

    Args:
        email (str): The email address to validate

    Returns:
        bool: True if email is valid, False otherwise

    Validation rules:
    - Must not contain spaces
    - Must contain exactly one @ symbol
    - Must contain exactly one dot (.)
    """
    if len(email.strip().split(" ")) > 1:
        return False
    elif len(email.split("@")) == 2 and len(email.split(".")) == 2:
        return True
    else:
        return False


def valid_phone(phone):
    """
    Validates if a string represents a valid phone number.

    Args:
        phone (str): The phone number to validate

    Returns:
        bool: True if phone number is exactly 10 digits, False otherwise
    """
    return len(phone) == 10


def clean_email(email):
    """
    Normalizes an email address by converting to lowercase and removing whitespace.

    Args:
        email (str): The email address to clean

    Returns:
        str: The normalized email address
    """
    return email.lower().strip()


def clean_phone(phone):
    """
    Extracts only the digits from a phone number string.

    Args:
        phone (str): The phone number to clean

    Returns:
        str: A string containing only the digits from the input
    """
    return "".join(filter(lambda n: n.isdigit(), phone))


def organize_contacts(contact_list):
    """
    Processes and filters a list of contacts by validating and
    deduplicating emails and phones.

    Args:
        contact_list (list): List of dictionaries containing contact information
                           with 'email' and 'phone' keys

    Returns:
        list: Filtered list of valid, unique contacts with normalized data

    Process:
    1. Cleans and validates each contact's email and phone
    2. Removes duplicates based on email or phone
    3. Updates contact information with cleaned data
    """
    seen_mails = set()
    seen_phones = set()
    valid_contact_list = []
    for contact in contact_list:
        email = contact["email"]
        phone = contact["phone"]
        cm = clean_email(email)
        cp = clean_phone(phone)
        if (
            valid_email(cm)
            and valid_phone(cp)
            and (cm not in seen_mails)
            and (cp not in seen_phones)
        ):
            seen_mails.add(cm)
            seen_phones.add(cp)
            contact["email"] = cm
            contact["phone"] = cp
            valid_contact_list.append(contact)
    return valid_contact_list


def main():
    # Example usage of the functions
    contacts = [
        {"email": "ajlaskj@jklsad.asdhl", "phone": "123-456-7890"},
        {"email": "invalid mail", "phone": "1234567890"},
        {"email": "  hh@laj.cj  ", "phone": "(098) 765-4321"},
    ]
    print(organize_contacts(contacts))
    return None


if __name__ == "__main__":
    main()
