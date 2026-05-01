import requests
import csv


asset_ids = ["6j5TiqTFl6o", "A204252258767106", "A138391271962845"]  # Sample asset IDs

content_owner_id = "" # Enter valid content owner ID

access_token = ""  # Replace with the actual OAuth access token

base_url = "https://www.googleapis.com/youtube/partner/v1/assets"

output_csv = "/Users/saralunardelli/documents/asset_ownership_results.csv"

def get_asset_ownership(asset_id):
  
    url = f"{base_url}/{asset_id}?onBehalfOfContentOwner={content_owner_id}&fetchOwnership=true"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }


    response = requests.get(url, headers=headers)

    if response.status_code == 200:
  
        return response.json()
    else:
        print(f"Failed to fetch ownership for asset {asset_id}: {response.status_code} - {response.text}")
        return None

with open(output_csv, mode="w", newline="") as file:

    fieldnames = ["Asset ID", "Owner Name", "Owner ID", "Ownership Ratio", "Asset Type"]
    
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    

    writer.writeheader()

    for asset_id in asset_ids:
        ownership_data = get_asset_ownership(asset_id)
        
        if ownership_data:
            
            asset_type = ownership_data.get('type', 'N/A')
            owners = ownership_data.get('ownership', {}).get('general', {}).get('owner', [])
            
          
            for owner in owners:
                owner_name = owner.get('ownerName', 'N/A')
                owner_id = owner.get('contentOwner', 'N/A')
                ownership_ratio = owner.get('ratio', 'N/A')

                
                writer.writerow({
                    "Asset ID": asset_id,
                    "Owner Name": owner_name,
                    "Owner ID": owner_id,
                    "Ownership Ratio": ownership_ratio,
                    "Asset Type": asset_type
                })

print(f"Ownership results have been saved to {output_csv}.")

