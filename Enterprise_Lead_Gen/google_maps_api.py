import googlemaps
import time
import os
from dotenv import load_dotenv

load_dotenv()

def get_places(query, max_results=20):
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key or api_key == "pune_cheia_aici":
        raise ValueError("GOOGLE_MAPS_API_KEY lipseste sau este invalid in fisierul .env")
        
    gmaps = googlemaps.Client(key=api_key)
    
    places_result = []
    
    # Text search
    try:
        results = gmaps.places(query=query)
        places_result.extend(results.get('results', []))
        
        # Google returns max 20 per page. If there is a next page and we need more...
        next_page_token = results.get('next_page_token')
        while next_page_token and len(places_result) < max_results:
            time.sleep(2) # required delay before using token
            results = gmaps.places(query=query, page_token=next_page_token)
            places_result.extend(results.get('results', []))
            next_page_token = results.get('next_page_token')
            
    except Exception as e:
        print(f"Eroare la Google Places API: {e}")
        
    extracted_data = []
    
    for place in places_result[:max_results]:
        # Detailed place info to get website and phone
        place_id = place['place_id']
        try:
            details = gmaps.place(place_id, fields=['name', 'formatted_address', 'formatted_phone_number', 'website', 'rating'])['result']
            
            extracted_data.append({
                "Name": details.get('name'),
                "Address": details.get('formatted_address'),
                "Phone": details.get('formatted_phone_number'),
                "Website": details.get('website'),
                "Rating": details.get('rating')
            })
        except Exception as e:
            pass
            
    return extracted_data
