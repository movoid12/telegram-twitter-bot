import os
import tweepy
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()

# Set up Twitter API
auth = tweepy.OAuthHandler(
    os.environ["TWITTER_API_KEY"], os.environ["TWITTER_API_SECRET"])
auth.set_access_token(
    os.environ["TWITTER_ACCESS_TOKEN"], os.environ["TWITTER_ACCESS_SECRET"])
api = tweepy.API(auth)

# Set up Telegram API
updater = Updater(os.environ["TELEGRAM_BOT_TOKEN"])
dispatcher = updater.dispatcher

# Function to get top 5 Twitter trends


def get_top_5_trends(woeid):
    trends = api.trends_place(woeid)[0]["trends"]
    sorted_trends = sorted(
        trends, key=lambda x: x["tweet_volume"], reverse=True)[:5]
    return [t["name"] for t in sorted_trends]

# Function to handle the /trends command


def trends(update: Update, context: CallbackContext):
    woeid = 23424848  # Replace with your desired country's WOEID
    trends = get_top_5_trends(woeid)
    message = "Top 5 Twitter trends:\n\n" + "\n".join(trends)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)


dispatcher.add_handler(CommandHandler("trends", trends))

# Schedule daily trends post


def daily_trends(context: CallbackContext):
    woeid = 23424848  # Replace with your desired country's WOEID
    trends = get_top_5_trends(woeid)
    message = "Daily top 5 Twitter trends:\n\n" + "\n".join(trends)
    context.bot.send_message(
        chat_id=os.environ["TELEGRAM_CHAT_ID"], text=message, parse_mode=ParseMode.HTML)


job_queue = updater.job_queue
job_queue.run_daily(daily_trends, time=datetime.time(hour=13, minute=0))

# Start the bot
updater.start_polling()

updater.idle()
