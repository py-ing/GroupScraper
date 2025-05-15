import requests
import time
import os

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1311032100962570250/CeOeJhaPlZ1pt6TQEgfDylHmWwRTsOTxqF_x6FFyS8w-61qHN9ZYu2acP0OJpwmRImwq"

def fetch_group_info(group_id):
    """
    Fetch group information from Roblox API for a given group ID.
    """
    try:
        url = f"https://groups.roblox.com/v1/groups/{group_id}"
        response = requests.get(url)
        
        if response.status_code == 404:
            print(f"Group ID {group_id} does not exist. Skipping...")
            return None 
        if response.status_code != 200:
            print(f"Failed to fetch group information for Group ID {group_id}. HTTP Status: {response.status_code}")
            return None
        
        group_data = response.json()

        group_name = group_data.get("name", "Unknown Group")
        owner = group_data.get("owner", {}).get("username", "No Owner")
        member_count = group_data.get("memberCount", 0)
        robux = group_data.get("funds", "N/A") # Funds may not always be shown
        browser_link = f"https://www.roblox.com/groups/{group_id}"
        
        return group_id, group_name, owner, member_count, robux, browser_link
    
    except Exception as e:
        print(f"An error occurred while fetching group information for Group ID {group_id}: {e}")
        return None

def send_discord_notification(message):
    """
    Send a notification to Discord using the webhook.
    """
    try:
        data = {
            "content": message
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        
        if response.status_code != 204:
            print(f"Failed to send message to Discord. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error sending message to Discord: {e}")

def log_group_info(group_info, file_path="group_info.txt", processed_ids_path="processed_ids.txt"):
    """
    Log group information to the file and mark the group ID as processed.
    """
    try:
        group_id, group_name, owner, member_count, robux, browser_link = group_info
        
        log_entry = (
            f"{group_id} | {group_name} by {owner} | {member_count} Members | {robux}\n"
            f"{browser_link}\n\n"
        )
        
        with open(file_path, "a") as file:
            file.write(log_entry)
        
        with open(processed_ids_path, "a") as id_file:
            id_file.write(f"{group_id}\n")
        
        print(f"Group information logged successfully for Group ID {group_id}.")
        
        # Send Discord notification with the group information
        discord_message = f"New Group Logged: {group_name} ({group_id})\nOwner: {owner}\nMembers: {member_count}\nRobux: {robux}\n{browser_link}"
        send_discord_notification(discord_message)
    
    except Exception as e:
        print(f"Failed to log group information for Group ID {group_id}: {e}")

def load_processed_ids(processed_ids_path="processed_ids.txt"):
    """
    Load the list of already processed group IDs.
    """
    if not os.path.exists(processed_ids_path):
        return set() 
    
    with open(processed_ids_path, "r") as file:
        return set(line.strip() for line in file)

def main():
    # Range of IDs
    start_id = 1
    end_id = 1000000

    processed_ids = load_processed_ids()

    for group_id in range(start_id, end_id + 1):
        if str(group_id) in processed_ids:
            print(f"Group ID {group_id} already processed. Skipping...")
            continue
        
        print(f"Fetching information for Group ID {group_id}...")
        group_info = fetch_group_info(group_id)
        
        if group_info:
            log_group_info(group_info)
        
        time.sleep(3)  # Delay to avoid rate limits

if __name__ == "__main__":
    main()