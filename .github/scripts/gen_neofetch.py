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
    ("OS", "GitHub Profile"),
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

logo = [
    "                   -",
    "                  .o+`",
    "                 `ooo/",
    "                `+oooo:",
    "               `+oooooo:",
    "               -+oooooo+:",
    "             `/:-:++oooo+:",
    "            `/++++/+++++++:",
    "           `/++++++++++++++:",
    "          `/+++ooooooooooooo/`",
    "         ./ooosssso++osssssso+`",
    "        .oossssso-````/ossssss+`",
    "       -osssssso.      :ssssssso.",
    "      :osssssss/        osssso+++.`",
    "     /ossssssss/        +ssssoooo/-",
    "   `/ossssso+/:-        -:/+osssso+-",
    "  `+sso+:-`   `-/ooooo+/::::::::",
    " `++:.`                       `.-/+",
    " .`",
]

logo_svg = "\n".join(f'    <text x="40" y="{44 + i*16}">{l}</text>' for i, l in enumerate(logo))

info_svg = (
    '    <text x="470" y="48" fill="#f5f5f7">pal404error<tspan fill="#86868b">@github</tspan></text>\n'
    '    <text x="470" y="68" fill="#86868b">----------------</text>\n'
)
y = 96
for key, val in kv:
    info_svg += f'    <text x="470" y="{y}"><tspan fill="url(#key)">{key}</tspan><tspan fill="#f5f5f7">: {val}</tspan></text>\n'
    y += 22

svg = f'''<svg width="1000" height="380" viewBox="0 0 1000 380" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="neofetch">
  <defs>
    <linearGradient id="lg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#00F0FF"/>
      <stop offset="1" stop-color="#A855F7"/>
    </linearGradient>
    <linearGradient id="key" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2997ff"/>
      <stop offset="1" stop-color="#A855F7"/>
    </linearGradient>
  </defs>

  <rect width="1000" height="380" rx="18" fill="#0a0a0c" stroke="#1d1d1f" stroke-width="1"/>

  <g font-family="ui-monospace, 'SF Mono', Menlo, Consolas, monospace" font-size="12" fill="url(#lg)" xml:space="preserve">
{logo_svg}
  </g>

  <g font-family="ui-monospace, 'SF Mono', Menlo, Consolas, monospace" font-size="15" xml:space="preserve">
{info_svg}  </g>
</svg>
'''

with open("assets/neofetch.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("neofetch.svg generated ->", f"followers={user['followers']} stars={total_stars} repos={user['public_repos']} top={top_lang}")
