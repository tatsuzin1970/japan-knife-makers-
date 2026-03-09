"""
Japan Knife Makers Database — Individual Page Generator
Run: python generate_pages.py
Output: items/ フォルダに [slug].html を30件生成
"""

import json, os, re

# ── スラグ生成 ──
def slugify(name):
    name = re.sub(r'\(.*?\)', '', name)   # 括弧内を削除
    name = name.lower().strip()
    name = re.sub(r'[^a-z0-9\s-]', '', name)
    name = re.sub(r'\s+', '-', name)
    name = re.sub(r'-+', '-', name).strip('-')
    return name

# ── 星評価HTML ──
def stars_html(rating):
    return ''.join(
        f'<span class="star">★</span>' if i < rating else '<span class="star empty">★</span>'
        for i in range(5)
    )

# ── 価格帯ラベル ──
PRICE_LABEL = {
    'budget':  'Budget (under $100)',
    'mid':     'Mid-range ($100–$300)',
    'high':    'High-end ($300–$600)',
    'premium': 'Premium ($600+)',
}

# ── 産地説明 ──
REGION_DESC = {
    'Sakai':   'Sakai (Osaka Prefecture) has been Japan\'s knife capital for over 600 years. Blades here are produced through a strict division of labor among specialist smiths, sharpeners, and handle-makers — resulting in unrivaled single-bevel precision.',
    'Echizen': 'Echizen (Fukui Prefecture) is home to Takefu Knife Village, a cooperative of master smiths who preserve traditional forging while embracing modern steels. Known for innovative Damascus patterns and laser-thin grinds.',
    'Seki':    'Seki (Gifu Prefecture) is Japan\'s largest knife-producing city and one of the world\'s three great blade centers alongside Solingen, Germany. Seki excels in high-volume precision and stainless steel technology.',
    'Tosa':    'Tosa (Kochi Prefecture) follows the tradition of "jiyū-tanzō" — free-form forging that adapts to each order. Tosa smiths are celebrated for functional, no-nonsense blades with excellent reactive carbon steel.',
    'Sanjo':   'Sanjo (Niigata Prefecture) produces the Echigo Sanjo Uchi Hamono, a designated Traditional Craft. The region is known for durable, handmade tools and houses some of Japan\'s best value-oriented knife brands.',
    'Miki':    'Miki (Hyogo Prefecture) has a 500-year history of blade-making known as Banshu Hamono. The region produces kitchen knives, garden tools, and craft blades with a focus on everyday practicality.',
    'Niigata': 'Niigata Prefecture\'s blade-making tradition spans centuries, from samurai sword production to modern kitchen knives. Home to several innovative makers blending heritage techniques with contemporary steels.',
}

# ── 個別ページHTMLテンプレート ──
def build_page(maker, all_makers, slug):
    related = [m for m in all_makers
               if m['region'] == maker['region'] and m['id'] != maker['id']][:3]

    specialty_pills = ''.join(
        f'<span class="pill">{s}</span>' for s in maker['specialtyTypes']
    )
    steel_pills = ''.join(
        f'<span class="pill steel">{s}</span>' for s in maker['steelTypes']
    )
    tag_spans = ''.join(
        f'<span class="tag">{t.replace("-"," ")}</span>' for t in maker['tags']
    )
    stars = stars_html(maker['rating'])
    price_label = PRICE_LABEL.get(maker['priceRange'], '')
    region_desc = REGION_DESC.get(maker['region'], '')
    founded_html = f'<div class="spec-item"><span class="spec-label">Founded</span><span class="spec-val">{maker["foundedYear"]}</span></div>' if maker.get('foundedYear') else ''
    visit_html = ''
    if maker.get('workshopExperience'):
        visit_html = '<div class="visit-badge exp">🔨 Workshop / Experience Available</div>'
    elif maker.get('canVisit'):
        visit_html = '<div class="visit-badge">📍 Shop / Forge Visitable</div>'

    site_btn = ''
    if maker.get('url'):
        site_btn = f'<a class="btn-primary" href="{maker["url"]}" target="_blank" rel="noopener">Visit Official Site ↗</a>'

    related_cards = ''
    for r in related:
        rslug = slugify(r['nameEn'])
        rstars = stars_html(r['rating'])
        related_cards += f'''
        <a class="related-card" href="{rslug}.html">
          <div class="related-name">{r['nameEn']}</div>
          <div class="related-forge">{r['forge']}</div>
          <div class="related-stars">{rstars}</div>
          <div class="related-price">${r['priceMin']}–${r['priceMax']}</div>
        </a>'''

    maker_type = 'Blacksmith' if maker['type'] == 'individual' else 'Brand'
    title_seo = f"{maker['nameEn']} | {maker['region']} Japanese Knife {'Blacksmith' if maker['type']=='individual' else 'Maker'} | Japan Knife Makers Database"
    meta_desc = f"{maker['description']} Region: {maker['region']}, {maker['prefecture']}. Price: ${maker['priceMin']}–${maker['priceMax']}."

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>{title_seo}</title>
  <meta name="description" content="{meta_desc}"/>
  <meta property="og:title" content="{maker['nameEn']} — Japan Knife Makers Database"/>
  <meta property="og:description" content="{maker['description']}"/>
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
    :root{{--bg:#F7F5F0;--surface:#FFF;--navy:#1C2340;--gold:#B8933F;--gold-lt:#F0E6CC;--red:#8C2020;--text:#2A2A2A;--muted:#6B6B6B;--border:#E0DDD6;--radius:8px}}
    body{{font-family:'Georgia','Times New Roman',serif;background:var(--bg);color:var(--text);line-height:1.6}}
    a{{color:var(--navy);text-decoration:none}}
    a:hover{{text-decoration:underline}}

    /* NAV */
    nav{{background:var(--navy);padding:14px 24px;display:flex;align-items:center;gap:8px;font-family:'Helvetica Neue',Arial,sans-serif;font-size:.82rem}}
    nav a{{color:#8A90A8}}
    nav a:hover{{color:#fff;text-decoration:none}}
    nav .sep{{color:#3A4060}}

    /* HERO */
    .hero{{background:var(--navy);color:#fff;padding:40px 24px 36px;text-align:center}}
    .hero .kamon{{font-size:2.2rem;color:var(--gold);margin-bottom:8px}}
    .hero h1{{font-size:clamp(1.8rem,4vw,2.8rem);font-weight:normal;letter-spacing:.03em}}
    .hero .name-ja{{margin-top:6px;color:#8A90A8;font-family:'Helvetica Neue',Arial,sans-serif;font-size:.9rem}}
    .hero .badges{{margin-top:16px;display:flex;justify-content:center;gap:8px;flex-wrap:wrap}}
    .badge{{padding:4px 14px;border-radius:20px;font-family:'Helvetica Neue',Arial,sans-serif;font-size:.78rem;font-weight:600}}
    .badge-region{{background:var(--gold-lt);color:#7A5C20}}
    .badge-type{{background:#1E3060;color:#8AAAE8}}
    .badge-est{{background:#2A1A1A;color:#D08080}}
    .hero .stars{{margin-top:14px;display:flex;justify-content:center;gap:3px}}
    .star{{color:var(--gold);font-size:1.1rem}}
    .star.empty{{color:#3A4060}}

    /* MAIN */
    .main{{max-width:860px;margin:0 auto;padding:32px 24px 64px}}

    /* SPECS GRID */
    .specs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;margin-bottom:28px}}
    .spec-item{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px 16px}}
    .spec-label{{display:block;font-family:'Helvetica Neue',Arial,sans-serif;font-size:.7rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:4px}}
    .spec-val{{font-family:'Helvetica Neue',Arial,sans-serif;font-size:.95rem;font-weight:600;color:var(--navy)}}

    /* SECTION */
    .section{{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:24px;margin-bottom:20px}}
    .section h2{{font-size:1rem;font-family:'Helvetica Neue',Arial,sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid var(--border)}}
    .description-text{{font-size:.95rem;line-height:1.7;color:var(--text)}}

    /* PILLS */
    .pill-list{{display:flex;flex-wrap:wrap;gap:6px}}
    .pill{{padding:4px 12px;background:var(--bg);border:1px solid var(--border);border-radius:20px;font-family:'Helvetica Neue',Arial,sans-serif;font-size:.8rem;color:var(--text)}}
    .pill.steel{{background:#F0F5F0;border-color:#C0D4C0;color:#2A4A2A}}

    /* TAGS */
    .tag-list{{display:flex;flex-wrap:wrap;gap:6px}}
    .tag{{padding:3px 10px;border-radius:4px;font-size:.73rem;font-family:'Helvetica Neue',Arial,sans-serif;background:#F2F0EB;color:#5A5550;border:1px solid #E0DDD6}}

    /* VISIT */
    .visit-badge{{display:inline-block;padding:6px 14px;border-radius:var(--radius);font-family:'Helvetica Neue',Arial,sans-serif;font-size:.82rem;color:#2A7A4A;background:#E8F5EE;border:1px solid #B8DFC8;margin-bottom:16px}}
    .visit-badge.exp{{color:#7A4A2A;background:#F5EEE8;border-color:#DFC8B8}}

    /* REGION BOX */
    .region-box{{background:#F0F5FF;border:1px solid #C0D0E8;border-radius:var(--radius);padding:16px 20px;font-family:'Helvetica Neue',Arial,sans-serif;font-size:.85rem;line-height:1.6;color:#2A3A5A}}

    /* BUTTONS */
    .btn-primary{{display:inline-block;padding:12px 28px;background:var(--navy);color:#fff;border-radius:var(--radius);font-family:'Helvetica Neue',Arial,sans-serif;font-size:.9rem;transition:background .2s}}
    .btn-primary:hover{{background:var(--gold);text-decoration:none;color:#fff}}
    .btn-back{{display:inline-block;padding:8px 18px;border:1.5px solid var(--border);border-radius:var(--radius);font-family:'Helvetica Neue',Arial,sans-serif;font-size:.82rem;color:var(--muted);transition:all .2s}}
    .btn-back:hover{{border-color:var(--navy);color:var(--navy);text-decoration:none}}
    .actions{{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-top:4px}}

    /* RELATED */
    .related-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}}
    .related-card{{background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:14px;display:block;transition:transform .2s,box-shadow .2s}}
    .related-card:hover{{transform:translateY(-2px);box-shadow:0 4px 16px rgba(0,0,0,.1);text-decoration:none}}
    .related-name{{font-weight:bold;font-size:.88rem;color:var(--navy);margin-bottom:2px}}
    .related-forge{{font-size:.75rem;color:var(--muted);font-family:'Helvetica Neue',Arial,sans-serif;margin-bottom:4px}}
    .related-stars{{font-size:.75rem;color:var(--gold);margin-bottom:2px}}
    .related-price{{font-size:.75rem;color:var(--muted);font-family:'Helvetica Neue',Arial,sans-serif}}

    /* FOOTER */
    footer{{background:var(--navy);color:#8A90A8;text-align:center;padding:28px 24px;font-family:'Helvetica Neue',Arial,sans-serif;font-size:.8rem}}
    footer strong{{color:#fff}}

    @media(max-width:600px){{
      .hero{{padding:28px 16px 24px}}
      .main{{padding:20px 16px 48px}}
      .specs{{grid-template-columns:1fr 1fr}}
    }}
  </style>
</head>
<body>

<nav>
  <a href="../index.html">⚔ Japan Knife Makers</a>
  <span class="sep">›</span>
  <a href="../index.html?region={maker['region']}">{maker['region']}</a>
  <span class="sep">›</span>
  <span style="color:#fff">{maker['nameEn']}</span>
</nav>

<div class="hero">
  <div class="kamon">⚔</div>
  <h1>{maker['nameEn']}</h1>
  <div class="name-ja">{maker['nameJa']} · {maker['forge']}</div>
  <div class="badges">
    <span class="badge badge-region">{maker['region']} · {maker['prefecture']}</span>
    <span class="badge badge-type">{maker_type}</span>
    {f'<span class="badge badge-est">Est. {maker["foundedYear"]}</span>' if maker.get('foundedYear') else ''}
  </div>
  <div class="stars">{stars}</div>
</div>

<div class="main">

  <!-- SPECS -->
  <div class="specs">
    <div class="spec-item">
      <span class="spec-label">Region</span>
      <span class="spec-val">{maker['region']}, {maker['prefecture']}</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Handle Style</span>
      <span class="spec-val">{maker['handleStyle']}</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Price Range</span>
      <span class="spec-val">${maker['priceMin']}–${maker['priceMax']}</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Tier</span>
      <span class="spec-val">{price_label}</span>
    </div>
    {founded_html}
    <div class="spec-item">
      <span class="spec-label">Type</span>
      <span class="spec-val">{maker_type}</span>
    </div>
  </div>

  <!-- ABOUT -->
  <div class="section">
    <h2>About {maker['nameEn']}</h2>
    {visit_html}
    <p class="description-text">{maker['description']}</p>
  </div>

  <!-- SPECIALTY -->
  <div class="section">
    <h2>Specialty Knife Types</h2>
    <div class="pill-list">{specialty_pills}</div>
  </div>

  <!-- STEEL -->
  <div class="section">
    <h2>Steel Types Used</h2>
    <div class="pill-list">{steel_pills}</div>
  </div>

  <!-- TAGS -->
  <div class="section">
    <h2>Tags</h2>
    <div class="tag-list">{tag_spans}</div>
  </div>

  <!-- REGION -->
  <div class="section">
    <h2>About the {maker['region']} Region</h2>
    <div class="region-box">{region_desc}</div>
  </div>

  <!-- ACTIONS -->
  <div class="actions" style="margin-bottom:32px">
    {site_btn}
    <a class="btn-back" href="../index.html">← Back to All Makers</a>
  </div>

  <!-- RELATED -->
  {'<div class="section"><h2>Other ' + maker["region"] + ' Makers</h2><div class="related-grid">' + related_cards + '</div></div>' if related_cards else ''}

</div>

<footer>
  <strong>Japan Knife Makers Database</strong>
  <p>An independent guide to Japanese knife-making traditions. · <a href="../index.html" style="color:#8A90A8">← All Makers</a></p>
</footer>

</body>
</html>'''

# ── メイン処理 ──
def main():
    with open('data.json', encoding='utf-8') as f:
        makers = json.load(f)

    os.makedirs('items', exist_ok=True)
    slug_map = {}

    for maker in makers:
        slug = slugify(maker['nameEn'])
        slug_map[maker['id']] = slug
        html = build_page(maker, makers, slug)
        path = os.path.join('items', f'{slug}.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"OK: {path}")

    # index.html 用のスラグマップを出力
    print(f"\nDone: {len(makers)} HTML files generated in items/")
    print("\n--- slug map ---")
    for mid, slug in slug_map.items():
        print(f"  {mid}: '{slug}'")

if __name__ == '__main__':
    main()
