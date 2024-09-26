import os
import discord
from discord.ext import commands, tasks
import random
from flask import Flask, jsonify
import threading
from flask_cors import CORS

# Pega o token da variável de ambiente
TOKEN = os.getenv('TOKEN')

# Configurações dos "intents" para o bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Lista de atividades para o bot
atividades = [
    "sobrevivendo ao apocalipse",
    "jogando 7 Days to Die",
    "escapando de uma horda de zumbis",
    "protegendo o abrigo",
    "construindo fortificações",
    "enfrentando uma lua de sangue",
    "caçando suprimentos",
    "montando armadilhas",
    "liderando um grupo de sobreviventes",
    "fortalecendo a resistência",
    "explorando ruínas",
    "lutando contra os infectados",
    "ajudando novos jogadores",
    "coletando materiais",
    "construindo uma base secreta",
    "reparando veículos",
    "fugindo da morte certa",
    "negociando com comerciantes",
    "falando com Willi",
    "montando defesas contra a invasão"
]

# Evento que indica quando o bot está pronto
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    mudar_atividade.start()

# Tarefa que muda a atividade do bot periodicamente
@tasks.loop(minutes=5)
async def mudar_atividade():
    atividade = random.choice(atividades)
    await bot.change_presence(activity=discord.Game(name=atividade))

# ---- Comando "futuro" com 100 mensagens apocalípticas ----

mensagens_apocalipticas = [
  "A escuridão nos cerca... mas nós continuamos lutando.",
    "Os zumbis não descansam... e você também não deveria.",
    "Cada passo em falso pode ser o último. Esteja sempre pronto.",
    "Há rumores de um abrigo ao norte, mas ninguém sabe ao certo.",
    "As hordas de zumbis estão crescendo. Prepare-se.",
    "O silêncio antes da tempestade é sempre o mais assustador.",
    "O que não nos mata nos torna mais espertos... ou assim espero.",
    "Você está a uma mordida de se juntar a eles... cuidado.",
    "Os infectados estão mais ativos à noite. Não saia do abrigo.",
    "Lembre-se: a esperança é o único recurso que nunca acaba.",
    "Se os mortos estão caminhando, talvez a sobrevivência seja uma ilusão.",
    "Só os mais fortes e atentos conseguem sobreviver a este mundo.",
    "Os suprimentos estão acabando... mas a esperança não.",
    "Em tempos como este, a confiança é uma moeda rara. Escolha bem em quem confiar.",
    "Cuidado com os sobreviventes... nem todos têm boas intenções.",
    "As ruínas guardam segredos... e armadilhas mortais.",
    "O perigo não vem só dos zumbis, mas também dos sobreviventes desesperados.",
    "A horda está cada vez mais perto... tempo está se esgotando.",
    "A verdadeira luta não é contra os zumbis... mas contra o desespero.",
    "Os infectados são rápidos. Não deixe que te alcancem.",
    "Nem todos os sobreviventes querem sua ajuda... alguns preferem seu sangue.",
    "A comida está acabando, a água está contaminada... o que você fará agora?",
    "Algumas vezes, se esconder é a única chance de sobreviver.",
    "As luzes das cidades se apagaram... mas o medo continua aceso.",
    "Amanhã é incerto. Hoje, sobreviva.",
    "Fique em silêncio... eles podem te ouvir.",
    "A morte pode estar ao virar da esquina... mantenha-se atento.",
    "Os infectados não são o pior perigo. Os humanos podem ser muito piores.",
    "A noite é longa, e o amanhecer pode nunca chegar.",
    "Você ainda está aqui, o que significa que ainda há esperança.",
    "Os infectados não perdoam. Nem os sobreviventes.",
    "Não há heróis no apocalipse, só sobreviventes.",
    "Os gritos no vento... não vá em direção a eles.",
    "Cada dia é uma luta... e cada noite é um pesadelo.",
    "Se você está ouvindo isso, significa que ainda há tempo.",
    "Os suprimentos são poucos, mas sua vontade de viver deve ser infinita.",
    "Os mortos andam. E a noite pertence a eles.",
    "Se você está com medo, significa que ainda está vivo.",
    "Os que perderam a esperança já estão mortos por dentro.",
    "Mantenha-se vivo, mesmo que isso signifique perder tudo o que você tinha antes.",
    "Os infectados estão ficando mais fortes... e mais rápidos.",
    "Nunca confie em um silêncio muito profundo.",
    "Os muros do abrigo podem não segurar por muito mais tempo.",
    "Você acha que está seguro... até a próxima mordida.",
    "Nunca fique em um lugar por muito tempo. Eles sempre acham um jeito de entrar.",
    "Cada pessoa que você encontra pode ser um aliado... ou um inimigo.",
    "Se você ainda pode correr, corra.",
    "Os gritos à distância são um aviso. Não ignore.",
    "Os infectados podem ter perdido sua humanidade, mas ainda têm fome.",
    "Os fortes sobrevivem. Os fracos se tornam parte da horda.",
    "Aqueles que param para descansar, nunca acordam para lutar novamente.",
    "Se você puder lutar, lute. Se não puder, corra.",
    "Os dias parecem longos... mas as noites são intermináveis.",
    "O cheiro de morte está em todo lugar... até mesmo dentro de nós.",
    "Nunca olhe para trás. O passado não tem nada a te oferecer agora.",
    "As noites sem lua são as piores... você nunca sabe o que está à espreita.",
    "Os gritos de um sobrevivente podem atrair mais do que você gostaria.",
    "Sobreviver é uma escolha que você faz todos os dias. Não desista agora.",
    "Há coisas piores do que zumbis lá fora... e elas sabem seu nome.",
    "Os infectados podem estar por perto. Mantenha-se em silêncio.",
    "Cuidado com os becos... eles são armadilhas mortais.",
    "Os zumbis podem não ter alma, mas ainda têm fome.",
    "Nunca subestime o silêncio. Ele pode ser mais mortal que o barulho.",
    "Cada esquina é um risco. Mas você não tem escolha.",
    "Os mortos podem não sentir dor... mas você sente.",
    "As chances de sobrevivência diminuem a cada segundo.",
    "Os infectados nunca dormem... e você também não deveria.",
    "A cada grito na noite, uma nova horda se aproxima.",
    "Os zumbis não vão parar até que não sobre mais ninguém.",
    "A única constante no apocalipse é o medo.",
    "Os becos escuros guardam mais segredos do que você gostaria de saber.",
    "Os zumbis não sentem cansaço. Eles te seguirão até o fim.",
    "Sobreviver a cada dia é uma batalha, e a guerra nunca termina.",
    "As cicatrizes que carregamos são lembretes de que ainda estamos aqui.",
    "Não há lugar seguro. Apenas lugares menos perigosos.",
    "O que você faria por uma lata de comida agora?",
    "Os infectados estão sempre a uma mordida de distância.",
    "Sobreviver não é mais uma questão de sorte. É uma questão de escolha.",
    "O silêncio é seu maior aliado... e seu pior inimigo.",
    "O fim do mundo chegou... mas o seu ainda não terminou.",
    "A noite é perigosa... mas às vezes o dia é pior.",
    "A cada passo que você dá, você desafia a morte.",
    "Os infectados não sabem a diferença entre amigo ou inimigo. Eles só querem carne.",
    "Não se apegue demais aos outros. No apocalipse, todos estão por conta própria.",
    "Os zumbis podem ser lentos, mas o desespero é rápido.",
    "Os mortos estão por toda parte, mas você ainda está aqui. Lute por isso.",
    "Os gritos dos outros sobreviventes ecoam pelas ruínas. Você vai responder?",
    "Os infectados não são o único problema... a fome também mata.",
    "As ruas são traiçoeiras, e o silêncio pode ser uma armadilha.",
    "Você sobreviveu até agora... mas a próxima luta pode ser a última.",
    "O abrigo está ficando fraco... talvez seja hora de procurar outro.",
    "Nunca baixe a guarda. A qualquer momento, tudo pode mudar.",
    "A fome está te corroendo por dentro... mas o medo é ainda pior.",
    "A verdadeira luta não é contra os zumbis... é contra o desespero."
]

@bot.command(name='futuro')
async def futuro(ctx):
    """Responde com uma mensagem apocalíptica sobre o futuro."""
    mensagem = random.choice(mensagens_apocalipticas)
    await ctx.send(f"🔮 **O Futuro no Apocalipse diz:** {mensagem}")

# ---- Comando para listar jogadores online ----
app = Flask(__name__)
# Permite acessos de qualquer origem
CORS(app, resources={r"/*": {"origins": "*"}})  # Permite qualquer origem

@bot.command(name='listar_jogadores_online')
async def listar_jogadores_online(ctx):
    """Lista os jogadores online no servidor no estilo apocalíptico, com apelidos destacados e mensagens aleatórias."""
    guild = ctx.guild  # Obtém o servidor atual
    membros_online = [member for member in guild.members if member.status != discord.Status.offline and not member.bot]

    # Mensagens apocalípticas para diferentes status
    mensagens_ativo = [
        "Ativo em combate!",
        "Matando zumbis incansavelmente!",
        "Lutando contra os infectados sem parar!",
        "Em plena ação, sobrevivendo ao caos!",
        "Explorando territórios devastados!",
        "Protegendo o abrigo dos invasores!",
        "Armas em punho, sem descanso!",
        "Patrulhando as fronteiras!",
        "Lidando com uma horda de infectados!",
        "No comando da resistência!"
    ]

    mensagens_ausente = [
        "Descansando nas sombras...",
        "Fora de vista, mas atento...",
        "Recarregando energias para a próxima batalha...",
        "Escondido, planejando o próximo movimento...",
        "Recuperando forças em algum refúgio...",
        "Observando à distância, aguardando o momento certo...",
        "Deixando os aliados temporariamente...",
        "Desaparecido, mas ainda vivo...",
        "Dando uma pausa antes da próxima missão...",
        "Camuflado nas ruínas, preparando-se para voltar!"
    ]

    mensagens_missao = [
        "Em missão secreta. Não perturbe!",
        "Preparando-se para um confronto perigoso.",
        "Em busca de suprimentos. Não interrompa!",
        "Cumprindo um objetivo vital. Não perturbe!",
        "Investigando território hostil.",
        "Em contato com sobreviventes distantes.",
        "Liderando uma operação arriscada.",
        "Realizando tarefas essenciais para a sobrevivência.",
        "Em patrulha avançada, sem tempo para distrações.",
        "Focado em uma missão crítica!"
    ]

    if not membros_online:
        await ctx.send("🚨 **Nenhum sobrevivente foi avistado no momento... O silêncio predomina na Nova Era.**")
    else:
        resposta = "🌍 **Sobreviventes Avistados na Nova Era** 🌍\n"
        for member in membros_online:
            nome = f"**{member.display_name}**"  # Usa o apelido destacado (negrito)

            # Definir status de presença com mensagem aleatória
            if member.status == discord.Status.online:
                status_emoji = "🟢"
                status_nome = random.choice(mensagens_ativo)
            elif member.status == discord.Status.idle:
                status_emoji = "🟠"
                status_nome = random.choice(mensagens_ausente)
            elif member.status == discord.Status.dnd:
                status_emoji = "🔴"
                status_nome = random.choice(mensagens_missao)
            else:
                status_emoji = "⚪"
                status_nome = "Desconhecido"

            # Adicionar à resposta
            resposta += f"{status_emoji} {nome} - {status_nome}\n"
        resposta += "\n⚠️ **Mantenha-se atento, as forças hostis podem atacar a qualquer momento!** ⚠️"

        await ctx.send(resposta)

@bot.command(name='roleta_russa')
async def roleta_russa(ctx):
    """Simula uma roleta russa apocalíptica."""
    bala = random.randint(1, 6)  # Define um número aleatório de 1 a 6 para representar a bala no tambor
    tiro = random.randint(1, 6)  # Define um número aleatório de 1 a 6 para o tiro

    if bala == tiro:
        await ctx.send(f"💥 *Clique!* Você sobreviveu... desta vez.")
    else:
        await ctx.send(f"💥 *Bang!* {ctx.author.mention}, você não teve tanta sorte...")


# ---- Parte do Flask ----

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'status': 'Bot está online e rodando!'})

@app.route('/destaques')
def get_destaques():
    guild = bot.get_guild(1186390028990025820)
    if guild is None:
        return jsonify({'error': 'Servidor não encontrado'}), 404

    role = discord.utils.get(guild.roles, name="Destaque")
    if not role:
        return jsonify({'error': 'Função não encontrada'}), 404

    members = [{
        'id': member.id,
        'username': member.name,
        'avatar': member.avatar.url if member.avatar else None
    } for member in role.members]

    return jsonify(members)




# Função para rodar a API Flask em uma thread separada
def run_api():
    app.run(host='0.0.0.0', port=5000)

# Função para rodar o bot e a API ao mesmo tempo
def run_bot():
    bot.run(TOKEN)

# Iniciar as threads
if __name__ == '__main__':
    threading.Thread(target=run_api).start()
    run_bot()
