import os
import requests
from llm_api import process_user_message
import feedparser
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file

DISCORD_URL=os.environ.get('DISCORD_URL')
securityToken=os.environ.get('securityToken')
userUid=os.environ.get('userUid')
orgUid=os.environ.get('orgUid')

# SENDGRID_API_KEY=os.environ.get('SENDGRID_API_KEY')
# FROM=os.environ.get('FROMEMAIL')
# TO=os.environ.get('TOEMAILS')
# SUBJECT='New Job on UpWork'

# def send_out_email(email_body):
#     message = Mail(
#         from_email=FROM,
#         to_emails=TO,
#         subject=SUBJECT,
#         plain_text_content=email_body
#         )
#     try:
#         sg = SendGridAPIClient(SENDGRID_API_KEY)
#         response = sg.send(message)
#         print(response.status_code)
#         print(response.body)
#         print(response.headers)
#     except Exception as e:
#         print("Exception happened in SendGridAPI: ",e)


def send_discord_message(webhook_url, message):
    try:
        data = {"content": message}
        response = requests.post(webhook_url, json=data)
        
        if response.status_code == 204:
            print("Message sent successfully")
        else:
            print(f"Failed to send message, status code: {response.status_code}\n{response.text}")
    except Exception as e:
        print("Exception happened in Discord webhook: ",e)


def fetch_new_jobs(url):
    feed = feedparser.parse(url)
    one_hour_ago = datetime.utcnow() - timedelta(minutes=10)  # UTC time, offset-naive

    for post in feed.entries:
        email_content = ""
        published_date = parsedate_to_datetime(post.published).replace(tzinfo=None)  # Make offset-naive
        if published_date > one_hour_ago:
            print(f"New Job: {post.title}")
            email_content += f"\n\n======================\nNew Job: \n{post.title}\nLink: \n{post.link}"
            llm_input = str(post.title) + str(post.summary) 
            llm_result = process_user_message(llm_input)
            email_content += "\n\nCustomized Message:\n" + llm_result
            send_discord_message(DISCORD_URL, email_content)



if __name__ == "__main__":

    search_query = f"https://www.upwork.com/ab/feed/jobs/rss?contractor_tier=3&location=Canada%2CUnited+Kingdom%2CUnited+States&paging=0%3B10&verified_payment_only=1&proposals=0-4%2C5-9%2C10-14&sort=recency&subcategory2_uid=531770282593251329&api_params=1&q=&securityToken={securityToken}userUid={userUid}orgUid={orgUid}"
    fetch_new_jobs(search_query)

    



