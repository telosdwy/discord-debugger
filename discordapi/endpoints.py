from . import *
# This Python isn't the best, but please deal with it for me.

class API_Exception(Exception):
    pass

def simpleRequest(method, url, headers, data = None):
    r = requests.request(
        method,
        url,
        headers = headers,
        data = data,
    )
    try:
        r.raise_for_status()
    except:
        raise API_Exception(r.text)
    try:
        return r.json()
    except:
        return r.text

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
    return simpleRequest('POST', '%s/oauth2/token' % API_ENDPOINT, headers, data)

class API:
    def __init__(self, user_token:str):
        self.user_token = user_token

    def identityUser(self, **kwargs:dict):
        headers = {
            'Authorization': 'Bearer %s' % self.user_token,
        }
        return simpleRequest('GET', '%s' % USERS_ENDPOINT, headers)

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
        return simpleRequest(
            'PUT',
            '%s/guilds/%s/members/%s' % (API_ENDPOINT, guild_id, user_id),
            headers,
            json.dumps(data),
        )

    def createGroupDM(self, **kwargs:dict):
        data = {
            'access_tokens': [self.user_token,],
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bot %s' % BOT_TOKEN,
        }
        return simpleRequest(
            'POST',
            '%s/channels' % USERS_ENDPOINT,
            headers,
            json.dumps(data),
        )

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
        return simpleRequest(
            'PUT',
            '%s/channels/%s/recipients/%s' % (API_ENDPOINT, channel_id, user_id),
            headers,
            json.dumps(data),
        )

    def removeGroupMember(self, **kwargs:dict):
        channel_id:int = kwargs['channel_id']
        user_id:int = kwargs['user_id']
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bot %s' % BOT_TOKEN,
        }
        return simpleRequest(
            'DELETE',
            '%s/channels/%s/recipients/%s' % (API_ENDPOINT, channel_id, user_id),
            headers,
        )

    def getConnections(self, **kwargs:dict):
        application_id:int = kwargs['application_id']
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % self.user_token,
        }
        return simpleRequest(
            'GET',
            '%s/applications/%s/role-connection' % (USERS_ENDPOINT, application_id),
            headers,
        )

class Route:
    def __init__(self, *,
        name:str = '',
        oauth:list = [],
        note:str = '',
        route:str = '',
        function = '',
        requires:list = []
    ):
        self.name = name
        self.oauth = oauth
        self.note = note
        self.route = route
        self.function = function
        self.requires = requires

routes = [
    Route(
        name = 'identity_user',
        oauth = [
            'identity',
        ],
        note = 'User token',
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
        note = 'User token, Bot token',
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
        note = 'User token(s), Bot token\n(can have more than one user/access_token, but this implementation only uses your access_token)',
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
        note = 'User token, Bot token',
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
        note = 'Bot token',
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
        note = 'User token',
        route = '/users/@me/applications/{application.id}/role-connection',
        function = API.getConnections,
        requires = [
            'application_id',
        ],
    ),
]
