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
        'id': 'maltego',
        'name': 'Maltego',
        'description': 'Visual link analysis and entity mapping (commercial).',
        'check_url': 'https://www.maltego.com/'
    },
    {
        'id': 'sociallinks',
        'name': 'Social Links (Crimewall)',
        'description': 'Browser-based OSINT suite for social analysis.',
        'check_url': 'https://sociallinks.io/'
    },
    {
        'id': 'shadowdragon',
        'name': 'ShadowDragon',
        'description': 'Enterprise OSINT & identity resolution.',
        'check_url': 'https://shadowdragon.io/'
    },
    {
        'id': 'shodan',
        'name': 'Shodan',
        'description': 'Search engine for internet-connected devices (has API).',
        'check_url': 'https://www.shodan.io/'
    },
    {
        'id': 'censys',
        'name': 'Censys',
        'description': 'Network and certificate search (REST API).',
        'check_url': 'https://censys.io/'
    },
    {
        'id': 'intelx',
        'name': 'IntelX',
        'description': 'Multisource search (leaks, social, email).',
        'check_url': 'https://intelx.io/'
    },
    {
        'id': 'securitytrails',
        'name': 'SecurityTrails',
        'description': 'Domain/subdomain and passive DNS API.',
        'check_url': 'https://securitytrails.com/'
    },
    {
        'id': 'whoisxml',
        'name': 'WhoisXML API',
        'description': 'WHOIS and domain intelligence REST API.',
        'check_url': 'https://whoisxmlapi.com/'
    },
    {
        'id': 'sherlock',
        'name': 'Sherlock',
        'description': 'Username search across many services (open-source).',
        'check_url': 'https://github.com/sherlock-project/sherlock'
    },
    {
        'id': 'social-analyzer',
        'name': 'Social Analyzer',
        'description': 'Username/profile analysis across social networks.',
        'check_url': 'https://github.com/qeeqbox/social-analyzer'
    },
    {
        'id': 'exiftool',
        'name': 'ExifTool',
        'description': 'Media metadata extraction tool (local).',
        'check_url': 'https://exiftool.org/'
    }
]

HEADERS = {
    'User-Agent': 'Nexus-OSINT-Platform/1.0 (+https://github.com)'
}


def _check_url(url, timeout=5):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        return {'up': r.status_code == 200, 'code': r.status_code}
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
