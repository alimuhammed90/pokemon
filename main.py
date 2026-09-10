import discord
from discord.ext import commands
from config import token
from logic import Pokemon, Wizard, Fighter
import random
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı: {bot.user.name}')

@bot.command()
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        chance = random.randint(1, 3)
        if chance == 1:
            pokemon = Pokemon(author)
        elif chance == 2:
            pokemon = Wizard(author)
        elif chance == 3:
            pokemon = Fighter(author)
        await ctx.send(await pokemon.info())
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokemon görüntüsü yüklenemedi.")
    else:
        await ctx.send("Zaten bir Pokemon oluşturdunuz.")

@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None
    if target:
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]
            attacker = Pokemon.pokemons[ctx.author.name]
            result = await attacker.attack(enemy)
            await ctx.send(result)
        else:
            await ctx.send("Savaşmak için her iki katılımcının da Pokemon sahibi olması gerekir!")
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")

@bot.command()
async def info(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        await ctx.send(await pokemon.info())
    else:
        await ctx.send("Pokémon sahibi değilsiniz!")

async def feed(self, feed_interval= 20, hp_increase=10 ):
    current_time = datetime.now() 
    delta_time = timedelta(hours=feed_interval) 
    if (current_time - self.last_feed_time) > delta_time :
        self.hp += hp_increase
        self.last_feed_time = current_time 
        return f"Pokémon sağlığı geri yüklenir. Mevcut HP: {self.hp}"
    else:
        return f"Pokémonunuzu şu zaman besleyebilirsiniz:{current_time + delta_time }"

@bot.command()
async def feed(ctx):
    author=ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        response = await pokemon.feed()
        await ctx.send(response)
    else:
        await ctx.send("Böyle bir pokemon yok!")






bot.run(token)
