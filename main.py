
import discord
from discord.ext import commands

from config import token
from logic import Pokemon


intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Bot giriş yaptı: {bot.user}")
    print("Komutlar hazır!")


@bot.command()
async def go(ctx):

    author = str(ctx.author.id)

    if author in Pokemon.pokemons:
        await ctx.send(
            "Zaten bir Pokémon'un var!\n"
            "Bilgilerini görmek için `!pokemon` yaz."
        )
        return

    pokemon = Pokemon(author)

    info = await pokemon.info()

    await ctx.send(
        f"Pokémon'un oluşturuldu!\n\n"
        f"{info}"
    )

    image_url = await pokemon.show_img()

    if image_url:

        embed = discord.Embed(
            title=f"{pokemon.name}"
        )

        embed.set_image(url=image_url)

        await ctx.send(embed=embed)


@bot.command()
async def pokemon(ctx):

    author = str(ctx.author.id)

    if author not in Pokemon.pokemons:

        await ctx.send(
            "Henüz Pokémon'un yok!\n"
            "Önce `!go` yaz."
        )
        return

    pokemon = Pokemon.pokemons[author]

    info = await pokemon.info()

    await ctx.send(info)


@bot.command()
async def info(ctx):

    author = str(ctx.author.id)

    if author in Pokemon.pokemons:
        pok = Pokemon.pokemons[author]
        await ctx.send(await pok.info())
    else:
        await ctx.send(
            "Önce !go komutunu kullanarak bir Pokémon oluşturmalısın."
        )


@bot.command()
async def besle(ctx):

    author = str(ctx.author.id)

    if author not in Pokemon.pokemons:

        await ctx.send(
            "Önce `!go` komutuyla Pokémon oluşturmalısın."
        )
        return

    pokemon = Pokemon.pokemons[author]

    result = pokemon.feed()

    await ctx.send(result)


@bot.command()
async def attack(ctx, enemy: discord.Member):

    attacker_id = str(ctx.author.id)
    enemy_id = str(enemy.id)

    if attacker_id == enemy_id:

        await ctx.send(
            "Kendine saldıramazsın!"
        )
        return

    if attacker_id not in Pokemon.pokemons:

        await ctx.send(
            "Önce `!go` ile kendi Pokémon'unu oluştur."
        )
        return

    if enemy_id not in Pokemon.pokemons:

        await ctx.send(
            f"{enemy.mention} adlı kullanıcının Pokémon'u yok."
        )
        return

    attacker = Pokemon.pokemons[attacker_id]
    defender = Pokemon.pokemons[enemy_id]

    if attacker.hp <= 0:

        await ctx.send(
            "Pokémon'unun HP'si 0!\n"
            "Savaşamazsın."
        )
        return

    if defender.hp <= 0:

        await ctx.send(
            "Bu Pokémon'un HP'si zaten 0."
        )
        return

    result = await attacker.attack(defender)

    await ctx.send(result)


@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):

        await ctx.send(
            "Böyle bir komut yok.\n"
            "Kullanabileceğin komutlar:\n"
            "`!go`\n"
            "`!pokemon`\n"
            "`!info`\n"
            "`!besle`\n"
            "`!attack @kullanıcı`"
        )

    elif isinstance(error, commands.MissingRequiredArgument):

        await ctx.send(
            "Eksik bilgi.\n"
            "Örnek: `!attack @kullanıcı`"
        )

    elif isinstance(error, commands.MemberNotFound):

        await ctx.send(
            "Kullanıcı bulunamadı."
        )

    else:

        print(f"Hata: {error}")


bot.run(token)

