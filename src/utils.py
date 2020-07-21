import random, string

# Creates a random string of lower case ascii characters
# default is length 5
def new_slug(length=5):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

# Validates the slug. Only ascii characters allowed
def validate_slug(slug):
    try:
        slug.decode('ascii')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return False
    return True
