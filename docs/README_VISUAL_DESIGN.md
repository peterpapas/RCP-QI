# README visual design and figure provenance

This is a presentation update to a **suspended** research archive. It does not add a quantum result, change a historical experiment or reopen V11.

## Audit and before/after

The previous README was a concise text entry point with a status note, four findings and an archive navigation table. The repository already contained valid V1/V2 plots and V5.1 classical SAT figures, but their styles differed and the original recursive hypothesis had no single prominent illustration. The post-publication [partial-search correction](../research/corrections/FINAL_CORRECTION_REPORT.md) had a comparison plot, but the front page did not visually distinguish the V3 bit-only control from intra-block diffusion.

The redesigned README opens with the research question and a five-stage original-hypothesis illustration, then presents supported findings and four source-backed figures. Its timeline routes readers to the full V1–V10 registry. The original published text remains in [README_AT_PUBLICATION.md](../README_AT_PUBLICATION.md); all old plots and raw files remain in place. The new charts are **presentation derivatives**, not new experiments.

## Visual language

Every asset uses a self-contained midnight-navy canvas so it remains legible in GitHub light and dark themes. Cyan means candidate information or a supported signal; blue means established search operations; violet means analytical or structural relationships; amber marks barriers, hypothetical access or negative limitations. Text and numeric labels supplement every colour distinction. Arial/sans-serif text, high-contrast labels, restrained grids and explicit units keep the figures readable at typical desktop widths. Each of the eight visuals has a narrow-screen SVG selected by GitHub-supported `<picture>` / `<source media>` markup. The text captions and alternative text remain available when graphics are scaled or unavailable.

## Asset register

| Asset | Classification | Evidence and boundary |
| --- | --- | --- |
| [Hero banner](assets/branding/hero-banner.svg) | Conceptual illustration | Original states, waveform and path; the amber cost label prevents reading the path as a proved algorithm. |
| [Recursive partitioning](assets/concepts/recursive-quantum-partitioning.svg) | Conceptual illustration | Unique-solution complementarity, proposed interference and a conditional square-root cost model. Highlighted branch is hypothetical. |
| [Research findings](assets/concepts/research-findings.svg) | Conceptual evidence summary | Distinguishes established/scoped results, absent claims and open questions. Exact proof and experiment scopes remain in the linked catalogue. |
| [V1 bias](assets/figures/interference-bias.svg) | Analytical prediction + archived statevector result | [`results/one_iteration.json`](../results/one_iteration.json): points at `N=4…256`, formula curve through `N=4096`. No sampled shots or hardware. The right axis shows bias above random guessing on a logarithmic scale. |
| [Partial-search comparison](assets/figures/partial-search-comparison.svg) | Analytical threshold count + archived statevector verification + published operator family | [Correction thresholds](../results/corrections/partial_search_20261127/thresholds.csv), [V3 bit-only control](../results/phase2_partition_register.json). `N=256` bars are one-shot minima in a defined global/local/final-global family; exact-item Grover is a different output task. V3 was tested at `N=4…64`, never at `N=256`. |
| [Query scaling](assets/figures/query-complexity-scaling.svg) | Analytical asymptotic illustration + hypothetical comparison | Left: classical `N`, near-certain full Grover `π√N/4`, [Korepin two-block](../research/corrections/PARTIAL_SEARCH_PRIOR_ART.md) `π√N/(4√2)` leading coefficients. Right: `n` ideal partition decisions from an **unavailable cheap oracle**. Panels use different access models; no observed runtime is plotted. |
| [Recursive cost](assets/figures/recursive-query-cost.svg) | Conditional analytical illustration | `N=2¹⁶`, assumed `C(m)=√m` (illustrative coefficient 1), per-stage and cumulative cost. It excludes preparation, errors and final verification. |
| [Research timeline](assets/timeline/research-timeline.svg) | Conceptual archive map | Version groups and outcomes checked against the [roadmap](../research/roadmap.md) and [registry](../research/experiment_registry.md). It does not imply continuous algorithmic progress. |

The narrow-screen companions use the same names with `-mobile.svg` before the extension. They reflow or simplify the same statements; they are not additional evidence. The mobile scaling chart omits the separate hypothetical panel and states that model as text, while the desktop chart keeps the models in separate panels.

## Rebuild and verify

Python 3.12, locked `uv` dependencies and Matplotlib already belong to the project; no new runtime dependency was added. From the root:

```sh
uv sync --locked
uv run python scripts/build_readme_figures.py
uv run python scripts/build_readme_figures.py --check
```

The script regenerates the four desktop charts and four narrow-screen variants in `docs/assets/figures/`. It never rewrites `results/`. The editable conceptual SVGs are version-controlled in `docs/assets/branding/`, `concepts/` and `timeline/`. [`manifest.json`](assets/figures/manifest.json) records SHA-256 and byte lengths for three archived inputs, eight generated SVGs and eight static SVGs. `--check` verifies these bytes, SVG title/description elements and README image paths/alternative text. Platform-dependent regenerated SVG bytes are not claimed to match a different font stack; the committed integrity check covers the published assets. Analytic values and source-row assertions run during regeneration.

## Visual QA

Inspect the [rendered README](https://github.com/peterpapas/RCP-QI) at desktop and narrow widths, including light and dark GitHub themes. The SVGs use local paths and no script, external font or external image. The README captions repeat the figure category, axes, units, source and assumptions in selectable text. The [archived V5.1 classical figures](../results/processed/v5_1/) remain linked rather than mixing their wall-clock times into quantum oracle-query charts.

The local SVGs were rendered and inspected at desktop widths; the concept and timeline were also inspected as tall single-column graphics. GitHub's actual README preview was checked at 1,280 px and 390 px viewports with light and dark color schemes. All eight `<picture>` elements selected their desktop or mobile SVG as intended; no image had zero natural width. The first mobile pass revealed crowded plot labels, which were separated and rerendered before the final audit.

Rendered GitHub previews from the design branch:

- [Desktop, light theme](preview/readme-desktop-light.png)
- [Desktop, dark theme](preview/readme-desktop-dark.png)
- [Mobile opening](preview/readme-mobile-top.png)
- [Mobile concept](preview/readme-mobile-concept.png)

These screenshots are review aids, not scientific figures or new measurements. GitHub's interface and badges can change after capture.
