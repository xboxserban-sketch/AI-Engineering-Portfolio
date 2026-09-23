from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def extract_emails_playwright(url):
    emails = set()
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            
            page.set_default_timeout(15000)
            
            try:
                page.goto(url)
                page.wait_for_load_state("networkidle", timeout=10000)
            except:
                pass
                
            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find emails on homepage
            emails.update(re.findall(email_pattern, soup.get_text()))
            
            # Look for contact page
            contact_links = []
            for a in soup.find_all('a', href=True):
                href = a.get('href', '')
                if 'mailto:' in href:
                    clean_email = href.replace('mailto:', '').split('?')[0].strip()
                    emails.add(clean_email)
                elif 'contact' in href.lower() or 'despre' in href.lower():
                    contact_links.append(href)
                    
            # Visit first contact page if found
            if contact_links:
                contact_url = urljoin(url, contact_links[0])
                try:
                    page.goto(contact_url)
                    page.wait_for_load_state("domcontentloaded", timeout=5000)
                    contact_content = page.content()
                    emails.update(re.findall(email_pattern, BeautifulSoup(contact_content, 'html.parser').get_text()))
                except:
                    pass
                    
            browser.close()
    except Exception as e:
        pass
        
    clean_emails = [e for e in emails if not e.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.mp4'))]
    return list(set(clean_emails))
