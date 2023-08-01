from . import *
# This Python isn't the best, but please deal with it for me.

def fetchBearerToken(code:str):
    data = {
        'client_id': '%s' % CLIENT_ID,
        'client_secret': '%s' % CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': '%s' % HOST,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data = data, headers = headers)
    try:
        r.raise_for_status()
    except:
        raise Exception(r.text)
    return r.json()

class API:
    def __init__(self, user_token:str):
        self.user_token = user_token

    def identityUser(self, **kwargs:dict):
        headers = {
            'Authorization': 'Bearer %s' % self.user_token,
        }
        r = requests.get('%s' % USERS_ENDPOINT, headers = headers)
        try:
            r.raise_for_status()
        except:
            raise Exception(r.text)
        return r.json()

    def addGuildMember(self, **kwargs:dict):
        guild_id:int = kwargs['guild_id']
        user_id:int = kwargs['user_id']
        data = {
            'access_token': self.user_token,
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bot %s' % BOT_TOKEN,
        }
        r = requests.put('%s/guilds/%s/members/%s' % (API_ENDPOINT, guild_id, user_id), data = json.dumps(data), headers = headers)
        try:
            r.raise_for_status()
        except:
            raise Exception(r.text)
        return r.json()

    def createGroupDM(self, **kwargs:dict):
        data = {
            'access_tokens': [self.user_token,],
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bot %s' % BOT_TOKEN,
        }
        r = requests.post('%s/channels' % USERS_ENDPOINT, data = json.dumps(data), headers = headers)
        try:
            r.raise_for_status()
        except:
            raise Exception(r.text)
        return r.json()

    def addGroupMember(self, **kwargs:dict):
        channel_id:int = kwargs['channel_id']
        user_id:int = kwargs['user_id']
        data = {
            'access_token': self.user_token,
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bot %s' % BOT_TOKEN,
        }
        r = requests.put('%s/channels/%s/recipients/%s' % (API_ENDPOINT, channel_id, user_id), data = json.dumps(data), headers = headers)
        try:
            r.raise_for_status()
        except:
            raise Exception(r.text)
        return r.text

    def removeGroupMember(self, **kwargs:dict):
        channel_id:int = kwargs['channel_id']
        user_id:int = kwargs['user_id']
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bot %s' % BOT_TOKEN,
        }
        r = requests.delete('%s/channels/%s/recipients/%s' % (API_ENDPOINT, channel_id, user_id), headers = headers)
        try:
            r.raise_for_status()
        except:
            raise Exception(r.text)
        return r.text

    def getConnections(self, **kwargs:dict):
        application_id:int = kwargs['application_id']
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % self.user_token,
        }
        r = requests.get('%s/applications/%s/role-connection' % (USERS_ENDPOINT, application_id), headers = headers)
        try:
            r.raise_for_status()
        except:
            raise Exception(r.text)
        return r.text

class Route:
    def __init__(self, *, name:str = '', oauth:list = [], route:str = '', function = '', requires:list = []):
        self.name = name
        self.oauth = oauth
        self.route = route
        self.function = function
        self.requires = requires

routes = [
    Route(
        name = 'identity_user',
        oauth = [
            'identity',
        ],
        route = '/users/@me',
        function = API.identityUser,
        requires = [
        ],
    ),
    Route(
        name = 'join_guild',
        oauth = [
            'guilds.join',
        ],
        route = '/guilds/{guild.id}/members/{user.id}',
        function = API.addGuildMember,
        requires = [
            'guild_id',
            'user_id',
        ],
    ),
    Route(
        name = 'create_group_dm',
        oauth = [
            'gdm.join',
        ],
        route = '/users/@me/channels',
        function = API.createGroupDM,
        requires = [
        ],
    ),
    Route(
        name = 'join_group_dm',
        oauth = [
            'gdm.join',
        ],
        route = '/channels/{channel.id}/recipients/{user.id}',
        function = API.addGroupMember,
        requires = [
            'channel_id',
            'user_id',
        ],
    ),
    Route(
        name = 'remove_group_dm',
        oauth = [
            'gdm.join',
        ],
        route = '/channels/{channel.id}/recipients/{user.id}',
        function = API.removeGroupMember,
        requires = [
            'channel_id',
            'user_id',
        ],
    ),
    Route(
        name = 'get_connections',
        oauth = [
            'role_connections.write',
        ],
        route = '/users/@me/applications/{application.id}/role-connection',
        function = API.getConnections,
        requires = [
            'application_id',
        ],
    ),
]
