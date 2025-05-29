import xml.etree.ElementTree as ET
import requests
from datetime import datetime
import os

# List of XML feed URLs
FEED_URLS = [
    'https://www.philstar.com/rss/nation',  # Philippine Star - Nation
    'https://news.abs-cbn.com/xml/rss/news'  # ABS-CBN News
]

# Output file path
OUTPUT_FILE = 'pinas_merged_feed.xml'

def fetch_xml_feed(url):
    """Fetch XML content from a given URL."""
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
    """Merge multiple XML feeds into a single XML structure."""
    # Create root element for merged feed
    merged_root = ET.Element('rss', version='2.0')
    merged_channel = ET.SubElement(merged_root, 'channel')
    
    # Add basic channel information
    ET.SubElement(merged_channel, 'title').text = 'Pinas Merged XML Feed'
    ET.SubElement(merged_channel, 'description').text = 'A merged feed of Philippine news'
    ET.SubElement(merged_channel, 'lastBuildDate').text = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

    # Fetch and merge items from each feed
    for url in FEED_URLS:
        feed = fetch_xml_feed(url)
        if feed is None:
            continue
        
        # Find the channel element
        channel = feed.find('channel')
        if channel is None:
            print(f"No channel found in {url}")
            continue

        # Copy items to merged feed
        for item in channel.findall('item'):
            merged_channel.append(item)

    # Write merged feed to file
    tree = ET.ElementTree(merged_root)
    with open(OUTPUT_FILE, 'wb') as f:
        tree.write(f, encoding='utf-8', xml_declaration=True)
    print(f"Merged feed written to {OUTPUT_FILE}")

if __name__ == '__main__':
    merge_xml_feeds()
