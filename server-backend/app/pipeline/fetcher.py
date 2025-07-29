import requests

from datetime import datetime
from urllib.parse import urlparse

BASE_URL = "https://archive.org/wayback/available"

def get_wayback_snapshot_url(target_url: str) -> str:
    """
    Fetches the Wayback Machine snapshot URL for a given URL and date.
    """
    params = {
        "url": target_url,
    }
    # # Add timestamp if it's a Telegram link
    # if "telegram.org" in target_url or "t.me" in target_url:
    #     current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    #     params["timestamp"] = current_timestamp
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    print(f"Response from Wayback Machine for {target_url}: {data}")
    snapshot = data.get('archived_snapshots', {}).get('closest')
    print(f"Snapshot data: {snapshot}")
    if snapshot and snapshot.get('available'):
        snapshot_url = snapshot['url']
         # Fix malformed Telegram snapshots
        if "telegram.org" in target_url or "t.me" in target_url:
            parsed = urlparse(snapshot_url)
            fixed_snapshot_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path.split('/https:/')[0]}/https://{urlparse(target_url).netloc}{urlparse(target_url).path}"
            print(f"Fixed snapshot URL: {fixed_snapshot_url}")
            return fixed_snapshot_url
            
        return snapshot_url
    
    
    return None
        
def fetch_wayback_snapshot(target_url: str) -> str:
    """Fetch the actual HTML content from the Wayback Machine snapshot of the given URL."""
    snapshot_url = get_wayback_snapshot_url(target_url)
    print(f"Snapshot URL: {snapshot_url}")
    if not snapshot_url:
        raise ValueError(f"No Wayback Machine snapshot found for {target_url}")

    response = requests.get(snapshot_url)
    # print("^^^^^^^^")
    # print(response)
    # print("^^^^^^^^")
    if response.status_code != 200:
        raise ValueError(f"Snapshot URL returned status code {response.status_code}")
    

    return response.text
    
    # this version return URL
    # """
    # Fetches the Wayback Machine snapshot URL for a given URL.
    # """
    
    # snapshot_url = get_wayback_snapshot_url(target_url)
    # if not snapshot_url:
    #     raise ValueError(f"No Wayback Machine snapshot found for {target_url}")
    
    # return snapshot_url  
    
    # this verrsion return content
