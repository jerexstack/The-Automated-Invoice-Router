import time
import json
import logging  # Import standard logging library
import invoice_engine

# Configure the Prodauction logging engine
logging.basicConfig(
     level=logging.INFO,
     format="%(asctime)s [%(levelname)s] %(message)s",
     handlers=[
          logging.FileHandler("production_pipeline.log"), # writes to a file
          logging.StreamHandler()                         # Still prints to terminal
     ]
)

incoming_invoices = [
    {"invoice_id": 901, "client": "  Acme Corp--", "billing_amount": 450000},
    {"invoice_id": 902, "client": "Global Tech Ltd", "billing_amount": 1200000},
    {"invoice_id": 903, "client": None, "billing_amount": 350000},
    {"invoice_id": 904, "client": "  Alpha Omega  ", "billing_amount": 80000}
]

successful_records =  []
failed_records = []

print("Starting Live Automation Simulator...")
start_clock = time.time()

for invoice in incoming_invoices:
    print(f"--- Processing Account ID: {invoice['invoice_id']}")
    time.sleep(1)
    print(f"\n [Webhook Recieved] Processing Item ID: {invoice['invoice_id']}")

    try:
        raw_ref = invoice["client"]
        deposit = invoice["billing_amount"]


        clean_ref, routing_target = invoice_engine.process_transaction(raw_ref, deposit)
        print(f"Clean data: {clean_ref}")
        print(f"Routing target: sending funds to ->{routing_target}")

        success_payload = {
            "invoice_id": invoice["invoice_id"],
            "client_name": clean_ref,
            "amount": deposit,
            "tier": routing_target,
            "processed_at": time.strftime("%Y-%M-%D %H:%M:%S")
        }
        successful_records.append(success_payload)

    except Exception as error_message:
         # Log errors with anexplict WARNING serverity level
         logging.warning(f"Validation faliure on Item ID: {invoice['invoice_id']} | Reason: {error_message}")

         failed_payload = {
             "invoice_id": invoice["invoice_id"],
             "attempted_amount": invoice["billing_amount"],
             "error_log": str(error_message),
             "failed_at": time.strftime("%Y-%M-%D %H:%M:%S")
         }
         failed_records.append(failed_payload)

logging.info("Synchronised data records to permanent JSON storage file...")

with open("processed_invoices.json", "w") as success_file:
        json.dump(successful_records, success_file, indent=4)

with open("failed_invoices.json", "w") as failure_file:
     json.dump(failed_records, failure_file, indent=4)

end_clock = time.time()
latency = end_clock - start_clock
print(f"Process took {latency} seconds!")




