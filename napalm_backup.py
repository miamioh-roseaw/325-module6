from napalm import get_network_driver
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Fetch credentials from environment variables
USERNAME = os.environ.get("CISCO_CREDS_USR")
PASSWORD = os.environ.get("CISCO_CREDS_PSW")

if not USERNAME or not PASSWORD:
    raise ValueError("Missing environment variables for credentials.")

# Define devices
devices = {
    'regrtr': '10.10.10.2',
    'ham-rtr': '10.10.10.3',
    'mid-rtr': '10.10.10.4'
}

# Create backup directory if not exists
os.makedirs("backups", exist_ok=True)

# Get NAPALM driver for Cisco IOS
driver = get_network_driver('ios')

# Loop through and back up
for hostname, ip in devices.items():
    try:
        logging.info(f"Connecting to {hostname} at {ip}")
        device = driver(hostname=ip, username=USERNAME, password=PASSWORD)
        device.open()
        config = device.get_config()
        filepath = f'backups/{hostname}_running.txt'
        with open(filepath, 'w') as f:
            f.write(config['running'])
        logging.info(f"[✓] Backed up {hostname} to {filepath}")
        device.close()
    except Exception as e:
        logging.error(f"[✗] Failed to back up {hostname} ({ip}): {e}")
