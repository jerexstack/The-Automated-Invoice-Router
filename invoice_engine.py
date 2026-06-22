import json

# Load the dynamic routing rulefrom the configuration gateway at boot time
with open("gateway_config.json", "r") as config_file:
    config = json.load(config_file)

# Extract rules into operational variabes
RULES = config["billing_rules"]

def process_transaction(client_reference, billing_amount):
    if client_reference is None:
        raise Exception("Missing Client Reference data!")
    
    clean_reference = client_reference.strip().replace("--", "").upper()

    if billing_amount >= RULES["premium_threshold"]:
        target_vault = RULES["premium_route"]
    else:
        target_vault = RULES["standard_route"]

    return clean_reference, target_vault

if __name__ == "__main__":
    print("Testing Code")
    text1, text2 = process_transaction(" Jerex ", 10000)
    print(f"cleansed data: {text1}")
    print(f"Routing target: Routing funds to {text2}...")
    
    


