import os
import discord
from discord.ext import commands

# Configurações e Token
TOKEN = os.getenv('TOKEN')  # Certifique-se de que essa variável está corretamente configurada no ambiente Railway
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Defina o ID do canal onde as mensagens de prêmios serão enviadas
CHANNEL_ID = 1186636197934661632

# Itens e chances
items = [
    {"name": "AK47", "image": "images/ak47.png", "chance": 5},
    {"name": "VIP", "image": "images/vip.png", "chance": 5},
    {"name": "GIROCOPITERO", "image": "images/giro.png", "chance": 5},
    {"name": "MOTO", "image": "images/moto.png", "chance": 5},
    {"name": "3.000 EMBERS", "image": "images/ember.png", "chance": 10},
    {"name": "SEM SORTE", "image": "images/fail.png", "chance": 70}
]

# Função para enviar a mensagem de prêmio no Discord
async def enviar_mensagem_premio(jogador, item_ganho):
    canal = bot.get_channel(CHANNEL_ID)
    if canal:
        if item_ganho["name"] == "SEM SORTE":
            await canal.send(f"Infelizmente, {jogador}, você não teve sorte desta vez. Tente novamente em 2 horas!")
        else:
            await canal.send(f"Parabéns, {jogador}! Você ganhou o prêmio: **{item_ganho['name']}** 🎉")

# Evento quando o bot estiver pronto
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

# Função de premiação que será chamada quando o jogador abrir a caixa
def abrir_caixa(jogador):
    import random
    total_chance = sum(item['chance'] for item in items)
    sorteio = random.uniform(0, total_chance)
    acumulado = 0
    for item in items:
        acumulado += item['chance']
        if sorteio <= acumulado:
            return item

# Simulação da função para abrir a caixa e notificar o jogador no Discord
@bot.command()
async def abrir(ctx):
    jogador = ctx.author.display_name  # Pega o nome do jogador
    item_ganho = abrir_caixa(jogador)  # Sorteia o prêmio
    await enviar_mensagem_premio(jogador, item_ganho)  # Envia o prêmio ao canal do Discord
    await ctx.send(f"Caixa aberta por {jogador}. Confira o canal de prêmios no Discord!")  # Confirmação no chat

# Iniciar o bot
bot.run(TOKEN)
