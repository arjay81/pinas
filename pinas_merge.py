import xml.etree.ElementTree as ET
import requests
from datetime import datetime, UTC
import os

# Base URL for EPG feeds with channel IDs
BASE_URL = 'https://epg.pw/api/epg.xml?lang=en&timezone={timezone}&date={date}&channel_id={channel_id}'
CHANNELS = [
    {'id': '405058', 'timezone': 'VVMvRWFzdGVybg%3D%3D'},
    {'id': '412143', 'timezone': 'VVMvRWFzdGVybg%3D%3D'},
    {'id': '404926', 'timezone': 'VVMvRWFzdGVybg%3D%3D'},
    {'id': '405132', 'timezone': 'VVMvRWFzdGVybg%3D%3D'},
    {'id': '369842', 'timezone': 'VVMvRWFzdGVybg%3D%3D'},
    {'id': '403813', 'timezone': 'VVMvRWFzdGVybg%3D%3D'},
    {'id': '404871', 'timezone': 'VVMvRWFzdGVybg%3D%3D'},
    {'id': '429570', 'timezone': 'VVMvRWFzdGVybg%3D%3D'},
    {'id': '403541', 'timezone': 'VVMvRWFzdGVybg%3D%3D'},
    {'id': '7870', 'timezone': 'QW1lcmljYS9Ub3JvbnRv'},
    {'id': '70615', 'timezone': 'QW1lcmljYS9Ub3JvbnRv'},
    {'id': '322467', 'timezone': 'QW1lcmljYS9Ub3JvbnRv'},
    {'id': '7864', 'timezone': 'QW1lcmljYS9Ub3JvbnRv'},
    {'id': '322511', 'timezone': 'QW1lcmljYS9Ub3JvbnRv'},
    {'id': '322493', 'timezone': 'QW1lcmljYS9Ub3JvbnRv'},
    {'id': '408276', 'timezone': 'QW1lcmljYS9Ub3JvbnRv'},
    {'id': '429756', 'timezone': 'QW1lcmljYS9Ub3JvbnRv'},
    {'id': '429763', 'timezone': 'QW1lcmljYS9Ub3JvbnRv'},
    {'id': '322511', 'timezone': 'QW1lcmljYS9Ub3JvbnRv'},  # Duplicate handled
    {'id': '322466', 'timezone': 'QW1lcmljYS9Ub3JvbnRv'}
]

# Output file path
OUTPUT_FILE = 'pinas_merged_feed.xml'

def fetch_xml_feed(channel_id, timezone):
    """Fetch EPG XML content for a given channel and timezone."""
    # Use current date for dynamic updates
    current_date = datetime.now(UTC).strftime('%Y%m%d')
    url = BASE_URL.format(timezone=timezone, date=current_date, channel_id=channel_id)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return ET.fromstring(response.text)
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    except ET.ParseError as e:
        print(f"Error parsing XML from {url}: {e}")
        return None

def merge_xml_feeds():
    """Merge multiple EPG XML feeds into a single XML structure."""
    # Create root element for merged feed
    merged_root = ET.Element('tv')

    # Track unique programme entries to avoid duplicates
    seen_programmes = set()

    # Fetch and merge programmes from each feed
    for channel in CHANNELS:
        feed = fetch_xml_feed(channel['id'], channel['timezone'])
        if feed is None:
            continue

        # Copy channel elements
        for channel_elem in feed.findall('channel'):
            channel_id = channel_elem.get('id')
            if channel_id and channel_id not in [c.get('id') for c in merged_root.findall('channel')]:
                merged_root.append(channel_elem)

        # Copy programme elements, avoiding duplicates
        for programme in feed.findall('programme'):
            programme_key = (programme.get('start'), programme.get('stop'), programme.get('channel'))
            if programme_key not in seen_programmes:
                merged_root.append(programme)
                seen_programmes.add(programme_key)

    # Write merged feed to file
    tree = ET.ElementTree(merged_root)
    with open(OUTPUT_FILE, 'wb') as f:
        tree.write(f, encoding='utf-8', xml_declaration=True)
    print(f"Merged feed written to {OUTPUT_FILE}")

if __name__ == '__main__':
    merge_xml_feeds()
