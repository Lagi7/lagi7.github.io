# Portfolio

Łagi's projects page: two avatars, the name "Łagi", the motto "Amalgamator of sprites, tailor
of rules.", and nine square buttons that each open a project page (Houses of Fading Suns, RUST,
Nevsky: Swantopolk II, Bitter Heretic, Age of Wonders 1 art, War1gus, Burning Banners: Elves,
Aethra Chronicles, Cyclades variant).

It is published in two places:

- **https://lagi7.github.io**: public, from this repository (GitHub Pages).
- **https://claude.ai/artifact/FM6WqrhaxD1JxakZQAzHcj**: private until shared from the page's Share menu.

## Folders

| Path | What it is |
|---|---|
| `page.html` | The page itself, as published on claude.ai. It has no `<html>`/`<head>` tags because claude.ai adds them. The Morpheus font is embedded in it. |
| `index.html` | The same page wrapped as a normal web page for GitHub Pages. Generated: do not edit it by hand. |
| `img/` | Pictures the page uses. |
| `source/` | The two original avatar pictures, the name design (`name-design.png`), the drawn name (`name.svg`) and the Bitter Heretic screenshots (`bitter-heretic-screen.webp` gives that project its tile and page picture; `bitter-heretic-wheel.png` shows the weapon wheel). |
| `fonts/` | Morpheus's readme and licence note (the font file itself is kept out of the repository). Shareware by Kiwi Media: the author asks $5 if you like it. |
| `tools/make_images.py` | Rebuilds everything in `img/` from the original art in the Desktop project folders. |
| `tools/build_site.py` | Rebuilds `index.html` from `page.html`. |
| `tools/knight_from_design.py` | Reads the knight avatar back, pixel by pixel, from the design screenshot `source/avatar-knight-design.png` and saves `img/av-knight-design.png`, the avatar used in the header. |

## Changing the page

1. Edit `page.html` (or ask Claude Code to, in a session opened in this folder).
2. Run `python tools/build_site.py` to rebuild `index.html`.
3. Commit and push with GitHub Desktop. GitHub Pages updates https://lagi7.github.io within a minute or two.
4. To update the claude.ai copy as well, ask Claude to republish `page.html` to
   https://claude.ai/artifact/FM6WqrhaxD1JxakZQAzHcj so it keeps the same link.

## Rebuilding the pictures

    python tools/make_images.py

It reads the art from `Desktop/FadingSuns`, `Desktop/nevsky`, `Desktop/Age of Wonders 1`
and `Desktop/stare z pulpitu`, and needs Pillow (`pip install pillow`).

The name "Łagi" in the header is one inline SVG drawn from the Morpheus letter outlines, plus the
changes from the design in `source/name-design.png`: the two slashes of the Ł (traced from that
image and smoothed), the A's two bars moved apart, and the upright line inside the G. A copy of the
drawing is in `source/name.svg`.
