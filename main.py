import discord
from discord.ext import commands

import sqlite3

bot = commands.Bot(command_prefix=".", intents = discord.Intents.all())

con = sqlite3.connect('level.db')
cur = con.cursor()


@bot.event
async def on_ready():
    print("i'm alive")
    game = discord.Streaming(name="Solaris", url="https://www.twitch.tv/amatsumlv")
    await bot.change_presence(status=discord.Status.dnd, activity=game)
    channel = bot.get_channel(1038818345069318154)
    embed=discord.Embed(title=":blue_circle: Natsu is connected", color=discord.Color.blue())
    await channel.send(embed=embed)

@bot.event
async def on_message(message: discord.Message):
    channel = bot.get_channel(1038834843607371786)
    embed = discord.Embed(description=message.content, color=0xFDFDFD)
    embed.set_author(name=message.author.name+"#"+message.author.discriminator)
    if message.guild is None and not message.author.bot:
        await channel.send(embed=embed)
    await bot.process_commands(message)

#RANK SYSTEM
@bot.command()
async def init(ctx):
    cur.execute(f'''CREATE TABLE IF NOT EXISTS GUILD_{ctx.guild.id} (user_id int NOT NULL, exp int DEFAULT 0) ''')
    for x in ctx.guild.members:
        if x.bot != True:
            cur.execute(f"INSERT INTO GUILD_{ctx.guild.id} (user_id) VALUES ({x.id})")

        con.commit()
        embed=discord.Embed(title=":blue_circle: Initalisation du système de ranking terminée.", color=discord.Colour.green())
        await ctx.channel.send(embed=embed)

#LOGS CHANNELS DEFINED

##channel log
logchan = bot.get_channel(1038818345069318154)

@bot.command()
async def embedsay(ctx, *text):
    embed=discord.Embed(description=f"{text}".join(text), color=discord.Colour.blue())
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def say(ctx, *, texte):
    if texte=="pute":
        embed=discord.Embed(title=":red_circle: An error has occured while sending the request.", description=f"Error: {texte} contains a blacklisted word.", color=discord.Color.red())
        await ctx.send(embed=embed)
    if texte=="connard":
        embed=discord.Embed(title=":red_circle: An error has occured while sending the request.", description=f"Error: {texte} contains a blacklisted word.", color=discord.Color.red()) 
        await ctx.send(embed=embed)
    else:    
        await ctx.send(" ".join(texte))
        await ctx.message.delete()
        embed=discord.Embed(title="<:Community:1064157108037230642> `.say` command issued.")
        embed.add_field(name="Text sended:", value=f" ".join(texte))
        logchan = bot.get_channel(1038818345069318154)
        await logchan.send(embed=embed)

@bot.command()
async def hello(ctx):
    await ctx.send("hi")

@bot.command()
async def addrole(ctx, member : discord.Member, role : discord.Role):
    await member.add_roles(role)
    embed=discord.Embed(title=":green_circle: Modification des rôles effectuée", description="Cette commande est réservée au propriétaire du bot.", colour=discord.Color.red())
    await ctx.send(embed=embed)
    
@bot.command()
async def removeroles(ctx, member : discord.Member, role : discord.Role):
    await member.remove_roles(role)
    embed=discord.Embed(title=":red_circle: Impossible de modifier vos rôles", description="Cette commande est réservée au propriétaire du bot.", colour=discord.Color.red())
    await ctx.send(embed=embed)

@bot.command()
async def print(ctx, *, text):
    await ctx.send(f"{text}")
    embed = discord.Embed(description="*Note: L'équipe Solaris n'est pas responsable du contenu qui peut être print par des utilisateurs.*")
    await ctx.send(embed=embed)

@bot.command()
async def reg(ctx, arg = None):
    if arg == None:
        embed = discord.Embed(title="<:loader:1073971806567940146> Une erreur est survenue", description = "Argument manquant.", color=discord.Colour.red())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=":green_circle: Successfully registered", description=f"{arg} added to list.", color=discord.Colour.blurple())
        await ctx.send(embed=embed)

@bot.command()
async def assistance(ctx, arg = None):
    if arg == "fr":
        await ctx.send("Merci de bien vouloir ouvrir une demande dans le salon forum. Un modérateur / administrateur prendra votre demande en compte prochainement")
    if arg == "en":
        await ctx.send("Please open a support ticket in 'forum'. A mod/admin will answer later.")
    if arg == None:
        await ctx.send("Please specify a language. Ex: `.assistance fr (for French)` `.assistance en (for English)`")

@bot.command()
async def userinfo(ctx, member : discord.Member = None):
    member = ctx.author if not member else member
    # LIBS
    roles = [role for role in member.roles]
    embed = discord.Embed(color=member.color)
    embed.set_author(name=f"Informations sur l'utilisateur - {member}")
    #embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")
    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Guild name:", value=member.display_name, inline=False)
    embed.add_field(name="Account created at:", value=member.created_at.strftime("%a %#d %B %Y, %I %M %p UTC"), inline=True)
    embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a %#d %B %Y, %I %M %p UTC"), inline=False)
    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]), inline=True)
    embed.add_field(name="Top role:", value=member.top_role.mention, inline=False)
    embed.add_field(name="Is bot ?", value=member.bot, inline=True)
    await ctx.send(embed=embed)

@ bot.command()
async def dm(ctx, user: discord.User, *, message=None):
    message = message
    await user.send(message)
    channel=bot.get_channel(1038834823034314825)
    embed=discord.Embed(description=message, color=discord.Colour.red())
    embed.set_author(name=ctx.author.name+"#"+ctx.author.discriminator)
    await channel.send(embed=embed)

bot.run("TOKEN_HERE")
