# misc groupme utilities

from urllib.parse import urlparse

def group_sharing_url_to_id(url: str) -> str:
    """
    Convert a GroupMe group sharing url to an ID.

    For example, given a URL https://groupme.com/join_group/91994372/901HvAj3, the
    returned ID should be 91994372.

    The return type is a string because of BigNum future concerns.
    """

    parsed = urlparse(url)
    splitted = parsed.path.split('/')
    group_id = splitted[2]

    return group_id