"""Refresh the profile card from public GitHub REST data; no credentials needed."""
from datetime import datetime, timezone
from pathlib import Path
import json
import urllib.request

BASE = Path(__file__).resolve().parent
USERNAME = 'u8bj'

def public_json(endpoint):
    req = urllib.request.Request('https://api.github.com/' + endpoint,
                                 headers={'User-Agent': 'u8bj-Public-Profile', 'Accept': 'application/vnd.github+json'})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)

def refresh():
    user = public_json('users/' + USERNAME)
    repos, page = [], 1
    while True:
        batch = public_json(f'users/{USERNAME}/repos?per_page=100&page={page}')
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    values = [('Public repositories', user['public_repos']), ('Followers', user['followers']),
              ('Repository stars', sum(r['stargazers_count'] for r in repos)),
              ('Repository forks', sum(r['forks_count'] for r in repos))]
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="165" viewBox="0 0 1000 165" role="img" aria-label="Public GitHub statistics">',
             '<rect x="1" y="1" width="998" height="163" rx="14" fill="#0f1119" stroke="#30263c"/>']
    for index, (label, value) in enumerate(values):
        x = 126 + index * 250
        if index:
            parts.append(f'<path d="M{x-125} 30v88" stroke="#30263c"/>')
        parts.append(f'<text x="{x}" y="80" text-anchor="middle" fill="#c4a0ff" font-family="Segoe UI,Arial,sans-serif" font-size="38" font-weight="600">{int(value)}</text>')
        parts.append(f'<text x="{x}" y="110" text-anchor="middle" fill="#a89cb8" font-family="Segoe UI,Arial,sans-serif" font-size="13">{label}</text>')
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    parts.append(f'<text x="30" y="145" fill="#756b84" font-family="Segoe UI,Arial,sans-serif" font-size="10">PUBLIC GITHUB DATA / REFRESHED {stamp} UTC</text></svg>')
    (BASE / 'assets' / 'stats.svg').write_text('\n'.join(parts) + '\n', encoding='utf-8')
    print('Refreshed public statistics:', dict(values))

if __name__ == '__main__':
    refresh()
