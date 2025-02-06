import discord
from discord.ext import commands, tasks
import random
import time
import os
import asyncio
from datetime import datetime

# ---------------------------
# Configuração dos Intents e Criação do Bot (discord.py 2.0+)
# ---------------------------
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------------------
# Variáve is e Estruturas de Dados
# ---------------------------

# Lista de prêmios para o comando abrir_caixa
prizes = [
    {"name": "AK47", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144266105618573/ak47.png", "chance": 1},
    {"name": "VIP", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144289367228446/vip.png", "chance": 1},
    {"name": "GIROCOPITERO", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144105841393694/drop-aberto.png", "chance": 1},
    {"name": "MOTO", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144223407607869/moto.png", "chance": 1},
    {"name": "3.000 EMBERS", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144200271695962/ember.png", "chance": 2},
    {"name": "SEM SORTE", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144175944863784/fail.png", "chance": 91}
]

# Mensagens padrão
mensagens_sem_sorte = [
    "Os céus escureceram e os ventos anunciam uma maré de azar hoje...",
    "A sorte se escondeu entre as sombras. Tente novamente mais tarde!",
    "Parece que o apocalipse não favorece todos os guerreiros hoje."
]
mensagens_com_sorte = [
    "Hoje, as estrelas conspiram a seu favor!",
    "Você demonstrou coragem e a sorte respondeu positivamente!",
    "Os deuses do apocalipse sorriem para você!"
]
mensagens_apocalipticas = [
    "As nuvens negras se abrem para {user}!",
    "O destino sussurra: {user}, sua hora chegou!",
    "Em meio ao caos, {user} se destaca com brilho único!",
    "{user}, o universo reconhece sua bravura!"
]

# Dados dos jogos e contadores diários
last_attempt_time = {}    # Cooldown de 3 horas para abrir a caixa
player_prizes = {}        # Prêmios ganhos (exceto "SEM SORTE")
player_box_opens = {}     # Número de caixas abertas
player_embers = {}        # Saldo geral de embers (dos 3 jogos)

last_dado_time = {}       # Cooldown de 2 horas para rolar o dado
player_dado_wins = {}     # Vitórias no dado
player_dado_embers = {}   # Embers ganhos com o dado

last_roleta_time = {}     # Cooldown de 2 horas para usar !roleta
player_roleta_wins = {}   # Vitórias na roleta
player_roleta_tokens = {} # Tokens VIP ganhos na roleta

# Limites diários
daily_box_wins = {}       # Máximo de 2 prêmios na caixa por dia
daily_dado_wins = {}      # Máximo de 3 vitórias no dado por dia
daily_roleta_wins = {}    # Máximo de 3 vitórias na roleta por dia

# ID do Admin para notificação (altere conforme necessário)
ADMIN_ID = 470628393272999948

# Emojis para reações
reacoes = ["🔥", "⭐", "🎉", "💎", "👍"]

# ---------------------------
# Funções Auxiliares
# ---------------------------
def escolher_premio():
    total = sum(item['chance'] for item in prizes)
    rand = random.uniform(0, total)
    current = 0
    for item in prizes:
        current += item['chance']
        if rand <= current:
            return item

def tempo_restante(last_time, cooldown):
    return max(0, cooldown - (time.time() - last_time))

def formatar_tempo(segundos):
    h = int(segundos // 3600)
    m = int((segundos % 3600) // 60)
    s = int(segundos % 60)
    return f"{h}h {m}m {s}s"

# ---------------------------
# Comandos do Bot
# ---------------------------

# COMANDO: abrir_caixa
@bot.command()
async def abrir_caixa(ctx):
    canal_permitido = 1292879357446062162  # Canal permitido
    if ctx.channel.id != canal_permitido:
        await ctx.send(embed=discord.Embed(
            title="Canal Incorreto",
            description=f"{ctx.author.mention}, use o comando no canal: <#{canal_permitido}>",
            color=discord.Color.orange()
        ))
        return

    user = ctx.author
    if user.id in last_attempt_time:
        restante = tempo_restante(last_attempt_time[user.id], 10800)
        if restante > 0:
            embed_cd = discord.Embed(
                title="Caixa em Recarga",
                description=f"{user.mention}, aguarde {formatar_tempo(restante)} para abrir outra caixa.",
                color=discord.Color.dark_orange()
            )
            return await ctx.send(embed=embed_cd)

    prize = escolher_premio()
    if prize["name"] != "SEM SORTE" and daily_box_wins.get(user.id, 0) >= 2:
        prize = {"name": "SEM SORTE", "image": prizes[-1]["image"], "chance": 91}

    if prize["name"] == "SEM SORTE":
        mensagem = random.choice(mensagens_sem_sorte)
    else:
        mensagem = random.choice(mensagens_com_sorte)
        player_prizes[user.id] = player_prizes.get(user.id, []) + [prize["name"]]
        daily_box_wins[user.id] = daily_box_wins.get(user.id, 0) + 1
        mensagem_extra = random.choice(mensagens_apocalipticas).format(user=user.display_name)
        await ctx.send(embed=discord.Embed(
            title="Força do Apocalipse",
            description=mensagem_extra,
            color=discord.Color.purple()
        ))

    player_box_opens[user.id] = player_box_opens.get(user.id, 0) + 1
    last_attempt_time[user.id] = time.time()

    embed = discord.Embed(
        title="🎁 Caixa de Presentes Aberta!",
        description=f"{user.mention}, {mensagem}\nVocê ganhou: **{prize['name']}**",
        color=discord.Color.gold()
    )
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
    embed.set_image(url=prize['image'])
    embed.set_footer(text="Use os prêmios com sabedoria e continue lutando!")
    msg = await ctx.send(embed=embed)
    if prize["name"] != "SEM SORTE":
        await msg.add_reaction(random.choice(reacoes))

# COMANDO: rolardado com 2% de chance
@bot.command()
async def rolardado(ctx):
    user = ctx.author
    if user.id in last_dado_time:
        restante = tempo_restante(last_dado_time[user.id], 7200)
        if restante > 0:
            embed_cd = discord.Embed(
                title="Dado em Preparação",
                description=f"{user.mention}, aguarde {formatar_tempo(restante)} para rolar o dado novamente.",
                color=discord.Color.dark_blue()
            )
            return await ctx.send(embed=embed_cd)

    last_dado_time[user.id] = time.time()
    embed_rolando = discord.Embed(
        title="🎲 Rolando o Dado...",
        description="O dado está em movimento. Mantenha os olhos abertos!",
        color=discord.Color.blue()
    )
    embed_rolando.set_image(url="https://imgur.com/PEpiSuw.gif")
    mensagem_gif = await ctx.send(embed=embed_rolando)
    await asyncio.sleep(3)

    resultado = random.randint(1, 6)
    mensagem_resultado = f"{user.mention}, você rolou um **{resultado}**!\n"
    if random.random() < 0.02:
        embers_ganhos = 5000 if resultado < 6 else 6000
        mensagem_resultado += f"Parabéns! Você ganhou **{embers_ganhos} embers**!"
        daily_dado_wins[user.id] = daily_dado_wins.get(user.id, 0) + 1
        player_dado_wins[user.id] = player_dado_wins.get(user.id, 0) + 1
        player_dado_embers[user.id] = player_dado_embers.get(user.id, 0) + embers_ganhos
        player_embers[user.id] = player_embers.get(user.id, 0) + embers_ganhos
        await ctx.send(f"<@{ADMIN_ID}>, libere o prêmio para {user.mention}!")
    else:
        mensagem_resultado += "Que pena, a sorte não estava a seu favor desta vez."

    await mensagem_gif.delete()
    embed_resultado = discord.Embed(
        title="🎲 Resultado do Dado",
        description=mensagem_resultado,
        color=discord.Color.blue()
    )
    embed_resultado.set_footer(text="Continue tentando e a sorte poderá mudar!")
    await ctx.send(embed=embed_resultado)

# COMANDO: roleta com 2% de chance
@bot.command()
async def roleta(ctx):
    user = ctx.author
    if user.id in last_roleta_time:
        restante = tempo_restante(last_roleta_time[user.id], 7200)
        if restante > 0:
            embed_cd = discord.Embed(
                title="Roleta em Preparação",
                description=f"{user.mention}, aguarde {formatar_tempo(restante)} para jogar a roleta novamente.",
                color=discord.Color.dark_purple()
            )
            return await ctx.send(embed=embed_cd)

    last_roleta_time[user.id] = time.time()
    embed_rodando = discord.Embed(
        title="🔫 Girando a Roleta Russa...",
        description="A sorte está sendo decidida...",
        color=discord.Color.purple()
    )
    embed_rodando.set_image(url="https://imgur.com/5TEQXni.gif")
    msg_roleta = await ctx.send(embed=embed_rodando)
    await asyncio.sleep(3)

    if random.random() < 0.02:
        if daily_roleta_wins.get(user.id, 0) >= 3:
            mensagem_resultado = f"{user.mention}, você atingiu o limite diário de vitórias na roleta."
            embed_final = discord.Embed(
                title="🔫 Resultado da Roleta Russa",
                description=mensagem_resultado,
                color=discord.Color.red()
            )
            embed_final.set_image(url="https://imgur.com/IGfEwcg.gif")
        else:
            mensagem_resultado = f"{user.mention}, parabéns! Você sobreviveu e ganhou **2 Token VIP**!"
            embed_final = discord.Embed(
                title="🔫 Resultado da Roleta Russa",
                description=mensagem_resultado,
                color=discord.Color.green()
            )
            daily_roleta_wins[user.id] = daily_roleta_wins.get(user.id, 0) + 1
            player_roleta_wins[user.id] = player_roleta_wins.get(user.id, 0) + 1
            player_roleta_tokens[user.id] = player_roleta_tokens.get(user.id, 0) + 2
            player_embers[user.id] = player_embers.get(user.id, 0) + 2
            await ctx.send(f"<@{ADMIN_ID}>, libere o prêmio para {user.mention}!")
    else:
        mensagem_resultado = f"{user.mention}, a roleta parou e... você foi atingido!"
        embed_final = discord.Embed(
            title="🔫 Resultado da Roleta Russa",
            description=mensagem_resultado,
            color=discord.Color.red()
        )
        embed_final.set_image(url="https://imgur.com/IGfEwcg.gif")

    await msg_roleta.delete()
    embed_final.set_footer(text="Roleta Russa - Jogue com coragem!")
    await ctx.send(embed=embed_final)

# ---------------------------
# Exemplo de Comando Interativo para Ranking (Usando discord.ui)
# ---------------------------
class RankingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.current_page = 0
        self.rank_data = []  # Será carregado quando o comando for executado

    async def update_message(self, interaction: discord.Interaction):
        embed = discord.Embed(title="🏆 Ranking dos Melhores Prêmios da Caixa!", color=discord.Color.gold())
        start = self.current_page * 5
        end = start + 5
        for i, (user_id, prizes_list) in enumerate(self.rank_data[start:end], start=start+1):
            user = await bot.fetch_user(user_id)
            itens_raros = [p for p in prizes_list if p != "SEM SORTE"]
            embed.add_field(name=f"{i}. {user.display_name}",
                            value=f"{len(itens_raros)} prêmios raros: {', '.join(itens_raros)}",
                            inline=False)
        embed.set_footer(text=f"Página {self.current_page+1}/{(len(self.rank_data)-1)//5+1}")
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Anterior", style=discord.ButtonStyle.primary)
    async def previous(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_message(interaction)
        else:
            await interaction.response.send_message("Você já está na primeira página.", ephemeral=True)

    @discord.ui.button(label="Próximo", style=discord.ButtonStyle.primary)
    async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
        max_page = (len(self.rank_data)-1) // 5
        if self.current_page < max_page:
            self.current_page += 1
            await self.update_message(interaction)
        else:
            await interaction.response.send_message("Você já está na última página.", ephemeral=True)

@bot.command()
async def ranking(ctx):
    # Exemplo: Ranking dos melhores prêmios (use a mesma lógica do seu loop, mas de forma interativa)
    rank = sorted(player_prizes.items(), key=lambda x: sum(1 for prize in x[1] if prize != "SEM SORTE"), reverse=True)
    if not rank:
        await ctx.send("Nenhum prêmio registrado no momento.")
        return
    view = RankingView()
    view.rank_data = rank
    embed = discord.Embed(title="🏆 Ranking dos Melhores Prêmios da Caixa!", color=discord.Color.gold())
    for i, (user_id, prizes_list) in enumerate(rank[:5], start=1):
        user = await bot.fetch_user(user_id)
        itens_raros = [p for p in prizes_list if p != "SEM SORTE"]
        embed.add_field(name=f"{i}. {user.display_name}",
                        value=f"{len(itens_raros)} prêmios raros: {', '.join(itens_raros)}",
                        inline=False)
    embed.set_footer(text="Página 1")
    await ctx.send(embed=embed, view=view)

# ---------------------------
# Loops de Rankings e Reset Diário (mantidos como exemplo)
# ---------------------------
@tasks.loop(hours=6)
async def rank_melhores_presentes():
    channel = bot.get_channel(1304040902498713631)
    rank = sorted(player_prizes.items(), key=lambda x: sum(1 for prize in x[1] if prize != "SEM SORTE"), reverse=True)
    mensagem = "🏆 **Ranking dos Melhores Prêmios da Caixa!** 🏆\n\n"
    for i, (user_id, prizes_list) in enumerate(rank[:10], start=1):
        user = await bot.fetch_user(user_id)
        itens_raros = [p for p in prizes_list if p != "SEM SORTE"]
        mensagem += f"{i}. **{user.display_name}** - {len(itens_raros)} prêmios raros: {', '.join(itens_raros)}\n"
    await channel.send(mensagem)

@tasks.loop(hours=6.5)
async def rank_aberturas_caixa():
    channel = bot.get_channel(1304040902498713631)
    rank = sorted(player_box_opens.items(), key=lambda x: x[1], reverse=True)
    mensagem = "📦 **Ranking de Abertura de Caixas** 📦\n\n"
    for i, (user_id, opens) in enumerate(rank[:10], start=1):
        user = await bot.fetch_user(user_id)
        mensagem += f"{i}. **{user.display_name}** - {opens} caixas abertas\n"
    await channel.send(mensagem)

@tasks.loop(hours=7)
async def rank_dados():
    channel = bot.get_channel(1304040902498713631)
    rank = sorted(player_dado_embers.items(), key=lambda x: x[1], reverse=True)
    mensagem = "🎲 **Ranking de Prêmios dos Dados** 🎲\n\n"
    for i, (user_id, embers_total) in enumerate(rank[:10], start=1):
        user = await bot.fetch_user(user_id)
        wins = player_dado_wins.get(user_id, 0)
        mensagem += f"{i}. **{user.display_name}** - {wins} vitórias (Total: {embers_total} embers)\n"
    await channel.send(mensagem)

@tasks.loop(hours=8)
async def rank_roleta():
    channel = bot.get_channel(1304040902498713631)
    rank = sorted(player_roleta_tokens.items(), key=lambda x: x[1], reverse=True)
    mensagem = "🔫 **Ranking da Roleta Russa** 🔫\n\n"
    for i, (user_id, tokens) in enumerate(rank[:10], start=1):
        user = await bot.fetch_user(user_id)
        wins = player_roleta_wins.get(user_id, 0)
        mensagem += f"{i}. **{user.display_name}** - {wins} vitórias (Total: {tokens} Token VIP)\n"
    await channel.send(mensagem)

@tasks.loop(minutes=1)
async def reset_rankings():
    now = datetime.now()
    if now.hour == 0 and now.minute == 0:
        canal_reset = bot.get_channel(1292879357446062162)
        rank_melhores = sorted(player_prizes.items(), key=lambda x: sum(1 for prize in x[1] if prize != "SEM SORTE"), reverse=True)
        if rank_melhores:
            melhor_jogador, _ = rank_melhores[0]
            player_embers[melhor_jogador] = player_embers.get(melhor_jogador, 0) + 100
            user = await bot.fetch_user(melhor_jogador)
            mensagem_extra = random.choice(mensagens_apocalipticas).format(user=user.display_name)
            await canal_reset.send(f"{mensagem_extra}\nParabéns {user.mention}! Você recebeu **100 embers** por dominar o ranking de prêmios!")
        
        rank_aberturas = sorted(player_box_opens.items(), key=lambda x: x[1], reverse=True)
        if rank_aberturas:
            melhor_abertura, _ = rank_aberturas[0]
            player_embers[melhor_abertura] = player_embers.get(melhor_abertura, 0) + 100
            user = await bot.fetch_user(melhor_abertura)
            mensagem_extra = random.choice(mensagens_apocalipticas).format(user=user.display_name)
            await canal_reset.send(f"{mensagem_extra}\nParabéns {user.mention}! Você recebeu **100 embers** por ser o maior abridor de caixas!")
        
        # Reseta contadores diários
        player_prizes.clear()
        player_box_opens.clear()
        daily_box_wins.clear()
        daily_dado_wins.clear()
        daily_roleta_wins.clear()
        
        await canal_reset.purge(limit=None)
        await canal_reset.send("🧹 **O chat foi limpo para um novo começo apocalíptico!**")

@tasks.loop(minutes=5)
async def mudar_status():
    status_list = [
        "sobrevivendo ao apocalipse",
        "enfrentando hordas de zumbis",
        "explorando novos horizontes",
        "coletando suprimentos",
        "protegendo o refúgio"
    ]
    await bot.change_presence(activity=discord.Game(random.choice(status_list)))

# ---------------------------
# Evento on_ready: Inicializa os loops e notifica conexão
# ---------------------------
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    mudar_status.start()
    rank_melhores_presentes.start()
    rank_aberturas_caixa.start()
    rank_dados.start()
    rank_roleta.start()
    reset_rankings.start()

# ---------------------------
# Inicia o Bot
# ---------------------------
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("TOKEN não definido. Configure a variável de ambiente 'TOKEN'.")
bot.run(TOKEN)
