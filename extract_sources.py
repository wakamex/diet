#!/usr/bin/env python3
"""Extract Stigler diet sources via Firecrawl v2 API."""
import json
import os
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

API_KEY = os.environ["FIRECRAWL_API_KEY"]
OUT_DIR = Path("/code/diet/sources")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SOURCES = [
    ("01_wikipedia_stigler_diet", "https://en.wikipedia.org/wiki/Stigler_diet"),
    ("02_stiglers_diet_problem_revisited_2001", "https://mate.unipv.it/~gualandi/famo2conti/papers/stigler.pdf"),
    ("03_google_or_tools_stigler", "https://developers.google.com/optimization/lp/stigler_diet"),
    ("04_frontiers_2018_lp_diet_review", "https://www.frontiersin.org/articles/10.3389/fnut.2018.00048/full"),
    ("05_neos_guide_diet_problem", "https://neos-guide.org/case-studies/om/the-diet-problem/"),
    ("06_cambridge_diet_history", "http://www.statslab.cam.ac.uk/~rrw1/opt/diet_history.html"),
    ("07_springer_2025_balancing_health_sustainability", "https://link.springer.com/article/10.1007/s11831-025-10457-8"),
    ("08_wiley_2023_systematic_review_lp_diet", "https://onlinelibrary.wiley.com/doi/10.1155/2023/1271115"),
    ("09_mdpi_2015_low_price_low_climate", "https://www.mdpi.com/2071-1050/7/9/12837/htm"),
    ("10_wikipedia_planetary_health_diet", "https://en.wikipedia.org/wiki/Planetary_health_diet"),
    ("11_brazilian_carbon_footprint_meals", "https://www.sciencedirect.com/science/article/pii/S1877050922019019"),
    ("12_arxiv_2025_decision_space_diversity", "https://arxiv.org/html/2508.07077"),
    ("13_frontiers_2026_multi_objective_national_diet", "https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2026.1758724/full"),
    ("14_pmc_spanish_multi_objective_diet", "https://pmc.ncbi.nlm.nih.gov/articles/PMC7696294/"),
    ("15_pmc_planetary_boundaries_diet", "https://pmc.ncbi.nlm.nih.gov/articles/PMC10927557/"),
    ("16_google_blog_2014_ten_cent_diet", "https://developers.googleblog.com/2014/09/sudoku-linear-optimization-and-ten-cent.html"),
    ("17_grokipedia_stigler_diet", "https://grokipedia.com/page/Stigler_diet"),
    ("18_mit_blossoms_optimizing_diet", "https://blossoms.mit.edu/videos/lessons/optimizing_your_diet_what_linear_programming_can_tell_you"),
    ("19_eat_lancet_summary_report", "https://eatforum.org/eat-lancet/summary-report/"),
    ("20_eat_lancet_planetary_health_diet", "https://eatforum.org/eat-lancet/the-planetary-health-diet/"),
]


def fetch(slug: str, url: str) -> tuple[str, str, str | None, int]:
    body = json.dumps({"url": url, "formats": ["markdown"], "onlyMainContent": True}).encode()
    req = urllib.request.Request(
        "https://api.firecrawl.dev/v2/scrape",
        data=body,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            payload = json.loads(resp.read())
        if not payload.get("success"):
            return slug, url, f"API success=false: {payload.get('error', payload)[:200]}", 0
        md = (payload.get("data") or {}).get("markdown") or ""
        if not md.strip():
            return slug, url, "empty markdown", 0
        meta = (payload.get("data") or {}).get("metadata") or {}
        title = meta.get("title") or meta.get("ogTitle") or slug
        header = f"# Source: {title}\n\n- URL: {url}\n- Slug: {slug}\n\n---\n\n"
        (OUT_DIR / f"{slug}.md").write_text(header + md, encoding="utf-8")
        return slug, url, None, len(md)
    except urllib.error.HTTPError as e:
        return slug, url, f"HTTP {e.code}: {e.read()[:200].decode('utf-8', 'ignore')}", 0
    except Exception as e:
        return slug, url, f"{type(e).__name__}: {e}", 0


def main() -> int:
    failures = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futures = {ex.submit(fetch, slug, url): (slug, url) for slug, url in SOURCES}
        for fut in as_completed(futures):
            slug, url, err, n = fut.result()
            if err:
                print(f"FAIL  {slug}  ({url})  -> {err}", flush=True)
                failures.append((slug, url, err))
            else:
                print(f"OK    {slug}  ({n} chars)", flush=True)
    if failures:
        print(f"\n{len(failures)} failures:")
        for slug, url, err in failures:
            print(f"  {slug}: {err}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
