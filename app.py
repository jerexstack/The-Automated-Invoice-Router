import logging
import os
import json
# Import your actual enterprise validation logic from your previous milestone!
import invoice_engine
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

# 1. System Observility Setup 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("production_pipeline.log"),
        logging.StreamHandler()
    ]
)


app = FastAPI(title="Automated Invoice Router Gateway")

# 2. Token Ingress Security Definition
API_KEY_NAME = "X-API-Key"
API_KEY_SECRET = "ZapierDevOpsSecretToken2026"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def verify_api_token(api_key: str = Depends(api_key_header)):
    """Perimeter Security: Validates the keycard badge before parsing."""
    if api_key != API_KEY_SECRET:
        logging.warning("Security Alert: Unauthorized connection attempt dropped.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Ingress Credentials"
        )
    return api_key

# 3. Pydantic Strict Data Schema Framework
class InvoicePayload(BaseModel):
    invoice_id: str
    client: str
    billing_amount: float 

# 3. Define an Explict HTTP Network Route
@app.post('/api/v1/invoice', dependencies=[Depends(verify_api_token)])
async def inbound_invoice_receiver(payload: InvoicePayload):
    """
    Listens for incoming HTTP POST network payloads, intercepts JSON data streams,
    and passes them directly into the core invoice_engine validation gates.
    """

    logging.info("Network Layer Event: Inbound HTTP POST request detected.")
    
    # Extract data directly from validated Pydantic model state fields using clean don (.) notation
    invoice_id = payload.invoice_id
    raw_ref = payload.client
    deposit = payload.billing_amount

    logging.info(f"Processing Remote Transaction - ID: {invoice_id}")

    try:
        # Execute your existing production code logic!
        clean_ref, routing_target = invoice_engine.process_transaction(raw_ref, deposit)


        # ===== START OF A NEW DATA BASE CODE ====
        
        db_file = "invoices.json"

        new_entry = {
             "invoice_id": invoice_id,
             "client": raw_ref,
             "billing_amount": deposit,
             "assigned_route": routing_target,
             "status": "Success"
        }

        data_store = []
        if os.path.exists(db_file):
            with open(db_file, "r") as f:
                try:
                    data_store = json.load(f)
                except json.JSONDecodeError:
                    data_store = []

        data_store.append(new_entry)

        with open(db_file, "w") as f:
            json.dump(data_store, f, indent=4)
        # ===== END OF NEW DATABASE CODE =====

        # Construct the enterprise response payload to return to the sender
        success_response = {
            "status": "Success",
            "invoice_id": invoice_id,
            "sanitised_client": clean_ref,
            "assigned_route": routing_target,
            "message": "Transaction cleared system validation gates successfilly."
        }

        logging.info(f"Transaction Cleared: Route to -> {routing_target}")
        return success_response
    
    except Exception as error_message:
        logging.error(f"Validation failure on ID {invoice_id}: {error_message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "rejected",
                "invoice_id": invoice_id,
                "reason": str(error_message)
            }
        )

if __name__ == "__main__":
    print("To run this server, execute: uvicorn app:app --reload --port 5000")