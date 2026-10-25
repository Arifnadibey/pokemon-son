import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random
from datetime import datetime, timedelta
class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.last_feed_time = datetime.now()  # Pokémonun son beslenme zamanını başlatma
        self.hp = random.randint(200, 400)
        self.power = random.randint(30, 60)
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['forms'][0]['name']  #  Pokémon adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür

    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            self.name = await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
        return f"Pokémonunuzun ismi: {self.name} canı: {self.hp} gücü: {self.power}"

    async def attack(self,enemy):
        if isinstance(enemy,Wizard):
            chance = random.randint(1, 5)
            if chance==1:
                return"Büyücü bir kalkan kullandı!"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu şimdi {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"

    async def feed(self, feed_interval= 60, hp_increase=10 ):
        current_time = datetime.now() 
        delta_time = timedelta(seconds=feed_interval) 
        if (current_time - self.last_feed_time) > delta_time :
            self.hp += hp_increase
            self.last_feed_time = current_time 
            return f"Pokémon sağlığı geri yüklenir. Mevcut HP: {self.hp}"
        else:
            return f"Pokémonunuzu şu zaman besleyebilirsiniz:{self.last_feed_time + delta_time}"

    
    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data["sprites"]["front_default"]  #  Pokémon adını döndürme
                else:
                    return "Resim bulunamadı"  # İstek başarısız olursa varsayılan adı döndürür

class Fighter(Pokemon):
    async def feed(self):
        return await super().feed(hp_increase=20)
    async def attack(self, enemy):
        power = random.randint(5, 15)  
        self.power += power
        result = await super().attack(enemy)  
        self.power -= power
        return result + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {power}"
    


class Wizard(Pokemon):
    async def feed(self):
        return await super().feed(feed_interval=30)
    async def attack(self, enemy):
        power = 0
        for i in range(5):
            power += random.randint(1, 5) 
        self.power += power
        result = await super().attack(enemy)  
        self.power -= power
        return result + f"\nSihirbaz Pokémon süper saldırı kullandı. Eklenen güç: {power}"


