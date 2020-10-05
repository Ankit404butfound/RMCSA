from telegram.ext import Updater, CommandHandler, MessageHandler,InlineQueryHandler, Filters,CallbackContext
from telegram import Update, Bot
from telegram.utils.helpers import mention_markdown
import random
import time
import requests
import os

king_score = 1000
mantri_score = 800
sipahi_score = 500
aam_score = 100


group_lst = []
GROUP = ""
username_lst = []
chatid_lst = []
name_lst = []
whose_chance = 0
used_word_lst = []
user_num = 0
round_com = 1
user_lst = []
game_started = False
start_time = 0
end_time = 0
user_point_dic = {}
id_user_dic = {}
user_role_dic = {}
role_user_dic = {}
username_id_dic = {}
id_username_dic = {}

chor = 0
king = 0
TOKEN = os.environ.get("TOKEN")
PORT = int(os.environ.get('PORT', 5000))
#PORT = int(os.environ.get('PORT', 5000))
updater = Updater(TOKEN)

def cancel(bot,update):
    global rounds,group_lst,get_chor,GROUP,username_lst,chatid_lst,name_lst,whose_chance,used_word_lst,user_num,round_com,user_lst,game_started,start_time,end_time,user_point_dic,id_user_dic,user_role_dic,username_id_dic,id_username_dic,chor,king
    update.message.reply_text("Game CANCELED!!!")
    
    group_lst = []
    GROUP = update.message.chat_id
    username_lst = []
    chatid_lst = []
    name_lst = []
    whose_chance = 0
    used_word_lst = []
    user_num = 0
    round_com = 1
    user_lst = []
    game_started = False
    start_time = 0
    end_time = 0
    user_point_dic = {}
    id_user_dic = {}
    user_role_dic = {}
    username_id_dic = {}
    id_username_dic = {}
    chor = 0
    king = 0
    get_chor = False

def join(bot,update):
    username = update.message.from_user.username
    name = update.message.from_user.first_name
    chat_id = update.message.from_user.id
    print(username,name,chat_id,end="\n")
    try:
        if chat_id not in chatid_lst:
            user_point_dic[chat_id] = 0
            id_user_dic[chat_id] = name
            username_id_dic[username] = chat_id
            id_username_dic[chat_id] = username
            name_lst.append(name)
            chatid_lst.append(chat_id)
            user_role_dic[chat_id] = "None"
            username_lst.append(username)
            user_point_dic[chat_id] = 0
            bot.sendMessage(GROUP,text=f"{mention_markdown(chat_id,name)} joined the game, there are currently {len(chatid_lst)} players.",parse_mode="Markdown")
            bot.sendMessage(chat_id,"You have successfully joined the game")

        elif len(username_lst) >= 10:
            update.message.reply_text("Sorry, game full, wait for next game \U0001F605.")

        elif chat_id in chatid_lst:
            update.message.reply_text("You have already joined the game")

        else:
            update.message.reply_text("Game has started \U0001F605")

    except Exception as e:
        print(e)
        bot.sendMessage(GROUP,f"{mention_markdown(chat_id,name)}, I can't message you, press 'start' in our private chat.",parse_mode="Markdown")


def whoischor(bot,update):
    global round_com, chor, solder, user_role_lst
    if get_chor:
        username = update.message.chat.username
        chat_id = update.message.chat_id
        #alluser = get_userdata().split("\n")
        
        if int(solder) == int(update.message.chat_id):
            message = update.message.text
            if "/" in message:
                message = message.replace("/","").strip()
                message = username_id_dic[message]
                bot.send_message(GROUP,f"{mention_markdown(solder,id_user_dic[solder])} selected {mention_markdown(message,id_user_dic[message])} as CHOR(Thief)",parse_mode="Markdown")
                if int(message) == int(chor):
                    bot.send_message(GROUP, f"{mention_markdown(solder,id_user_dic[solder])} guessed correctly, you earn 500 points.",parse_mode="Markdown")
                    score = user_point_dic[solder]
                    user_point_dic[solder] = score+sipahi_score

    ##                for data in alldata_lst:
    ##                    if chor in data:
    ##                        chor_score = int(data.split()[2])
    ##                        #alldata = alldata.replace(data,f"{data.split()[0]} {chor} 0")
    ##                        updatetxt(data,f"{data.split()[0]} {data.split()[1]} 0")

    ##                for data in alldata_lst:
    ##                    if solder in data:
    ##                        solder_score = int(data.split()[2])
    ##                        updatetxt(data,f"{data.split()[0]} {data.split()[1]} {solder_score+5}")


                else:
                    bot.send_message(GROUP, f"{mention_markdown(solder,id_user_dic[solder])} guess is wrong, {mention_markdown(chor,id_user_dic[chor])} who is CHOR(Thief) gets 500 points and {mention_markdown(message,id_user_dic[message])} who was wrongly blamed to be CHOR(Thief) gets 300 bonus points.",parse_mode="Markdown")
                    score = user_point_dic[solder]
                    user_point_dic[solder] = score-500
                    score = user_point_dic[message]
                    user_point_dic[message] = score+300

                for id in chatid_lst:
                    role = user_role_dic[id]
                    if role == "AAM AADMI(Civilian)":
                        score = user_point_dic[id]
                        user_point_dic[id] = score+aam_score
                    if role == "RAJA(king)":
                        score = user_point_dic[id]
                        user_point_dic[id] = score+king_score
                    if role == "MANTRI(Minister)":
                        score = user_point_dic[id]
                        user_point_dic[id] = score+mantri_score


                data_string = ""
                for i in range(len(chatid_lst)):
                    user_id = chatid_lst[i]
                    name = name_lst[i]
                    score = user_point_dic[user_id]
                    data_string = data_string+"\n"+mention_markdown(user_id,name)+" : "+str(score)
                bot.send_message(GROUP,f"Final score is as followed{data_string}",parse_mode="Markdown")
                time.sleep(5)
                round_com += 1
                allot_role(bot=bot,update=update)


def allot_role(bot=None,update=None):
    global rounds,group_lst,get_chor,GROUP,username_lst,chatid_lst,name_lst,whose_chance,used_word_lst,user_num,round_com,user_lst,game_started,start_time,end_time,user_point_dic,id_user_dic,user_role_dic,username_id_dic,id_username_dic,chor,king
    local_user_lst = []
    #user_role_lst = []
    if round_com < rounds:
        role_lst = ["RAJA(king)","SIPAHI(Soldier)","CHOR(Thief)","MANTRI(Minister)","AAM AADMI(Civilian)","AAM AADMI(Civilian)","AAM AADMI(Civilian)","AAM AADMI(Civilian)","AAM AADMI(Civilian)","AAM AADMI(Civilian)"]
        for cid in chatid_lst:
            local_user_lst.append(cid)
            
        print(user_lst)
        solder = ""
        #userdata = get_userdata().split("\n")
        for i in range(len(local_user_lst)):

            if local_user_lst != []:
                userid = random.choice(local_user_lst)
                local_user_lst.remove(userid)
                user_role_dic[userid] = role_lst[i]
                print("appended")
                role = user_role_dic[userid]
                bot.send_message(userid,f"Your role is {role}.")
                if role == "CHOR(Thief)":
                    chor = userid
                    print(chor)
                if role == "RAJA(king)":
                    king = userid
                    print(king)
                if role == "SIPAHI(Soldier)":
                    solder = userid
                        
                    
        bot.send_message(GROUP,f"RAJA(king) is {mention_markdown(king,id_user_dic[king])}\nSIPAHI(Soldier) is {mention_markdown(solder,id_user_dic[solder])}\n{mention_markdown(solder,id_user_dic[solder])} please discuss with others and select whom do you think is CHOR(Thief) in our private chat.",parse_mode="Markdown")
   
        suspect_str = ""
        print(solder,king)
        sus_lst = []
        for users in username_lst:
            sus_lst.append(users)
        sus_lst.remove(id_username_dic[solder])
        sus_lst.remove(id_username_dic[king])
        print(sus_lst)
        for users in sus_lst:
            suspect_str = suspect_str + "/" + users + "\n"
        bot.send_message(solder,"Who do you think is CHOR(Thief)\n"+  suspect_str)
        get_chor = True
        
    else:
        bot.send_message(GROUP, "GAME FINISHED!!!")
        group_lst = []
        GROUP = update.message.chat_id
        username_lst = []
        chatid_lst = []
        name_lst = []
        whose_chance = 0
        used_word_lst = []
        user_num = 0
        round_com = 1
        user_lst = []
        game_started = False
        start_time = 0
        end_time = 0
        user_point_dic = {}
        id_user_dic = {}
        user_role_dic = {}
        username_id_dic = {}
        id_username_dic = {}
        chor = 0
        king = 0
        get_chor = False

def startRMCSA(bot,update):
    global game_started
##    try:
    if len(chatid_lst) >= 2:
    
        update.message.reply_text(f"Starting game with {len(chatid_lst)} players.")
        allot_role(bot=bot,update=update)
        game_started = True

    else:
        update.message.reply_text(f"Game must be running and have at least 4 players")
        
##    except Exception as e:
##        update.message.reply_text(f"{e}")
##        pass

def newRMCSA(bot,update):
    global rounds,group_lst,get_chor,GROUP,username_lst,chatid_lst,name_lst,whose_chance,used_word_lst,user_num,round_com,user_lst,game_started,start_time,end_time,user_point_dic,id_user_dic,user_role_dic,username_id_dic,id_username_dic,chor,king
    message = update.message.text
    message = message.replace("/new_game","").strip()
    if not game_started:
        
        try:
            rounds = int(message)

        except:
            rounds = 5
            
        group_lst = []
        GROUP = update.message.chat_id
        username_lst = []
        chatid_lst = []
        name_lst = []
        whose_chance = 0
        used_word_lst = []
        user_num = 0
        round_com = 1
        user_lst = []
        game_started = False
        start_time = 0
        end_time = 0
        user_point_dic = {}
        id_user_dic = {}
        user_role_dic = {}
        username_id_dic = {}
        id_username_dic = {}
        chor = 0
        king = 0
        get_chor = False
        update.message.reply_text(f"Starting new game with {rounds} rounds.\nType /joinRMCSA to join the game.")
        updater.dispatcher.add_handler(CommandHandler("joinRMCSA",join))
        updater.dispatcher.add_handler(CommandHandler("startRMCSA",startRMCSA))
        updater.dispatcher.add_handler(MessageHandler(Filters.text,whoischor))
        updater.dispatcher.add_handler(CommandHandler("cancelRMCSA",cancel))
        
    else:
        update.message.reply_text(f"A game is already running")


updater.dispatcher.add_handler(CommandHandler("newRMCSA",newRMCSA))
updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
updater.bot.setWebhook('https://rmcsa.herokuapp.com/' + TOKEN)                                 
updater.idle()



