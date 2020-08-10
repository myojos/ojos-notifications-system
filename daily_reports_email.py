import logging
from random import choice
import pandas as pd
import psycopg2
import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape

from settings import DATABASE_CONNECTION_PARAMETERS, REPORT_DATE, MAILGUN_API_KEY


def send_email(to, html):
    return requests.post(
        "https://api.eu.mailgun.net/v3/mg.myojos.tech/messages",
        auth=("api", MAILGUN_API_KEY),
        data={"from": "OJOS <reports@myojos.tech>",
              "to": [to],
              "subject": f"Your daily report - {REPORT_DATE}",
              "html": html})


def main():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    # Jinja2 environment
    logging.info(f"Sending email reports for {REPORT_DATE}")
    logging.info("Reading email template")
    env = Environment(
        loader=FileSystemLoader('./templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    reports_template = env.get_template('report.html')

    # Load daily quote
    with open("quotes.txt", 'r') as f:
        quotes = f.readlines()
    daily_quote = choice(quotes).strip()

    # Get daily events
    logging.info("Getting daily events")
    with psycopg2.connect(**DATABASE_CONNECTION_PARAMETERS) as con:
        daily_events_df = pd.read_sql_query(f"""
        SELECT u.email, e.event_type, e.timestamp, e.video_link
        FROM home_ojosuser u 
        JOIN app_camera a ON u.id = a.user_id 
        JOIN app_event e ON a.id = e.camera_id
        WHERE e.timestamp::date = '{REPORT_DATE}'
        """, con)

    daily_events_df.at[:3, 'email'] = 'harelj6@gmail.com'

    daily_events_df.set_index('email', inplace=True)
    all_users = daily_events_df.index.unique()
    num_users = len(all_users)
    for idx, user_email in enumerate(all_users, 1):
        logging.info(f"Sending email to {user_email}")
        email_content = reports_template.render(user_events=daily_events_df.loc[[user_email], :],
                                                date=REPORT_DATE, quote=daily_quote)
        send_email(user_email, email_content)
        logging.info(f"Success. {idx} / {num_users} ")

    logging.info("Done.")


if __name__ == '__main__':
    main()
