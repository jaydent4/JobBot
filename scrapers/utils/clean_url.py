from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def clean_url(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    allowed_keys = {
        'c',
        'job_id',
        'gh_jid',
        'lever_jid',
        'reqid',
        'requisitionId',
        'jid'
    }

    filtered_query = {}
    for k, v in query.items():
        if k in allowed_keys:
            filtered_query[k] = v
    
    cleaned_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path.rstrip('/'),
        '',
        urlencode(filtered_query, doseq=True),
        ''
    ))

    return cleaned_url