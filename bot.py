import discord
from discord.ext import commands, tasks
import random
import time
import os
import asyncio
from datetime import datetime, timedelta

# Definindo intents necessários
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

# Criando o bot com os intents necessários
bot = commands.Bot(command_prefix="!", intents=intents)

# Lista de prêmios com as imagens e suas respectivas probabilidades para o comando abrir_caixa
prizes = [
    {"name": "AK47", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144266105618573/ak47.png", "chance": 1},
    {"name": "VIP", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144289367228446/vip.png", "chance": 1},
    {"name": "GIROCOPITERO", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144105841393694/drop-aberto.png", "chance": 1},
    {"name": "MOTO", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144223407607869/moto.png", "chance": 1},
    {"name": "3.000 EMBERS", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144200271695962/ember.png", "chance": 2},
    {"name": "SEM SORTE", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144175944863784/fail.png", "chance": 91}
]

# Mensagens de azar para o comando abrir_caixa
mensagens_sem_sorte = [
    "Os céus escureceram e os ventos trazem más notícias... hoje não é seu dia de sorte!",
    "As hordas estão crescendo e a sorte está se esvaindo... tente novamente mais tarde!",
    "Você caminhou em vão, o apocalipse não perdoa... talvez a próxima vez seja melhor.",
    # ... (adicione outras mensagens se desejar)
]

# Mensagens de sorte para o comando abrir_caixa
mensagens_com_sorte = [
    "O apocalipse pode ser sombrio, mas hoje você brilhou!",
    "Sua sorte virou as costas para os zumbis, parabéns pelo prêmio!",
    "O destino sorriu para você hoje... aproveite seu prêmio!",
    # ... (adicione outras mensagens se desejar)
]

# Mensagens apocalípticas para prêmios valiosos e rankings
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

# Dicionários para armazenar dados dos jogadores (para o comando abrir_caixa)
last_attempt_time = {}  # Para controlar o cooldown de 3 horas na abertura de caixa
player_prizes = {}      # Para armazenar os prêmios ganhos (exceto "SEM SORTE")
player_box_opens = {}   # Para contar quantas caixas foram abertas
player_embers = {}      # Para armazenar a quantidade total de embers ganhos (por ambos os jogos)

# Dicionários para armazenar dados do jogo dos dados
player_dado_wins = {}    # Quantas vezes o jogador ganhou (quando os dados premiam)
player_dado_embers = {}  # Quantidade de embers ganhos somente com o jogo dos dados

# Emojis de reação para adicionar na mensagem de prêmios da caixa
reacoes = ["🔥", "<:emoji_1:1262824010723365030>", "<:emoji_2:1261377496893489242>", "<:emoji_3:1261374830088032378>", "<:emoji_4:1260945241918279751>"]

# Função para selecionar um prêmio com base nas chances (para o abrir_caixa)
def escolher_premio():
    total = sum(item['chance'] for item in prizes)
    rand = random.uniform(0, total)
    current = 0
    for item in prizes:
        current += item['chance']
        if rand <= current:
            return item

# Função para calcular o tempo restante para a próxima abertura de caixa (3 horas)
def tempo_restante(last_time):
    return max(0, 10800 - (time.time() - last_time))  # 3 horas = 10800 segundos

# ---------------------------
# COMANDO: abrir_caixa
# ---------------------------
@bot.command()
async def abrir_caixa(ctx):
    canal_permitido = 1292879357446062162
    if ctx.channel.id != canal_permitido:
        await ctx.send(f"{ctx.author.mention}, você só pode usar o comando neste canal: <#{canal_permitido}>")
        return

    user = ctx.author

    # Verifica se o jogador já tentou nos últimos 3 horas
    if user.id in last_attempt_time:
        tempo_rest = tempo_restante(last_attempt_time[user.id])
        if tempo_rest > 0:
            horas = int(tempo_rest // 3600)
            minutos = int((tempo_rest % 3600) // 60)
            segundos = int(tempo_rest % 60)
            await ctx.send(f"{user.mention}, você precisa esperar {horas}h {minutos}m {segundos}s para tentar novamente.")
            return

    # Sorteia um prêmio com base nas chances
    prize = escolher_premio()

    # Seleciona a mensagem de resposta conforme o prêmio
    if prize["name"] == "SEM SORTE":
        mensagem = random.choice(mensagens_sem_sorte)
    else:
        mensagem = random.choice(mensagens_com_sorte)
        player_prizes[user.id] = player_prizes.get(user.id, []) + [prize["name"]]
        # Envia mensagem apocalíptica para prêmios valiosos
        mensagem_apocaliptica = random.choice(mensagens_apocalipticas).format(user=user.display_name)
        await ctx.send(mensagem_apocaliptica)

    # Incrementa o contador de caixas abertas
    player_box_opens[user.id] = player_box_opens.get(user.id, 0) + 1

    # Cria embed com o prêmio ou mensagem de azar
    embed = discord.Embed(
        title="🎁 Você abriu a Caixa de Presentes!",
        description=(f"{user.mention}, {mensagem} Você ganhou: **{prize['name']}**!"
                     if prize["name"] != "SEM SORTE" else f"{user.mention}, {mensagem}"),
        color=discord.Color.gold()
    )
    embed.set_image(url=prize['image'])

    # Envia o embed e adiciona uma reação se houver prêmio
    msg = await ctx.send(embed=embed)
    if prize["name"] != "SEM SORTE":
        await msg.add_reaction(random.choice(reacoes))

    # Atualiza o tempo da última tentativa
    last_attempt_time[user.id] = time.time()

# ---------------------------
# COMANDO: rolardado
# ---------------------------
@bot.command()
async def rolardado(ctx):
    """Jogo de dado com animação: se cair 5 ou 6, o jogador pode ganhar embers (chance baixa)."""
    user = ctx.author

    # Envia embed com um GIF simulando o dado rolando
    gif_url = "https://imgur.com/PEpiSuw.gif"  # Altere o URL do GIF se desejar
    embed_rolando = discord.Embed(
        title="🎲 Rolando o Dado...",
        description="Aguarde enquanto o dado está sendo rolado.",
        color=discord.Color.blue()
    )
    embed_rolando.set_image(url=gif_url)
    mensagem_gif = await ctx.send(embed=embed_rolando)

    # Aguarda alguns segundos para simular a rolagem
    await asyncio.sleep(3)

    # Calcula o resultado do dado (1 a 6)
    resultado = random.randint(1, 6)
    mensagem_resultado = f"{user.mention} rolou o dado e saiu **{resultado}**!\n"
    
    embers_ganhos = 0
    # Apenas se o resultado for 5 ou 6, uma verificação extra define se o jogador ganha ou não (chance baixa)
    if resultado == 5:
        # Chance de 20% de ganhar
        if random.random() < 0.20:
            embers_ganhos = 5000
            mensagem_resultado += f"Parabéns! Você ganhou **{embers_ganhos} embers**!"
        else:
            mensagem_resultado += "Que pena, a sorte não colaborou desta vez."
    elif resultado == 6:
        if random.random() < 0.20:
            embers_ganhos = 6000
            mensagem_resultado += f"Parabéns! Você ganhou **{embers_ganhos} embers**!"
        else:
            mensagem_resultado += "Que pena, a sorte não colaborou desta vez."
    else:
        mensagem_resultado += "Que pena, dessa vez a sorte não esteve ao seu lado."

    # Atualiza o saldo de embers do jogador, se aplicável (acrescenta tanto no geral quanto no ranking dos dados)
    if embers_ganhos > 0:
        player_embers[user.id] = player_embers.get(user.id, 0) + embers_ganhos
        player_dado_wins[user.id] = player_dado_wins.get(user.id, 0) + 1
        player_dado_embers[user.id] = player_dado_embers.get(user.id, 0) + embers_ganhos

    # Apaga a mensagem com o GIF
    await mensagem_gif.delete()

    # Envia o embed com o resultado final do dado
    embed_resultado = discord.Embed(
        title="🎲 Resultado do Dado",
        description=mensagem_resultado,
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed_resultado)

# ---------------------------
# LOOP: Ranking dos melhores prêmios da Caixa (a cada 6 horas)
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
    # Ordena pelo total de embers ganhos apenas com os dados
    rank = sorted(player_dado_embers.items(), key=lambda x: x[1], reverse=True)
    mensagem = "🎲 **Ranking de Prêmios dos Dados** 🎲\n\n"
    for i, (user_id, embers_total) in enumerate(rank[:10], start=1):
        user = await bot.fetch_user(user_id)
        wins = player_dado_wins.get(user_id, 0)
        mensagem += f"{i}. **{user.display_name}** - {wins} vitórias (Total: {embers_total} embers)\n"
    await channel.send(mensagem)

# ---------------------------
# LOOP: Resetar Rankings, Premiações e Limpar o Chat às 00:00 (verificado a cada minuto)
# ---------------------------
@tasks.loop(minutes=1)
async def reset_rankings():
    now = datetime.now()
    if now.hour == 0 and now.minute == 0:  # Exatamente à meia-noite
        channel = bot.get_channel(1292879357446062162)
        
        # Premiar o primeiro lugar no ranking de prêmios da caixa
        rank_melhores = sorted(player_prizes.items(), key=lambda x: sum(1 for prize in x[1] if prize != "SEM SORTE"), reverse=True)
        if rank_melhores:
            melhor_jogador, _ = rank_melhores[0]
            player_embers[melhor_jogador] = player_embers.get(melhor_jogador, 0) + 100
            user = await bot.fetch_user(melhor_jogador)
            mensagem_apocaliptica = random.choice(mensagens_apocalipticas).format(user=user.display_name)
            await channel.send(f"{mensagem_apocaliptica}\nParabéns {user.mention}! Você recebeu **100 embers** por ser o melhor do ranking de prêmios!")

        # Premiar o primeiro lugar no ranking de aberturas de caixas
        rank_aberturas = sorted(player_box_opens.items(), key=lambda x: x[1], reverse=True)
        if rank_aberturas:
            melhor_abertura, _ = rank_aberturas[0]
            player_embers[melhor_abertura] = player_embers.get(melhor_abertura, 0) + 100
            user = await bot.fetch_user(melhor_abertura)
            mensagem_apocaliptica = random.choice(mensagens_apocalipticas).format(user=user.display_name)
            await channel.send(f"{mensagem_apocaliptica}\nParabéns {user.mention}! Você recebeu **100 embers** por ser o melhor do ranking de aberturas de caixas!")

        # Resetar dados da caixa e limpar o canal
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

# Evento on_ready: quando o bot estiver online, inicia os loops
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    mudar_status.start()            # Inicia o loop de status
    rank_melhores_presentes.start() # Inicia o loop de ranking dos melhores prêmios da caixa
    rank_aberturas_caixa.start()    # Inicia o loop de ranking de aberturas de caixas
    rank_dados.start()              # Inicia o loop de ranking dos prêmios dos dados
    reset_rankings.start()          # Inicia o loop de reset dos rankings e limpeza do chat

# Obtendo o token da variável de ambiente e iniciando o bot
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("TOKEN não definido. Certifique-se de que a variável de ambiente 'TOKEN' está configurada corretamente.")
bot.run(TOKEN)
