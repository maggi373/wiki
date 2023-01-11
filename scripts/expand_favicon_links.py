import sys
import re
from pathlib import Path

if len(sys.argv) != 3:
    sys.exit(f'''Usage: {sys.argv[0]} IN OUT

Expands the favicon links in the markdown file named IN, and writes the output
to OUT.

A favicon link has the following syntax:
    {{siteid:url}}

Where `siteid` is the id of the site, and url is the url of the link.

These will be replaced with an image of the website's favicon which links to
the url.
''')

inFile = sys.argv[1]
outFile = sys.argv[2]

short2long = {
"gh": "github",
"cb": "codeberg",
"mr": "modrinth",
"cf": "curseforge",
"mcf": "minecraftforum",
}

text = open(inFile, "r", encoding="utf8").read()
outText = ""
pos = 0

outText += f'''<!-- 
    DO NOT EDIT THIS FILE! It was generated from {inFile} using expand_mod_links.py
-->

'''

p = re.compile(r'{(.*?):(.*?)}')

while True:
    m = p.search(text, pos)
    
    if not m:
        break
    
    site = m[1]
    
    siteLong = short2long.get(site) or site
    
    iconPath = Path(outFile).parent / "img" / "favicon" / (siteLong + ".png")
    
    if not iconPath.exists():
        sys.exit(f"Unknown site `{site}` in favicon link {m[0]} (couldn't find {iconPath})")
    
    url = m[2]
    
    outText += text[pos:m.start()]
    
    outText += f"[![icon-{siteLong}](img/favicon/{siteLong}.png)]({url})"
    
    pos = m.end()
    
outText += text[pos:]

with open(outFile, "w", encoding="utf8") as fp:
    fp.write(outText)
