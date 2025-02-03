import discord
from discord.ext import commands, tasks
import random
import time
import os
import asyncio
from datetime import datetime, timedelta

# ---------------------------
# Configuração dos Intents e Criação do Bot
# ---------------------------
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------------------
# Variáveis e Estruturas de Dados
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

# Mensagens para o comando abrir_caixa
mensagens_sem_sorte = [
    "Os céus escureceram e os ventos trazem más notícias... hoje não é seu dia de sorte!",
    "As hordas estão crescendo e a sorte está se esvaindo... tente novamente mais tarde!",
    "Você caminhou em vão, o apocalipse não perdoa... talvez a próxima vez seja melhor."
]
mensagens_com_sorte = [
    "O apocalipse pode ser sombrio, mas hoje você brilhou!",
    "Sua sorte virou as costas para os zumbis, parabéns pelo prêmio!",
    "O destino sorriu para você hoje... aproveite seu prêmio!"
]
mensagens_apocalipticas = [
    "As nuvens negras se abrem, e o poder está ao seu alcance, {user}!",
    "Os espíritos do apocalipse sussurram seu nome... você foi escolhido, {user}!",
    "Hoje, os mortos levantaram-se para saudar {user}. A sorte está ao seu lado!",
    "Nas trevas do apocalipse, um brilho de esperança aparece para {user}.",
    "Você venceu o apocalipse e emergiu como um verdadeiro guerreiro, {user}!",
    "{user}, a devastação não é párea para sua sorte. Domine a vitória!",
    "Os ventos da destruição carregam seu nome, {user}. Hoje, você é imbatível!",
    "A terra treme sob seus pés, {user}, enquanto o apocalipse se curva diante de sua vitória!",
    "{user}, você foi agraciado pelas forças do além. Este é o seu dia de sorte!",
    "Com os olhos da noite sobre você, {user}, a fortuna finalmente lhe sorriu!"
]

# Dados para o jogo da Caixa
last_attempt_time = {}  # Cooldown de 3 horas (10800 seg) para abrir a caixa
player_prizes = {}      # Prêmios ganhos (exceto "SEM SORTE")
player_box_opens = {}   # Número de caixas abertas
# Saldo geral de embers (dos 3 jogos)
player_embers = {}

# Dados para o jogo dos Dados
last_dado_time = {}     # Cooldown de 2 horas (7200 seg) para rolar o dado
player_dado_wins = {}   # Número de vitórias (quando rola 5 ou 6)
player_dado_embers = {} # Embers ganhos somente com o dado

# Dados para o jogo da Roleta Russa
last_roleta_time = {}    # Cooldown (2 horas, 7200 seg) para usar !roleta
player_roleta_wins = {}  # Número de vitórias (sobreviveu e ganhou prêmio)
player_roleta_tokens = {}# Tokens VIP ganhos via roleta

# ID do Admin para notificação (altere se necessário)
ADMIN_ID = 470628393272999948

# Emojis para reações (usados no abrir_caixa)
reacoes = [
    "🔥", 
    "<:emoji_1:1262824010723365030>", 
    "<:emoji_2:1261377496893489242>", 
    "<:emoji_3:1261374830088032378>", 
    "<:emoji_4:1260945241918279751>"
]

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

# ---------------------------
# COMANDO: abrir_caixa
# ---------------------------
@bot.command()
async def abrir_caixa(ctx):
    canal_permitido = 1292879357446062162  # ID do canal permitido
    if ctx.channel.id != canal_permitido:
        await ctx.send(f"{ctx.author.mention}, você só pode usar este comando neste canal: <#{canal_permitido}>")
        return

    user = ctx.author

    # Cooldown de 3 horas (10800 seg)
    if user.id in last_attempt_time:
        restante = tempo_restante(last_attempt_time[user.id], 10800)
        if restante > 0:
            horas = int(restante // 3600)
            minutos = int((restante % 3600) // 60)
            segundos = int(restante % 60)
            await ctx.send(f"{user.mention}, aguarde {horas}h {minutos}m {segundos}s para abrir outra caixa.")
            return

    prize = escolher_premio()

    if prize["name"] == "SEM SORTE":
        mensagem = random.choice(mensagens_sem_sorte)
    else:
        mensagem = random.choice(mensagens_com_sorte)
        player_prizes[user.id] = player_prizes.get(user.id, []) + [prize["name"]]
        mensagem_apocaliptica = random.choice(mensagens_apocalipticas).format(user=user.display_name)
        await ctx.send(mensagem_apocaliptica)

    player_box_opens[user.id] = player_box_opens.get(user.id, 0) + 1

    embed = discord.Embed(
        title="🎁 Você abriu a Caixa de Presentes!",
        description=(f"{user.mention}, {mensagem} Você ganhou: **{prize['name']}**!"
                     if prize["name"] != "SEM SORTE" else f"{user.mention}, {mensagem}"),
        color=discord.Color.gold()
    )
    embed.set_image(url=prize['image'])

    msg = await ctx.send(embed=embed)
    if prize["name"] != "SEM SORTE":
        await msg.add_reaction(random.choice(reacoes))

    last_attempt_time[user.id] = time.time()

# ---------------------------
# COMANDO: rolardado
# ---------------------------
@bot.command()
async def rolardado(ctx):
    """Jogo de dado: se o resultado for 5 ou 6, ganha embers.
       Cooldown: 2 horas."""
    user = ctx.author

    if user.id in last_dado_time:
        restante = tempo_restante(last_dado_time[user.id], 7200)
        if restante > 0:
            horas = int(restante // 3600)
            minutos = int((restante % 3600) // 60)
            segundos = int(restante % 60)
            await ctx.send(f"{user.mention}, aguarde {horas}h {minutos}m {segundos}s para rolar o dado novamente.")
            return

    last_dado_time[user.id] = time.time()

    gif_url = "https://imgur.com/PEpiSuw.gif"  # GIF de rolagem do dado (altere se desejar)
    embed_rolando = discord.Embed(
        title="🎲 Rolando o Dado...",
        description="Aguarde enquanto o dado é lançado.",
        color=discord.Color.blue()
    )
    embed_rolando.set_image(url=gif_url)
    mensagem_gif = await ctx.send(embed=embed_rolando)

    await asyncio.sleep(3)

    resultado = random.randint(1, 6)
    mensagem_resultado = f"{user.mention} rolou o dado e saiu **{resultado}**!\n"

    embers_ganhos = 0
    if resultado == 5:
        embers_ganhos = 5000
        mensagem_resultado += "Parabéns! Você ganhou **5000 embers**!"
    elif resultado == 6:
        embers_ganhos = 6000
        mensagem_resultado += "Parabéns! Você ganhou **6000 embers**!"
    else:
        mensagem_resultado += "Que pena, dessa vez a sorte não colaborou."

    if embers_ganhos > 0:
        player_embers[user.id] = player_embers.get(user.id, 0) + embers_ganhos
        player_dado_wins[user.id] = player_dado_wins.get(user.id, 0) + 1
        player_dado_embers[user.id] = player_dado_embers.get(user.id, 0) + embers_ganhos
        await ctx.send(f"<@{ADMIN_ID}>, por favor, libere o prêmio para {user.mention}!")

    await mensagem_gif.delete()

    embed_resultado = discord.Embed(
        title="🎲 Resultado do Dado",
        description=mensagem_resultado,
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed_resultado)

# ---------------------------
# COMANDO: roleta (Roleta Russa)
# ---------------------------
@bot.command()
async def roleta(ctx):
    """Jogo de roleta russa:
    - O usuário aciona a roleta com animação.
    - Chance baixa de levar "tiro" (resultado ruim).
    - Se não levar tiro, ganha **2 Token VIP**.
    - Notifica o admin em caso de prêmio.
    Cooldown: 2 horas."""
    user = ctx.author

    # Cooldown de 2 horas para o jogo da roleta
    if user.id in last_roleta_time:
        restante = tempo_restante(last_roleta_time[user.id], 7200)
        if restante > 0:
            horas = int(restante // 3600)
            minutos = int((restante % 3600) // 60)
            segundos = int(restante % 60)
            await ctx.send(f"{user.mention}, aguarde {horas}h {minutos}m {segundos}s para jogar a roleta novamente.")
            return

    last_roleta_time[user.id] = time.time()

    # Envia embed com GIF de roleta girando
    gif_roleta = "https://imgur.com/5TEQXni.gif"  # Exemplo de GIF para roleta (altere se desejar)
    embed_rodando = discord.Embed(
        title="🔫 Jogando a Roleta Russa...",
        description="A roleta está girando. Aguarde o resultado.",
        color=discord.Color.purple()
    )
    embed_rodando.set_image(url=gif_roleta)
    msg_roleta = await ctx.send(embed=embed_rodando)

    await asyncio.sleep(3)

    # Define a chance: 10% de levar tiro; 90% de ganhar 2 Token VIP.
    if random.random() < 0.10:
        # Resultado: levou tiro
        resultado = "tiro"
        mensagem_resultado = f"{user.mention}, a roleta parou! Infelizmente, você foi atingido!"
        # GIF para tiro (exemplo)
        gif_tiro = "https://imgur.com/IGfEwcg.gif"
        embed_final = discord.Embed(
            title="🔫 Resultado da Roleta Russa",
            description=mensagem_resultado,
            color=discord.Color.red()
        )
        embed_final.set_image(url=gif_tiro)
        # Não há prêmio; o usuário "levou tiro"
    else:
        # Resultado: não levou tiro, ganha 2 Token VIP
        resultado = "sobreviveu"
        premio = "2 Token VIP"
        mensagem_resultado = f"{user.mention}, parabéns! Você sobreviveu e ganhou **{premio}**!"
        embed_final = discord.Embed(
            title="🔫 Resultado da Roleta Russa",
            description=mensagem_resultado,
            color=discord.Color.green()
        )
        # Notifica o admin para liberar o prêmio
        await ctx.send(f"<@{ADMIN_ID}>, por favor, libere o prêmio para {user.mention}!")
        # Atualiza os dados do jogo da roleta
        player_roleta_wins[user.id] = player_roleta_wins.get(user.id, 0) + 1
        player_roleta_tokens[user.id] = player_roleta_tokens.get(user.id, 0) + 2
        # Atualiza também o saldo geral de embers (se os tokens VIP forem contabilizados como embers)
        player_embers[user.id] = player_embers.get(user.id, 0) + 2

    await msg_roleta.delete()

    embed_final.set_footer(text="Jogo de Roleta Russa")
    await ctx.send(embed=embed_final)

# ---------------------------
# LOOP: Ranking dos Melhores Prêmios da Caixa (a cada 6 horas)
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

# ---------------------------
# LOOP: Ranking de Aberturas de Caixas (a cada 6.5 horas)
# ---------------------------
@tasks.loop(hours=6.5)
async def rank_aberturas_caixa():
    channel = bot.get_channel(1304040902498713631)
    rank = sorted(player_box_opens.items(), key=lambda x: x[1], reverse=True)
    mensagem = "📦 **Ranking de Abertura de Caixas** 📦\n\n"
    for i, (user_id, opens) in enumerate(rank[:10], start=1):
        user = await bot.fetch_user(user_id)
        mensagem += f"{i}. **{user.display_name}** - {opens} caixas abertas\n"
    await channel.send(mensagem)

# ---------------------------
# LOOP: Ranking dos Prêmios dos Dados (a cada 7 horas)
# ---------------------------
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

# ---------------------------
# LOOP: Ranking da Roleta Russa (a cada 8 horas)
# ---------------------------
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

# ---------------------------
# LOOP: Resetar Rankings, Premiações e Limpar o Chat às 00:00 (verificado a cada minuto)
# ---------------------------
@tasks.loop(minutes=1)
async def reset_rankings():
    now = datetime.now()
    if now.hour == 0 and now.minute == 0:
        channel = bot.get_channel(1292879357446062162)
        
        rank_melhores = sorted(player_prizes.items(), key=lambda x: sum(1 for prize in x[1] if prize != "SEM SORTE"), reverse=True)
        if rank_melhores:
            melhor_jogador, _ = rank_melhores[0]
            player_embers[melhor_jogador] = player_embers.get(melhor_jogador, 0) + 100
            user = await bot.fetch_user(melhor_jogador)
            mensagem_apocaliptica = random.choice(mensagens_apocalipticas).format(user=user.display_name)
            await channel.send(f"{mensagem_apocaliptica}\nParabéns {user.mention}! Você recebeu **100 embers** por ser o melhor do ranking de prêmios!")
        
        rank_aberturas = sorted(player_box_opens.items(), key=lambda x: x[1], reverse=True)
        if rank_aberturas:
            melhor_abertura, _ = rank_aberturas[0]
            player_embers[melhor_abertura] = player_embers.get(melhor_abertura, 0) + 100
            user = await bot.fetch_user(melhor_abertura)
            mensagem_apocaliptica = random.choice(mensagens_apocalipticas).format(user=user.display_name)
            await channel.send(f"{mensagem_apocaliptica}\nParabéns {user.mention}! Você recebeu **100 embers** por ser o melhor do ranking de aberturas de caixas!")
        
        player_prizes.clear()
        player_box_opens.clear()
        print("Rankings da Caixa resetados!")
        
        await channel.purge(limit=None)
        await channel.send("🧹 O chat foi limpo para um novo começo apocalíptico!")

# ---------------------------
# LOOP: Mudar o Status do Bot Periodicamente (a cada 5 minutos)
# ---------------------------
@tasks.loop(minutes=5)
async def mudar_status():
    status_list = [
        "sobrevivendo ao apocalipse",
        "enfrentando hordas de zumbis",
        "explorando novas bases",
        "coletando suprimentos",
        "protegendo o refúgio"
    ]
    await bot.change_presence(activity=discord.Game(random.choice(status_list)))

# ---------------------------
# Evento on_ready: Inicia os Loops
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
