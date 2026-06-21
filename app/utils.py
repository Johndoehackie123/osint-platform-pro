import requests
import whois
import socket
import dns.resolver
from datetime import datetime

def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        return {
            "domain_name": w.domain_name,
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "emails": w.emails,
            "name_servers": w.name_servers
        }
    except Exception as e:
        return {"error": str(e)}

def get_dns_records(domain):
    records = {}
    for rtype in ['A', 'MX', 'NS', 'TXT']:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            records[rtype] = [str(rdata) for rdata in answers]
        except Exception:
            records[rtype] = []
    return records

def search_username(username):
    platforms = {
        "GitHub": f"https://github.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "Reddit": f"https://reddit.com/user/{username}",
        "Pinterest": f"https://pinterest.com/{username}",
        "YouTube": f"https://youtube.com/@{username}",
        "TikTok": f"https://tiktok.com/@{username}"
    }
    results = {}
    for name, url in platforms.items():
        try:
            res = requests.get(url, timeout=3)
            if res.status_code == 200:
                results[name] = {"status": "Found", "url": url}
            else:
                results[name] = {"status": "Not Found", "url": url}
        except Exception:
            results[name] = {"status": "Error", "url": url}
    return results

def analyze_website(url):
    if not url.startswith('http'):
        url = 'http://' + url
    try:
        res = requests.get(url, timeout=5)
        return {
            "status_code": res.status_code,
            "headers": dict(res.headers),
            "server": res.headers.get('Server', 'Unknown'),
            "content_type": res.headers.get('Content-Type', 'Unknown')
        }
    except Exception as e:
        return {"error": str(e)}
