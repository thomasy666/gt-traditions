from hashlib import md5
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
FRAGMENTS = ROOT / "fragments"
URL_ATTRIBUTE = re.compile(r'(?<![\w-])(href|src|srcset)="([^"]+)"')
GITHUB_PAGES_PATH = "/gt-traditions/"

TITLE = "What’s All the Buzz at GT?"
CREDIT = "Sarah, Mina, Owen, Alex, and Thomas"
PAGES = [
    ("home", "Home", "/"),
    ("wreck", "The Wreck", "/wreck/"),
    ("buzz", "Buzz & the Jackets", "/buzz/"),
    ("crowd", "The Crowd", "/crowd/"),
    ("sources", "Sources", "/sources/"),
]
CHAPTERS = {
    "wreck": {
        "description": "How a beat-up student car became Tech’s most famous ride, and how students keep it on the road.",
        "label": "The Wreck",
        "image": "drive-wreck-banner.webp",
        "alt": "The gold and white Ramblin’ Wreck at a home game",
        "full_image": "drive-wreck-program.webp",
        "caption": "The Ramblin’ Wreck pictured in a Georgia Tech football program. <a href=\"/sources/#source-programs\">Football Programs and Guides</a>.",
        "stops": [
            ("year-1908", "Building the field"),
            ("year-1961", "From student cars to the Model A"),
            ("year-2024", "Students keep it on the road"),
            ("wreck-source-gap", "What our sources don’t show"),
        ],
        "next": ("Buzz & the Jackets", "/buzz/"),
    },
    "buzz": {
        "description": "How a yellow jacket went from student cartoons to a homemade costume and a crowd-surfing mascot.",
        "label": "Buzz & the Jackets",
        "image": "drive-buzz-banner.webp",
        "alt": "An illustration of Buzz alongside Central Florida’s mascot",
        "full_image": "drive-img_2704.webp",
        "caption": "Illustrated cover of the Central Florida game program, September 18, 1999. <a href=\"/sources/#source-program-1999\">Program citation</a>.",
        "stops": [
            ("year-1908", "Drawing a Tech identity"),
            ("year-1979", "A homemade costume"),
            ("year-1999", "From the sidelines to the cover"),
            ("year-2025", "Buzz in the stands and on the brand"),
            ("buzz-source-gap", "What our sources don’t show"),
        ],
        "next": ("The Crowd", "/crowd/"),
    },
    "crowd": {
        "description": "The songs, chants, and student section that make game day loud.",
        "label": "The Crowd",
        "image": "drive-crowd-banner.webp",
        "alt": "Mounted slides of students and marching band members in the stands",
        "full_image": "drive-img_0451.webp",
        "caption": "Band members and spectators, slides 669–672. <a href=\"/sources/#source-slides\">Dean of Students collection</a>.",
        "stops": [
            ("year-1923", "Learning what to sing"),
            ("year-1941", "Who gets a seat?"),
            ("year-1968", "When the stands became part of the show"),
            ("year-1995", "Back to Our Roots"),
            ("year-2024", "A full student section"),
            ("crowd-source-gap", "What our sources don’t show"),
        ],
        "next": ("Sources", "/sources/"),
    },
}
TIMELINE = [
    ("1908", "The Blue Print records that students helped build the athletic field.", (("wreck", "1908"),)),
    ("1914", "Students raise $2,200 for the athletic grounds.", (("wreck", "1914"),)),
    ("1923", "Frank Roman and Iver Granath’s Georgia Tech alma mater appears in print.", (("crowd", "1923"),)),
    ("1941", "The Technique prints student letters about overcrowded stands.", (("crowd", "1941"),)),
    ("1961", "The 1930 Ford Model A debuts as the official Ramblin’ Wreck.", (("wreck", "1961"),)),
    ("1968–70", "Slides record the band, cheerleaders, and student card displays.", (("crowd", "1968"),)),
    ("1979–80", "Richie Bland’s costume appears in 1979 and Buzz becomes official in 1980.", (("buzz", "1979"),)),
    ("1995", "The Blue Print looks back on Tech’s “Back to Our Roots” season.", (("crowd", "1995"),)),
    ("1999", "Buzz appears on the cover of a football program.", (("buzz", "1999"),)),
    ("2024", "Student season tickets sell out, and the Wreck breaks a mileage record.", (("crowd", "2024"), ("wreck", "2024"))),
]


def asset_version(name):
    return md5((ROOT / "assets" / name).read_bytes()).hexdigest()[:8]


def page(key, title, description, content):
    nav_items = []
    for page_key, label, href in PAGES:
        current = ' aria-current="page"' if page_key == key else ""
        nav_items.append(f'<a href="{href}"{current}>{escape(label)}</a>')
    nav = "\n      ".join(nav_items)
    page_title = TITLE if key == "home" else f"{title} | {TITLE}"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description)}">
  <meta name="theme-color" content="#131e31">
  <title>{escape(page_title)}</title>
  <link rel="icon" href="/assets/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&amp;family=DM+Sans:wght@400;600;700;800&amp;family=Graduate&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/style.css?v={asset_version("style.css")}">
  <script src="/assets/story.js?v={asset_version("story.js")}" defer></script>
</head>
<body>
<a href="#main" class="skip-link">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a href="/" class="wordmark"><span class="monogram" aria-hidden="true">GT</span><span class="wordmark-text">{TITLE}</span></a>
    <nav class="site-nav" aria-label="Main navigation">
      {nav}
    </nav>
  </div>
</header>
<main id="main">
{content}
</main>
<footer class="site-footer">
  <div class="wrap footer-inner">
    <div>
      <p class="footer-title">{TITLE}</p>
      <p class="footer-credit">A digital story by {CREDIT}.</p>
    </div>
    <nav class="footer-links" aria-label="Footer navigation">
      <a href="/#timeline">Timeline</a>
      <a href="/sources/">Sources &amp; credits</a>
    </nav>
  </div>
</footer>
</body>
</html>
"""


TIMELINE_SPAN = (1900, 2030)


def timeline_row(index, year, event, chapters):
    first_key, first_year = chapters[0]
    year_link = f"/{first_key}/#year-{first_year}"
    links = " ".join(
        f'<a href="/{key}/#year-{anchor}">{escape(CHAPTERS[key]["label"])}</a>'
        for key, anchor in chapters
    )
    start, end = TIMELINE_SPAN
    position = round((int(year[:4]) - start) / (end - start) * 100, 2)
    side = "above" if index % 2 == 0 else "below"
    return f"""<li style="--pos: {position}%">
    <button class="timeline-dot" type="button" data-side="{side}" aria-controls="timeline-card-{index}" hidden><span class="timeline-dot-label">{year}</span><span class="timeline-dot-mark" aria-hidden="true"></span></button>
    <div class="timeline-card" id="timeline-card-{index}">
      <a class="timeline-year" href="{year_link}">{year}</a>
      <span class="timeline-event">{escape(event)}</span>
      <span class="timeline-destinations">{links}</span>
    </div>
  </li>"""


def chapter_card(key, chapter):
    return f"""<a class="chapter-card" href="/{key}/">
  <div class="card-image"><img src="/assets/{chapter["image"]}" alt="" loading="lazy"></div>
  <div class="card-body">
    <h3>{escape(chapter["label"])}</h3>
    <p>{escape(chapter["description"])}</p>
    <span class="card-arrow" aria-hidden="true">↗</span>
  </div>
</a>"""


def homepage():
    cards = "\n".join(chapter_card(key, chapter) for key, chapter in CHAPTERS.items())
    years = "\n".join(timeline_row(index, *entry) for index, entry in enumerate(TIMELINE))
    return f"""<section class="cover" aria-labelledby="cover-title">
  <div class="cover-inner">
    <h1 id="cover-title" class="sr-only">{TITLE}</h1>
    <img src="/assets/cover.webp" srcset="/assets/cover-small.webp 1000w, /assets/cover.webp 2138w"
         sizes="(max-width: 680px) calc(100vw - 20px), (max-width: 920px) calc(100vw - 38px), (max-width: 1196px) calc(100vw - 76px), 1120px"
         width="2138" height="1246" fetchpriority="high"
         alt="Collage of Buzz at Bobby Dodd Stadium, a cheering student, the Ramblin’ Wreck, and fight-song sheet music. A digital story.">
    <div class="cover-actions">
      <a class="action action-primary" href="#chapters">Explore the chapters <span aria-hidden="true">↓</span></a>
      <a class="action action-link" href="#timeline">Jump to the timeline <span aria-hidden="true">↓</span></a>
    </div>
  </div>
</section>
<section class="story" id="story">
  <div class="wrap story-grid">
    <div>
      <h2>Who keeps the<br> traditions going?</h2>
      <p class="home-question">How have students kept up and changed Georgia Tech’s traditions over time through football?</p>
      <figure class="home-archive">
        <a href="/assets/drive-img_0456.webp"><img src="/assets/drive-buzz-1995.webp" width="1450" height="707" alt="Buzz presents the 1995 football team as the players gather at the field entrance" loading="lazy"></a>
        <figcaption>Buzz presents the 1995 Jackets. Chris Carr, <cite>Blue Print</cite>, 1996, p. 218. <a href="/sources/#source-memberg">Yearbook citation</a>.</figcaption>
      </figure>
    </div>
    <div class="story-copy">
      <p class="byline">By {CREDIT}</p>
      <p>If you’ve been to a home game at Bobby Dodd Stadium, you’ve probably seen the same few things happen every time. A gold and white 1930 Ford Model A drives onto the field with the team following it, Buzz gets the crowd going, and the student section sings a fight song that’s over 100 years old. A lot of us know these traditions really well, but not as many of us know where they came from or who kept them going.</p>
      <p>Students raised money, built things, drove the car, made the costume, and showed up to sing, even in seasons when the team wasn’t winning much. We used yearbooks, game programs, student newspapers, slides, and sheet music from the Georgia Tech Archives to follow three of these traditions from their beginnings to today.</p>
    </div>
  </div>
</section>
<section class="chapters" id="chapters" aria-labelledby="chapters-title">
  <div class="wrap explore-grid">
    <h2 id="chapters-title" class="explore-title"><span>Explore the</span> <span>traditions</span></h2>
    {cards}
  </div>
</section>
<section class="timeline" id="timeline" aria-labelledby="timeline-title">
  <div class="wrap">
    <h2 id="timeline-title">Timeline</h2>
    <p class="timeline-intro">Choose a year to see what happened, then jump to its story.</p>
    <div data-timeline>
      <ol class="timeline-list">{years}</ol>
      <div class="timeline-steps" hidden>
        <button type="button" data-step="-1"><span aria-hidden="true">←</span> Earlier</button>
        <span class="timeline-count" aria-live="polite"></span>
        <button type="button" data-step="1">Later <span aria-hidden="true">→</span></button>
      </div>
    </div>
  </div>
</section>"""


def chapter_page(key, chapter, content):
    links = "\n".join(f'<a href="#{anchor}">{escape(label)}</a>' for anchor, label in chapter["stops"])
    next_label, next_href = chapter["next"]
    return f"""<header class="chapter-banner banner-{key}">
  <div class="wrap chapter-banner-inner chapter-banner-grid">
    <div>
      <a class="breadcrumb" href="/#chapters">← All chapters</a>
      <h1>{escape(chapter["label"])}</h1>
      <p>{escape(chapter["description"])}</p>
    </div>
    <figure class="banner-image">
      <a href="/assets/{chapter["full_image"]}"><img src="/assets/{chapter["image"]}" alt="{escape(chapter["alt"])}" fetchpriority="high"></a>
      <figcaption>{chapter["caption"]}</figcaption>
    </figure>
  </div>
</header>
<div class="wrap article-layout">
  <article class="prose">{content}
    <a class="action action-primary next-chapter" href="{next_href}">{escape(next_label)} <span aria-hidden="true">→</span></a>
  </article>
  <aside class="article-aside">
    <p class="eyebrow">On this page</p>
    <nav aria-label="Chapter sections">{links}</nav>
  </aside>
</div>"""


def sources_page(content):
    return f"""<header class="chapter-banner">
  <div class="wrap chapter-banner-inner">
    <a class="breadcrumb" href="/#chapters">← All chapters</a>
    <h1>Sources &amp; credits</h1>
    <p>Archival records, reporting, and research behind our digital story.</p>
  </div>
</header>
<div class="wrap article-layout">
  <article class="prose">{content}</article>
  <aside class="article-aside">
    <p class="eyebrow">The digital story</p>
    <nav aria-label="Chapters">{''.join(f'<a href="/{key}/">{escape(chapter["label"])}</a>' for key, chapter in CHAPTERS.items())}</nav>
  </aside>
</div>"""


def write_page(path, markup, root_path=None):
    target = ROOT / path
    if root_path is None:
        depth = len(target.parent.relative_to(ROOT).parts)
        root_path = "../" * depth or "./"

    def resolve(url):
        if url.startswith("/") and not url.startswith("//"):
            return root_path + url[1:]
        return url

    def rewrite_attribute(match):
        name, value = match.groups()
        if name == "srcset":
            candidates = []
            for candidate in value.split(","):
                url, separator, descriptor = candidate.strip().partition(" ")
                candidates.append(resolve(url) + separator + descriptor)
            value = ", ".join(candidates)
        else:
            value = resolve(value)
        return f'{name}="{value}"'

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(URL_ATTRIBUTE.sub(rewrite_attribute, markup), encoding="utf-8")


def build():
    write_page("index.html", page("home", TITLE, "A student digital story about Georgia Tech football traditions.", homepage()))
    for key, chapter in CHAPTERS.items():
        content = (FRAGMENTS / f"{key}.html").read_text(encoding="utf-8")
        for marker in ("WRECK-COMPARE", "RAT-CAP", "BUZZ-GALLERY", "SONG-NOTES", "CARD-STUNT"):
            comment = f"<!-- {marker} -->"
            if comment in content:
                insert = (FRAGMENTS / f"{marker.lower()}.html").read_text(encoding="utf-8")
                content = content.replace(comment, insert)
        write_page(f"{key}/index.html", page(key, chapter["label"], chapter["description"], chapter_page(key, chapter, content)))
    sources = (FRAGMENTS / "sources.html").read_text(encoding="utf-8")
    write_page("sources/index.html", page("sources", "Sources & credits", "Research, archive collections, and credits.", sources_page(sources)))
    missing = page("404", "Page not found", "Return to the digital story.",
        '<section class="wrap timeline"><h1>Page not found</h1><p><a href="/">Return to the story</a></p></section>')
    # GitHub Pages serves this document at the original, possibly nested URL.
    write_page("404.html", missing, root_path=GITHUB_PAGES_PATH)


if __name__ == "__main__":
    build()
