"""
SteamCommunity OpenID support

No extra configurations are needed to make this work.

## Based on native Yahoo OpenID backend ##

"""
import logging
logger = logging.getLogger(__name__)

from django.utils import simplejson
from social_auth.backends import OpenIDBackend, OpenIdAuth, setting, USERNAME
from urlparse import urlsplit
import urllib

STEAM_OPENID_URL = 'http://steamcommunity.com/openid'
STEAM_WEB_USER_API = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=' % setting('STEAM_WEB_API_KEY')

class SteamBackend(OpenIDBackend):
    """Steam OpenID authentication backend"""
    name = 'steam'

    def __init__(self, *args, **kwargs):
        super(SteamBackend, self).__init__(*args, **kwargs)
        self.steam_profile = None
        
    def get_user_id(self, details, response):
        """Return user unique id provided by service"""
        try:
            return urlsplit(response.identity_url).path.rsplit("/",1)[-1]
        except:
            return super(SteamBackend,self).get_user_id(self, details, response)
        
    def get_user_details(self, response):
        details = super(SteamBackend, self).get_user_details(response)
        try:
            profile = self.get_steam_profile(response)
            details[USERNAME] = profile["personaname"]
            details["fullname"] = profile["realname"]
        except Exception as e:
            pass
        return details
    
    def extra_data(self, user, uid, response, details):
        """Return default blank user extra data"""
        try:
            return self.get_steam_profile(response)
        except:
            return ""
    
    def get_steam_profile(self, response):
        if not self.steam_profile:
            url = STEAM_WEB_USER_API + self.get_user_id({}, response)
            self.steam_profile = simplejson.load(urllib.urlopen(url))["response"]["players"][0]
        return self.steam_profile
        
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