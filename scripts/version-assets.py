#!/usr/bin/env python3
"""Refresh browser asset caches without changing portfolio content or layout."""
from pathlib import Path
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]

def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:12]

css = ROOT / 'assets/css/style.css'
style = css.read_text()
style = re.sub(r"\.\./images/robotics-background\.jpg(?:\?v=[a-f0-9]+)?", '../images/robotics-background.jpg?v=' + digest('assets/images/robotics-background.jpg'), style)
css.write_text(style)
assets = ['assets/css/style.css', 'assets/js/site.js', 'assets/images/ethan-profile.jpg']
for page in [*ROOT.glob('*.html'), *ROOT.glob('projects/*.html')]:
    text = page.read_text()
    for asset in assets:
        text = re.sub(re.escape(asset) + r'(?:\?v=[a-f0-9]+)?(?=")', asset + '?v=' + digest(asset), text)
    page.write_text(text)
print('Versioned portfolio stylesheet, motion script, background image, and portrait.')
