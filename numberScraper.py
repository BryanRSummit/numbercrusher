import requests
import re
from requests.exceptions import Timeout

def extract_phone_numbers(url):
    try:
        # Fetch the HTML content of the webpage
        response = requests.get(url, timeout=1.5)
        html_content = response.text

        phone_regex1 = (r'(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1['
                        r'02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{'
                        r'2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?')

        # Use regular expression to find phone numbers
        phone_numbers = re.findall(phone_regex1, html_content)

        # Super pythonic way of getting rid of duplicates
        # Dicts only have unique keys then converting back to a list
        phone_numbers = list(dict.fromkeys(phone_numbers))
        phone_numbers = validAreaCodes(phone_numbers)

        return phone_numbers
    except Timeout:
        return None
    except Exception as e:
        # Handle any other exceptions that might occur
        print(f"An error occurred: {str(e)}")
        return None

def validAreaCodes(phone_numbers):
    valid_numbers = []
    for number in phone_numbers:
        if re.match(r'^[2-9][0-9][0-9]$', number[1]):
            valid_numbers.append(number)
    return valid_numbers