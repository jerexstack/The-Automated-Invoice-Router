import logging
import json
from flask import Flask, request, jsonify
# Import your actual enterprise validation logic from your previous milestone!
import invoice_engine

# 1. System Observility Setup 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("production_pipeline.log"),
        logging.StreamHandler()
    ]
)

# 2. Initialize the Flask Web Server Engine
app = Flask(__name__)

# 3. Define an Explict HTTP Network Route
@app.route('/api/v1/invoice', methods=["POST"])
def inbound_invoice_receiver():
    """
    Listens for incoming HTTP POST network payloads, intercepts JSON data streams,
    and passes them directly into the core invoice_engine validation gates.
    """

    logging.info("Network Layer Event: Inbound HTTP POST request detected.")
    # Extract the raw JSON data stream sent over the network 
    payload = request.get_json()

    # Defensive check: Verify the client actually sent valid JSON text data
    if not payload:
        logging.warning("Ingrees Blocked: Emoty or invalid payload framework recieved.")
        return jsonify({"status": "error", "message": "Malformed SON payload"}), 400
    
    try:
        #Extract fields exactly like your automation_simulator did
        raw_ref = payload.get("client")
        deposit = payload.get("billing_amount")
        invoice_id = payload.get("invoice_id")

        logging.info(f"Processing Remote Transaction - ID: {invoice_id}")

        # Execute your existing production code logic!
        clean_ref, routing_target = invoice_engine.process_transaction(raw_ref, deposit)

        #Execute your existingproduction code logic!
        clean_ref, routing_target = invoice_engine.process_transaction(raw_ref, deposit)

        # ===== START OF A NEW DATA BASE CODE ====
        import os
        db_file = "invoices.json"

        new_entry = {
             "invoice_id": invoice_id,
             "client": raw_ref,
             "billing_amount": deposit,
             "assigned_route": routing_target,
             "status": "Success"
        }

        if os.path.exists(db_file):
             with open(db_file, "r") as f:
                try:
                       data_store = json.load(f)
                except json.JSONDecodeError: 
                     data_store = []
        else:
             data_store = []
        
        data_store.append(new_entry)

        with open(db_file, "w") as f:
             json.dump(data_store, f, indent=4)

        # ==== END OF NEW DATABASE CODE =====
        
        # Construct athe enterprise response payload to return to the sender
        sucess_response = {
            "status": "Success",
            "invoice_id": invoice_id,
            "sanitised_client": clean_ref,
            "assigned_route": routing_target,
            "message": "Transaction cleared system validation gates successfilly."
        }

        logging.info(f"Transaction Cleared: Route to -> {routing_target}")
        return jsonify(sucess_response)
    
    except Exception as error_message:
        #If your invoice_engine raises an exception (like a missing client name), catch it here!
        logging.error(f"Validation failure on ID {locals().get('invoice_id')}: {error_message}")

        falilure_response = {
            "status": "rejected",
            "invoice_id": payload.get('invoice_id'),
            "reason": str(error_message)
        }
        return jsonify(falilure_response)
    
if __name__ == "__main__":
        print("Booting Core Infrastrucyture Webhook Server...")
        # Run the server locally on port 5000
        app.run(host="127.0.0.1", port=5000, debug=True)