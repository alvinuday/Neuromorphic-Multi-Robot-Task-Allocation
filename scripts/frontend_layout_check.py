from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SCREENSHOTS = DOCS / "screenshots"


def check_panel_overflow(page, selector: str) -> dict:
    return page.evaluate(
        """
        (sel) => {
          const root = document.querySelector(sel);
          if (!root) return {missing: true};
          const style = getComputedStyle(root);
          const vr = root.getBoundingClientRect();
          const nodes = Array.from(root.querySelectorAll('canvas, svg, table, .card, .stats-bar, .step-header, h1, h2, h3, p, div'));
          let overflowCount = 0;
          for (const el of nodes) {
            const r = el.getBoundingClientRect();
            if (r.width <= 0 || r.height <= 0) continue;
            if (r.left < vr.left - 6 || r.right > vr.right + 6) overflowCount += 1;
          }
          return {
            overflowCount,
            needsScroll: root.scrollHeight > root.clientHeight + 2,
            canScroll: !['hidden','clip'].includes(style.overflowY),
          };
        }
        """,
        selector,
    )


def run_checks() -> list[dict]:
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)

    pages = [
        ("slide_deck", (ROOT / "SlideDeck" / "OIM_MRTA_Slides.html").resolve().as_uri()),
        ("viz", (ROOT / "oim_mrta_viz.html").resolve().as_uri()),
    ]
    viewports = {
        "desktop": {"width": 1920, "height": 1080},
        "laptop": {"width": 1366, "height": 768},
        "mobile": {"width": 390, "height": 844},
    }

    results: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for page_name, url in pages:
            for vp_name, vp in viewports.items():
                context = browser.new_context(viewport=vp)
                page = context.new_page()
                page.goto(url, wait_until="load")
                page.wait_for_timeout(300)

                max_overflow = 0
                blocking_scroll = 0
                checked_views = 0

                if page_name == "slide_deck":
                    for slide in range(1, 15):
                        page.evaluate(f"goTo({slide})")
                        page.wait_for_timeout(120)
                        data = check_panel_overflow(page, ".slide.active")
                        max_overflow = max(max_overflow, data.get("overflowCount", 0))
                        if data.get("needsScroll") and not data.get("canScroll"):
                            blocking_scroll += 1
                        checked_views += 1
                else:
                    for step in range(0, 6):
                        page.evaluate(f"setStep({step})")
                        page.wait_for_timeout(120)
                        data = check_panel_overflow(page, ".viz-panel.active")
                        max_overflow = max(max_overflow, data.get("overflowCount", 0))
                        if data.get("needsScroll") and not data.get("canScroll"):
                            blocking_scroll += 1
                        checked_views += 1

                screenshot_path = SCREENSHOTS / f"{page_name}_{vp_name}.png"
                page.screenshot(path=str(screenshot_path), full_page=True)

                body_overflow = page.evaluate("""() => getComputedStyle(document.body).overflow""")
                has_doc_overflow = page.evaluate(
                    """() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 2"""
                )

                results.append(
                    {
                        "page": page_name,
                        "viewport": vp_name,
                        "viewport_px": vp,
                        "bodyOverflow": body_overflow,
                        "hasHorizontalDocOverflow": bool(has_doc_overflow),
                        "maxOverflowCount": max_overflow,
                        "unscrollableViews": blocking_scroll,
                        "checkedViews": checked_views,
                        "screenshot": str(screenshot_path.relative_to(ROOT)),
                        "pass": (not has_doc_overflow) and blocking_scroll == 0,
                    }
                )

                context.close()

        browser.close()

    return results


def main() -> None:
    results = run_checks()
    out = DOCS / "frontend_test_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote {out}")
    for row in results:
        print(
            row["page"],
            row["viewport"],
            "pass=" + str(row["pass"]),
            "maxOverflow=" + str(row["maxOverflowCount"]),
            "unscrollable=" + str(row["unscrollableViews"]),
        )


if __name__ == "__main__":
    main()
