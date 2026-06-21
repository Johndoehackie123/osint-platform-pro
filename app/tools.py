import requests
import time

# Simple in-memory TTL cache for tool statuses
_cache = {
    'timestamp': 0,
    'ttl': 30,  # seconds
    'data': []
}

TOOLS = [
    {
        'id': 'ip-api',
        'name': 'IP-API',
        'description': 'Free IP geolocation API (no key, limited rate).',
        'check_url': 'http://ip-api.com/json/8.8.8.8'
    },
    {
        'id': 'ipwhois',
        'name': 'ipwho.is',
        'description': 'IP geolocation and ASN service (no key for basic JSON).',
        'check_url': 'https://ipwho.is/8.8.8.8'
    },
    {
        'id': 'dns_google',
        'name': 'Google DNS over HTTPS',
        'description': 'DNS-over-HTTPS resolver by Google (no key).',
        'check_url': 'https://dns.google/resolve?name=example.com&type=A'
    },
    {
        'id': 'cloudflare_doh',
        'name': 'Cloudflare DNS over HTTPS',
        'description': 'Cloudflare DOH endpoint (no key).',
        'check_url': 'https://cloudflare-dns.com/dns-query?name=example.com&type=A'
    },
    {
        'id': 'crtsh',
        'name': 'crt.sh (Certificate Transparency)',
        'description': 'Certificate transparency search (public, no key).',
        'check_url': 'https://crt.sh/?q=example.com&output=json'
    },
    {
        'id': 'rdap_org',
        'name': 'RDAP (rdap.org)',
        'description': 'Registration Data Access Protocol lookup (no key).',
        'check_url': 'https://rdap.org/domain/example.com'
    },
    {
        'id': 'sherlock',
        'name': 'Sherlock (GitHub)',
        'description': 'Username discovery project (repo reachable).',
        'check_url': 'https://github.com/sherlock-project/sherlock'
    },
    {
        'id': 'exiftool',
        'name': 'ExifTool (Website)',
        'description': 'Metadata extraction tool site.',
        'check_url': 'https://exiftool.org/'
    }
]

HEADERS = {
    'User-Agent': 'Nexus-OSINT-Platform/1.0 (+https://github.com)'
}


def _check_url(url, timeout=6):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        return {'up': r.status_code >= 200 and r.status_code < 400, 'code': r.status_code}
    except Exception as e:
        return {'up': False, 'error': str(e)}


def get_tools_status(force=False):
    now = time.time()
    if not force and (now - _cache['timestamp'] < _cache['ttl']) and _cache['data']:
        return _cache['data']

    statuses = []
    for t in TOOLS:
        res = _check_url(t['check_url'])
        status = {
            'id': t['id'],
            'name': t['name'],
            'description': t['description'],
            'ok': bool(res.get('up')),
            'code': res.get('code'),
            'error': res.get('error') if not res.get('up') else None,
            'checked_at': int(now)
        }
        statuses.append(status)

    _cache['timestamp'] = now
    _cache['data'] = statuses
    return statuses
