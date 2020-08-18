#!/usr/bin/env python3

from azure.storage import table
import sys, getopt
from os.path import join, dirname
from os import getenv
from dotenv import load_dotenv

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)


ACCOUNT_NAME = getenv('LOG_ACCOUNT_NAME')
ACCOUNT_KEY = getenv('LOG_ACCOUN_KEY')

def show_help():
    print('{0} -l [inps|ade] -f <fiscal code>'.format(sys.argv[0]))

def main(argv):

    fiscal_code = log_table =None
    try:
        opts, args = getopt.getopt(argv,"l:f:",["l=","f="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    if len(opts) == 0:
        show_help()
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            show_help()
            sys.exit()
        elif opt in ("-f", "--fiscalcode"):
            fiscal_code = arg
        elif opt in ("-l", "--log") and arg in ('inps', 'ade'):
            log_table = arg
        else:
            show_help()
            sys.exit(2)

    if not (log_table and fiscal_code):
        show_help()
        sys.exit(0)

    table_service = table.TableService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)

    filter = "PartitionKey eq '{0}'".format(fiscal_code.upper())

    entries = table_service.query_entities('{0}logs'.format(log_table), filter=filter)

    for e in entries:
        print(e)

if __name__ == "__main__":
    main(sys.argv[1:])
