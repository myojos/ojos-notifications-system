import os
from datetime import datetime

from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(verbose=True, dotenv_path=os.path.join(BASE_DIR, '.env'))

REPORT_DATE = (datetime.today() - relativedelta(days=1)).date()

DATABASE_CONNECTION_PARAMETERS = {
    'host': os.getenv('POSTGRES_HOST'),
    'port': '5432',
    'user': os.getenv('POSTGRES_USERNAME'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'database': os.getenv('POSTGRES_DATABASE'),
}

MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')