#!/usr/bin/env python3
"""Turn an issue post into email-ready HTML for a Kit HTML block.

Usage: python3 scripts/build_email.py _posts/2026-11-26-slug.html
Writes email/<slug>.html (served at https://thedirtonfolsom.github.io/email/<slug>.html)
and prints the subject line and preview text.
"""
import os
import re
import sys

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    sys.exit("Needs beautifulsoup4: pip install beautifulsoup4 --break-system-packages")

SITE = "https://thedirtonfolsom.github.io"
INK, INK2, MUTED, LINE = "#17140F", "#44403C", "#57534E", "#E7E5E4"
ACCENT, SOFT = "#C2410C", "#FFF7ED"
DISPLAY = "'Arial Black', Arial, Helvetica, sans-serif"
BODY = "Arial, Helvetica, sans-serif"

CLASS_STYLES = {
    "story": f"padding:22px 0;border-bottom:1px solid {LINE};",
    "story__head": "",
    "story__num": f"font-family:{DISPLAY};font-size:28px;color:{ACCENT};",
    "story__body": "",
    "explainer": f"margin:18px 0 0;padding:16px 18px;background:{SOFT};border-radius:8px;",
    "explainer__title": f"font-family:{DISPLAY};font-size:17px;color:{INK};",
    "sources": f"font-size:14px;color:{MUTED};",
    "homes": "",
    "home-row": f"padding:14px 0;border-bottom:1px solid {LINE};",
    "home-row__top": "",
    "home-row__name": f"font-family:{DISPLAY};font-size:17px;color:{INK};",
    "home-row__price": f"font-weight:bold;font-size:17px;color:{INK};",
    "home-row__desc": f"margin-top:4px;font-size:16px;color:{INK2};line-height:1.55;",
    "callout": f"margin-top:28px;padding:20px;border:2px solid {INK};border-radius:8px;",
    "callout__label": f"font-family:{DISPLAY};font-size:13px;letter-spacing:2px;text-transform:uppercase;color:{ACCENT};",
    "callout__title": f"margin-top:8px;font-family:{DISPLAY};font-size:21px;color:{INK};line-height:1.25;",
    "callout__meta": f"margin-top:6px;font-size:15px;color:{MUTED};",
}
TAG_STYLES = {
    "h2": f"margin:34px 0 0;padding-bottom:8px;border-bottom:3px solid {INK};font-family:{DISPLAY};font-size:24px;line-height:1.2;color:{INK};",
    "h3": f"display:inline;margin:0;font-family:{DISPLAY};font-size:21px;line-height:1.3;color:{INK};",
    "p": f"margin:12px 0 0;font-size:17px;line-height:1.65;color:{INK};",
    "ul": "margin:10px 0 0;padding-left:22px;",
    "li": f"margin-top:6px;font-size:17px;line-height:1.6;color:{INK};",
    "a": f"color:{ACCENT};",
    "strong": f"color:{INK};",
}


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        sys.exit("No front matter found")
    fm, body = m.group(1), m.group(2)

    def field(name):
        mm = re.search(rf"^{name}:\s*(.+)$", fm, re.M)
        return mm.group(1).strip().strip('"') if mm else ""

    return {"title": field("title"), "dek": field("dek"), "issue": field("issue")}, body


def main(path):
    text = open(path, encoding="utf-8").read()
    meta, body = front_matter(text)
    m = re.match(r".*/(\d{4})-(\d{2})-(\d{2})-(.+)\.html$", path)
    y, mo, d, slug = m.groups()
    web_url = f"{SITE}/issues/{y}/{mo}/{d}/{slug}/"

    # Resolve Liquid links used in posts.
    body = re.sub(r"\{\{\s*'([^']*)'\s*\|\s*relative_url\s*\}\}", lambda mm: SITE + mm.group(1), body)

    soup = BeautifulSoup(body, "html.parser")
    for tag in soup.find_all(True):
        style = TAG_STYLES.get(tag.name, "")
        for cls in tag.get("class", []):
            style += CLASS_STYLES.get(cls, "")
        if tag.name == "aside":
            tag.name = "div"
        if tag.get("class"):
            del tag["class"]
        if tag.get("id"):
            del tag["id"]
        if style:
            tag["style"] = style + tag.get("style", "")
        if tag.name == "a" and tag.get("href", "").startswith("/"):
            tag["href"] = SITE + tag["href"]
    for top in soup.find_all("div"):
        spans = top.find_all("span", recursive=False)
        if len(spans) == 2 and "from $" in spans[1].get_text():
            spans[0].insert_after(" — ")
    content = str(soup)

    header = f"""
<div style="font-family:{BODY};color:{INK};max-width:640px;margin:0 auto;">
  <table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 18px;"><tr><td>
    <div style="font-family:{DISPLAY};font-size:11px;letter-spacing:5px;color:{INK};">THE</div>
    <div style="font-family:{DISPLAY};font-size:34px;line-height:1;color:{INK};letter-spacing:-1px;">DIRT</div>
    <div style="background:{ACCENT};color:#ffffff;font-family:{DISPLAY};font-size:9px;letter-spacing:3px;text-align:center;padding:3px 4px 2px;">ON FOLSOM</div>
  </td></tr></table>
  <div style="font-family:{DISPLAY};font-size:13px;letter-spacing:2px;text-transform:uppercase;color:{ACCENT};">Issue #{meta['issue']} · Folsom &amp; El Dorado Hills real estate</div>
  <h1 style="margin:10px 0 0;font-family:{DISPLAY};font-size:30px;line-height:1.1;color:{INK};">{meta['title']}</h1>
  <p style="margin:12px 0 0;font-size:18px;line-height:1.55;color:{INK2};">{meta['dek']}</p>
  <p style="margin:12px 0 0;font-size:15px;color:{MUTED};"><a href="{web_url}" style="color:{ACCENT};">Read this issue on the web</a></p>
"""
    footer = f"""
  <div style="margin-top:34px;padding-top:16px;border-top:1px solid {LINE};font-size:15px;line-height:1.6;color:{MUTED};">
    <p style="margin:0;font-size:15px;color:{MUTED};">Got a tip or a correction? Just reply to this email.</p>
    <p style="margin:10px 0 0;font-size:15px;color:{MUTED};">Forward this to a neighbor who'd want it. New readers can subscribe at <a href="{SITE}" style="color:{ACCENT};">thedirtonfolsom.github.io</a>.</p>
    <p style="margin:10px 0 0;font-size:13px;color:{MUTED};">The mailing address below belongs to our newsletter service, Kit. Anti-spam law requires every newsletter to list one. To reach us, email thedirtonfolsom@gmail.com or just reply to this email.</p>
  </div>
</div>
"""
    html = header + content + footer
    # One line, no indentation: pastes/types cleanly into Kit's HTML block.
    html = re.sub(r"\n\s*", "", html)
    os.makedirs("email", exist_ok=True)
    out = f"email/{slug}.html"
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {out} ({len(html):,} bytes)")
    print(f"Subject: {meta['title']}")
    print(f"Preview text: {meta['dek']}")
    print(f"Email URL: {SITE}/{out}")


if __name__ == "__main__":
    main(sys.argv[1])
