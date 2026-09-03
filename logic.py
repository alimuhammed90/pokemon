import aiohttp
import random


class Pokemon:

    # Bütün Pokémonları burada tutuyoruz
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer

        # Rastgele Pokémon numarası
        self.pokemon_number = random.randint(1, 1000)

        # Pokémon adı
        self.name = None

        # Seviye ve XP
        self.level = 1
        self.xp = 0

        # %10 ihtimalle nadir
        self.rare = random.random() < 0.10

        # Savaş özellikleri
        self.hp = random.randint(80, 120)
        self.max_hp = self.hp
        self.power = random.randint(10, 20)

        # Pokémon'u kaydet
        Pokemon.pokemons[pokemon_trainer] = self

    async def get_data(self):
        """PokeAPI'den Pokémon bilgilerini alır."""

        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:

                    if response.status == 200:
                        return await response.json()

        except Exception:
            pass

        return None

    async def get_name(self):
        """Pokémon'un adını getirir."""

        data = await self.get_data()

        if data:
            return data["forms"][0]["name"]

        return "pikachu"

    async def show_img(self):
        """Pokémon'un resmini getirir."""

        data = await self.get_data()

        if data:
            return data["sprites"]["front_default"]

        return None

    async def info(self):
        """Pokémon bilgilerini gösterir."""

        if self.name is None:
            self.name = await self.get_name()

        rare_text = "💎 Evet" if self.rare else "❌ Hayır"

        return (
            f"🐾 Pokémon: **{self.name}**\n"
            f"⭐ Seviye: **{self.level}**\n"
            f"✨ XP: **{self.xp}/{self.level * 100}**\n"
            f"❤️ HP: **{self.hp}/{self.max_hp}**\n"
            f"⚔️ Güç: **{self.power}**\n"
            f"💎 Nadir: **{rare_text}**"
        )

    def feed(self):
        """Pokémon'a XP verir."""

        # Normal Pokémon 20 XP
        xp_gain = 20

        # Nadir Pokémon 50 XP
        if self.rare:
            xp_gain = 50

        self.xp += xp_gain

        required_xp = self.level * 100

        message = (
            f"🍖 Pokémonunuzu beslediniz!\n"
            f"✨ **+{xp_gain} XP**\n"
        )

        # Level atlama
        if self.xp >= required_xp:

            self.xp -= required_xp
            self.level += 1

            # Level atlayınca biraz güçlensin
            self.max_hp += 10
            self.hp = self.max_hp
            self.power += 2

            message += (
                f"\n🎉 **Seviye atladınız!**\n"
                f"⭐ Yeni seviye: **{self.level}**\n"
                f"❤️ HP: **{self.max_hp}**\n"
                f"⚔️ Güç: **{self.power}**"
            )

        else:

            message += (
                f"⭐ Seviye: **{self.level}**\n"
                f"✨ XP: **{self.xp}/{required_xp}**"
            )

        return message

    async def attack(self, enemy):
        """Başka bir Pokémon'a saldırır."""

        damage = self.power

        # Düşmanın canı
        if enemy.hp > damage:

            enemy.hp -= damage

            return (
                f"⚔️ **Saldırı!**\n"
                f"🐾 @{self.pokemon_trainer} → @{enemy.pokemon_trainer}\n"
                f"💥 Verilen hasar: **{damage}**\n"
                f"❤️ Düşmanın kalan HP'si: **{enemy.hp}/{enemy.max_hp}**"
            )

        else:

            enemy.hp = 0

            return (
                f"⚔️ **Saldırı!**\n"
                f"🐾 @{self.pokemon_trainer}, "
                f"@{enemy.pokemon_trainer}'nin Pokémon'unu yendi! 🏆\n"
                f"💥 Hasar: **{damage}**"
            )
