import requests
import json
from xml.etree import ElementTree as ET
from xml.dom.minidom import parseString

def print_pretty_xml(xml_str):
    """Print XML in a nicely formatted way."""
    dom = parseString(xml_str)
    print(dom.toprettyxml())

def test_xml_service():
    base_url = "http://localhost:8000"
    
    # Test service info
    print("\nTesting service info...")
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("Service Info Response:")
            print_pretty_xml(response.text)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error getting service info: {e}")
    
    # Test get_player_stats
    print("\nTesting get_player_stats...")
    try:
        response = requests.post(
            f"{base_url}/player/stats",
            json={"name": "Patrick Mahomes"}
        )
        
        if response.status_code == 200:
            print("Player Stats Response:")
            print_pretty_xml(response.text)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error getting player stats: {e}")
    
    # Test get_radar_chart with QBs
    print("\nTesting get_radar_chart with QBs (Mahomes vs Allen)...")
    try:
        response = requests.post(
            f"{base_url}/player/radar-chart",
            json={
                "player_ids": ["2558125", "2560955"]  # Mahomes and Josh Allen
            }
        )
        
        if response.status_code == 200:
            print("Radar Chart Response:")
            print_pretty_xml(response.text)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error getting radar chart: {e}")
    
    # Test get_radar_chart with WRs
    print("\nTesting get_radar_chart with WRs (Hill vs Jefferson)...")
    try:
        response = requests.post(
            f"{base_url}/player/radar-chart",
            json={
                "player_ids": ["2556214", "2564556"]  # Tyreek Hill and Justin Jefferson
            }
        )
        
        if response.status_code == 200:
            print("Radar Chart Response:")
            print_pretty_xml(response.text)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error getting radar chart: {e}")

if __name__ == '__main__':
    test_xml_service() 