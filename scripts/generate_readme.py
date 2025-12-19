import os
import re

COMPANIES_DIR = "stories"
README_PATH = "stories.md"

def slugify(title: str) -> str:
    title = title.lower()
    title = re.sub(r"[^\w\s-]", "", title)
    title = re.sub(r"\s+", "-", title)
    return title

lines = [
    "# Interview Stories\n",
    "\n",
    "A curated set of real-world engineering stories structured for behavioral interviews.\n",
    "Each story highlights ownership, technical judgment, collaboration, and impact.\n",
    "\n",
    "## 📂 Companies\n\n"
]

for filename in sorted(os.listdir(COMPANIES_DIR)):
    if not filename.endswith(".md"):
        continue

    path = os.path.join(COMPANIES_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    company_match = re.search(r"^##\s+(.+)", content, re.MULTILINE)
    if not company_match:
        continue

    company_name = company_match.group(1).strip()
    lines.append(f"### {company_name}\n\n")

    for story in re.findall(r"^###\s+(.+)", content, re.MULTILINE):
        anchor = slugify(story)
        lines.append(
            f"- [{story}](./{COMPANIES_DIR}/{filename}#{anchor})\n"
        )

    lines.append("\n")

with open(README_PATH, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("README.md generated successfully.")
