from discord.ext import tasks
import discord, requests

TOKEN = "OTQyMzkwNDg2Mzk0NjE3OTE2.YgjziA.Y21QSw7agbTNxGw4EjhLcSiKXQo" #BOT ID
INTERVAL = 10 # interval (in seconds) of update
GUILD_IDS = [932424489986301992] #Discord Server ID

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        self.sol_price = 420.69
        self.xmr_price = 420.69
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        self.update_nickname.start()

    def update_price(self):
        try:
            self.xmr_price = round(float(requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol=XMRUSDT").json()["price"]), 2)
            self.btc_price = round(float(requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()["price"]), 2)
            print(self.xmr_price)
            print(self.btc_price)
        except Exception as e:
            print("Error while fetching price:", e)

    @tasks.loop(seconds=INTERVAL)
    async def update_nickname(self):
        try:
            self.update_price()
            for GUILD_ID in GUILD_IDS:
                await self.get_guild(GUILD_ID).me.edit(nick=f"XMR ${self.xmr_price}")
                await self.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = f"BTC ${self.btc_price}"))

        except Exception as e: print("Error:", e)

client = MyClient()
client.run(TOKEN)
