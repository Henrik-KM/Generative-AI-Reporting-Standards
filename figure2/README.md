# Stage counts and plotting script for Figure 2

Figure 2 of the accompanying article compiles the stage-wise counts reported in seven published generative and screening campaigns, in order to show where candidates are lost and how strongly the choice of denominator shapes reported success. Since the figure is only as reliable as the counts behind it, every value is traceable to its source.

`data/figure2_stage_counts.json` lists, for each of the seven published campaigns in Figure 2a,b of the accompanying article, every reported stage with its candidate count, the evidence level to which it is assigned, and its source location in the cited publication. It also contains the stability rates from the matched comparison of Szymanski and Bartel shown in Figure 2c. Counts are taken directly from the publications; the SyntheMol total is the sum of three stated generation runs.

`tools/make_figure2.py` draws the figure (`figures/Figure_2.pdf` and `.png`) and writes the LaTeX source table of Supplementary Note 4 (`si_figure2_sources.tex`). It requires Python 3 and Matplotlib and is run from this directory:

```console
python tools/make_figure2.py
```

The same files are provided as Supplementary Data 1 of the article.
