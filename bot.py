import discord
from discord.ext import commands
import random

bot = commands.Bot(command_prefix="!")

# Lista de prêmios com as imagens atualizadas
prizes = [
    {"name": "AK47", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144266105618573/ak47.png?ex=66ff074d&is=66fdb5cd&hm=a99d2330c123bd5add6a73dc89dc1d6f9d34018e7cb65f4934ac8201c4611949&=&format=webp&quality=lossless&width=176&height=176"},
    {"name": "VIP", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144289367228446/vip.png?ex=66ff0752&is=66fdb5d2&hm=2bef9e8b92217199e41d1a801c5ce4c0867a6c1e3df08220af03b362da589447&=&format=webp&quality=lossless&width=517&height=165"},
    {"name": "GIROCOPITERO", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144105841393694/drop-aberto.png?ex=66ff0727&is=66fdb5a7&hm=781d4875800217af3b9898bba186b5cf56c94a76c55b95e1f2584fca8a22bb1d&=&format=webp&quality=lossless&width=619&height=619"},
    {"name": "MOTO", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144223407607869/moto.png?ex=66ff0743&is=66fdb5c3&hm=106ebe00732e5cfcd749c696ae7a2540743e89aa7a273960f39244982dddaf73&=&format=webp&quality=lossless&width=176&height=176"},
    {"name": "3.000 EMBERS", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144200271695962/ember.png?ex=66ff073d&is=66fdb5bd&hm=c8a2cfee6c021fc3704432d99773dec10153b931467e073199a491210ae1be65&=&format=webp&quality=lossless&width=385&height=385"},
    {"name": "SEM SORTE", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144175944863784/fail.png?ex=66ff0737&is=66fdb5b7&hm=02abcf68da7473f54d7b5b221f15ae6cb47aeb4402c839ac6450cb5525409153&=&format=webp&quality=lossless&width=619&height=619"}
]

# Comando para abrir a caixa
@bot.command()
async def abrir_caixa(ctx):
    # Menciona o jogador que abriu a caixa
    user = ctx.message.author.mention
    
    # Sorteia um prêmio aleatoriamente
    prize = random.choice(prizes)
    
    # Cria o embed com a imagem do prêmio ou da caixa fechada
    embed = discord.Embed(
        title="🎁 Você abriu a Caixa de Presentes!",
        description=f"{user}, você ganhou: **{prize['name']}**!",
        color=discord.Color.gold()
    )
    embed.set_image(url=prize['image'])

    # Envia a mensagem com o embed no canal
    await ctx.send(embed=embed)

# Rodando o bot
bot.run("SEU_TOKEN_AQUI")
