import telebot, requests, qrcode, os
from time import sleep
from telebot.types import InlineKeyboardButton as ikb
from telebot.types import InlineKeyboardMarkup as ikm
from alive import keep_alive
from telebot.types import InlineQueryResultArticle as search
from telebot.types import InputTextMessageContent as MSG


keep_alive()

Access_Token = os.environ["TOKEN"]
bot = telebot.TeleBot(Access_Token, parse_mode='HTML')
print("Bot started! Running...")


wlcm_msg = """, Welcome to the Superdoge Bot! Feel free to ask any questions you have in our <a href='https://t.me/superdogecoin'>Telegram Group</a>.

<b>Wallet Guides:-</b> /guides
<b>See all bot commands:</b> /cmds

Check Bot Uptime: https://bit.ly/sdogebot"""

guide = """<ins>The following guides are available related to SuperDoge Wallet:</ins>

<b>Stuck Block:-</b> https://tiny.one/stuckblock
- If your wallet isn't synchronising, stuck at a particular block, use this guide

<b>Masternode Guide:-</b> https://tiny.one/masternode
- Setup Masternode to receive masternode rewards, minimum required SDOGE: 2000 SDOGE for SILVER or 4000 SDOGE for GOLD Masternode (any one of them will do the work)

<b>Staking Link:-</b> https://tiny.one/staking
- A short guide on how to stake your SDOGE coins right in your wallet to receive staking rewards (7.5 SDOGE frequenty)

<b>Wallet Guide:-</b> https://tiny.one/walletguide
- Beginner's guide to wallet interface

<b>Wallet Encryption Guide:-</b> https://tiny.one/encrypt
- Encrypt your wallet to make your funds safe (Not necessary, but recommended)

<b>Backup & Restore Wallet:-</b> https://tiny.one/backupwallet
- A guide on how-to backup your wallet and restore your wallet using wallet.dat file


In case you need any other guides or if you think any other topic would be useful, do write it in our group:)"""


admins = """⚠️ <b><ins>Admins will never DM first</ins></b>
Keep this in mind, <b>Admins of Superdoge will never DM you first!!</b> Name, bio or profile photo can be faked but not usernames, do cross check the username! The only official admins are: @robertoslo @CoinViking_DK @advik_143

NEVER SHARE OR ACCEPT PHRASES OR KEYS nor send payments to anyone! If anyone asks this from you, forward one of the scammer's messages (not screenshots) to a real admin and immediately report/block the scammer.
"""

backup = ['backup', 'restore', 'back', 'rest', 'bac', 'res']
encrypt = ["encrypt", "enc", "en", "encr", "encry", "encryp", "decrypt", "decr", "dec"]
manual = ["guide", "guides", "tutorial", "tut", "tutor", "gui", "guid", "tuto"]
masternode = ["masternode", "mast", "mas", "maste", "master", "node", "mining", "mine", "min", "ma"]
stake = ["stake", "staking", "sta", "stak", "yield", "yie"]
sync = ["not", "sync", "synchronising", "synchronize", "synchronise", "stuck", "block"]

wallet = backup + encrypt + manual + masternode + stake + sync


@bot.message_handler(content_types=['document'])
def docmsg(message):
    m = message.chat.id
    bot.send_message(m, "I don't process documents but anyways, I'll keep it:) Thanks!")

    
@bot.message_handler(commands=['start', 'home', 'help'])
def startmsg(message):
    m = message.chat.id
    mrkp = ikm()
    mrkp.add(ikb("Website", url="https://superdoge.com"), ikb("About SDOGE", url="https://t.me/superdogecoin/20595"))
    mrkp.add(ikb("Blockchain Explorer", url="https://explorer.superdoge.net"))
    bot.send_message(m, "Heyo " + message.from_user.first_name + wlcm_msg, reply_markup=mrkp, disable_web_page_preview=True)
    

@bot.message_handler(commands=["admin", "admins"])
def adminmsg(msg):
	m = msg.chat.id
	bot.send_message(m, admins)


@bot.message_handler(commands=['guide', 'guides', "manual"])
def guideslist(message):
    m = message.chat.id
    bot.send_message(m, guide, disable_web_page_preview=True)
    

@bot.message_handler(commands=['burn', 'burnaddress', 'swap'])
def swapaddr(message):
    m = message.chat.id
    bot.send_message(m, "🔥 Burn Address: <code>0xa5199B30047D4f5d20C06B4E780aAc3659Bf701c</code>.\n📤 Send the tokens to this address and send the screenshot of your transaction, your BNB address and your SDOGE coin address to swap@superdoge.com")


@bot.message_handler(commands=['info', 'dev'])
def whosdadev(message):
	m = message.chat.id
	msg = """🤖 Bot I made for <a href='https://t.me/superdogecoin'>SuperDoge </a>Group.
Dev: @advik_143"""
	bot.send_message(m, msg, disable_web_page_preview=True)

    
@bot.message_handler(commands=['cmds', 'commands'])
def cmds(message):
    m = message.chat.id
    bot.send_message(m, """<b>Following available commands:</b>
🏠 /home: Info
📖 /guides: Available Superdoge-Core wallet guides
💰 /balance <code>address</code>: See available SDOGE coins in the given address
📦 /supply: See current circulation supply of SDOGE Coin
🖼 /qr <code>address/text</code>: Generate QR Code for a specific address (BETA)
⌨️ Inline Command for guides: Type @Superdogecoinbot on keyboard!""")

    
@bot.message_handler(commands=['supply'])
def supply(message):
    m = message.chat.id
    circulating = requests.get('https://explorer.superdoge.net/ext/getmoneysupply')
    circulating = circulating.text[:15]
    bot.send_message(m, "⚖️ Current circulation supply of SDOGE: " + circulating)

    
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
        bot.send_message(m, "<b>Incorrect Address format!</b> \nMake sure the address starts with <b>S</b>.\nFor example: <code>/balance ScAfTJwi37dFhsPEzkzn6zxtwqs1yHhoBP</code>")
    
        
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


@bot.inline_handler(lambda query: query.query in backup)
def querytext(query):
    try:
        r = search('1', "Backup & Restore Your Wallet" ,MSG("https://telegra.ph/blanke-07-02"), url="https://telegra.ph/blanke-07-02", description="A guide on how to backup & restore your SUPERDOGE wallet.", thumb_url="https://telegra.ph/file/19b663b45c5bd822780db.jpg")
        
        bot.answer_inline_query(query.id, [r])
    except Exception as e:
        print(e)
	
	
@bot.inline_handler(lambda query: query.query in encrypt)
def encryptwallet(query):
	try:
		Encryption = search("1", "Encrypt your SUPERDOGE Wallet", MSG("https://telegra.ph/How-do-I-encrypt-my-SuperDoge-wallet-06-20"), url="https://telegra.ph/How-do-I-encrypt-my-SuperDoge-wallet-06-20", description="A guide on how to Encrypt your SUPERDOGE Wallet", thumb_url="https://telegra.ph/file/aefef4547205e94cfcc0b.jpg")
		
		bot.answer_inline_query(query.id, [Encryption])
	except Exception as e:
		print(e)


@bot.inline_handler(lambda query: query.query in manual)
def walletguide(query):
	try:
		guides = search("1", "SUPERDOGE Wallet Guide", MSG("https://telegra.ph/SuperDoge-Wallet-GuideManual-06-20"), url="https://telegra.ph/SuperDoge-Wallet-GuideManual-06-20", description="Beginner's Guide/Manual to SUPERDOGE Wallet", thumb_url="https://telegra.ph/file/4b48a1ae0eb1f831e1dfc.jpg")
		
		bot.answer_inline_query(query.id, [guides])
	except Exception as e:
		print(e)
		
		
@bot.inline_handler(lambda query: query.query in masternode)
def node(query):
	try:
		mstrnode = search("1", "Setup Masternode to receive Rewards", MSG("https://telegra.ph/How-to-enablecreate-Superdoge-Masternode-06-19"), url="https://telegra.ph/How-to-enablecreate-Superdoge-Masternode-06-19", description="A guide for how-to enable SUPERDOGE Masternode to receive masternode rewards", thumb_url="https://telegra.ph/file/408fc0c72a4945b6eb192.jpg")
		
		bot.answer_inline_query(query.id, [mstrnode])
	except Exception as e:
		print(e)
		
		
@bot.inline_handler(lambda query: query.query in stake)
def staking(query):
	try:
		stak = search("1", "Stake your SDOGE Coins", MSG("https://telegra.ph/How-do-I-ensure-if-my-wallet-is-staking-the-coins-06-19"), url="https://telegra.ph/How-do-I-ensure-if-my-wallet-is-staking-the-coins-06-19", description="A short manual for staking your coins in your SUPERDOGE-Core Wallet", thumb_url="https://telegra.ph/file/f950bfd5c86e63af5b695.jpg")
		
		bot.answer_inline_query(query.id, [stak])
	except Exception as e:
		print(e)
		
		
@bot.inline_handler(lambda query: query.query in sync)
def synchronise(query):
	try:
		resync = search("1", "Troubleshoot Synchronising Wallet", MSG("https://telegra.ph/My-wallet-is-not-synchronizing-stuck-at-a-particular-block-How-to-fix-it-06-19"), url="https://telegra.ph/My-wallet-is-not-synchronizing-stuck-at-a-particular-block-How-to-fix-it-06-19", description="Follow this guide if you're stuck while syncing your wallet.", thumb_url="https://telegra.ph/file/eb165d9b402e403cba1eb.jpg")
		
		bot.answer_inline_query(query.id, [resync])
	except Exception as e:
		print(e)


@bot.inline_handler(lambda query: query.query not in wallet)
def all(query):
	try:
		bckp = search('1', "Backup & Restore Your Wallet" ,MSG("https://telegra.ph/blanke-07-02"), url="https://telegra.ph/blanke-07-02", description="A guide on how to backup & restore your SUPERDOGE wallet.", thumb_url="https://telegra.ph/file/19b663b45c5bd822780db.jpg")
		
		Encryption = search("2", "Encrypt your SUPERDOGE Wallet", MSG("https://telegra.ph/How-do-I-encrypt-my-SuperDoge-wallet-06-20"), url="https://telegra.ph/How-do-I-encrypt-my-SuperDoge-wallet-06-20", description="A guide on how to Encrypt your SUPERDOGE Wallet", thumb_url="https://telegra.ph/file/aefef4547205e94cfcc0b.jpg")
		
		manual = search("3", "SUPERDOGE Wallet Guide", MSG("https://telegra.ph/SuperDoge-Wallet-GuideManual-06-20"), url="https://telegra.ph/SuperDoge-Wallet-GuideManual-06-20", description="Beginner's Guide/Manual to SUPERDOGE Wallet", thumb_url="https://telegra.ph/file/4b48a1ae0eb1f831e1dfc.jpg")
		
		mstrnode = search("4", "Setup Masternode to receive Rewards", MSG("https://telegra.ph/How-to-enablecreate-Superdoge-Masternode-06-19"), url="https://telegra.ph/How-to-enablecreate-Superdoge-Masternode-06-19", description="A guide for how-to enable SUPERDOGE Masternode to receive masternode rewards", thumb_url="https://telegra.ph/file/408fc0c72a4945b6eb192.jpg")
		
		stak = search("5", "Stake your SDOGE Coins", MSG("https://telegra.ph/How-do-I-ensure-if-my-wallet-is-staking-the-coins-06-19"), url="https://telegra.ph/How-do-I-ensure-if-my-wallet-is-staking-the-coins-06-19", description="A short manual for staking your coins in your SUPERDOGE-Core Wallet", thumb_url="https://telegra.ph/file/f950bfd5c86e63af5b695.jpg")
		
		resync = search("6", "Troubleshoot Synchronising Wallet", MSG("https://telegra.ph/My-wallet-is-not-synchronizing-stuck-at-a-particular-block-How-to-fix-it-06-19"), url="https://telegra.ph/My-wallet-is-not-synchronizing-stuck-at-a-particular-block-How-to-fix-it-06-19", description="Follow this guide if you're stuck while syncing your wallet.", thumb_url="https://telegra.ph/file/eb165d9b402e403cba1eb.jpg")
		
		bot.answer_inline_query(query.id, [bckp, Encryption, mstrnode, resync, manual, stak])
	except Exception as e:
		print(e)


while True:
    try:
        telebot.apihelper.SESSION_TIME_TO_LIVE = 1600
        bot.polling()
    except:
        sleep(1)
