from telegram.ext import Updater, CommandHandler, MessageHandler,InlineQueryHandler, Filters,CallbackContext
from telegram import Update, Bot
import random
import time
import requests

user_role_lst = []
user_lst = []
game_started = False
GROUP = -402125669#-455705027
get_chor = False
rounds_completed = 0
chor = ""
king = ""

def get_userdata():
    try:
        data = requests.get("http://rajma.pythonanywhere.com/retreve?uname=RMCSA&method=r").text
        return data.strip()
    except:
        return ""

def add_user(bot,update):
    try:
        userdata = get_userdata()
    except:
        userdata = ""
    username = update.message.from_user.username
    chat_id = update.message.from_user.id
    if str(chat_id) not in userdata:
##        file = open("user_data.txt","a")
##        file.write(f"{username} {chat_id} 0\n")
##        file.close()
        requests.get(f"http://rajma.pythonanywhere.com/retreve?uname=RMCSA&method=a&data={username} {chat_id} 0\n")
        update.message.reply_text("You have successfully registered.")

    else:
        update.message.reply_text("You have already registered")



def updatetxt(old,new):
    data = get_userdata()
    data = data.replace(old,new)
    requests.get("http://rajma.pythonanywhere.com/retreve?uname=RMCSA&method=w&data="+data)
##    file = open("user_data.txt","w")
##    file.write(data)
##    file.close()

def whoischor(bot,update):
    global rounds_completed, chor, solder, user_role_lst
    if get_chor:
        username = update.message.chat.username
        if username == solder:
            message = update.message.text
            message = message.replace("/chor @","").strip()
            bot.send_message(GROUP,f"@{solder} selected @{message} as CHOR(Thief)")
            if message == chor:
                bot.send_message(GROUP, f"@{solder} guessed correctly, you earn +5 points.")
                alldata = get_userdata()
                alldata_lst = alldata.split("\n")
                
##                for data in alldata_lst:
##                    if chor in data:
##                        chor_score = int(data.split()[2])
##                        #alldata = alldata.replace(data,f"{data.split()[0]} {chor} 0")
##                        updatetxt(data,f"{data.split()[0]} {data.split()[1]} 0")
                        
                for data in alldata_lst:
                    if solder in data:
                        solder_score = int(data.split()[2])
                        updatetxt(data,f"{data.split()[0]} {data.split()[1]} {solder_score+5}")
                        
                
            else:
                bot.send_message(GROUP, f"@{solder} guess is wrong, @{chor} who is CHOR(Thief) gets +5 points and @{message} who was wrongly blamed to be CHOR(Thief) gets +3 bonus points.")
                alldata = get_userdata()
                alldata_lst = alldata.split("\n")
                
                for data in alldata_lst:
                    if message in data:
                        blame_score = int(data.split()[2])
                        updatetxt(data,f"{data.split()[0]} {data.split()[1]} {blame_score+3}")

                for data in alldata_lst:
                    if chor in data:
                        chor_score = int(data.split()[2])
                        updatetxt(data,f"{data.split()[0]} {data.split()[1]} {5+chor_score}")

        allnewdata = get_userdata().split("\n")
        print(user_role_lst)
        for newdata in allnewdata:
            for user_role in user_role_lst:
                if user_role.split(":")[0] == newdata.split()[0]:
                    if user_role.split(":")[1] != "SIPAHI(Soldier)" or user_role.split(":")[1] != "CHOR(Thief)":
                        if user_role.split(":")[1] == "RAJA(king)":
                            score = int(newdata.split()[2])
                            updatetxt(newdata,f"{newdata.split()[0]} {newdata.split()[1]} {score+5}")
                            
                        if user_role.split(":")[1] == "MANTRI(Minister)":
                            score = int(newdata.split()[2])
                            print("Mantri")
                            updatetxt(newdata,f"{newdata.split()[0]} {newdata.split()[1]} {score+3}")

                        if user_role.split(":")[1] == "AAM AADMI(Civilian)":
                            score = int(newdata.split()[2])
                            updatetxt(newdata,f"{newdata.split()[0]} {newdata.split()[1]} {score+1}")
                            
        allnewdata = get_userdata().split("\n")
        data_string = ""
        for datas in allnewdata:
            if datas.split()[0] in user_lst:
                data_string = data_string+"\n"+"@"+datas.split()[0]+" : "+datas.split()[2]
        bot.send_message(GROUP,f"Final score is as followed{data_string}")
        time.sleep(5)
        rounds_completed += 1
        allot_role(bot=bot,update=update)

def join(bot,update):
    global user_lst
    if len(user_lst) < 10 and not game_started:
        username = update.message.from_user.username
        if username in get_userdata():
            if username not in user_lst:
                userdata = get_userdata()
                userdatalst = userdata.split("\n")
                #print(username)
                for reg_username in userdatalst:
                    #print(reg_username.split()[0])
                    if username == reg_username.split()[0]:
                        #print(username,reg_username.split()[0])
                        user_lst.append(username)
                        bot.send_message(reg_username.split()[1],f"You have successfully joined the game. I will soon tell you your role.")
                        update.message.reply_text(f"You have successfully joined the game.\nTotal player/s = {len(user_lst)}/10")
                        break
                        

            else:
                update.message.reply_text("You seem excited \U0001F61D")
        else:
            update.message.reply_text(f"@{username}, I can't message you, please send a /start in our private chat.")
            
    elif len(user_lst) >= 10:
        update.message.reply_text("Sorry, game full, wait for next game \U0001F605.")

    else:
        update.message.reply_text("Game has started \U0001F605")

def allot_role(bot=None,update=None):
    global count, solder, chor, get_chor, rounds_completed, user_lst, rounds, user_role_lst, game_started
    local_user_lst = []
    user_role_lst = []
    if rounds_completed < rounds:
        role_lst = ["RAJA(king)","SIPAHI(Soldier)","CHOR(Thief)","MANTRI(Minister)","AAM AADMI(Civilian)","AAM AADMI(Civilian)","AAM AADMI(Civilian)","AAM AADMI(Civilian)","AAM AADMI(Civilian)","AAM AADMI(Civilian)"]
        #local_user_lst = user_lst
        for ele in user_lst:
            local_user_lst.append(ele)
        print(user_lst)
        solder = ""
        userdata = get_userdata().split("\n")
        for role in role_lst:
            
            if local_user_lst != []:
                user = random.choice(local_user_lst)
                local_user_lst.remove(user)
                #print(f"{user}:{role}")
                user_role_lst.append(f"{user}:{role}")
                print("appended")
                for reg_user in userdata:
                    if user in reg_user:
                        their_chatid = reg_user.split()[1]
                        bot.send_message(their_chatid,f"Your role is {role}.")
                        if role == "CHOR(Thief)":
                            chor = reg_user.split()[0]
                            print(chor)
                        if role == "RAJA(king)":
                            king = reg_user.split()[0]
                            print(king)
                        break
        #print(user_role_lst)
        for roles in user_role_lst:
            if "SIPAHI(Soldier)" in roles:
                #print(roles)
                solder = roles.split(":")[0]
                bot.send_message(GROUP,f"RAJA(king) is @{king}\nSIPAHI(Soldier) is @{roles.split(':')[0]}\n@{roles.split(':')[0]} please discuss with others and select whom do you think is CHOR(Thief), in our private chat.")
                break
        alluser = get_userdata().split("\n")
        for udata in alluser:
            if solder in udata:
                solder_chatid = udata.split()[1]
                break
    ##    solder_message = user_lst
    ##    solder_message.remove(solder)
        suspect
        bot.send_message(solder_chatid,"Who do you think is CHOR(Thief), reply with '/chor' followed by their username either here or in group.")
        get_chor = True

    else:
        bot.send_message(GROUP,"Game finished")
        
    
    
def newRMCSA(bot,update):
    global game_started, rounds

    to_be_updated = get_userdata()
    requests.get("http://rajma.pythonanywhere.com/retreve?uname=RMCSA&method=w&data=")
    to_be_updated_lst = to_be_updated.split("\n")
    for data in to_be_updated_lst:
        requests.get(f"http://rajma.pythonanywhere.com/retreve?uname=RMCSA&method=a&data={data.split()[0]} {data.split()[1]} 0\n")
    message = update.message.text
    message = message.replace("/new_game","").strip()

    if not game_started:
        
        try:
            rounds = int(message)

        except:
            rounds = 5

        update.message.reply_text(f"Starting game with {rounds} rounds.\nType /join to join the game.")
    else:
        update.message.reply_text(f"A game is already running")
    
    #print(user_lst)
     
def startRMCSA(bot,update):
    global game_started
    try:
        if len(user_lst) >= 4:
        
            update.message.reply_text(f"Starting game with {len(user_lst)} players.")
            allot_role(bot=bot,update=update)
            game_started = True

        else:
            update.message.reply_text(f"Game must have at least 4 players")
        
    except:
        update.message.reply_text(f"No new game, type /new_game for a new game.")

updater = Updater("TOKEN")
dp = updater.dispatcher
dp.add_handler(CommandHandler("join", join))
dp.add_handler(CommandHandler("start", add_user))
dp.add_handler(CommandHandler("new_game", newRMCSA))
dp.add_handler(CommandHandler("start_game", startRMCSA))
dp.add_handler(CommandHandler("chor", whoischor))
updater.start_polling()
updater.idle()
