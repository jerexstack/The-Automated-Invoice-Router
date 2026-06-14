import time
import invoice_engine

incoming_invoices = [
    {"invoice_id": 901, "client": "  Acme Corp--", "billing_amount": 450000},
    {"invoice_id": 902, "client": "Global Tech Ltd", "billing_amount": 1200000},
    {"invoice_id": 903, "client": None, "billing_amount": 350000},
    {"invoice_id": 904, "client": "  Alpha Omega  ", "billing_amount": 80000}
]

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

    except Exception as error_message:
         print(f"CRITICAL ERROR' Failed to process Item ID: {invoice['invoice_id']}")
         print(f"Reason: {error_message}")

    end_clock = time.time()
    latency = end_clock - start_clock
    print(f"Process took {latency} seconds!")




