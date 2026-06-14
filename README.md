# The Automated Invoice Router 

A fault-tolerant Pythonautomation pipeline that streams incoming invoice data, sanitizes fields routes clients based on billing tiers, and utilizes validation gates to catch to catch corruptpayloads safely without crashing.

---

## System Architecture and Data Flow

This engine simulates a producttion-grade automation pipeline built to process data streams dynamically businnes rules from executin logic.

[Incoming Data Stream]

│

▼

┌──────────────────────┐ Reads Rules

│ invoice_engine.py │◄───────────────── [gateway_config.json]

└──────────┬───────────┘ (Dynamic Thresholds)

│

┌───────┴───────┐

▼ ▼

(Valid Data) (Corrupt Data)

│ │

▼ ▼

┌───────────┐ ┌───────────┐ Both streams parsed, formatted,

│ SUCCESS │ │ FAILURE │ and stamped simultaneously into:

│ Bucket │ │ Bucket │

└─────┬─────┘ └─────┬─────┘ ➔ [processed_invoices.json]

│ │ ➔ [failed_invoices.json]

└───────┬───────┘ ➔ [production_pipeline.log]

▼

[GitHub Remote Repository]

##  Core engineering Features

* **Decoupled Configuration Gateway:** Operational business rules, tier classifications, and billing thresholds are completely removed from the source code and managed viaan external text-based gateway ('gateway_config.json.')
* **Deterministic Validation Gates:** Built in faukt protection layers utilize structure exception handling loops to isolate corrupted JSON payloads (e.g., missing keys or data anomalies) without forcing fatal  runtime framework failures.
* **Dual-Stream Syste Logging:** Intergrates Python's native 'logging' matrix with a multi-handler layout, recording operational history to 'production_pipeline.log' wuth distinct severity makers while sustaining standard  visual output.
* **Structured Disk Persistance:** Successsfully validated arrays are mapped into long-term structured storage ('processed_invoices.py'), separating successfully managed payloads from error records.

---

## Installation and Execution

### Prerequisites
Ensure your local environment runs python 3.x.

### 1. Initialize the Core Test Environment
To test th isolated processing engine independently via its dunder main testing framework:
'''bash
py invoice_engine.py