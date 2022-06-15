import json, requests, os, aiohttp, asyncio, datetime, random
from flask import Flask, request, Response, jsonify
from threading import Thread
try:
  import nextcord
except ImportError:
  os.system("pip install -U nextcord")
import nextcord
from nextcord.ext import commands
from nextcord.ui.view import View
from nextcord.ui import Button, Select
from nextcord import Webhook

Token = os.environ.get("Token")
Ryou = commands.Bot(command_prefix = "/", status = nextcord.Status.idle, activity = nextcord.Activity(type = nextcord.ActivityType.watching, name = "Hentai"))
Ryou.remove_command("help")

@Ryou.slash_command(description = "Search up an anime.")
async def anime(ctx, name):
    class Data(object):
        pass
    Tracking = Data()
    Tracking.Page = 0
    Buttons = View(timeout = None)
    Back = Button(emoji = "<:Left:985729503378681876>", style = nextcord.ButtonStyle.blurple)
    Next = Button(emoji = "<:Right:985729495967350884>", style = nextcord.ButtonStyle.blurple)
    Buttons.add_item(Back)
    Buttons.add_item(Next)
    Anime = json.loads(requests.get(f"https://kitsu.io/api/edge/anime?filter[text]={name}").text)["data"]
    def GetAnime():
        Title = Anime[Tracking.Page]["attributes"]["canonicalTitle"]
        Description = Anime[Tracking.Page]["attributes"]["description"]
        Rating = str(Anime[Tracking.Page]["attributes"]["averageRating"]) + "/100"
        Popularity = "#" + str(Anime[Tracking.Page]["attributes"]["popularityRank"])
        Status = Anime[Tracking.Page]["attributes"]["status"].capitalize()
        Type = Anime[Tracking.Page]["attributes"]["showType"].capitalize()
        Start = Anime[Tracking.Page]["attributes"]["startDate"]
        End = Anime[Tracking.Page]["attributes"]["endDate"]
        AgeRating = Anime[Tracking.Page]["attributes"]["ageRatingGuide"]
        Image = Anime[Tracking.Page]["attributes"]["posterImage"]["original"]
        Frame = nextcord.Embed(title = Title, description = Description, color = 0x5865F2)
        Frame.add_field(name = "Status", value = f"**{Status}**", inline = False)
        Frame.add_field(name = "Rating", value = f"**{Rating}**")
        Frame.add_field(name = "Ranking", value = f"**{Popularity}**")
        Frame.add_field(name = "Age Rating", value = f"**{AgeRating}**", inline = False)
        Frame.add_field(name = "Started Airing", value = f"**{Start}**")
        Frame.add_field(name = "Ended", value = f"**{End}**")
        Frame.add_field(name = "Show Type", value = f"**{Type}**", inline = False)
        Frame.set_thumbnail(url = Image)
        Frame.timestamp = datetime.datetime.utcnow()
        return Frame
    try:
        Message = await ctx.response.send_message(embed = GetAnime(), view = Buttons, ephemeral = True)
    except:
        await ctx.response.send_message(embed = nextcord.Embed(description = "No anime found.", color = 0x5865F2), ephemeral = True)
    async def MoveBack(interaction):
        Tracking.Page -= 1
        if Tracking.Page < 0:
            Tracking.Page += 1
        else:
            await Message.edit(embed = GetAnime())
    async def MoveNext(interaction):
        Tracking.Page += 1
        if Tracking.Page > len(Anime):
            Tracking.Page -= 1
        else:
            await Message.edit(embed = GetAnime())
    Next.callback = MoveNext
    Back.callback = MoveBack

@Ryou.slash_command(description = "Roleplaying commands.")
async def rp(ctx, user: nextcord.Member):
    Buttons = View(timeout = None)
    Options = Select(placeholder = "Pick an action to roleplay.", max_values = 1, min_values = 1, options = [
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Bully"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Hug"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Kiss"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Lick"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Pat"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Bonk"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Yeet"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Highfive"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Bite"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Slap"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Kill"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Kick"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Poke"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Handhold")])
    Buttons.add_item(Options)
    Picking = nextcord.Embed(description = f"Pick an option.", color = 0x5865F2)
    Message = await ctx.response.send_message(embed = Picking, view = Buttons, ephemeral = True)
    def GetImage(Type):
        Image = json.loads(requests.get(f"https://api.waifu.pics/sfw/{Type.lower()}").text)["url"]
        Frame = nextcord.Embed(description = f"{ctx.user.mention} decides to {Type.lower()} {user.mention}", color = 0x5865F2)
        Frame.set_image(url = Image)
        Frame.set_footer(text = Type)
        Frame.timestamp = datetime.datetime.utcnow()
        return Frame
    def GetImage(Type):
        Image = json.loads(requests.get(f"https://api.waifu.pics/sfw/{Type.lower()}").text)["url"]
        Frame = nextcord.Embed(description = f"{ctx.user.mention} decides to {Type.lower()} {user.mention}", color = 0x5865F2)
        Frame.set_image(url = Image)
        Frame.set_footer(text = Type)
        Frame.timestamp = datetime.datetime.utcnow()
        return Frame
    async def Action(interaction):
        Type = Options.values[0]
        Options.disabled = True
        await Message.edit(embed = Picking, view = Buttons)
        await ctx.channel.send(embed = GetImage(Type), view = None)
    Options.callback = Action

@Ryou.slash_command(description = "Search up rule34 images.")
async def rule34(ctx, name):
    class Data(object):
        pass
    Tracking = Data()
    Buttons = View(timeout = None)
    Tracking.Type = name
    History = []
    Tracking.Current = 0
    Tracking.Pages = len(History)
    Preloaded = random.choice(json.loads(requests.get(f"https://api.rule34.xxx//index.php?page=dapi&s=post&q=index&json=1&limit=500&tags={Tracking.Type.replace(' ', '_')}", headers = {"Content-Type": "application/json"}).text))["file_url"]
    History.append(Preloaded)
    def GetImage(Type):
        Image = random.choice(json.loads(requests.get(f"https://api.rule34.xxx//index.php?page=dapi&s=post&q=index&json=1&limit=500&tags={Type.replace(' ', '_')}", headers = {"Content-Type": "application/json"}).text))["file_url"]
        History.append(Image)
        Tracking.Pages = len(History)
        Frame = nextcord.Embed(color = 0x5865F2)
        Frame.set_image(url = History[Tracking.Current])
        Frame.set_footer(text = Type)
        Frame.timestamp = datetime.datetime.utcnow()
        return Frame
    Back = Button(emoji = "<:Left:985729503378681876>", style = nextcord.ButtonStyle.blurple)
    Next = Button(emoji = "<:Right:985729495967350884>", style = nextcord.ButtonStyle.blurple)
    Buttons.add_item(Back)
    Buttons.add_item(Next)
    try:
        Message = await ctx.response.send_message(embed = GetImage(Tracking.Type), view = Buttons, ephemeral = True)
    except:
        await ctx.response.send_message(embed = nextcord.Embed(description = "No images found.", color = 0x5865F2), ephemeral = True)
    async def MoveNext(interaction):
        Tracking.Current += 1
        if Tracking.Current > Tracking.Pages:
            Tracking.Current -= 1
        else:
            await Message.edit(embed = GetImage(Tracking.Type))
    async def MoveBack(interaction):
        Tracking.Current -= 1
        if Tracking.Current < 0:
            Tracking.Current += 1
        else:
            await Message.edit(embed = GetImage(Tracking.Type))
    Next.callback = MoveNext
    Back.callback = MoveBack

@Ryou.slash_command(description = "Randomly generated porn.")
async def porn(ctx):
    class Data(object):
        pass
    Tracking = Data()
    Buttons = View(timeout = None)
    Tracking.Type = "4K"
    History = []
    Tracking.Current = 0
    Tracking.Pages = len(History)
    Preloaded = json.loads(requests.get(f"https://nekobot.xyz/api/image?type={Tracking.Type.lower()}", headers = {"Content-Type": "application/json", "Authorization": "015445535454455354D6"}).text)["message"]
    History.append(Preloaded)
    def GetImage(Type):
        Image = json.loads(requests.get(f"https://nekobot.xyz/api/image?type={Type.lower()}", headers = {"Content-Type": "application/json", "Authorization": "015445535454455354D6"}).text)["message"]
        History.append(Image)
        Tracking.Pages = len(History)
        Frame = nextcord.Embed(color = 0x5865F2)
        Frame.set_image(url = History[Tracking.Current])
        Frame.set_footer(text = Type)
        Frame.timestamp = datetime.datetime.utcnow()
        return Frame
    Options = Select(placeholder = "Choose an image category.", max_values = 1, min_values = 1, options = [
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "4K"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Anal"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Ass"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Pussy"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Thigh"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Boobs")])
    Back = Button(emoji = "<:Left:985729503378681876>", style = nextcord.ButtonStyle.blurple)
    Next = Button(emoji = "<:Right:985729495967350884>", style = nextcord.ButtonStyle.blurple)
    Buttons.add_item(Options)
    Buttons.add_item(Back)
    Buttons.add_item(Next)
    Message = await ctx.response.send_message(embed = GetImage(Tracking.Type), view = Buttons, ephemeral = True)
    async def ChangeCategory(interaction):
        History.clear()
        Tracking.Type = Options.values[0]
        Tracking.Current = 0
        await Message.edit(embed = GetImage(Tracking.Type))
    async def MoveNext(interaction):
        Tracking.Current += 1
        if Tracking.Current > Tracking.Pages:
            Tracking.Current -= 1
        else:
            await Message.edit(embed = GetImage(Tracking.Type))
    async def MoveBack(interaction):
        Tracking.Current -= 1
        if Tracking.Current < 0:
            Tracking.Current += 1
        else:
            await Message.edit(embed = GetImage(Tracking.Type))
    Next.callback = MoveNext
    Back.callback = MoveBack
    Options.callback = ChangeCategory

@Ryou.slash_command(description = "Randomly generated Hentai.")
async def hentai(ctx):
    class Data(object):
        pass
    Tracking = Data()
    Buttons = View(timeout = None)
    Tracking.Type = "Waifu"
    History = []
    Tracking.Current = 0
    Tracking.Pages = len(History)
    Preloaded = json.loads(requests.get(f"https://api.waifu.pics/nsfw/{Tracking.Type.lower()}").text)["url"]
    History.append(Preloaded)
    def GetImage(Type):
        try:
            Image = json.loads(requests.get(f"https://api.waifu.pics/nsfw/{Type.lower()}").text)["url"]
        except:
            try:
                Image = json.loads(requests.get(f"https://api.waifu.im/random/?selected_tags={Type.lower()}").text)["images"][0]["url"]
            except:
                Image = json.loads(requests.get(f"https://nekobot.xyz/api/image?type={Type.lower()}", headers = {"Content-Type": "application/json", "Authorization": "015445535454455354D6"}).text)["message"]
        History.append(Image)
        Tracking.Pages = len(History)
        Frame = nextcord.Embed(color = 0x5865F2)
        Frame.set_image(url = History[Tracking.Current])
        Frame.set_footer(text = Type)
        Frame.timestamp = datetime.datetime.utcnow()
        return Frame
    Options = Select(placeholder = "Choose an image category.", max_values = 1, min_values = 1, options = [
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Waifu"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Trap"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Blowjob"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Ass"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Paizuri"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Oral"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Neko"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Tentacle"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "hThigh"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "hAnal"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Milf")])
    Back = Button(emoji = "<:Left:985729503378681876>", style = nextcord.ButtonStyle.blurple)
    Next = Button(emoji = "<:Right:985729495967350884>", style = nextcord.ButtonStyle.blurple)
    Buttons.add_item(Options)
    Buttons.add_item(Back)
    Buttons.add_item(Next)
    Message = await ctx.response.send_message(embed = GetImage(Tracking.Type), view = Buttons, ephemeral = True)
    async def ChangeCategory(interaction):
        History.clear()
        Tracking.Type = Options.values[0]
        Tracking.Current = 0
        await Message.edit(embed = GetImage(Tracking.Type))
    async def MoveNext(interaction):
        Tracking.Current += 1
        if Tracking.Current > Tracking.Pages:
            Tracking.Current -= 1
        else:
            await Message.edit(embed = GetImage(Tracking.Type))
    async def MoveBack(interaction):
        Tracking.Current -= 1
        if Tracking.Current < 0:
            Tracking.Current += 1
        else:
            await Message.edit(embed = GetImage(Tracking.Type))
    Next.callback = MoveNext
    Back.callback = MoveBack
    Options.callback = ChangeCategory

@Ryou.slash_command(description = "Randomly generated Waifus.")
async def waifu(ctx):
    class Data(object):
        pass
    Tracking = Data()
    Buttons = View(timeout = None)
    Tracking.Type = "Waifu"
    History = []
    Tracking.Current = 0
    Tracking.Pages = len(History)
    Preloaded = json.loads(requests.get(f"https://api.waifu.pics/sfw/{Tracking.Type.lower()}").text)["url"]
    History.append(Preloaded)
    def GetImage(Type):
        try:
            Image = json.loads(requests.get(f"https://api.waifu.pics/sfw/{Type.lower()}").text)["url"]
        except:
            try:
                Image = json.loads(requests.get(f"https://api.waifu.im/random/?selected_tags={Type.lower()}").text)["images"][0]["url"]
            except:
                Image = json.loads(requests.get(f"https://nekobot.xyz/api/image?type={Type.lower()}", headers = {"Content-Type": "application/json", "Authorization": "015445535454455354D6"}).text)["message"]
        History.append(Image)
        Tracking.Pages = len(History)
        Frame = nextcord.Embed(color = 0x5865F2)
        Frame.set_image(url = History[Tracking.Current])
        Frame.set_footer(text = Type)
        Frame.timestamp = datetime.datetime.utcnow()
        return Frame
    Options = Select(placeholder = "Choose an image category.", max_values = 1, min_values = 1, options = [
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Waifu"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Shinobu"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Megumin"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Neko"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Uniform"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Maid"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Selfies"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Marin-Kitagawa"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Mori-Calliope"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Raiden-Shogun"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Oppai"),
    nextcord.SelectOption(emoji = "<:Dot:986203986803695687>", label = "Coffee")])
    Back = Button(emoji = "<:Left:985729503378681876>", style = nextcord.ButtonStyle.blurple)
    Next = Button(emoji = "<:Right:985729495967350884>", style = nextcord.ButtonStyle.blurple)
    Buttons.add_item(Options)
    Buttons.add_item(Back)
    Buttons.add_item(Next)
    Message = await ctx.response.send_message(embed = GetImage(Tracking.Type), view = Buttons, ephemeral = True)
    async def ChangeCategory(interaction):
        History.clear()
        Tracking.Type = Options.values[0]
        Tracking.Current = 0
        await Message.edit(embed = GetImage(Tracking.Type))
    async def MoveNext(interaction):
        Tracking.Current += 1
        if Tracking.Current > Tracking.Pages:
            Tracking.Current -= 1
        else:
            await Message.edit(embed = GetImage(Tracking.Type))
    async def MoveBack(interaction):
        Tracking.Current -= 1
        if Tracking.Current < 0:
            Tracking.Current += 1
        else:
            await Message.edit(embed = GetImage(Tracking.Type))
    Next.callback = MoveNext
    Back.callback = MoveBack
    Options.callback = ChangeCategory

@Ryou.slash_command(description = "Create an IP logger.")
async def create(ctx, name, webhook, redirect):
    Buttons = View(timeout = None)
    Website = Button(label = "Link", style = nextcord.ButtonStyle.url, url = f"https://ryou.bot.nu/gen?id={name.lower()}")
    Invite = Button(label = "Invite", style = nextcord.ButtonStyle.url, url = "https://discord.com/api/oauth2/authorize?client_id=981007469302136834&permissions=274877990912&scope=bot%20applications.commands")
    Buttons.add_item(Website)
    Frame = nextcord.Embed(title = "Success", description = f"Your IP logger has been successfully created.\n\n**• Name: {name}\n• Link: https://ryou.bot.nu/gen?id={name.lower()}**", color = 0x5865F2)
    Frame.add_field(name = "Redirect", value = f"```{redirect}```", inline = False)
    Frame.add_field(name = "Webhook", value = f"```{webhook}```", inline = False)
    with open("Webhooks.json", "r") as File:
        Webhooks = json.load(File)
    Webhooks[name.lower()] = {"webhook": webhook, "link": redirect}
    with open("Webhooks.json", "w") as File:
        json.dump(Webhooks, File)
    await ctx.response.send_message(embed = Frame, view = Buttons, ephemeral = True)




async def Sender(URL, Content):
    async with aiohttp.ClientSession() as Session:
        Hook = Webhook.from_url(URL, session = Session)
        await Hook.send(embed = Content, username = f"{Ryou.user.name} - Logger", avatar_url = Ryou.user.avatar)

Server = Flask("Ryou")

@Server.route("/gen")
def Log():
    try:
        IP = request.environ["HTTP_X_FORWARDED_FOR"]
        Info = json.loads(requests.get(f"https://tools.keycdn.com/geo.json?host={IP}", headers = {"User-Agent": "keycdn-tools:https://zec.69.mu"}).text)["data"]["geo"]
        Date, Time = Info["datetime"].split(" ")
        ID = request.args.get("id", None).lower()
        with open("Webhooks.json", "r") as File:
            Webhooks = json.load(File)
        WebhookID = Webhooks[ID]["webhook"]
        Link = Webhooks[ID]["link"]
        Redirect = Response()
        Redirect.headers["Refresh"] = f"0; url = {Link}"
        Frame = nextcord.Embed(title = "Ryou", color = 0x5865F2)
        Frame.add_field(name = "Country", value = f"```{Info['country_name']} ({Info['country_code']})```")
        Frame.add_field(name = "City", value = f"```{Info['city']}```")
        Frame.add_field(name = "IP Address", value = f"```{IP}```", inline = False)
        Frame.add_field(name = "Continent", value = f"```{Info['continent_name']} ({Info['continent_code']})```", inline = False)
        Frame.add_field(name = "Provider", value = f"```{Info['isp']}```")
        Frame.add_field(name = "System Number", value = f"```{Info['asn']}```")
        Frame.add_field(name = "Postal Code", value = f"```{Info['postal_code']}```")
        Frame.add_field(name = "Reverse DNS", value = f"```{Info['rdns']}```", inline = False)
        Frame.add_field(name = "Time Zone", value = f"```{Info['timezone']}```", inline = False)
        Frame.add_field(name = "Date", value = f"```{Date}```")
        Frame.add_field(name = "Time", value = f"```{Time}```")
        asyncio.run(Sender(WebhookID, Frame))
    except:
        pass
    return Redirect

@Server.errorhandler(404)
def page_not_found(e):
    Value = {"guilds": len(Ryou.guilds), "tag": str(Ryou.user), "id": Ryou.user.id, "invite": "dsc.gg/ryou", "support": "discord.gg/YyH2fjnfq3"}
    return jsonify(Value)

def Host():
    Server.run(host = "0.0.0.0", port = 8080)

def UpTime():
     Server = Thread(target = Host)
     Server.start()

UpTime()
Ryou.run(Token)
