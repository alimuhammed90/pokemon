import discord
from discord.ext import commands
from config import token
from logic import Pokemon

# Bot için yetkileri/intents ayarlama
intents = discord.Intents.default()  # Varsayılan ayarların alınması
intents.messages = True              # Botun mesajları işlemesine izin verme
intents.message_content = True       # Botun mesaj içeriğini okumasına izin verme
intents.guilds = True                # Botun sunucularla çalışmasına izin verme

# Tanımlanmış bir komut önekine ve etkinleştirilmiş amaçlara sahip bir bot oluşturma
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot çalışmaya hazır olduğunda tetiklenen bir olay
@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')  # Botun adını konsola çıktı olarak verir


# "Gamer" sınıfının tanımı
# Görev 2. nickname alanını ekleyin
# Görev 3. email alanını ekleyin
class Gamer:
    def __init__(self, name, age, nickname, email):
        self.name = name
        self.age = age

        self.nickname = nickname
        self.email = email





        self.games = []

    def add_game(self, game):
        self.games.append(game)

    # Görev 4: Mesajı değiştirin
    def introduce(self):
       print(f"Merhaba, benim adım {self.name}, ve ben {self.age} yaşındayım. Bana her zaman {self.email} adresinden e-posta göndererek ulaşabilirsiniz. Oyunda {self.nickname} takma adıyla beni arayın.")


# Oyuncu sınıfının bir örneğini oluşturma
gamer1 = Gamer("Emre", 14, "PrensEmre", "emre@gmail.com")

# Oyunları ekleme
gamer1.add_game("Minecraft")
gamer1.add_game("Dota 2")

# Bir oyuncunun mini sunumu
gamer1.introduce()

# Favori oyunların çıktısının alınması
print(f"{gamer1.name} şu oyunları seviyor: {', '.join(gamer1.games)}")

# '!go' komutu
@bot.command()
async def go(ctx):
    author = ctx.author.name  # Mesaj yazarının adını alma
    # Kullanıcının zaten bir Pokémon'u olup olmadığını kontrol edin. Eğer yoksa, o zaman...
    if author not in Pokemon.pokemons.keys():
        pokemon = Pokemon(author)  # Yeni bir Pokémon oluşturma
        await ctx.send(await pokemon.info())  # Pokémon hakkında bilgi gönderilmesi
        image_url = await pokemon.show_img()  # Pokémon resminin URL'sini alma
        if image_url:
            embed = discord.Embed()  # Gömülü mesajı oluşturma
            embed.set_image(url=image_url)  # Pokémon'un görüntüsünün ayarlanması
            await ctx.send(embed=embed)  # Görüntü içeren gömülü bir mesaj gönderme
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten kendi Pokémonunuzu oluşturdunuz!")  # Bir Pokémon'un daha önce oluşturulup oluşturulmadığını gösteren bir mesaj
# Botun çalıştırılması
bot.run(token)
