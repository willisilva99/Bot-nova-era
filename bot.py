import discord
from discord.ext import commands, tasks
import random
import time
import os

# Definindo intents necessários
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

# Criando o bot com os intents necessários
bot = commands.Bot(command_prefix="!", intents=intents)

# Lista de prêmios com as imagens e suas respectivas probabilidades
prizes = [
    {"name": "AK47", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144266105618573/ak47.png", "chance": 2},  # 2% de chance
    {"name": "VIP", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144289367228446/vip.png", "chance": 3},  # 3% de chance
    {"name": "GIROCOPITERO", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144105841393694/drop-aberto.png", "chance": 2},  # 2% de chance
    {"name": "MOTO", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144223407607869/moto.png", "chance": 2},  # 2% de chance
    {"name": "3.000 EMBERS", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144200271695962/ember.png", "chance": 8},  # 5% de chance
    {"name": "SEM SORTE", "image": "https://media.discordapp.net/attachments/1291144028590706799/1291144175944863784/fail.png", "chance": 82}  # 87% de chance
]

mensagens_sem_sorte = [
    "Os céus escureceram e os ventos trazem más notícias... hoje não é seu dia de sorte!",
    "As hordas estão crescendo e a sorte está se esvaindo... tente novamente mais tarde!",
    "Você caminhou em vão, o apocalipse não perdoa... talvez a próxima vez seja melhor.",
    "O sol se pôs e com ele sua sorte... os zumbis se aproximam, melhor se preparar!",
    "Nada além de trevas à frente, a sorte lhe virou as costas desta vez.",
    "A escuridão tomou conta e a sorte lhe escapou pelos dedos. Tente de novo mais tarde.",
    "Os gritos das almas perdidas ecoam... mas sua sorte foi silenciada.",
    "Hoje, o apocalipse venceu, mas amanhã pode ser diferente... quem sabe?",
    "As ruínas sussurram seu nome, mas sem sorte desta vez.",
    "A batalha foi árdua, mas a vitória não lhe pertenceu hoje. Quem sabe amanhã?",
    "Você lutou contra as probabilidades, mas o apocalipse prevaleceu.",
    "Os portões da esperança se fecharam para você, mas novas chances virão.",
    "A sorte passou despercebida por você, assim como os rastros dos mortos.",
    "Os ventos do destino não sopraram a seu favor hoje... mas continue lutando!",
    "Sua chama de esperança foi extinta momentaneamente, mas ressurge a cada novo dia.",
    "O apocalipse não perdoa... e hoje, você foi uma vítima do azar.",
    "O silêncio da noite engoliu sua sorte... mas ainda há luz no horizonte.",
    "Nenhum raio de sorte atravessou as nuvens escuras desta vez. Talvez amanhã?",
    "O futuro é incerto e a sorte foi cruel. Hoje, não há vitória para você.",
    "O caos prevaleceu e a sorte virou as costas... amanhã pode ser diferente.",
    "O eco do apocalipse abafou sua sorte... tente novamente depois.",
    "A névoa do azar pairou sobre você... a sorte escapou por entre os dedos.",
    "Os mortos caminham com mais sorte que você... quem sabe na próxima tentativa?",
    "As sombras se fecharam sobre você e a sorte se escondeu em algum lugar.",
    "Nem mesmo o destino cruel do apocalipse permitiu um lampejo de sorte hoje.",
    "Sua jornada foi marcada pelo azar. Mas o tempo é seu aliado, tente depois.",
    "O apocalipse não deu trégua e a sorte estava distante... prepare-se para outra chance.",
    "Os céus estavam contra você hoje. A sorte decidiu dar uma pausa.",
    "Os mortos podem ter mais sorte do que você neste dia sombrio.",
    "Os sinais do azar estavam claros... o apocalipse não favoreceu sua sorte.",
    "As trevas envolveram seus passos... e a sorte seguiu por outro caminho.",
    "Sua determinação é louvável, mas a sorte não estava ao seu lado hoje.",
    "O destino riu em sua face e o apocalipse respondeu com silêncio.",
    "Você cruzou o campo de batalha, mas a sorte foi um espectador distante.",
    "Nada além de sombras e lamentos. A sorte foi esquiva desta vez.",
    "O apocalipse sussurrou em seus ouvidos... e a sorte não respondeu.",
    "Seu caminho foi marcado por incertezas e o azar caminhou ao seu lado.",
    "Hoje, os zumbis estavam mais afortunados que você... mas isso pode mudar.",
    "O crepúsculo trouxe má sorte e o amanhecer pode trazer novas esperanças.",
    "A escuridão envolveu sua jornada e a sorte foi consumida pelos zumbis.",
    "O caos dominou e a sorte se perdeu nas ruínas do apocalipse.",
    "O eco da desolação foi tudo que restou... e sua sorte foi engolida pelo vazio.",
    "Você vagou pelas ruínas, mas a sorte estava escondida em outro lugar.",
    "O vento frio trouxe apenas azar... mas a sorte pode estar no próximo sopro.",
    "Os tambores do apocalipse soaram e a sorte não estava em sua melodia.",
    "A sorte lhe virou as costas no último momento... mas ela pode voltar.",
    "Sua jornada foi longa, mas a sorte não cruzou seu caminho desta vez.",
    "O destino não sorriu para você hoje... mas a luta continua.",
    "Você enfrentou os horrores do apocalipse, mas a sorte permaneceu nas sombras.",
    "Nem mesmo o brilho da lua pôde iluminar sua sorte hoje. Quem sabe amanhã?"
]


mensagens_com_sorte = [
    "O apocalipse pode ser sombrio, mas hoje você brilhou!",
    "Sua sorte virou as costas para os zumbis, parabéns pelo prêmio!",
    "O destino sorriu para você hoje... aproveite seu prêmio!",
    "Em meio ao caos, você emergiu vitorioso. Parabéns!",
    "Nem mesmo os zumbis puderam deter sua sorte hoje!",
    "Você provou ser mais forte que o apocalipse... aproveite sua vitória!",
    "Hoje, a sorte esteve do seu lado. Use seu prêmio com sabedoria!",
    "Mesmo em meio às trevas, você encontrou a luz da vitória!",
    "Parabéns, sua habilidade e sorte prevaleceram sobre o caos!",
    "O apocalipse não pôde ofuscar o brilho da sua sorte!",
    "Você desafiou o destino e saiu vitorioso, bem jogado!",
    "Seu nome ecoará pelas ruínas... vencedor de mais um prêmio!",
    "Os céus sorriram para você hoje. Parabéns pelo prêmio!",
    "Em meio à destruição, você encontrou a glória. Aproveite!",
    "A resistência cresce, e você é o mais novo campeão!",
    "A vitória veio com um preço... mas hoje, você foi recompensado!",
    "Os mortos caminham, mas você caminha com sorte!",
    "Você venceu as probabilidades e conquistou o impossível!",
    "As hordas de zumbis não foram páreo para sua sorte!",
    "Você superou o caos e a sorte lhe sorriu. Parabéns!",
    "A escuridão não foi suficiente para apagar seu brilho hoje!",
    "Você desafiou o apocalipse e emergiu vitorioso!",
    "Nem mesmo os horrores do apocalipse puderam te parar!",
    "A sorte finalmente sorriu para você em meio à destruição!",
    "Hoje é o seu dia de sorte. Aproveite o prêmio!",
    "Sua coragem foi recompensada... parabéns pelo prêmio!",
    "A escuridão não é páreo para sua sorte. Aproveite a vitória!",
    "Você dominou o caos e reivindicou seu prêmio!",
    "O destino lhe reservou algo grandioso. Parabéns pela vitória!",
    "Sua vitória hoje é um farol de esperança em meio ao apocalipse!",
    "Os mortos se curvam diante de sua sorte. Aproveite o prêmio!",
    "Sua força e sorte são inegáveis... o prêmio é seu!",
    "Em meio à destruição, você brilhou com sorte e glória!",
    "Hoje, o apocalipse foi apenas um cenário para sua vitória!",
    "Você venceu a escuridão e conquistou a luz da vitória!",
    "Sua jornada no apocalipse trouxe um prêmio merecido!",
    "Nem mesmo o destino cruel pôde negar sua vitória!",
    "Você superou os desafios do apocalipse e conquistou o prêmio!",
    "O apocalipse se rendeu à sua sorte. Parabéns!",
    "Sua determinação foi recompensada com um prêmio glorioso!",
    "Os zumbis observam sua vitória... parabéns pelo prêmio!",
    "Você foi mais forte que o apocalipse. Aproveite sua sorte!",
    "Hoje, o caos foi derrotado por sua sorte. Parabéns!",
    "A destruição ao redor não pôde ofuscar sua glória!",
    "Você foi o escolhido pela sorte. Aproveite o prêmio!",
    "Nem os zumbis puderam resistir à sua vitória hoje!",
    "Você trouxe luz ao apocalipse com sua vitória. Parabéns!",
    "Seu nome será lembrado como o vencedor em meio ao caos!",
    "Sua coragem e sorte iluminaram as ruínas. Aproveite!",
    "Os ventos da destruição não foram páreos para sua vitória!"
]


# Dicionário para armazenar o último tempo de sorteio de cada jogador
last_attempt_time = {}

# Função para selecionar um prêmio com base nas chances
def escolher_premio():
    total = sum(item['chance'] for item in prizes)
    rand = random.uniform(0, total)
    current = 0
    for item in prizes:
        current += item['chance']
        if rand <= current:
            return item

# Função para calcular o tempo restante para o próximo sorteio
def tempo_restante(last_time):
    return max(0, 10800 - (time.time() - last_time))  # 3 horas = 10800 segundos

# Comando para abrir a caixa
@bot.command()
async def abrir_caixa(ctx):
    user = ctx.message.author

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

    # Mensagem diferente dependendo se ganhou ou não
    if prize["name"] == "SEM SORTE":
        mensagem = random.choice(mensagens_sem_sorte)
    else:
        mensagem = random.choice(mensagens_com_sorte)

    # Cria o embed com a imagem do prêmio ou da mensagem de azar
    embed = discord.Embed(
        title="🎁 Você abriu a Caixa de Presentes!",
        description=f"{user.mention}, {mensagem} Você ganhou: **{prize['name']}**!" if prize["name"] != "SEM SORTE" else f"{user.mention}, {mensagem}",
        color=discord.Color.gold()
    )
    embed.set_image(url=prize['image'])

    # Envia a mensagem com o embed no canal
    await ctx.send(embed=embed)

    # Atualiza o tempo da última tentativa do jogador
    last_attempt_time[user.id] = time.time()

# Função para mudar o status do bot periodicamente
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

# ---- Comando para compartilhar o link do grupo do WhatsApp ----
@bot.command(name='grupo')
async def grupo(ctx):
    """Compartilha o link do grupo de WhatsApp."""
    link_grupo = "https://chat.whatsapp.com/ILn1A5UKIXwBpL7voHsDBo"
    await ctx.send(f"📱 **Entre no nosso grupo do WhatsApp:** {link_grupo}")


# Evento quando o bot fica online
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    mudar_status.start()  # Inicia o loop de status

# Rodando o bot com o token de ambiente
TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
