# Math Wallpapers

**Math Wallpapers** is a project for generating beautiful, high-resolution PNG wallpapers from LaTeX Beamer slides. Each wallpaper visualizes a mathematical concept, theorem, or structure, with customizable text and background colors. The project is organized by mathematical domains, from theoretical computer science to calculus.

---

## Where are the wallpapers

You can view them [here](https://soneniko.github.io/math-wallpapers/)

## Features

- **Automated Workflow**: Write LaTeX Beamer slides, convert to PDF, and export to PNG wallpapers.
- **Highly Configurable**: Easily set text and background colors for each wallpaper.
- **Comprehensive Coverage**: Organized by mathematical fields, including logic, algebra, calculus, topology, data science, and more.
- **Extensible**: Add new topics or styles with minimal effort.

## Getting Started

### Prerequisites

- [LaTeX](https://www.latex-project.org/) (with Beamer)
- [ImageMagick](https://imagemagick.org/) (for PDF → PNG)
- Bash, Python 3

### Usage

Bash (root not required):
```bash
git clone https://github.com/yourusername/math-wallpapers.git
cd math-wallpapers
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 wallpapers.py
```

---

## Adding New Topics

1. Create a new subfolder under `tex/` for your topic or use an existing one.
2. Add your LaTeX Beamer `.tex` file. It should use the wallpaper package defined in `wallpapers.sty`.
3. Compile the LaTeX file to generate the PDF for testing purposes.
4. Use the provided scripts to generate the wallpapers

---


---

## Wallpaper Style Guidelines

Wallpapers follow a strict visual style to maintain consistency across the collection.

### Mathematical Content
- Wallpapers present a single mathematical concept — a theorem, identity, construction, or definition.
- The primary content is **display mathematics**: `align*`, `\[...\]`, or `\Huge` for single formulas.
- Text is used sparingly:
  - **Allowed**: logical connectives (*then*, *implies*, *such that*, *let*, *for*), sentence glue setting up a definition or theorem.
  - **Allowed in definitions**: formal definitional prose (e.g. "Let $(\Omega, \mathbb{P})$ be a probability space").
  - **Not allowed**: explanatory paragraphs, motivational text, historical notes, or informal descriptions.
- When in doubt: if it can be expressed as a formula, express it as a formula.

### LaTeX Structure
Every wallpaper is a self-contained `.tex` file:
```latex
\documentclass[aspectratio=169]{beamer}
\usepackage{wallpaper}

\begin{document}
\begin{wallpaperframe}
% content here
\end{wallpaperframe}
\end{document}
```
The `wallpaper` package handles all styling (colors, fonts, layout). Do not add custom colors, \setbeamercolor, or \tikz unless part of the mathematical content itself.

### Examples of good style
- A single `\Huge` formula (Stirling, Euler identity)
- A short setup sentence followed by display math (Bayes, Mandelbrot)
- A clean `align*` block of equations (Maxwell, RSA)
- A formal set-builder definition with logical connectives

## Contributing

- Fork and submit pull requests for new wallpapers or improvements.
- Please follow the folder structure and naming conventions.

## Releases

Releases are created by pushing a tag of any kind. All wallpapers will be built and added to the release. The github pages preview is also updated.
