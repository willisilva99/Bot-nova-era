import os
import discord
from discord.ext import commands, tasks
from flask import Flask, jsonify, request
import threading
from flask_cors import CORS
import asyncio

# Pega o token da variável de ambiente
TOKEN = os.getenv('TOKEN')
CHANNEL_ID = 1186636197934661632  # Substitua pelo ID do canal correto

# Configurações dos "intents" para o bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ---- API Flask ----
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'status': 'Bot está online e rodando!'})

# Endpoint para receber a mensagem do prêmio e postar no chat do Discord
@app.route('/post_reward', methods=['POST'])
def post_reward():
    data = request.json
    if 'player' in data and 'item' in data:
        player = data['player']
        item = data['item']
        message = f'{player} abriu a Caixa de Presentes e ganhou: **{item}**!'
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            asyncio.run_coroutine_threadsafe(channel.send(message), bot.loop)
        return jsonify({'status': 'Mensagem enviada para o Discord'}), 200
    else:
        return jsonify({'error': 'Dados inválidos'}), 400

# Função para rodar a API Flask em uma thread separada
def run_api():
    port = int(os.environ.get('PORT', 5000))  # Railway usa a variável de ambiente PORT
    app.run(host='0.0.0.0', port=port)

# Função para rodar o bot e a API ao mesmo tempo
def run_bot():
    bot.run(TOKEN)

# Iniciar as threads
if __name__ == '__main__':
    threading.Thread(target=run_api).start()
    run_bot()
