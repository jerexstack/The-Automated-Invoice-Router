import logging
import json
import requests # The enterprise standard for handling HTTP web traffic

# 1. System Observability Config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("api_gateway.log"),
        logging.StreamHandler()
    ]
)

def transmit_invoice_to_pipeline(target_url, invoice_payload):
    """
    Connects to an external REST API, handles network exceptions,
    and returns parsed JSON data streams safely.
    """
    logging.info(f"Initiating connection profile to remote cluster: {target_url}")

    try:
        # === NEW CODE: Crafting the security credential header envelope ===
        custom_headers = {
            "X-API-Key": "ZapierDevOpsSecretToken2026"
        }
        
        # Perform the live HTTP POST request with a 5 second network timeout window
        # We explicitly pass the headers dictionary parameter here!
        response = requests.post(
            target_url, 
            json=invoice_payload, 
            headers=custom_headers, 
            timeout=5
        )
       
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
    ENDPOINT = "http://127.0.0.1:8000/api/v1/invoice"

    # NEW CODE: Crafting a real invoice payload to send
    mock_invoice = {
        "invoice_id": "INV-2026-X99",
        "client": "Zapier_Remote_Enterprise",
        "billing_amount": 4500.80
    }

    print("Booting API Ingress Gateway Client")
    try:
        # NEW CODE: Execute the transfer by passing the target and the data
        server_ack = transmit_invoice_to_pipeline(ENDPOINT, mock_invoice)
        #Sample the first record returned from the web to cerify schema alignment
        
        print("\n=== Live Data Feedback from api Server ===")
        print(json.dumps(server_ack, indent=4))

    except Exception:
        print("System execution has halted due to unhandled injestion errors. Check log history")
        