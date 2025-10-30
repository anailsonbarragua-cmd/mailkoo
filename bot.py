import telebot
import random
import re

import os
bot = telebot.TeleBot(os.environ['8232810183:AAFjXZj9PjHc2eZsI33GvAwcMTg_0LdHBbw'])

bot = telebot.TeleBot('8232810183:AAFjXZj9PjHc2eZsI33GvAwcMTg_0LdHBbw')

@bot.message_handler(commands=['Gerador'])
def Gerador(mensagem):
    for _ in range(5):
        nove_digitos = ''.join([str(random.randint(0, 9)) for _ in range(9)])

        contador_regressivo_1 = 10
        resultado_digito_1 = sum(int(digito) * contador_regressivo_1 for digito, contador_regressivo_1 in zip(nove_digitos, range(10, 1, -1)))
        digito_1 = (resultado_digito_1 * 10) % 11
        digito_1 = digito_1 if digito_1 <= 9 else 0

        dez_digitos = nove_digitos + str(digito_1)
        resultado_digito_2 = sum(int(digito) * contador for digito, contador in zip(dez_digitos, range(11, 1, -1)))
        digito_2 = (resultado_digito_2 * 10) % 11
        digito_2 = digito_2 if digito_2 <= 9 else 0

        cpf_gerado_pelo_calculo = f'{nove_digitos}{digito_1}{digito_2}'
        bot.send_message(mensagem.chat.id, cpf_gerado_pelo_calculo)

    bot.send_message(mensagem.chat.id, "5 CPFs gerados com sucesso ✅✅")
    bot.send_message(mensagem.chat.id, "Posso ajudar em algo mais? Se sim, digite /iniciar")

@bot.message_handler(commands=['Validador'])
def Validador(mensagem):
    msg = bot.send_message(mensagem.chat.id, "Digite seu CPF:")
    bot.register_next_step_handler(msg, validar_cpf)

def validar_cpf(mensagem):
    cpf_enviado_usuario = re.sub(r'[^0-9]', '', mensagem.text)

    if len(cpf_enviado_usuario) != 11:
        bot.send_message(mensagem.chat.id, "O CPF deve ter 11 dígitos. Tente novamente.")
        return

    if cpf_enviado_usuario == cpf_enviado_usuario[0] * len(cpf_enviado_usuario):
        bot.send_message(mensagem.chat.id, "CPF inválido (sequência repetida).")
        return

    nove_digitos = cpf_enviado_usuario[:9]
    contador_regressivo_1 = 10
    resultado_digito_1 = 0

    for digito in nove_digitos:
        resultado_digito_1 += int(digito) * contador_regressivo_1
        contador_regressivo_1 -= 1

    digito_1 = (resultado_digito_1 * 10) % 11
    digito_1 = digito_1 if digito_1 <= 9 else 0

    dez_digitos = nove_digitos + str(digito_1)
    contador_regressivo_2 = 11
    resultado_digito_2 = 0

    for digito in dez_digitos:
        resultado_digito_2 += int(digito) * contador_regressivo_2
        contador_regressivo_2 -= 1

    digito_2 = (resultado_digito_2 * 10) % 11
    digito_2 = digito_2 if digito_2 <= 9 else 0

    cpf_gerado_pelo_calculo = f'{nove_digitos}{digito_1}{digito_2}'

    if cpf_enviado_usuario == cpf_gerado_pelo_calculo:
        bot.send_message(mensagem.chat.id, f'{cpf_enviado_usuario} é Válido. ✅')
    else:
        bot.send_message(mensagem.chat.id, "CPF inválido. Tente novamente. ❌")

    bot.send_message(mensagem.chat.id, "Posso ajudar em algo mais? Se sim, digite /iniciar")

def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """Olá! Por favor, escolha uma das opções:

/Gerador - Gerar CPF 🔄️
/Validador - Validar CPF ✅
"""
    bot.send_message(mensagem.chat.id, texto)

bot.polling()