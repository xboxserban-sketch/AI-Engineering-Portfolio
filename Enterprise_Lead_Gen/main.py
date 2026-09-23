import os
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table as SQLTable

from google_maps_api import get_places
from smart_crawler import extract_emails_playwright

load_dotenv()
console = Console()

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

def main():
    console.print("[bold cyan]=========================================[/bold cyan]")
    console.print("[bold cyan]   ENTERPRISE LEAD GENERATOR PRO v2.0    [/bold cyan]")
    console.print("[bold cyan]=========================================[/bold cyan]\n")
    
    if not os.getenv("GOOGLE_MAPS_API_KEY") or os.getenv("GOOGLE_MAPS_API_KEY") == "pune_cheia_aici":
        console.print("[bold red][!] Eroare: GOOGLE_MAPS_API_KEY lipseste sau este invalid in fisierul .env![/bold red]")
        console.print("[yellow]Te rog adauga cheia ta API in fisierul .env inainte de a rula aplicatia.[/yellow]")
        return

    query = Prompt.ask("[bold green]Ce nisa cautam azi?[/bold green] (ex: 'Clinica stomatologica Bucuresti')")
    max_results_str = Prompt.ask("[bold green]Cate firme vrei sa analizez?[/bold green]", default="10")
    
    try:
        max_results = int(max_results_str)
    except:
        max_results = 10
        
    console.print(f"\n[bold yellow][*] Conectare la Google Places API pentru '{query}'...[/bold yellow]")
    
    places = get_places(query, max_results)
    
    if not places:
        console.print("[bold red][-] Nu am gasit rezultate pe Google Maps.[/bold red]")
        return
        
    console.print(f"[bold green][+] Am gasit {len(places)} companii. Incepem extragerea inteligenta...[/bold green]\n")
    
    results = []
    
    with engine.connect() as conn:
        for p in places:
            name = p.get('Name', 'Unknown')
            website = p.get('Website')
            
            # Check if exists in DB
            from sqlalchemy import select
            s = select(leads_table).where(leads_table.c.name == name)
            existing = conn.execute(s).fetchone()
            
            if existing:
                console.print(f"[dim]Skip: {name} (deja in baza de date)[/dim]")
                continue
                
            emails_str = ""
            if website:
                console.print(f"[cyan]Crawler viziteaza:[/cyan] {website} ...")
                emails = extract_emails_playwright(website)
                emails_str = ", ".join(emails)
                if emails:
                    console.print(f"  [green]-> Gasit email: {emails_str}[/green]")
                else:
                    console.print(f"  [red]-> Niciun email gasit[/red]")
            else:
                console.print(f"[yellow]{name} nu are website listat pe Google Maps.[/yellow]")
                
            # Save to DB
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
            except Exception as e:
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
        
        console.print(f"\n[bold green]SUCCESS! Am salvat {len(results)} lead-uri noi in {filename}[/bold green]")
        
        # Display a nice table
        table = Table(title="Lead-uri Noi Extrase")
        table.add_column("Nume Firma", style="cyan")
        table.add_column("Telefon", justify="right", style="magenta")
        table.add_column("Email", justify="right", style="green")
        
        for r in results[:10]: # show max 10 in terminal
            table.add_row(r['Nume'][:30], str(r['Telefon'])[:20], str(r['Emailuri'])[:30])
            
        console.print(table)
    else:
        console.print("\n[bold yellow]Nu au fost adaugate lead-uri noi (fie nu aveau site, fie erau deja in DB).[/bold yellow]")

if __name__ == "__main__":
    main()
