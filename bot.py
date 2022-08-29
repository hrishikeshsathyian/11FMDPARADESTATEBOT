from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from extras import list
from database import addUser, removeUser, getStrength, displayNR , UserExists, getUser,getState, NRLIST, activateperma , disableperma , todays_date, restartPS, changeValue, NightStrength, getIn
from datetime import datetime, timedelta , date
import os

TOKEN = "5336621545:AAFtcRFQy2TgeRA8mWGAVJOWYj_RuLPm8GA"
PORT = int(os.environ.get("PORT","8443"))
updater = Updater(token="5336621545:AAFtcRFQy2TgeRA8mWGAVJOWYj_RuLPm8GA", use_context = True) #initiates updater object for our chat bot
dispatcher = updater.dispatcher

#variables
total_strength = getStrength()


#displays current parade state WITHOUT resetting it
def show_parade_state():
    text = "PARADE STATE FOR 11FMD " + "ON \n {}".format(todays_date) + "\n"+ "Total Strength: {}".format(getStrength())+ "\n"+ "Current Strength: {}".format(getIn("IN")) + "\n"+ "\n"+ "IN: {}".format(getState("IN"))+ "\n"+"\n"+ "LEAVE: {}".format(getState("LEAVE"))+ "\n"+ "\n"+"OFF: {}".format(getState("OFF"))+ "\n"+"\n"+ "DUTY: {}".format(getState("DUTY"))+ "\n"+"\n"+ "MA: {}".format(getState("MA"))+ "\n"+"\n"+ "MC: {}".format(getState("MC"))+ "\n"+"\n"+ "RSO: {}".format(getState("RSO"))+ "\n"+"\n"+ "RSI: {}".format(getState("RSI"))  + "\n" +"\n"+ "Others: {}".format(getState("OTHERS")) + "\n" +"\n"+ "AO: {}".format(getState("AO")) + "\n" +"\n"+ "OS: {}".format(getState("OS")) + "\n" +"\n"+ "CSE: {}".format(getState("CSE")) + "\n" +"\n"+ "Stay In: {}".format(getState("STAY-IN")) + "\n" + "\n" + "NULL: {}".format(getState("NULL"))
    return text

#displays full list of NR users that are registered as part of the bot system
def printNR(update:Update,context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,text="The total strength of the depot is {}".format(getStrength())+ "\n" +
                                                                    displayNR())
printNR_handler = CommandHandler("printNR", printNR)
dispatcher.add_handler(printNR_handler)

def help(update:Update,context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,text = "Welcome 11FMD! This is the help page that contains all the help you need to use the telegram bot. Below are all the commands one needs to know to fully use the bot!. To note, (STATE) would refer to the standard parade states such as in,off,leave,ao,cse, etc. \n /start --> generally used by Depot Clerk to restart parade state for the day \n /printPS ---> shows the parade state for the day \n /printNR ---> shows the full list of registered users \n /add_user (RANK) (NAME) (PLATOON) --> registers a user to the nominal roll \n /remove_user (RANK) (NAME) --> removes user from the nominal roll \n /perma (RANK) (NAME) (STATUS) (EXTRA INFO) --> sets you to a status permenantly if you are away for a long term e.g /perma ME3 ISAAC AO XWB22 \n /offperma (RANK) (NAME) --> takes away you're perma status and brings you back to having to update your parade state daily \n SETTING FOR YOURSELF --> /(state) (any additional info if required) \n SETTING FOR OTHERS --> /(state) (RANK) (NAME) (any additional info if required) \n")
help_handler = CommandHandler("help", help)
dispatcher.add_handler(help_handler)


#handler to add new user to the nominal_roll for the platoon
def add_user(update:Update, context: CallbackContext):
    user = update.message.from_user # gets data of user who sends the message
    user_id = user["id"] #gets tele id of user who sends the message
    if UserExists(user_id):
        context.bot.send_message(chat_id=update.effective_chat.id,text="oh no! you already have a user registered under this telegram ID")
    else:
        platoon = "".join(context.args[-1]).upper() # selects last item from list of args to be the platoon
        new_user = " ".join(context.args[:-1]).upper() #selects the rest as the name of the user
        addUser(user_id,new_user,platoon)
        context.bot.send_message(chat_id=update.effective_chat.id,text= new_user + " from {} has been added to the nominal roll".format(platoon))
add_user_handler = CommandHandler("add_user", add_user)
dispatcher.add_handler(add_user_handler)


#allows user to remove others from the NR in the event of ORD or accident

def remove_user(update:Update, context: CallbackContext):
    if len(context.args) < 1 :
        context.bot.send_message(chat_id=update.effective_chat.id,text="Please indicate the name of the person to remove")
    else:
        if UserExists(" ".join(context.args).upper()):
            user = " ".join(context.args).upper()
            removeUser(user)
            print(parade_state)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                    text=user + " has been removed from the nominal roll.Total strength of the platoon is now " + getStrength())
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                        text="user not recognized, please only put his rank and name as registered")
remove_user_handler = CommandHandler("remove_user", remove_user)
dispatcher.add_handler(remove_user_handler)

#cues the bot to start the parade state
def start_parade_state(update:Update, context:CallbackContext):
    restartPS()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text= "11FMD Parade State started, please input your AM status by 0800H and PM status, if any, by 1200H")
start_parade_state_handler = CommandHandler("start", start_parade_state)
dispatcher.add_handler(start_parade_state_handler)


def print_parade_state(update:Update, context:CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=show_parade_state())
print_parade_state_handler = CommandHandler("printPS", print_parade_state)
dispatcher.add_handler(print_parade_state_handler)


def perma(update:Update, context:CallbackContext):
    user_to_be_changed = [name for name in NRLIST() if (name in " ".join(context.args).upper())][0]
    user_to_be_changed_modified = getUser(user_to_be_changed)
    extra_data = [x for x in [k.upper() for k in context.args] if x not in user_to_be_changed.split()]
    activateperma(user_to_be_changed,extra_data)
perma_handler = CommandHandler("perma", perma)
dispatcher.add_handler(perma_handler)

def perma_off(update:Update, context:CallbackContext):
    user = " ".join(context.args).upper()
    disableperma(user)

perma_off_handler = CommandHandler("offperma", perma_off)
dispatcher.add_handler(perma_off_handler)

#allows user to change himself/someone else to IN

def set_in(update:Update, context:CallbackContext):
    if any(key in " ".join(context.args).upper() for key in NRLIST()):
        user_to_be_changed = [name for name in NRLIST() if (name in " ".join(context.args).upper())][0]
        extra_data = [x for x in [k.upper() for k in context.args] if x not in user_to_be_changed.split()]
        value = "IN {}".format(" ".join(extra_data).upper())
        changeValue(value,user_to_be_changed)

    else:
        user = update.message.from_user
        user_id = user["id"] #finds the matching user with the ID that sent the message
        value = "IN {}".format(" ".join(context.args).upper())
        changeValue(value,user_id)

set_in_handler = CommandHandler("in", set_in)
dispatcher.add_handler(set_in_handler)

def set_off(update:Update, context:CallbackContext):
    if any(key in " ".join(context.args).upper() for key in NRLIST()):
        user_to_be_changed = [name for name in NRLIST() if (name in " ".join(context.args).upper())][0]
        extra_data = [x for x in [k.upper() for k in context.args] if x not in user_to_be_changed.split()]
        value = "OFF {}".format(" ".join(extra_data).upper())
        changeValue(value,user_to_be_changed)

    else:
        user = update.message.from_user
        user_id = user["id"] #finds the matching user with the ID that sent the message
        value = "OFF {}".format(" ".join(context.args).upper())
        changeValue(value,user_id)
set_off_handler = CommandHandler("off", set_off)
dispatcher.add_handler(set_off_handler)

def set_leave(update:Update, context:CallbackContext):
    if any(key in " ".join(context.args).upper() for key in NRLIST()):
        user_to_be_changed = [name for name in NRLIST() if (name in " ".join(context.args).upper())][0]
        extra_data = [x for x in [k.upper() for k in context.args] if x not in user_to_be_changed.split()]
        value = "LEAVE {}".format(" ".join(extra_data).upper())
        changeValue(value,user_to_be_changed)

    else:
        user = update.message.from_user
        user_id = user["id"] #finds the matching user with the ID that sent the message
        value = "LEAVE {}".format(" ".join(context.args).upper())
        changeValue(value,user_id)

set_leave_handler = CommandHandler("leave", set_leave)
dispatcher.add_handler(set_leave_handler)

def set_duty(update:Update, context:CallbackContext):

    if any(key in " ".join(context.args).upper() for key in NRLIST()):
        user_to_be_changed = [name for name in NRLIST() if (name in " ".join(context.args).upper())][0]
        extra_data = [x for x in [k.upper() for k in context.args] if x not in user_to_be_changed.split()]
        value = "DUTY {}".format(" ".join(extra_data).upper())
        changeValue(value,user_to_be_changed)

    else:
        user = update.message.from_user
        user_id = user["id"] #finds the matching user with the ID that sent the message
        value = "DUTY {}".format(" ".join(context.args).upper())
        changeValue(value,user_id)


set_duty_handler = CommandHandler("duty", set_duty)
dispatcher.add_handler(set_duty_handler)

def set_MA(update:Update, context:CallbackContext):

    if any(key in " ".join(context.args).upper() for key in NRLIST()):
        user_to_be_changed = [name for name in NRLIST() if (name in " ".join(context.args).upper())][0]
        extra_data = [x for x in [k.upper() for k in context.args] if x not in user_to_be_changed.split()]
        value = "MA {}".format(" ".join(extra_data).upper())
        changeValue(value,user_to_be_changed)

    else:
        user = update.message.from_user
        user_id = user["id"] #finds the matching user with the ID that sent the message
        value = "MA {}".format(" ".join(context.args).upper())
        changeValue(value,user_id)


set_MA_handler = CommandHandler("MA", set_MA)
dispatcher.add_handler(set_MA_handler)

def set_MC(update:Update, context:CallbackContext):

    if any(key in " ".join(context.args).upper() for key in NRLIST()):
        user_to_be_changed = [name for name in NRLIST() if (name in " ".join(context.args).upper())][0]
        extra_data = [x for x in [k.upper() for k in context.args] if x not in user_to_be_changed.split()]
        value = "MC {}".format(" ".join(extra_data).upper())
        changeValue(value,user_to_be_changed)

    else:
        user = update.message.from_user
        user_id = user["id"] #finds the matching user with the ID that sent the message
        value = "MC {}".format(" ".join(context.args).upper())
        changeValue(value,user_id)


set_MC_handler = CommandHandler("MC", set_MC)
dispatcher.add_handler(set_MC_handler)

def set_RSO(update:Update, context:CallbackContext):

    if any(key in " ".join(context.args).upper() for key in NRLIST()):
        user_to_be_changed = [name for name in NRLIST() if (name in " ".join(context.args).upper())][0]
        extra_data = [x for x in [k.upper() for k in context.args] if x not in user_to_be_changed.split()]
        value = "RSO {}".format(" ".join(extra_data).upper())
        changeValue(value,user_to_be_changed)

    else:
        user = update.message.from_user
        user_id = user["id"] #finds the matching user with the ID that sent the message
        value = "RSO {}".format(" ".join(context.args).upper())
        changeValue(value,user_id)


set_RSO_handler = CommandHandler("RSO", set_RSO)
dispatcher.add_handler(set_RSO_handler)

def set_RSI(update:Update, context:CallbackContext):

    if any(key in " ".join(context.args).upper() for key in NRLIST()):
        user_to_be_changed = [name for name in NRLIST() if (name in " ".join(context.args).upper())][0]
        extra_data = [x for x in [k.upper() for k in context.args] if x not in user_to_be_changed.split()]
        value = "RSI {}".format(" ".join(extra_data).upper())
        changeValue(value,user_to_be_changed)

    else:
        user = update.message.from_user
        user_id = user["id"] #finds the matching user with the ID that sent the message
        value = "RSI {}".format(" ".join(context.args).upper())
        changeValue(value,user_id)


set_RSI_handler = CommandHandler("RSI", set_RSI)
dispatcher.add_handler(set_RSI_handler)


def set_OS(update:Update, context:CallbackContext):

    if any(key in " ".join(context.args).upper() for key in NRLIST()):
        user_to_be_changed = [name for name in NRLIST() if (name in " ".join(context.args).upper())][0]
        extra_data = [x for x in [k.upper() for k in context.args] if x not in user_to_be_changed.split()]
        value = "OS {}".format(" ".join(extra_data).upper())
        changeValue(value,user_to_be_changed)

    else:
        user = update.message.from_user
        user_id = user["id"] #finds the matching user with the ID that sent the message
        value = "OS {}".format(" ".join(context.args).upper())
        changeValue(value,user_id)


set_OS_handler = CommandHandler("OS", set_OS)
dispatcher.add_handler(set_OS_handler)

#
def set_CSE(update:Update, context:CallbackContext):

    if any(key in " ".join(context.args).upper() for key in NRLIST()):
        user_to_be_changed = [name for name in NRLIST() if (name in " ".join(context.args).upper())][0]
        extra_data = [x for x in [k.upper() for k in context.args] if x not in user_to_be_changed.split()]
        value = "CSE {}".format(" ".join(extra_data).upper())
        changeValue(value,user_to_be_changed)

    else:
        user = update.message.from_user
        user_id = user["id"] #finds the matching user with the ID that sent the message
        value = "CSE {}".format(" ".join(context.args).upper())
        changeValue(value,user_id)


set_CSE_handler = CommandHandler("CSE", set_CSE)
dispatcher.add_handler(set_CSE_handler)


def set_AO(update:Update, context:CallbackContext):

    if any(key in " ".join(context.args).upper() for key in NRLIST()):
        user_to_be_changed = [name for name in NRLIST() if (name in " ".join(context.args).upper())][0]
        extra_data = [x for x in [k.upper() for k in context.args] if x not in user_to_be_changed.split()]
        value = "AO {}".format(" ".join(extra_data).upper())
        changeValue(value,user_to_be_changed)

    else:
        user = update.message.from_user
        user_id = user["id"] #finds the matching user with the ID that sent the message
        value = "AO {}".format(" ".join(context.args).upper())
        changeValue(value,user_id)


set_AO_handler = CommandHandler("AO", set_AO)
dispatcher.add_handler(set_AO_handler)

def set_others(update:Update, context:CallbackContext):

    if any(key in " ".join(context.args).upper() for key in NRLIST()):
        user_to_be_changed = [name for name in NRLIST() if (name in " ".join(context.args).upper())][0]
        extra_data = [x for x in [k.upper() for k in context.args] if x not in user_to_be_changed.split()]
        value = "OTHERS {}".format(" ".join(extra_data).upper())
        changeValue(value,user_to_be_changed)

    else:
        user = update.message.from_user
        user_id = user["id"] #finds the matching user with the ID that sent the message
        value = "OTHERS {}".format(" ".join(context.args).upper())
        changeValue(value,user_id)


set_others_handler = CommandHandler("others", set_others)
dispatcher.add_handler(set_others_handler)

def set_stay_in(update:Update, context:CallbackContext):

    if any(key in " ".join(context.args).upper() for key in NRLIST()):
        user_to_be_changed = [name for name in NRLIST() if (name in " ".join(context.args).upper())][0]
        extra_data = [x for x in [k.upper() for k in context.args] if x not in user_to_be_changed.split()]
        value = "STAY-IN {}".format(" ".join(extra_data).upper())
        changeValue(value,user_to_be_changed)

    else:
        user = update.message.from_user
        user_id = user["id"] #finds the matching user with the ID that sent the message
        value = "STAY-IN {}".format(" ".join(context.args).upper())
        changeValue(value,user_id)


set_stay_in_handler = CommandHandler("stayin", set_stay_in)
dispatcher.add_handler(set_stay_in_handler)

def nightstrength(update:Update, context:CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                                text=NightStrength())
nightstrength_handler = CommandHandler("nightstrength", nightstrength)
dispatcher.add_handler(nightstrength_handler)


#starts the bot
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN,
                      webhook_url="https://desolate-temple-22646.herokuapp.com/" + TOKEN)
updater.idle()
