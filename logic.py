import aiohttp
import random


class Pokemon:

    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.level = 1
        self.xp = 0
        self.rare = random.random() < 0.10
        self.hp = random.randint(80, 120)
        self.max_hp = self.hp
        self.power = random.randint(10, 20)

        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self

    async def get_data(self):
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
        data = await self.get_data()

        if data:
            return data["forms"][0]["name"]

        return "pikachu"

    async def show_img(self):
        data = await self.get_data()

        if data:
            return data["sprites"]["front_default"]

        return None

    async def info(self):
        if self.name is None:
            self.name = await self.get_name()

        if self.rare:
            return (
                f"Pokémonunuzun ismi: **{self.name}**\n"
                f"Seviye: **{self.level}**\n"
                f"Nadir Pokémon olduğu için beslenirken daha fazla XP kazanır!"
            )

        return (
            f"Pokémonunuzun ismi: **{self.name}**\n"
            f"Seviye: **{self.level}**"
        )

    def feed(self):
        xp_gain = 20

        if self.rare:
            xp_gain = 50

        self.xp += xp_gain

        message = (
            f"Pokémonunuzu beslediniz!\n"
            f"**{xp_gain} XP** kazandı!\n"
        )

        required_xp = self.level * 100

        if self.xp >= required_xp:
            self.xp -= required_xp
            self.level += 1

            message += (
                f"**Tebrikler! Pokémonunuz seviye atladı!**\n"
                f"Yeni seviye: **{self.level}**"
            )
        else:
            message += (
                f"Seviye: **{self.level}**\n"
                f"XP: **{self.xp}/{required_xp}**"
            )

        return message

    async def attack(self, enemy):
        damage = self.power

        if enemy.hp > damage:
            enemy.hp -= damage

            return (
                f"Pokémon eğitmeni @{self.pokemon_trainer} "
                f"@{enemy.pokemon_trainer}'ne saldırdı\n"
                f"Verilen hasar: **{damage}**\n"
                f"@{enemy.pokemon_trainer}'nin sağlık durumu: **{enemy.hp}**"
            )

        enemy.hp = 0

        return (
            f"Pokémon eğitmeni @{self.pokemon_trainer} "
            f"@{enemy.pokemon_trainer}'ni yendi!"
        )
