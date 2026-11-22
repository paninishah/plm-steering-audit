# Poster-scale figure exports

For the AI4DD poster at NeurIPS 2026 (Sydney, 11 Dec 2026).
Board: **61 × 85 cm portrait**; design target **A1, 59.4 × 84.1 cm**.

Generated from the unmodified scripts in `../figure render scripts/`.
Nothing in those scripts was changed. The paper figures in `../final/` are untouched.

## The one thing to get right

Type size on the board is decided by **how wide you place the figure**, not by the
export:

    pt on the board = the figure's authored pt x (print width / authored width)

So a figure authored 6.6 in wide with 5.4 pt annotations reads at 8.7 pt if you drop
it in a 10.6 in column, and at 17.8 pt across the full 21.8 in content width. Each
file below is exported for **one** placement width. Place it at that width.

The PNGs are 300 DPI **at their intended width**. The PDFs are vector and scale
losslessly, so use those if your tool accepts them.

## Place at these widths

Assumes A1 with 2 cm margins and a 1.5 cm gutter: content 21.8 in, column 10.6 in.

| File | Paper figure | Place at | Smallest type |
|---|---|---|---|
| `fig3_gate` | **Figure 2** (headline) | 21.8 in / 55.4 cm — full width | 17.8 pt |
| `fig2_steering` | Figure A1 | 21.8 in / 55.4 cm — full width | 17.2 pt |
| `fig4_predictor` | Figure A4 | 21.8 in / 55.4 cm — full width | 18.2 pt |
| `figA2_sae_vs_raw` | Figure A3 | 10.6 in / 26.9 cm — one column | 16.1 pt |
| `figA3_gap_sweep` | Figure A7 | 10.6 in / 26.9 cm — one column | 15.1 pt |
| `figA4_truncation` | Figure A6 | 10.6 in / 26.9 cm — one column | 15.1 pt |
| `figA5_layer_asymmetry` | Figure A2 | 10.6 in / 26.9 cm — one column | 14.3 pt |

Filenames do not match figure numbers — that is inherited from the repo, see the
warning in the top-level README.

**The three full-width figures are two-panel and dense.** They only clear 18 pt at
the full content width. In a column they fall to ~9 pt. If you need one in a column,
the fix is to split the panels into separate figures, not to shrink it.

**The four column figures land at 14–16 pt, under the 18 pt target.** Fine for
supporting detail read at about a metre. To reach 18 pt they need roughly 12–13 in,
i.e. wider than a half-column — give them full width if they carry an argument.

## Not generated here

- **Figure 1, the pipeline diagram** — hand-drawn, not script output. Use
  `../final/fig0_pipeline.png` (6936 × 3102), plenty for any poster placement.
- **Figure A5, the two folded structures** — needs PyMOL and the two `.pdb` files,
  which are not in this repository (they live in `ai4dd-plm-steering/analysis/fig1/`).
  Note `fig1_structures.py` still has the 0–1 vs 0–100 pLDDT B-factor bug that renders
  everything red; only `regenerate_figA5_kaggle.ipynb` is correct.

## Regenerating

    python render_poster_figs.py <analysis dir> <out dir>

The driver sets no sizes of its own. It runs each script unmodified and exports at a
DPI chosen so the raster is 300 DPI at the placement width above.
