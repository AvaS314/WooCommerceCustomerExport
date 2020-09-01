from woocommerce import API
import csv
import datetime

wcapi = API(
    url="https://example.com", # Your store URL
    consumer_key="consumer_key", # Your consumer key
    consumer_secret="consumer_secret", # Your consumer secret
    wp_api=True, # Enable the WP REST API integration
    version="wc/v3", # WooCommerce WP REST API version
    timeout=20
    )

def process(writer, data, info, time):
    writer.writerow([data["first_name"], data["last_name"], data["company"], data["email"] if info == "b" else "", data["phone"] if info == "b" else "", info, data["address_1"], data["address_2"], data["city"], data["state"], data["postcode"], time])

with open("customers.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["First Name", "Last Name", "Company", "email", "phone", "Shipping/Billing", "Address Line 1", "Address Line 2", "City", "State", "ZIP", "Last Active"])
    page = 1
    while True:
        # print("Requesting " + str(page))
        resp = wcapi.get("customers", params={"page": page}).json()
        page += 1 
        if not resp:
            break
        for record in resp:
            time = ""
            for entry in record["meta_data"]:
                if entry["key"] == "wc_last_active":
                    time = datetime.datetime.fromtimestamp(int(entry["value"])).strftime("%m/%d/%Y")
            if record["billing"]["first_name"]:
                process(writer, record["billing"], "b", time)
            if record["shipping"]["first_name"]:
                if record["shipping"]["address_1"] == record["billing"]["address_1"]:
                    continue
                process(writer, record["shipping"], "s", time)
        

    print("Done")
