import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table as SQLTable

from google_maps_api import get_places
from smart_crawler import extract_emails_playwright

load_dotenv()

# Database Setup
engine = create_engine('sqlite:///leads.db')
metadata = MetaData()
leads_table = SQLTable(
    'leads', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, unique=True),
    Column('address', String),
    Column('phone', String),
    Column('website', String),
    Column('emails', String),
    Column('rating', String)
)
metadata.create_all(engine)

def run_auto(query="Clinica stomatologica Bucuresti", max_results=10):
    print(f"[*] Conectare la Google Places API pentru '{query}'...")
    
    try:
        places = get_places(query, max_results)
    except Exception as e:
        print(f"Eroare API: {e}")
        return
    
    if not places:
        print("[-] Nu am gasit rezultate pe Google Maps. Probabil cheia API este invalida sau nu are permisiuni.")
        return
        
    print(f"[+] Am gasit {len(places)} companii. Incepem extragerea...")
    
    results = []
    with engine.connect() as conn:
        for p in places:
            name = p.get('Name', 'Unknown')
            website = p.get('Website')
            
            # Check DB
            from sqlalchemy import select
            s = select(leads_table).where(leads_table.c.name == name)
            existing = conn.execute(s).fetchone()
            
            if existing:
                continue
                
            emails_str = ""
            if website:
                emails = extract_emails_playwright(website)
                emails_str = ", ".join(emails)
                
            ins = leads_table.insert().values(
                name=name,
                address=p.get('Address', ''),
                phone=p.get('Phone', ''),
                website=website if website else '',
                emails=emails_str,
                rating=str(p.get('Rating', ''))
            )
            try:
                conn.execute(ins)
                conn.commit()
            except:
                pass
                
            results.append({
                "Nume": name,
                "Adresa": p.get('Address', ''),
                "Telefon": p.get('Phone', ''),
                "Website": website,
                "Emailuri": emails_str,
                "Rating": p.get('Rating', '')
            })
            
    if results:
        df = pd.DataFrame(results)
        filename = f"Enterprise_Leads_{query.replace(' ', '_')}.csv"
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"\nSUCCESS! Am salvat {len(results)} lead-uri in {filename}")
    else:
        print("\nNu au fost adaugate lead-uri noi.")

if __name__ == "__main__":
    run_auto("Cabinet avocatura Bucuresti", 15)
