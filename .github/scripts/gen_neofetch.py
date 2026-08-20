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

kv = [
    ("Host", "github.com"),
    ("Uptime", age),
    ("Followers", str(user["followers"])),
    ("Following", str(user["following"])),
    ("Repos", str(user["public_repos"])),
    ("Stars", str(total_stars)),
    ("Top Lang", top_lang),
    ("Joined", created),
    ("Last Active", updated),
]

MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

# Official neofetch ASCII art (from the neofetch source), one file per distro.
oses = [
    {"file": ".github/ascii/arch.txt",    "name": "Arch Linux", "accent": "#00F0FF"},
    {"file": ".github/ascii/ubuntu.txt",  "name": "Ubuntu",      "accent": "#E95420"},
    {"file": ".github/ascii/fedora.txt",  "name": "Fedora",      "accent": "#3C6EB4"},
    {"file": ".github/ascii/windows.txt", "name": "Windows",     "accent": "#00A4EF"},
]

def load_art(path):
    with open(path, encoding="utf-8") as f:
        return [ln.rstrip("\n") for ln in f]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

N = len(oses)
slot = 5.0
total = N * slot

os_groups = ""
for i, o in enumerate(oses):
    art = load_art(o["file"])
    a = i * slot / total
    b = (i + 1) * slot / total
    keytimes = f"0;{a:.4f};{a:.4f};{b:.4f};1"
    init = "1" if i == 0 else "0"
    lines_svg = "\n".join(
        f'      <text x="40" y="{44 + k * 15}">{esc(ln)}</text>' for k, ln in enumerate(art)
    )
    os_groups += (
        f'  <g opacity="{init}">\n'
        f'    <animate attributeName="opacity" dur="{total:.1f}s" repeatCount="indefinite" '
        f'keyTimes="{keytimes}" values="0;0;1;0;0"/>\n'
        f'    <g font-family="{MONO}" font-size="12" fill="{o["accent"]}" xml:space="preserve">\n{lines_svg}\n    </g>\n'
        f'    <text x="470" y="96" font-family="{MONO}" font-size="15" fill="{o["accent"]}">OS: {o["name"]}</text>\n'
        f'  </g>\n'
    )

kv_svg = (
    f'  <g font-family="{MONO}" font-size="15" xml:space="preserve">\n'
    f'    <text x="470" y="48" fill="#f5f5f7">pal404error<tspan fill="#86868b">@github</tspan></text>\n'
    f'    <text x="470" y="68" fill="#86868b">----------------</text>\n'
)
y = 120
for key, val in kv:
    kv_svg += f'    <text x="470" y="{y}"><tspan fill="url(#key)">{key}</tspan><tspan fill="#f5f5f7">: {val}</tspan></text>\n'
    y += 21
kv_svg += '  </g>'

svg = f'''<svg width="1000" height="380" viewBox="0 0 1000 380" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="neofetch">
  <defs>
    <linearGradient id="key" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2997ff"/>
      <stop offset="1" stop-color="#A855F7"/>
    </linearGradient>
  </defs>

  <rect width="1000" height="380" rx="18" fill="#0a0a0c" stroke="#1d1d1f" stroke-width="1"/>

{os_groups}
{kv_svg}</svg>
'''

with open("assets/neofetch.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print(f"official neofetch ascii restored -> os={N} cycle={total:.1f}s stars={total_stars} repos={user['public_repos']}")
