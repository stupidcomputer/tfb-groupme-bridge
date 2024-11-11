# misc groupme utilities

from urllib.parse import urlparse, urlencode
from flask import current_app

from typing import Optional

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

def build_oauth_auth_url(state: Optional[str] = None, user_params: Optional[dict] = {}):
    """
    Build the OAuth redirect url to GroupMe.
    state is optional -- it is usually in reference to the organization in question.
    If so, state should be set to the organization's `addition_url`. (see schema.sql for info)
    """
    base = current_app.config["REDIRECT_URL"]
    params = {}
    if state:
        params["state"] = state

    params = params | user_params
    urlencoded = urlencode(params)

    if urlencoded:
        base += "&"

    return base + urlencoded

def get_oauth_auth_url(state: None | str = None):
    return build_oauth_auth_url(
        state
    )

def custom_get_oauth_auth(params):
    return build_oauth_auth_url(
        None,
        params
    )
    