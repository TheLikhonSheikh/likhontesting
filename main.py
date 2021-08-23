import telebot, requests
import qrcode
from telebot import types
from time import sleep
import price as p

bot = telebot.TeleBot('1806540764:AAHfQkvKp-CCzUyVCfTzTH7ePbQq2O8On9c', parse_mode='HTML')
print("Bot started! Running...")

wlcm_msg = """Welcome to the Superdoge Bot! Feel free to ask any questions you have in our <a href='https://t.me/superdogecoin'>Telegram Group</a>.

<b>Website:</b> https://superdoge.com

<b>Live on pancakeswap:</b> <a href='https://exchange.pancakeswap.finance/#/swap?outputCurrency=0xC87A96F7af449aC18Ae59201dDE32e5A38A41C0F'>Buy Now!!</a>

<b>About our project:</b> https://t.me/superdogecoin/20595

<b>Blockchain Explorer:</b> https://explorer.superdoge.net/

<b>Wallet Guides:-</b> /guides"""

guide = """"<ins>The following guides are available related to SuperDoge Wallet:</ins>

<b>Stuck Block:-</b> https://tiny.one/stuckblock
<b>Masternode Link:-</b> https://tiny.one/masternode
<b>Staking Link:-</b> https://tiny.one/staking
<b>Wallet Guide:-</b> https://tiny.one/walletguide
<b>Wallet Encryption Guide:-</b> https://tiny.one/encrypt
<b>Backup & Restore Wallet:-</b> https://tiny.one/backupwallet

In case you need any other guides or if you think any other topic would be useful, do write it in our group:)"""


def newmsgs(message):
    for m in message:
        if message.chat.type == 'private':
            if m.content_type=='text':
                print(str(m.chat.first_name) + ' sent: ' + m.text)
            elif m.content_type in ['audio', 'video', 'location', 'document', 'sticker', 'photo']:
                print(str(m.chat.first_name) + ' sent a misc file')

bot.set_update_listener(newmsgs)


@bot.message_handler(content_types=['document'])
def docmsg(message):
    m = message.chat.id
    bot.send_message(m, "I don't process documents but anyways, I'll keep it:) Thanks!")

    
@bot.message_handler(commands=['start', 'home', 'help'])
def startmsg(message):
    m = message.chat.id
    bot.send_message(m, "Heyo " + message.from_user.first_name + wlcm_msg, disable_web_page_preview=True)
    
    
@bot.message_handler(commands=['guide', 'guides'])
def guideslist(message):
    m = message.chat.id
    bot.send_message(m, guide, disable_web_page_preview=True)
    
    
@bot.message_handler(commands=['cmds', 'commands'])
def cmds(message):
    m = message.chat.id
    bot.send_message(m, """<b>Following available commands:</b>
🏠 /home: Info
📖 /guides: Available Superdoge-Core wallet guides
💰 /balance <code>address</code>: See available SDOGE coins in the given address
📦 /supply: See current circulation supply of SDOGE Coin
🖼 /qr <code>address/text</code>: Generate QR Code for a specific address (BETA)
💹 /price: Current price/details of SDOGE Token""")

    
@bot.message_handler(commands=['supply'])
def supply(message):
    m = message.chat.id
    circulating = requests.get('https://explorer.superdoge.net/ext/getmoneysupply')
    circulating = circulating.text[:15]
    bot.send_message(m, "⚖️ Current circulation supply of SDOGE:" + circulating)

    
@bot.message_handler(commands=['balance'])
def bal(message):
    m = message.chat.id
    msg = message.text
    address = msg[9:]
    if address.startswith('S'):
        if len(address) == 34:
            getbal = requests.get('https://explorer.superdoge.net/ext/getbalance/' + address)
            balance = getbal.text
            if balance.startswith('{'):
                bot.send_message(m, "<b>Invalid Address!</b>\nAddress does not exist!")
            else:
                bot.send_message(m, "💸 Current balance for this address: " + balance)
        else:
            bot.send_message(m, "<b>Invalid Address!</b>\nAddress does not contains 34 characters!")
    else:
        bot.send_message(m, "<b>Incorrect Address format!</b> \nMake sure the address starts with <b>S</b>.\nFor example: /balance ScAfTJwi37dFhsPEzkzn6zxtwqs1yHhoBP")
    
    
@bot.message_handler(commands=['p', 'price'])
def price(message):
    m = message.chat.id
    bot.send_message(m, p.pricesdoge(), disable_web_page_preview=True)

    
@bot.message_handler(commands=['qr'])
def qr(message):
    m = message.chat.id
    msg = message.text
    if len(msg)>4:
        address = msg[3:]
        img = qrcode.make(address)
        img.save('qrcode.png')
        qrimg = open('qrcode.png', 'rb')
        bot.send_photo(m, qrimg, caption="Here's the QR Code!")
        qrimg.close()
    else:
        bot.send_message(m, "Dude, where's the text?")




bot.polling()
