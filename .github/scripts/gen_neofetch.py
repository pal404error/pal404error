import urllib.request, json, os, datetime

USER = "pal404error"
token = os.environ.get("GITHUB_TOKEN", "")

def api(url):
    req = urllib.request.Request(url)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

user = api(f"https://api.github.com/users/{USER}")
repos = api(f"https://api.github.com/users/{USER}/repos?per_page=100")
total_stars = sum(r.get("stargazers_count", 0) for r in repos)

langs = {}
for r in repos:
    l = r.get("language")
    if l:
        langs[l] = langs.get(l, 0) + 1
top_lang = max(langs, key=langs.get) if langs else "—"

created = user["created_at"][:10]
cdate = datetime.date.fromisoformat(created)
days = (datetime.date.today() - cdate).days
age = f"{days // 365}y {days % 365}d"
updated = user["updated_at"][:10]

metrics = [
    ("Uptime", age),
    ("Followers", str(user["followers"])),
    ("Following", str(user["following"])),
    ("Public Repos", str(user["public_repos"])),
    ("Total Stars", str(total_stars)),
    ("Top Language", top_lang),
    ("Joined", created),
    ("Last Active", updated),
]

SF = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, Arial, sans-serif"

# Apple-HIG semantic palette
C_BG       = "#000000"   # window background
C_MATERIAL = "#1c1c1e"   # secondary background (grouped surface)
C_SEP      = "#38383a"   # separator
C_LABEL    = "#f5f5f7"   # primary label
C_SECOND   = "#98989d"   # secondary label
C_WHITE    = "#ffffff"

def g_apple():
    return ('<path transform="translate(100,125) scale(0.16)" fill="#ffffff" d='
            '"M788.1 340.9c-5.8 4.5-108.2 62.2-108.2 190.5 0 148.4 130.3 200.9 134.2 202.2-.6 3.2-20.7 71.9-67.5 141.5-41.7 60.6-84.9 120.8-153.4 120.8s-83.2-38.8-157.7-38.8c-71.8 0-97.3 39.7-156.4 39.7-66.6 0-111.3-37.5-151.4-94.3C21.9 899.9 0 762.5 0 666.5c0-194.4 134.4-297.5 265.8-297.5 68.1 0 124.8 44.7 151.6 44.7 27.2 0 80.5-46.7 149.5-46.7 18.1 0 134.6 1.6 193.2 101.2zm-234.8-92.3c31.5-38.9 53.1-92.8 53.1-147.3 0-7.5-.6-14.9-1.9-22.1-50 3.7-106.1 33.6-122.6 76.2-14.3 37-25.6 90.4-25.6 145.3 0 7.5.6 15.2 1.9 22.1 2.5.2.5.1.7.3 44.2 0 100.6-29.6 122.4-74.2z" />')

def g_ubuntu():
    return ('<circle cx="165" cy="205" r="58" fill="none" stroke="#ffffff" stroke-width="13"/>'
            '<circle cx="165" cy="205" r="32" fill="none" stroke="#ffffff" stroke-width="13"/>'
            '<circle cx="165" cy="147" r="7" fill="#ffffff"/>'
            '<circle cx="165" cy="263" r="7" fill="#ffffff"/>'
            '<circle cx="107" cy="205" r="7" fill="#ffffff"/>'
            '<circle cx="223" cy="205" r="7" fill="#ffffff"/>')

def g_fedora():
    return ('<circle cx="165" cy="205" r="58" fill="#ffffff" opacity="0.14"/>'
            f'<text x="165" y="248" text-anchor="middle" font-family="{SF}" font-size="110" font-weight="700" fill="#ffffff">f</text>')

def g_windows():
    return ('<rect x="96" y="136" width="64" height="64" rx="12" fill="#ffffff"/>'
            '<rect x="170" y="136" width="64" height="64" rx="12" fill="#ffffff"/>'
            '<rect x="96" y="210" width="64" height="64" rx="12" fill="#ffffff"/>'
            '<rect x="170" y="210" width="64" height="64" rx="12" fill="#ffffff"/>')

def g_arch():
    return f'<text x="165" y="262" text-anchor="middle" font-family="{SF}" font-size="150" font-weight="800" fill="#ffffff">A</text>'

oses = [
    {"name": "macOS",   "c1": "#0a84ff", "c2": "#5ac8fa", "glyph": g_apple()},
    {"name": "Ubuntu",  "c1": "#E95420", "c2": "#f97316", "glyph": g_ubuntu()},
    {"name": "Fedora",  "c1": "#3C6EB4", "c2": "#5b9bd5", "glyph": g_fedora()},
    {"name": "Windows", "c1": "#00A4EF", "c2": "#0078D4", "glyph": g_windows()},
    {"name": "Arch",    "c1": "#1793D1", "c2": "#00d4ff", "glyph": g_arch()},
]

N = len(oses)
slot = 5.0
total = N * slot

defs = ""
for i, o in enumerate(oses):
    defs += (f'    <linearGradient id="grad{i}" x1="0" y1="0" x2="0" y2="1">\n'
             f'      <stop offset="0" stop-color="{o["c1"]}"/>\n'
             f'      <stop offset="1" stop-color="{o["c2"]}"/>\n'
             f'    </linearGradient>\n')

# Animated per-OS group: icon + name + sub + accent bar
os_groups = ""
for i, o in enumerate(oses):
    a = i * slot / total
    b = (i + 1) * slot / total
    keytimes = f"0;{a:.4f};{a:.4f};{b:.4f};1"
    init = "1" if i == 0 else "0"
    os_groups += (
        f'  <g opacity="{init}">\n'
        f'    <animate attributeName="opacity" dur="{total:.1f}s" repeatCount="indefinite" keyTimes="{keytimes}" values="0;0;1;0;0"/>\n'
        f'    <rect x="80" y="120" width="170" height="170" rx="38" fill="url(#grad{i})"/>\n'
        f'    <rect x="80.75" y="120.75" width="168.5" height="168.5" rx="37" fill="none" stroke="#ffffff" stroke-opacity="0.22" stroke-width="1.5"/>\n'
        f'    {o["glyph"]}\n'
        f'    <text x="290" y="178" font-family="{SF}" font-size="34" font-weight="600" fill="{C_LABEL}">{o["name"]}</text>\n'
        f'    <text x="290" y="208" font-family="{SF}" font-size="15" font-weight="400" fill="{C_SECOND}">pal404error@github</text>\n'
        f'    <rect x="290" y="226" width="110" height="4" rx="2" fill="url(#grad{i})"/>\n'
        f'  </g>\n'
    )

# Static grouped metrics list (right of the divider), Apple "Settings > About" style
metrics_svg = ""
row_h = 46
start_y = 140
sep_x1, sep_x2 = 520, 920
for idx, (label, val) in enumerate(metrics):
    y = start_y + idx * row_h
    metrics_svg += (
        f'  <text x="{sep_x1}" y="{y}" font-family="{SF}" font-size="16" font-weight="400" fill="{C_SECOND}">{label}</text>\n'
        f'  <text x="{sep_x2}" y="{y}" text-anchor="end" font-family="{SF}" font-size="17" font-weight="500" fill="{C_LABEL}">{val}</text>\n'
    )
    if idx < len(metrics) - 1:
        sy = y + 28
        metrics_svg += f'  <line x1="{sep_x1}" y1="{sy}" x2="{sep_x2}" y2="{sy}" stroke="{C_SEP}" stroke-width="1"/>\n'

svg = f'''<svg width="1000" height="560" viewBox="0 0 1000 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="system">
  <defs>
{defs}  </defs>

  <rect width="1000" height="560" fill="{C_BG}"/>
  <rect x="40" y="40" width="920" height="480" rx="28" fill="{C_MATERIAL}" stroke="{C_SEP}" stroke-width="1"/>
  <line x1="480" y1="110" x2="480" y2="500" stroke="{C_SEP}" stroke-width="1"/>

{os_groups}
{metrics_svg}</svg>
'''

with open("assets/neofetch.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print(f"apple-HIG v2 generated -> os={N} cycle={total:.1f}s stars={total_stars} repos={user['public_repos']} bytes={len(svg)}")
