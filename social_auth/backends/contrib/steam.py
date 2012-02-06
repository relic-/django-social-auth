"""
SteamCommunity OpenID support

No extra configurations are needed to make this work.

## Based on native Yahoo OpenID backend ##

"""
import logging
logger = logging.getLogger(__name__)

from social_auth.backends import OpenIDBackend, OpenIdAuth


STEAM_OPENID_URL = 'http://steamcommunity.com/openid'


class SteamBackend(OpenIDBackend):
    """Steam OpenID authentication backend"""
    name = 'steam'


class SteamAuth(OpenIdAuth):
    """Steam OpenID authentication"""
    AUTH_BACKEND = SteamBackend

    def openid_url(self):
        """Return Steam OpenID service url"""
        return STEAM_OPENID_URL


# Backend definition
BACKENDS = {
    'steam': SteamAuth,
}