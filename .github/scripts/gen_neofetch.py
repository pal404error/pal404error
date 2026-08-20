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

arch_logo = [
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

def g_arch():
    lines = "\n".join(f'      <text x="40" y="{44 + i * 16}">{l}</text>' for i, l in enumerate(arch_logo))
    return f'    <g font-family="ui-monospace, Menlo, Consolas, monospace" font-size="12" fill="url(#lg)" xml:space="preserve">\n{lines}\n    </g>'

def g_apple():
    return (
        '    <g>'
        '      <path d="M200,92 C172,82 142,104 137,154 C133,194 152,238 197,252 C202,254 208,254 213,252 '
        'C258,238 277,194 273,154 C269,112 242,86 217,96 C212,82 206,84 200,92 Z" fill="#f5f5f7"/>'
        '      <path d="M204,90 C206,72 216,62 228,64 C226,80 216,92 204,90 Z" fill="#f5f5f7"/>'
        '      <circle cx="252" cy="150" r="22" fill="#0a0a0c"/>'
        '    </g>'
    )

def g_windows():
    return (
        '    <g>'
        '      <rect x="150" y="112" width="46" height="46" rx="4" fill="#F25022"/>'
        '      <rect x="206" y="112" width="46" height="46" rx="4" fill="#7FBA00"/>'
        '      <rect x="150" y="168" width="46" height="46" rx="4" fill="#00A4EF"/>'
        '      <rect x="206" y="168" width="46" height="46" rx="4" fill="#FFB900"/>'
        '    </g>'
    )

def g_ubuntu(c):
    return (
        f'    <g fill="none" stroke="{c}" stroke-width="13">'
        f'      <circle cx="200" cy="178" r="68"/>'
        f'      <circle cx="200" cy="178" r="38"/>'
        f'    </g>'
        f'    <g fill="{c}">'
        f'      <circle cx="200" cy="110" r="9"/>'
        f'      <circle cx="200" cy="246" r="9"/>'
        f'      <circle cx="132" cy="178" r="9"/>'
        f'      <circle cx="268" cy="178" r="9"/>'
        f'    </g>'
    )

def g_fedora(c):
    return (
        f'    <g>'
        f'      <circle cx="200" cy="178" r="70" fill="{c}"/>'
        f'      <text x="200" y="212" text-anchor="middle" font-family="Arial, sans-serif" '
        f'font-size="86" font-weight="700" fill="#ffffff">f</text>'
        f'    </g>'
    )

oses = [
    {"name": "Arch Linux", "accent": "#00F0FF", "logo": g_arch()},
    {"name": "macOS",      "accent": "#f5f5f7", "logo": g_apple()},
    {"name": "Ubuntu",     "accent": "#E95420", "logo": g_ubuntu("#E95420")},
    {"name": "Windows",    "accent": "#00A4EF", "logo": g_windows()},
    {"name": "Fedora",     "accent": "#3C6EB4", "logo": g_fedora("#3C6EB4")},
]

N = len(oses)
slot = 5.0
total = N * slot

os_groups = ""
for i, o in enumerate(oses):
    a = i * slot / total
    b = (i + 1) * slot / total
    keytimes = f"0;{a:.4f};{a:.4f};{b:.4f};1"
    init_op = "1" if i == 0 else "0"
    os_groups += (
        f'  <g opacity="{init_op}">\n'
        f'    <animate attributeName="opacity" dur="{total:.1f}s" repeatCount="indefinite" '
        f'keyTimes="{keytimes}" values="0;0;1;0;0"/>\n'
        f'    {o["logo"]}\n'
        f'    <text x="470" y="96" font-family="ui-monospace, Menlo, Consolas, monospace" '
        f'font-size="15" fill="{o["accent"]}">OS: {o["name"]}</text>\n'
        f'  </g>\n'
    )

kv_svg = (
    '  <g font-family="ui-monospace, Menlo, Consolas, monospace" font-size="15" xml:space="preserve">\n'
    '    <text x="470" y="48" fill="#f5f5f7">pal404error<tspan fill="#86868b">@github</tspan></text>\n'
    '    <text x="470" y="68" fill="#86868b">----------------</text>\n'
)
y = 120
for key, val in kv:
    kv_svg += f'    <text x="470" y="{y}"><tspan fill="url(#key)">{key}</tspan><tspan fill="#f5f5f7">: {val}</tspan></text>\n'
    y += 21
kv_svg += '  </g>'

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

{os_groups}
{kv_svg}</svg>
'''

with open("assets/neofetch.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("animated neofetch generated -> os_count=%d cycle=%.1fs metrics stars=%d repos=%d" % (N, total, total_stars, user["public_repos"]))
