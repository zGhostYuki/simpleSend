# (C) Yuki's Project 2018
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from Files import utils

updater = Updater('TOKEN')
master = 0
channel_nick = 'CHANNELNICK'
dp = updater.dispatcher


# Log #
def fprint(string):
    with open('Files/messages.log', 'a') as f:
        f.write(string + '\n')


# Start #
def start(bot, update):
    cid = update.message.chat_id
    nick = update.message.from_user.username
    uid = update.message.from_user.id
    first_name = update.message.from_user.first_name
    if not nick:
        bot.sendMessage(cid, f'Hi! Welcome to this bot! From now, you can send messages to @{channel_nick} from *this b'
                             f'ot*!\n\n❗️ *WARNING*: To use the bot, *set a username*.', 'markdown')
        fprint(f'NoNick {first_name} ({uid}) used \'/start\'')
    else:
        if utils.banned(uid):
            bot.sendMessage(cid, f'Hi! Welcome to this bot! From now, you can send messages to @{channel_nick} from *th'
                                 f'is bot*!\n\n🚫 *WARNING*: You\'re banned from this bot!', 'markdown')
            bot.sendMessage(master, f'*Banned* [{nick}](tg://user?id={uid}) (`{uid}`) tried to send \'/start\'!',
                            'markdown', disable_web_page_preview=True)
            fprint('Banned %s (%s) used \'/start\'!' % (nick, uid))
            return
        if uid == master:
            bot.sendMessage(cid, f'Hi! Welcome to this bot! From now, you can send messages to @{channel_nick} from *th'
                                 f'is bot*!\n\nYou\'re my *master*!', 'markdown')
            fprint(f'Founder {nick} ({uid}) used \'/start\'')
            return
        bot.sendMessage(cid, f'Hi! Welcome to this bot! From now, you can send messages to @{channel_nick} from *this b'
                             f'ot*!',
                        'markdown')
        fprint(f'User {nick} ({uid}) used \'/start\'')


# Messages #
def send_text(bot, update):
    send = bot.sendMessage
    reply = update.message.reply_text
    msg = update.message.text
    nick = update.message.from_user.username
    uid = update.message.from_user.id
    if uid == master:
        reply('*Sent!*', 'markdown')
        send(f'@{channel_nick}', f'👑 *{nick}*: {msg}', 'markdown', disable_web_page_preview=True)
        fprint(f'Founder {nick} ({uid}): {msg}')
    else:
        if utils.banned(uid):
            reply('*You\'re banned from this bot!*', 'markdown')
            send(master, f'*Banned* [{nick}](tg://user?id={uid}) (`{uid}`) tried to send \'{msg}\'', 'markdown',
                 disable_web_page_preview=True)
            fprint(f'Banned {nick} ({uid}) tried to send \'{msg}\'')
        else:
            reply('*Sent!*', 'markdown')
            send(master, f'*User* [{nick}](tg://user?id={uid}) (`{uid}`): {msg}', 'markdown',
                 disable_web_page_preview=True)
            send(f'@{channel_nick}', f'👤 *{nick}*: {msg}', 'markdown', disable_web_page_preview=True)
            fprint(f'User {nick} ({uid}): {msg}')


# Ban #
def ban_command(bot, update, args):
    uid = update.message.from_user.id
    reply = update.message.reply_text
    send = bot.sendMessage
    nick = update.message.from_user.username
    if uid == master:
        reply(f'`{args[0]}` banned!', 'markdown')
        utils.ban(args[0])
        send(args[0], 'You have been *banned from this bot*.', 'markdown')
        fprint(f'{args[0]} banned.')
        print('File banlist.txt updated.')
    else:
        reply('You cannot use *this command*!', 'markdown')
        send(master, f'{nick} tried to use \'/ban\'.')


# Handler #
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('ban', ban_command, pass_args=True))
dp.add_handler(MessageHandler(Filters.text, send_text))

updater.start_polling(print('Bot started.'))
updater.idle()
