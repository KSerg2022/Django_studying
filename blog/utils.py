""""""
import re


def create_slug(title):
    """Create slug from title."""
    normalize_title = re.sub(r'[,.:;!?+\-*/=()@№%&\\]', '', title).lower().strip()
    slug = re.sub(r'\s', '-', normalize_title)
    return slug


# print(create_slug('Ttt T;T!t, t?t.\t/'))
