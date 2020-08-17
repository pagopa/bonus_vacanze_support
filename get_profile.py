# pip install azure.cosmos
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import sys, getopt
from os.path import join, dirname
from os import getenv
from dotenv import load_dotenv

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)

endpoint = getenv('COSMOS_API_ENDPOINT')
key = getenv('COSMOS_API_KEY')

def show_help():
    print('{0} -f <fiscal code> -e <email>'.format(sys.argv[0]))

def main(argv):

    fiscal_code = None
    email = None
    try:
        opts, args = getopt.getopt(argv,"f:e:",["f=","e="])
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
        elif opt in ("-e", "--email"):
            email = arg

    client = CosmosClient(endpoint, key)

    # database
    database_name = 'db'
    database = client.get_database_client(database_name)

    # Container
    container_name = 'profiles'
    container = database.get_container_client(container_name)

    if fiscal_code:
        query = "SELECT * FROM c WHERE c.fiscalCode = \"{0}\"".format(fiscal_code)
    elif email:
        query = "SELECT * FROM c WHERE c.email = \"{0}\"".format(email)


    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

    print('Query returned {0} items. Operation consumed {1} request units'.format(len(items), request_charge))

    for i in items:
        print(i)
        print("")

if __name__ == "__main__":
    main(sys.argv[1:])
