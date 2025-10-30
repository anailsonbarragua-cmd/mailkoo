# ...existing code...
import os
import sys
import logging
import telebot
import yt_dlp

logging.basicConfig(level=logging.INFO)

# Carrega TOKEN da variável de ambiente ou do arquivo token.env (na raiz do workspace)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    env_path = os.path.join(os.path.dirname(__file__), "token.env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("TELEGRAM_TOKEN"):
                    _, _, val = line.partition("=")
                    TOKEN = val.strip().strip('"').strip("'")
                    break

if not TOKEN:
    logging.error("Variável de ambiente TELEGRAM_TOKEN não definida. Exporte TELEGRAM_TOKEN ou crie token.env.")
    sys.exit(1)

bot = telebot.TeleBot(TOKEN)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎵 Envie o link do YouTube que eu vou converter em MP3 pra você!")

@bot.message_handler(func=lambda m: True)
def baixar_mp3(message):
    url = (message.text or "").strip()
    if not ("youtube.com" in url or "youtu.be" in url):
        bot.reply_to(message, "❗ Envie um link válido do YouTube.")
        return

    status_msg = None
    try:
        status_msg = bot.send_message(message.chat.id, "🎬 Baixando e convertendo... aguarde ⏳")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(id)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            mp3_path = filename.rsplit('.', 1)[0] + '.mp3'

            if not os.path.exists(mp3_path):
                raise FileNotFoundError("Arquivo MP3 não encontrado após conversão.")

            with open(mp3_path, 'rb') as audio:
                bot.send_audio(message.chat.id, audio, title=info.get('title'))

    except Exception as e:
        logging.exception("Erro ao processar link")
        bot.send_message(message.chat.id, f"❌ Erro ao processar: {e}")
    finally:
        # limpeza de arquivos temporários
        for root, _, files in os.walk(DOWNLOAD_DIR):
            for f in files:
                try:
                    os.remove(os.path.join(root, f))
                except Exception:
                    pass
        if status_msg:
            try:
                bot.delete_message(message.chat.id, status_msg.message_id)
            except Exception:
                pass

if __name__ == "__main__":
    bot.polling(non_stop=True)
# ...existing code...