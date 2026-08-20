import urllib.request, json, os, datetime

USER = "pal404error"
token = os.environ.get("GITHUB_TOKEN", "")
README = "README.md"

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

arch = open(".github/ascii/arch.txt", encoding="utf-8").read().rstrip("\n").split("\n")

pairs = [
    ("OS", "Arch Linux x86_64"),
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
w = max(len(k) for k, _ in pairs)
body = "\n".join(f"{k:<{w}}: {v}" for k, v in pairs)

block = "```text\n" + "\n".join(arch) + "\n\n" + "pal404error@arch\n" + "-" * 16 + "\n" + body + "\n```"

readme = open(README, encoding="utf-8").read()
start, end = "<!-- NEOMONO_START -->", "<!-- NEOMONO_END -->"
if start in readme and end in readme:
    pre = readme.split(start)[0]
    post = readme.split(end)[1]
    readme = pre + start + "\n" + block + "\n" + end + post
    open(README, "w", encoding="utf-8").write(readme)
    print(f"README ascii block updated -> stars={total_stars} repos={user['public_repos']} followers={user['followers']}")
else:
    print("MARKERS NOT FOUND")
