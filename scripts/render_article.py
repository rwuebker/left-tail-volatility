"""Render the Part 1 LaTeX display equations for Medium and a local HTML preview.

Uses matplotlib mathtext (no external TeX installation) and the locked Jupyter
stack's mistune dependency. Does not run experiments or modify notebook cells.
"""
from pathlib import Path
import os
import re

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.uv-cache/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mistune


def main():
    article = ROOT / 'article'
    source = (article / '01_garch_foundations.md').read_text()
    equation_dir = article / 'equations'
    equation_dir.mkdir(exist_ok=True)
    count = 0

    def render(match):
        nonlocal count
        count += 1
        equation = ' '.join(match.group(1).strip().splitlines())
        name = f'part1_{count:02d}.png'
        fig = plt.figure(figsize=(10, 0.7), facecolor='white')
        fig.text(0.02, 0.5, f'${equation}$', fontsize=23, va='center', color='#172b3a')
        fig.savefig(equation_dir / name, dpi=240, bbox_inches='tight', pad_inches=0.15)
        plt.close(fig)
        alt = equation.replace('[', '(').replace(']', ')')
        return f'![Equation {count}: {alt}](equations/{name})'

    medium = re.sub(r'\$\$\s*\n(.*?)\n\$\$', render, source, flags=re.S)
    # Medium upload copy uses public links; the canonical article keeps portable
    # repository-relative links for GitHub and a local checkout.
    repo = 'https://github.com/rwuebker/left-tail-volatility/blob/main/'
    medium = medium.replace('(../README.md#', '(' + repo + 'README.md#')
    medium = medium.replace('(../notebooks/', '(' + repo + 'notebooks/')
    medium = medium.replace('(SERIES.md)', '(' + repo + 'article/SERIES.md)')
    preview = medium
    table_match = re.search(r'^\| Model .*?(?=\n\n)', medium, flags=re.M | re.S)
    if table_match:
        lines = table_match.group().splitlines()
        rows = [[cell.strip() for cell in line.strip('|').split('|')]
                for line in lines]
        fig, ax = plt.subplots(figsize=(11, 2.3))
        ax.axis('off')
        table = ax.table(cellText=rows[2:], colLabels=rows[0], loc='center',
                         cellLoc='left', colWidths=[0.43, 0.23, 0.16, 0.18])
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 1.9)
        for (row, _), cell in table.get_celld().items():
            cell.set_edgecolor('#d8e0e5')
            if row == 0:
                cell.set_facecolor('#eaf1f4')
                cell.set_text_props(weight='bold')
        fig.savefig(article / 'figures/part1_model_comparison.png', dpi=220,
                    bbox_inches='tight', pad_inches=0.15)
        plt.close(fig)
        medium = medium.replace(table_match.group(),
            '![Four training fits: parameter counts, persistence, and in-sample AIC. '
            'Values are available as text in the canonical GitHub article.]'
            '(figures/part1_model_comparison.png)')
    (article / '01_garch_foundations_medium.md').write_text(medium)
    markdown = mistune.create_markdown(escape=True, plugins=['table'])
    html = '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>How GARCH Models Volatility: Shocks, Persistence, and Asymmetry</title>
<style>body{max-width:800px;margin:60px auto;padding:0 24px;font:19px/1.65 Georgia,serif;color:#202a32;background:#fff}h1,h2{line-height:1.2;font-family:system-ui,sans-serif}h1{font-size:42px}h2{margin-top:2em;font-size:27px}img{max-width:100%;height:auto}img[alt^="Equation"]{max-height:85px;object-fit:contain;object-position:left}pre{padding:18px;background:#f3f5f7;overflow-x:auto;font-size:14px;line-height:1.5}code{font-size:.85em}table{border-collapse:collapse;font:14px/1.5 system-ui,sans-serif;width:100%}td,th{padding:10px;border-bottom:1px solid #ddd;text-align:left}a{color:#176d77}em{color:#4d5b65}</style><main>'''
    html += markdown(preview) + '</main></html>\n'
    (article / '01_garch_foundations.html').write_text(html)
    print(f'Rendered {count} equations, Medium Markdown, and HTML preview.')


if __name__ == '__main__':
    main()
