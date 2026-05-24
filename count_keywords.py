"""
pdf_keyword_search.py  —  Keyword inventory + KWIC extraction across multiple PDFs
-----------------------------------------------------------------------------------
Reads keywords from a two-column CSV (Category, Keyword) and searches all PDFs
in a folder, producing:

  keyword_matrix.csv    — one row per file; columns for each category (summed
                          counts) and each individual keyword
  keyword_details.csv   — one row per match: file | category | keyword | page |
                          excerpt (10 words each side)
  excerpts/             — one markdown file per category, all KWIC excerpts

CSV format (key_words_simple.csv)
----------------------------------
Two columns WITH a header row:
    Category, Keyword
    Buddhist tradition, Buddhism
    Buddhist tradition, Buddhist
    stupa variants, stupa
    stupa variants, stupas

Usage
-----
1. Edit the Configuration section below if needed.
2. Install dependency:
       pip install pdfplumber
3. Run:
       python pdf_keyword_search.py

Options
-------
CASE_SENSITIVE  : if False, matching ignores case (recommended)
WHOLE_WORD_ONLY : if True, "cat" won't match "catch" or "concatenate"
KWIC_WORDS      : number of words of context on each side of the match
"""

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    sys.exit("pdfplumber not found.  Run:  pip install pdfplumber")

# ── Configuration ─────────────────────────────────────────────────────────────

PDF_DIR       = "./standards_documents"   # folder containing your PDFs
KEYWORDS_FILE = "./keywords_simple.csv"  # CSV with headers: Category, Keyword
OUTPUT_DIR    = "."                        # where output files are written

CASE_SENSITIVE  = False   # True = exact case; False = ignore case
WHOLE_WORD_ONLY = True    # True = whole words only; False = substring matches
KWIC_WORDS      = 10      # words of context on each side of each match

# ── End configuration ──────────────────────────────────────────────────────────


# ── Keyword loading ────────────────────────────────────────────────────────────

def load_keywords(csv_path: Path) -> tuple[list[str], dict[str, str], list[str]]:
    """
    Parse the keywords CSV (header row: Category, Keyword).
    Returns:
      keywords   : ordered list of keyword strings
      kw_category: {keyword: category_label}
      categories : ordered unique list of category labels
    """
    keywords     = []
    kw_category  = {}
    cats_seen    = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            kw  = row.get("Keyword", "").strip()
            cat = row.get("Category", "").strip()
            if not kw:
                continue
            if not cat:
                cat = kw
            keywords.append(kw)
            kw_category[kw] = cat
            if cat not in cats_seen:
                cats_seen.append(cat)

    return keywords, kw_category, cats_seen


# ── Pattern building ───────────────────────────────────────────────────────────

def build_pattern(keyword: str) -> re.Pattern:
    escaped = re.escape(keyword)
    if WHOLE_WORD_ONLY:
        escaped = rf"\b{escaped}\b"
    flags = 0 if CASE_SENSITIVE else re.IGNORECASE
    return re.compile(escaped, flags)


# ── KWIC extraction ────────────────────────────────────────────────────────────

def extract_kwic(text: str, pattern: re.Pattern, n: int = 10) -> list[str]:
    """
    Return one KWIC string per match in text:
      '...word-n ... word-1 [KEYWORD] word+1 ... word+n...'
    Operates on whitespace tokens so bullet markers and abbreviation
    periods don't cause false splits.
    """
    tokens = [(m.group(), m.start(), m.end())
              for m in re.finditer(r'\S+', text)]
    if not tokens:
        return []

    token_strings = [t[0] for t in tokens]
    excerpts = []

    for match in pattern.finditer(text):
        match_start = match.start()
        match_end   = match.end()

        first_tok = next(
            (i for i, (_, ts, te) in enumerate(tokens) if ts <= match_start < te),
            None
        )
        last_tok = next(
            (i for i, (_, ts, te) in enumerate(tokens) if ts < match_end <= te),
            first_tok
        )
        if first_tok is None:
            continue
        if last_tok is None:
            last_tok = first_tok

        left_start  = max(0, first_tok - n)
        right_end   = min(len(tokens), last_tok + n + 1)

        left_ctx    = " ".join(token_strings[left_start:first_tok])
        keyword_hit = " ".join(token_strings[first_tok:last_tok + 1])
        right_ctx   = " ".join(token_strings[last_tok + 1:right_end])

        prefix  = "..." if left_start > 0             else ""
        suffix  = "..." if right_end  < len(tokens)   else ""
        excerpt = f"{prefix}{left_ctx} [{keyword_hit}] {right_ctx}{suffix}".strip()
        excerpts.append(excerpt)

    return excerpts


# ── PDF search ─────────────────────────────────────────────────────────────────

def search_pdf(pdf_path: Path,
               keywords: list[str],
               kw_category: dict[str, str],
               patterns: dict[str, re.Pattern]) -> dict | None:
    """
    Search one PDF. Returns:
      matrix  : {keyword: total_count}
      details : list of detail-row dicts (one per match instance)
    """
    matrix  = defaultdict(int)
    details = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                text = re.sub(r'[ \t]+', ' ', text)  # normalise whitespace

                for kw in keywords:
                    excerpts = extract_kwic(text, patterns[kw], KWIC_WORDS)
                    if excerpts:
                        matrix[kw] += len(excerpts)
                        for excerpt in excerpts:
                            details.append({
                                "file":     pdf_path.name,
                                "category": kw_category[kw],
                                "keyword":  kw,
                                "page":     page_num,
                                "excerpt":  excerpt,
                            })
    except Exception as exc:
        print(f"  WARNING: could not read {pdf_path.name}: {exc}")
        return None

    return {"matrix": dict(matrix), "details": details}


# ── Output writers ─────────────────────────────────────────────────────────────

def write_csv_matrix(rows: list[dict],
                     keywords: list[str],
                     categories: list[str],
                     kw_category: dict[str, str],
                     output_path: Path):
    """Matrix CSV: file | total | [category totals] | [keyword counts]"""
    cat_cols   = [f"CAT: {c}" for c in categories]
    fieldnames = ["file", "total_matches"] + cat_cols + keywords

    for row in rows:
        cat_sums = defaultdict(int)
        for kw in keywords:
            cat_sums[kw_category[kw]] += row.get(kw, 0)
        for c in categories:
            row[f"CAT: {c}"] = cat_sums[c]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Matrix CSV  → {output_path}")


def write_csv_details(rows: list[dict], output_path: Path):
    """Detail CSV: one row per match instance with KWIC excerpt."""
    fieldnames = ["file", "category", "keyword", "page", "excerpt"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Details CSV → {output_path}")


def write_markdown_files(rows: list[dict],
                         categories: list[str],
                         output_dir: Path):
    """
    One markdown file per category in output_dir/excerpts/.
    Within each file: sections by keyword, then by source file.
    """
    excerpts_dir = output_dir / "excerpts"
    excerpts_dir.mkdir(exist_ok=True)

    # Group rows: category → keyword → file → [excerpts]
    tree = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for row in rows:
        tree[row["category"]][row["keyword"]][row["file"]].append(
            (row["page"], row["excerpt"])
        )

    for category in categories:
        if category not in tree:
            continue

        # Sanitise category name for use as a filename
        safe_name = re.sub(r'[^\w\s-]', '', category).strip()
        safe_name = re.sub(r'[\s]+', '_', safe_name)
        md_path   = excerpts_dir / f"{safe_name}.md"

        lines = [f"# {category}\n"]

        for keyword, files in sorted(tree[category].items()):
            total = sum(len(v) for v in files.values())
            lines.append(f"## {keyword}  ({total} match{'es' if total != 1 else ''})\n")

            for filename, hits in sorted(files.items()):
                lines.append(f"### {filename}\n")
                for page, excerpt in sorted(hits, key=lambda x: x[0]):
                    lines.append(f"- **p. {page}** — {excerpt}\n")
                lines.append("")  # blank line between files

        md_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"  Markdown    → {md_path}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    pdf_dir    = Path(PDF_DIR)
    kw_file    = Path(KEYWORDS_FILE)
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not pdf_dir.exists():
        sys.exit(f"PDF_DIR not found: {pdf_dir.resolve()}")
    if not kw_file.exists():
        sys.exit(f"Keywords file not found: {kw_file.resolve()}")

    keywords, kw_category, categories = load_keywords(kw_file)
    if not keywords:
        sys.exit(f"No keywords found in {kw_file} — is the file empty?")

    pdf_files = sorted(pdf_dir.rglob("*.pdf"))
    if not pdf_files:
        sys.exit(f"No .pdf files found in {pdf_dir.resolve()}")

    patterns = {kw: build_pattern(kw) for kw in keywords}

    print(f"\nSearching {len(pdf_files)} PDF(s) for {len(keywords)} keyword(s) "
          f"in {len(categories)} category/categories...")
    print(f"  Case-sensitive : {CASE_SENSITIVE}")
    print(f"  Whole-word     : {WHOLE_WORD_ONLY}")
    print(f"  KWIC window    : ±{KWIC_WORDS} words\n")

    matrix_rows = []
    all_details = []
    skipped     = []

    for pdf_path in pdf_files:
        print(f"  {pdf_path.name}")
        result = search_pdf(pdf_path, keywords, kw_category, patterns)
        if result is None:
            skipped.append(pdf_path.name)
            continue

        row = {"file": pdf_path.name, "total_matches": sum(result["matrix"].values())}
        for kw in keywords:
            row[kw] = result["matrix"].get(kw, 0)
        matrix_rows.append(row)
        all_details.extend(result["details"])

    all_details.sort(key=lambda r: (r["category"], r["keyword"], r["file"], r["page"]))

    print(f"\nWriting output to {output_dir.resolve()}/")
    write_csv_matrix(matrix_rows, keywords, categories, kw_category,
                     output_dir / "keyword_matrix.csv")
    write_csv_details(all_details, output_dir / "keyword_details.csv")
    write_markdown_files(all_details, categories, output_dir)

    # ── Console summary ───────────────────────────────────────────────────────
    total_hits      = sum(r["total_matches"] for r in matrix_rows)
    files_with_hits = sum(1 for r in matrix_rows if r["total_matches"] > 0)

    print(f"\n── Summary ───────────────────────────────────────────")
    print(f"  PDFs scanned      : {len(pdf_files)}")
    print(f"  PDFs with hits    : {files_with_hits}")
    print(f"  Total matches     : {total_hits}")
    if skipped:
        print(f"  Skipped (errors)  : {len(skipped)}")
        for name in skipped:
            print(f"    • {name}")

    print(f"\nTop files by match count:")
    for row in sorted(matrix_rows, key=lambda r: r["total_matches"], reverse=True)[:10]:
        print(f"  {row['total_matches']:>5}  {row['file']}")

    print(f"\nMatches per category:")
    cat_totals = defaultdict(int)
    for row in matrix_rows:
        for kw in keywords:
            cat_totals[kw_category[kw]] += row.get(kw, 0)
    for c in categories:
        print(f"  {cat_totals[c]:>5}  {c}")

    print(f"\nMatches per keyword:")
    kw_totals = defaultdict(int)
    for row in matrix_rows:
        for kw in keywords:
            kw_totals[kw] += row.get(kw, 0)
    for kw in keywords:
        print(f"  {kw_totals[kw]:>5}  {kw}  ({kw_category[kw]})")


if __name__ == "__main__":
    main()