import os
import glob
from collections import defaultdict

def title(s):
    return s.replace('_', ' ').replace('-', ' ').title()

def anchor(parts):
    return '-'.join(parts)

def build_tree(pngs):
    """Parse flat filenames into nested dict tree."""
    tree = defaultdict(lambda: defaultdict(list))
    for fname in sorted(pngs):
        parts = os.path.splitext(fname)[0].split('-')
        if len(parts) >= 3:
            cat, subcat, name = parts[0], parts[1], '-'.join(parts[2:])
        elif len(parts) == 2:
            cat, subcat, name = parts[0], parts[1], parts[1]
        else:
            cat, subcat, name = 'misc', 'misc', parts[0]
        tree[cat][subcat].append((name, fname))
    return tree

def generate_html(release_dir='release_files'):
    pngs = [os.path.basename(f) for f in glob.glob(os.path.join(release_dir, '*.png'))
            if not os.path.basename(f).startswith('inv_')]
    pngs.sort()
    tree = build_tree(pngs)

    # Build sidebar HTML
    sidebar_items = []
    for cat in sorted(tree.keys()):
        cat_id = f'cat-{cat}'
        sidebar_items.append(f'''
        <div class="tree-category">
          <div class="tree-cat-header" onclick="toggleCat('{cat_id}')">
            <span class="arrow" id="arrow-{cat_id}">▶</span>
            <span>{title(cat)}</span>
          </div>
          <div class="tree-subcats" id="{cat_id}" style="display:none">''')
        for subcat in sorted(tree[cat].keys()):
            anch = anchor([cat, subcat])
            sidebar_items.append(f'''
            <div class="tree-subcat" onclick="jumpTo('{anch}')">{title(subcat)} <span class="count">{len(tree[cat][subcat])}</span></div>''')
        sidebar_items.append('          </div>\n        </div>')

    # Build main content HTML
    content_items = []
    for cat in sorted(tree.keys()):
        content_items.append(f'<div class="category-section">')
        content_items.append(f'<h2 class="cat-title">{title(cat)}</h2>')
        for subcat in sorted(tree[cat].keys()):
            anch = anchor([cat, subcat])
            items = tree[cat][subcat]
            content_items.append(f'<div class="subcat-section" id="{anch}">')
            content_items.append(f'<h3 class="subcat-title"><span class="breadcrumb">{title(cat)} /</span> {title(subcat)}</h3>')
            content_items.append('<div class="wallpaper-grid">')
            for name, fname in items:
                inv_fname = 'inv_' + fname
                anch_wp = anchor([cat, subcat, name])
                wp_title = title(name)
                content_items.append(f'''
              <div class="wallpaper-card" id="{anch_wp}" data-search="{title(cat)} {title(subcat)} {wp_title}">
                <div class="wallpaper-title">{wp_title}</div>
                <div class="wallpaper-viewer">
                  <img class="wp-img" src="./{fname}" alt="{wp_title}" loading="lazy">
                  <img class="wp-img" src="./{inv_fname}" alt="{wp_title} inverted" loading="lazy">
                </div>
                <div class="wallpaper-controls">
                  <a class="dl-btn" href="./{fname}" download>↓ Normal</a>
                  <a class="dl-btn" href="./{inv_fname}" download>↓ Inverted</a>
                </div>
              </div>''')
            content_items.append('</div></div>')
        content_items.append('</div>')

    sidebar_html = '\n'.join(sidebar_items)
    content_html = '\n'.join(content_items)
    total = len(pngs)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Math Wallpapers</title>
<style>
  :root {{
    --bg: #1a1a1a;
    --sidebar-bg: #111111;
    --card-bg: #1a1a1a;
    --text: #ffffff;
    --muted: #888888;
    --border: #333333;
    --hover: #242424;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--text); font-family: 'Segoe UI', system-ui, sans-serif; display: flex; min-height: 100vh; }}

  /* Sidebar */
  #sidebar {{
    width: 280px; min-width: 220px; max-width: 320px;
    background: var(--sidebar-bg);
    border-right: 1px solid var(--border);
    position: fixed; top: 0; left: 0; height: 100vh;
    overflow-y: auto; z-index: 100;
    display: flex; flex-direction: column;
  }}
  .sidebar-header {{
    padding: 20px 16px 12px;
    border-bottom: 1px solid var(--border);
  }}
  .sidebar-header h1 {{ font-size: 1.1rem; color: var(--text); margin-bottom: 8px; }}
  .sidebar-header .count {{ font-size: 0.78rem; color: var(--muted); }}
  #search {{
    width: 100%; padding: 8px 12px; margin-top: 10px;
    background: var(--bg); border: 1px solid var(--border);
    border-radius: 0; color: var(--text); font-size: 0.85rem;
    outline: none;
  }}
  #search:focus {{ border-color: var(--text); }}
  .tree-nav {{ padding: 8px 0; flex: 1; }}
  .tree-category {{ border-bottom: 1px solid var(--border); }}
  .tree-cat-header {{
    padding: 10px 16px; cursor: pointer; display: flex;
    align-items: center; gap: 8px; font-size: 0.88rem;
    font-weight: 600; color: var(--text); user-select: none;
    transition: background 0.15s;
  }}
  .tree-cat-header:hover {{ background: var(--hover); }}
  .arrow {{ font-size: 0.65rem; color: var(--muted); transition: transform 0.2s; display: inline-block; }}
  .arrow.open {{ transform: rotate(90deg); }}
  .tree-subcats {{ padding: 2px 0 6px; }}
  .tree-subcat {{
    padding: 6px 16px 6px 36px; font-size: 0.82rem;
    color: var(--muted); cursor: pointer; display: flex;
    justify-content: space-between; align-items: center;
    transition: background 0.15s, color 0.15s;
  }}
  .tree-subcat:hover {{ background: var(--hover); color: var(--text); }}
  .count {{ background: var(--border); color: var(--muted); font-size: 0.72rem; padding: 1px 6px; }}

  /* Main content */
  #main {{
    margin-left: 280px; flex: 1; padding: 32px 32px 64px;
    max-width: 1600px;
  }}
  .page-title {{
    font-size: 1.8rem; font-weight: 700; color: var(--text);
    margin-bottom: 4px;
  }}
  .page-subtitle {{ color: var(--muted); font-size: 0.9rem; margin-bottom: 36px; }}
  .page-subtitle a {{ color: var(--text); text-decoration: none; border-bottom: 1px solid var(--muted); }}
  .page-subtitle a:hover {{ border-bottom-color: var(--text); }}

  .category-section {{ margin-bottom: 48px; }}
  .cat-title {{
    font-size: 1.3rem; font-weight: 700; color: var(--text);
    padding: 8px 0; border-bottom: 1px solid var(--border);
    margin-bottom: 20px; text-transform: uppercase; letter-spacing: 0.05em;
  }}
  .subcat-section {{ margin-bottom: 32px; }}
  .subcat-title {{
    font-size: 1rem; font-weight: 600; color: var(--text);
    margin-bottom: 14px; padding: 6px 12px;
    background: var(--sidebar-bg);
    border-left: 2px solid var(--text);
  }}
  .breadcrumb {{ color: var(--muted); font-weight: 400; font-size: 0.85rem; }}

  .wallpaper-grid {{
    display: grid;
    grid-template-columns: 1fr;
    gap: 1px;
    background: var(--bg);
  }}
  .wallpaper-card {{
    background: var(--card-bg);
    overflow: hidden;
    border: 1px solid var(--border);
    transition: background 0.15s;
  }}
  .wallpaper-card:hover {{ background: var(--hover); }}
  .wallpaper-title {{
    padding: 10px 14px; font-size: 0.88rem;
    font-weight: 600; color: var(--text);
    border-bottom: 1px solid var(--border);
  }}
  .wallpaper-viewer {{
    display: flex; gap: 0; background: #000;
  }}
  .wp-img {{
    width: 50%; aspect-ratio: 16/9; object-fit: cover; display: block;
  }}
  .wallpaper-controls {{
    padding: 8px 10px; display: flex; gap: 0; flex-wrap: wrap;
    border-top: 1px solid var(--border);
  }}
  .dl-btn {{
    padding: 5px 12px; font-size: 0.78rem;
    border: none; border-right: 1px solid var(--border);
    background: var(--sidebar-bg);
    color: var(--muted); cursor: pointer; text-decoration: none;
    transition: background 0.15s, color 0.15s;
    display: inline-block;
  }}
  .dl-btn:hover {{
    background: var(--border); color: var(--text);
  }}
  .dl-btn:last-child {{ border-right: none; }}

  .sidebar-footer {{
    border-top: 1px solid var(--border);
    padding: 12px 16px;
    margin-top: auto;
  }}
  .sidebar-footer a {{
    color: var(--muted); text-decoration: none; font-size: 0.82rem;
    transition: color 0.15s;
  }}
  .sidebar-footer a:hover {{ color: var(--text); }}

  /* Hide filtered cards */
  .wallpaper-card.hidden {{ display: none; }}
  .subcat-section.empty {{ display: none; }}
  .category-section.empty {{ display: none; }}

  @media (max-width: 768px) {{
    #sidebar {{ width: 100%; height: auto; position: relative; }}
    #main {{ margin-left: 0; padding: 16px; }}
    .wallpaper-grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<nav id="sidebar">
  <div class="sidebar-header">
    <h1>🧮 Math Wallpapers</h1>
    <div class="count">{total} wallpapers</div>
    <input id="search" type="text" placeholder="Search wallpapers..." oninput="filterWallpapers(this.value)">
  </div>
  <div class="tree-nav">
    {sidebar_html}
    <div class="sidebar-footer">
      <a href="https://github.com/SoneNiko/math-wallpapers" target="_blank">⎋ GitHub Repository</a>
    </div>
  </div>
</nav>

<main id="main">
  <div class="page-title">Math Wallpapers</div>
  <div class="page-subtitle">{total} wallpapers &mdash; <a href="https://github.com/SoneNiko/math-wallpapers">View on GitHub</a></div>
  {content_html}
</main>

<script>
  function toggleCat(id) {{
    const el = document.getElementById(id);
    const arrow = document.getElementById('arrow-' + id);
    if (el.style.display === 'none') {{
      el.style.display = 'block';
      arrow.classList.add('open');
    }} else {{
      el.style.display = 'none';
      arrow.classList.remove('open');
    }}
  }}

  function jumpTo(id) {{
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }}


  function filterWallpapers(query) {{
    const q = query.toLowerCase();
    document.querySelectorAll('.wallpaper-card').forEach(card => {{
      const match = card.dataset.search.toLowerCase().includes(q);
      card.classList.toggle('hidden', !match);
    }});
    // Hide empty subcats and cats
    document.querySelectorAll('.subcat-section').forEach(sec => {{
      const visible = sec.querySelectorAll('.wallpaper-card:not(.hidden)').length > 0;
      sec.classList.toggle('empty', !visible);
    }});
    document.querySelectorAll('.category-section').forEach(sec => {{
      const visible = sec.querySelectorAll('.wallpaper-card:not(.hidden)').length > 0;
      sec.classList.toggle('empty', !visible);
    }});
  }}
</script>
</body>
</html>'''
    return html

if __name__ == '__main__':
    html = generate_html('release_files')
    with open('release_files/index.html', 'w') as f:
        f.write(html)
    print(f'Generated index.html')
