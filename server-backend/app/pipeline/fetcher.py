import requests

BASE_URL = "https://archive.org/wayback/available"

def get_wayback_snapshot_url(target_url: str) -> str:
    """
    Fetches the Wayback Machine snapshot URL for a given URL and date.
    """
    
    params = {
        "url": target_url,
    }
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    snapshot = data.get('archived_snapshots', {}).get('closest')
    if snapshot and snapshot.get('available'):
        return snapshot['url']
    return None
        
def fetch_wayback_snapshot(target_url: str) -> str:
    # """
    # Fetches the Wayback Machine snapshot URL for a given URL.
    # """
    
    # snapshot_url = get_wayback_snapshot_url(target_url)
    # if not snapshot_url:
    #     raise ValueError(f"No Wayback Machine snapshot found for {target_url}")
    
    # return snapshot_url  
    """Fetch the actual HTML content from the Wayback Machine snapshot of the given URL."""
    snapshot_url = get_wayback_snapshot_url(target_url)
    if not snapshot_url:
        raise ValueError(f"No Wayback Machine snapshot found for {target_url}")

    response = requests.get(snapshot_url)
    if response.status_code != 200:
        raise ValueError(f"Snapshot URL returned status code {response.status_code}")

    return response.text
