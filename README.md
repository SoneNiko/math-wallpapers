# Math Wallpapers

**Math Wallpapers** is a project for generating beautiful, high-resolution PNG wallpapers from LaTeX Beamer slides. Each wallpaper visualizes a mathematical concept, theorem, or structure, with customizable text and background colors. The project is organized by mathematical domains, from theoretical computer science to calculus.

---

## Where are the wallpapers

You need to generate them yourself. I can not provide pre-made wallpapers because the png file is modified each time you run the script. You will have to generate them yourself. Maybe at one point i can generate them and provide them in the releases.

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

```bash
git clone https://github.com/yourusername/math-wallpapers.git
cd math-wallpapers
python wallpapers.py
```

---

## Adding New Topics

1. Create a new subfolder under `tex/` for your topic or use an existing one.
2. Add your LaTeX Beamer `.tex` file. It should use the wallpaper package defined in `wallpapers.sty`.
3. Compile the LaTeX file to generate the PDF for testing purposes.
4. Use the provided scripts to generate the wallpapers

---

## Contributing

- Fork and submit pull requests for new wallpapers or improvements.
- Please follow the folder structure and naming conventions.
