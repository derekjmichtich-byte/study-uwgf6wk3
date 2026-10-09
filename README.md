# Practice pages

Static study site. Data lives in `site.json`; `build_site.py` renders the index pages.

## Add a new packet
```
./add_item.py --kid eli --title "Spelling list 5" --subject Spelling --date 2026-10-12 \
  --html /path/to/practice.html --pdf /path/to/printable.pdf [--slug spelling-list-5]
./publish.sh "Add Eli spelling list 5"
```
`add_item.py` copies files into `<kid>/` with kebab-case names, removes any email address, adds a noindex meta tag, refuses files containing private strings
(PDFs are checked with pdftotext/pdfinfo and never edited), and updates `site.json`.
`publish.sh` rebuilds, scans for private strings, commits, and pushes. Pages updates in ~1 minute.

Privacy: first names only; no school, teacher, or contact info.

## Re-copy rebuilt practice pages (same slugs)
`./sync_practice_pages.py` copies the rebuilt practice pages over their existing site copies (same scrubbing).
`/workspace/practice/reporting/enable_reporting.sh <URL|off>` does rebuild + sync + publish in one go.
Published pages contain the reporting URL + shared token when reporting is ON (unavoidable for a static site),
never a recipient email address.
