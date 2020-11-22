import json
from aiohttp import ClientSession
from asyncio import get_event_loop, AbstractEventLoop
from . import errors


class Client:
    """
    API wrapper for discordextremelist.xyz
    """

    def __init__(self, token: str = None, *, baseurl: str = "https://api.discordextremelist.xyz/v2/", loop: AbstractEventLoop=None):
        self.token = token
        self.baseurl = baseurl
        self.session = ClientSession(loop=loop if loop else get_event_loop())

    async def post_stats(self, botid: str, guildCount: int, shardCount: int = None):
        """
        :param botid: Bot to post server & shard count on
        :param guildCount: Server count
        :param shardCount: Shard count (optional)
        """

        headers = {"Authorization": self.token, "Content-Type": 'application/json'}
        if not self.token:
            raise errors.NoToken("The token is missing.")

        data = json.dumps({'guildCount': guildCount, 'shardCount': shardCount})
        if not shardCount:
            data = json.dumps({'guildCount': guildCount})

        async with self.session as session:
            async with session.post(self.baseurl+"bot/{0}/stats".format(botid), headers=headers, data=data) as r:
                result = await r.json()

                if result['error']:
                    raise errors.InvalidStats(f"Failed to post stats! Result:\n{result}")
    
    async def get_website_stats(self):
        """
        Get website statistics
        
        :return WebsiteStats: Website statistics
        """

        r = await self.session.get(self.baseurl+"/stats")
        data = json.loads(await r.text())
        return data
    
    async def get_website_health(self):
        """
        Get website health
        
        :return WebsiteHealth: Website health
        """

        r = await self.session.get(self.baseurl+"/health")
        data = json.loads(await r.text())
        return data

    async def get_bot_info(self, botid: str):
        """
        Get a bot listed on discordextremelist.xyz

        :param botid: Bot to be fetched
        :return Bot: Bot that was fetched
        """

        r = await self.session.get(self.baseurl+"bot/{0}".format(botid))
        data = json.loads(await r.text())
        return data
    
    async def get_server_info(self, serverid: str):
        """
        Get a server listed on discordextremelist.xyz

        :param serverid: Server to be fetched
        :return Server: Server that was fetched
        """

        r = await self.session.get(self.baseurl+"server/{0}".format(serverid))
        data = json.loads(await r.text())
        return data
    
    async def get_template_info(self, templateid: str):
        """
        Get a template listed on discordextremelist.xyz

        :param templateid: Template to be fetched
        :return Template: Template that was fetched
        """

        r = await self.session.get(self.baseurl+"template/{0}".format(templateid))
        data = json.loads(await r.text())
        return data
    
    async def get_user_info(self, userid: str):
        """
        Get a registered user on discordextremelist.xyz

        :param userid: User to be fetched
        :return User: User that was fetched
        """

        r = await self.session.get(self.baseurl+"user/{0}".format(userid))
        data = json.loads(await r.text())
        return data