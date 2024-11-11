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

def build_oauth_auth_url(client_id: str, state: Optional[str] = None, user_params: Optional[dict] = {}):
    """
    Build the OAuth redirect url to GroupMe.
    state is optional -- it is usually in reference to the organization in question.
    If so, state should be set to the organization's `addition_url`. (see schema.sql for info)
    """
    base = "https://oauth.groupme.com/oauth/authorize?"
    params = {}
    params["client_id"] = client_id
    if state:
        params["state"] = state

    params = params | user_params

    print(base + urlencode(params))
    print(params)
    return base + urlencode(params)

def get_oauth_auth_url(state: None | str = None):
    return build_oauth_auth_url(
        current_app.config["CLIENT_ID"],
        state
    )

def custom_get_oauth_auth(params):
    return build_oauth_auth_url(
        current_app.config["CLIENT_ID"],
        None,
        params
    )
    