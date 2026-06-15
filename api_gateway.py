import logging
import json
import requests # The enterprise standard for handling HHP web traffic
# 1. System Observability Config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("api_gateway.log"),
        logging.StreamHandler()
    ]
)

def fetch_remote_invoices(target_url):
    """
    Connects to an external REST API, handles network exceptions,
    and returns parsed JSON data streams safely.
    """
    logging.info(f"Initiating connection profile to remote cluster: {target_url}")

    try:
        # Perform the live HTTP GET reuest with a 5 second network timeout window
        response = requests.get(target_url, timeout=(5))

        # Defensive check:If the server returns an error code (e.g. 404 or 500 ),
        response.raise_for_status()

        logging.info(f"Network transaction successful. HTTP Status Code: {response.status_code}")

        # Parse the raw text response stream directly into a clean python list/dictionary
        data_stream = response.json()
        return data_stream
    
    except requests.exceptions.Timeout:
        logging.error("Transaction aborted: Network connection timeout threshold breached")
        raise
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"Ingrees Stream Failure: Remote server responded with bad status. Reason: {http_err}")
        raise
    except Exception as general_error:
        logging.error(f"Fatal System Intercept: Unexpected network later anomoly. Details: {general_error}")
        raise

if __name__ == "__main__":
    # Live sandbox testing URL simulating an external system endpoint
    ENDPOINT = "http://jsonplaceholder.typicode.com/users"

    print("Booting API Ingress Gateway Client")
    try:
        live_data = fetch_remote_invoices(ENDPOINT)
        #Sample the first record returned from the web to cerify schema alignment
        if live_data:
            print("\n Sample Live Data Stream Recieved from remote server")
            print(json.dumps(live_data[0], indent=4))

    except Exception:
        print("System execution has halted due to unhandled injestion errors. Check log history")