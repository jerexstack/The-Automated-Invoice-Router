#!/bin/bash

# 1. Define variables for our system files
LOG_FILE="production_pipeline.log"
REPORT_FILE="daily_metric_report.txt"

echo "=== Starting Automated Log Analysis Pipeline ==="

# 2. Extract metrics into local memory variables
TOTAL_CLEARED=$(cat $LOG_FILE | grep "Transaction Cleared" | wc -l)
SECURITY_ALERTS=$(cat $LOG_FILE | grep -i "security alert" | wc -l)

# 3. Compile a clean data summary report using append blocks
echo "=== SYSTEM PERFORMANCE REPORT ===" > $REPORT_FILE
echo "Timestamp: $(date)" >> $REPORT_FILE
echo "Total Successfully Cleared Invoices: $TOTAL_CLEARED" >> $REPORT_FILE
echo "Total Critical Security Triggers: $SECURITY_ALERTS" >> $REPORT_FILE

echo "Metrics calculated successfully! Report saved to $REPORT_FILE"