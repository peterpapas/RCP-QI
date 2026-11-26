# Unpublished manuscript scaffold

`main.tex` is a working research draft, not a preprint or publication. It cites only traceable primary sources in `references.bib` and describes the current negative controls without claiming a new speedup. Author and venue details should be confirmed before any submission. No peer-reviewed paper or preprint has been published; this draft is disclosed with the public research archive.

If a local LaTeX distribution is available, build with `pdflatex main.tex`, `bibtex main`, then `pdflatex main.tex` twice. The Python and Lean CI pipelines do not require LaTeX.
