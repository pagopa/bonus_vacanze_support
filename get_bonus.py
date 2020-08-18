#!/usr/bin/env python3

from azure.cosmos import exceptions, CosmosClient, PartitionKey
import sys, getopt
from os.path import join, dirname
from os import getenv
from dotenv import load_dotenv
import json


# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)

endpoint = getenv('COSMOS_BONUS_ENDPOINT')
key = getenv('COSMOS_BONUS_KEY')

def show_help():
    print('{0} -f <fiscal code>'.format(sys.argv[0]))

def main(argv):

    fiscal_code = None

    try:
        opts, args = getopt.getopt(argv,"f:",["f="])
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

    client = CosmosClient(endpoint, key)

    # database
    database_name = 'db'
    database = client.get_database_client(database_name)

    # Container
    container_name = 'bonus-activations'
    container = database.get_container_client(container_name)

    # Query these items using the SQL query syntax.
    # Specifying the partition key value in the query allows Cosmos DB to retrieve data only from the relevant partitions, which improves performance.
    query = "SELECT * FROM c WHERE c.applicantFiscalCode = \"{0}\"".format(fiscal_code.upper())

    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

    print('Query returned {0} items. Operation consumed {1} request units'.format(len(items), request_charge))

    for i in items:
        print(json.dumps(i,  sort_keys=True, indent=2))

if __name__ == "__main__":
    main(sys.argv[1:])
