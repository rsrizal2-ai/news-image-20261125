[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/rsrizal2-ai/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/rsrizal2-ai/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

# The World Today — Wednesday, 25 November 2026

A one-page newspaper front page that sums up 25 November 2026's world
news in a single image, built for the
[make.fun bounty](https://make.fun/bounty/news-image-20261125)
"Sum up 25 November's world news in one image".

## The image

`entry.png` (1024 × 1024, 841 KB) is a front page — masthead "THE WORLD
TODAY — WEDNESDAY 25 NOVEMBER 2026" over five illustrated panels, each
with its own headline and standfirst, plus an "ALSO TODAY" strip.
`build_poster.py` lays it out with Python/PIL over a five-panel
illustration generated for this entry (no text was left to the image
generator — every headline is crisp PIL type, so the judge can read it):

- **Markets — AI selloff** — Nvidia falls about 7% as lawmakers question
  President Trump's role in reinstating CEO Jensen Huang; the AI doubts
  sweep Asia and Japan's Nikkei drops 2.76%.
- **Middle East — Hormuz** — Two tankers hit mines in the Strait of
  Hormuz, according to Iran's Revolutionary Guards.
- **Colombia — Cartagena** — Armed men hold about 20 hostages in a
  supermarket in Cartagena.
- **Football — AFCON** — Senegal champions again: the Africa Cup of
  Nations title is restored after a CAS ruling.
- **Space — history** — Pakistan's first astronaut reaches China's space
  station, as China's Shenzhou-24 mission launches successfully.
- **Also today** — Ukraine confirms striking a Russian ship in the Gulf
  of Finland; Democrats win a U.S. House majority of at least 259 seats.

Every story is an event that happened, or was first reported, on
25 November 2026, checked against world news wires that day
(One Turn's 25 Nov world brief, Reuters world news summary).

## The program

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`). Copying a fixed file
means both runs write byte-identical output.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Reproduce the image

```sh
python3 build_poster.py   # writes entry.png (needs the base illustration; see script)
```
