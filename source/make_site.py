"""Generate index.html from washi.json so the palette table always equals the theme file."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, "..", "washi.json")))
C = T["colors"]
ROWS = [("canvas", "Paper", "The page. Fibres run through it."), ("sidebar", "Kozo", "Sidebar paper, a shade deeper."),
        ("messageSurface", "Label", "User bubbles, like a slip pasted on."), ("codeBackground", "Kraft", "Code blocks."),
        ("text", "Sumi", "Ink for reading."), ("textMuted", "Dry ink", "Secondary text."),
        ("accent", "Vermilion", "The hanko seal. Send, focus-adjacent, selected thread."), ("focus", "Indigo", "Focus rings, links, the composer's brush line."),
        ("warning", "Ochre", "Warnings."), ("error", "Madder", "Errors."),
        ("terminalBackground", "Ink slab", "Terminal."), ("border", "Fibre line", "Hairlines and borders.")]
rows = "".join(
    f'<button class="sw" data-hex="{C[k].upper()}" type="button"><i style="background:{C[k]}"></i><b>{n}</b><code>{C[k].upper()}</code><span>{d}</span></button>'
    for k, n, d in ROWS)
html = open(os.path.join(HERE, "index.template.html")).read().replace("{{PALETTE}}", rows)
open(os.path.join(HERE, "..", "index.html"), "w").write(html)
print("index.html", len(html))
