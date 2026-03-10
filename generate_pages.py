"""
Japan Knife Makers Database — Individual Page Generator
Run: python generate_pages.py
Output: items/ フォルダに [slug].html を30件生成
"""

import json, os, re

# ── スラグ生成 ──
def slugify(name):
    name = re.sub(r'\(.*?\)', '', name)
    name = name.lower().strip()
    name = re.sub(r'[^a-z0-9\s-]', '', name)
    name = re.sub(r'\s+', '-', name)
    name = re.sub(r'-+', '-', name).strip('-')
    return name

# ── 星評価HTML ──
def stars_html(rating):
    return ''.join(
        f'<span class="star">&#9733;</span>' if i < rating else '<span class="star empty">&#9733;</span>'
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
    'Sakai':   'Sakai (Osaka Prefecture) has been Japan\'s knife capital for over 600 years. Blades here are produced through a strict division of labor among specialist smiths, sharpeners, and handle-makers — resulting in unrivaled single-bevel precision. The city is home to some of Japan\'s most celebrated knife artisans, and Sakai knives are prized by professional chefs around the world for their thin geometry and superior edge quality.',
    'Echizen': 'Echizen (Fukui Prefecture) is home to Takefu Knife Village, a cooperative of master smiths who preserve traditional forging while embracing modern steels. Known for innovative Damascus patterns and laser-thin grinds, Echizen has produced some of Japan\'s most internationally recognized bladesmiths. The region\'s smiths are celebrated for combining centuries-old forging techniques with cutting-edge steel alloys.',
    'Seki':    'Seki (Gifu Prefecture) is Japan\'s largest knife-producing city and one of the world\'s three great blade centers alongside Solingen, Germany and Sheffield, England. Seki excels in high-volume precision and stainless steel technology, making it the home of many of Japan\'s most accessible and widely distributed knife brands. The city has been producing blades since the 13th century.',
    'Tosa':    'Tosa (Kochi Prefecture) follows the tradition of "jiyuu-tanzo" — free-form forging that adapts to each order. Tosa smiths are celebrated for functional, no-nonsense blades with excellent reactive carbon steel. The region\'s knives are known for outstanding value and performance, making Tosa one of the most popular origins for enthusiasts seeking quality Japanese carbon steel at accessible prices.',
    'Sanjo':   'Sanjo (Niigata Prefecture) produces the Echigo Sanjo Uchi Hamono, a designated Traditional Craft. The region is known for durable, handmade tools and houses some of Japan\'s best value-oriented knife brands. Sanjo\'s blade-making tradition extends back centuries, and the region continues to innovate with modern materials while honoring its craft heritage.',
    'Miki':    'Miki (Hyogo Prefecture) has a 500-year history of blade-making known as Banshu Hamono. The region produces kitchen knives, garden tools, and craft blades with a focus on everyday practicality. Miki knives are valued for their durability and honest craftsmanship, representing a different but equally important strand of Japan\'s rich blade-making heritage.',
    'Niigata': 'Niigata Prefecture\'s blade-making tradition spans centuries, from samurai sword production to modern kitchen knives. Home to several innovative makers blending heritage techniques with contemporary steels, Niigata represents one of Japan\'s most exciting regional knife-making scenes. The prefecture\'s long winters and artisan culture have fostered generations of skilled metalworkers.',
}

# ── 鋼材説明 ──
STEEL_DESC = {
    'Aogami Super': 'Aogami Super (Blue Super Steel) is widely regarded as one of the finest carbon steels available for kitchen knives. It contains added tungsten and molybdenum, giving it exceptional edge retention and the ability to take an extremely sharp edge. Aogami Super is a favorite of serious enthusiasts who appreciate reactive carbon steels and are willing to perform proper care and maintenance.',
    'Aogami #1': 'Aogami #1 (Blue Steel #1) is a high-carbon tool steel known for its exceptional hardness and ability to take a razor-sharp edge. It contains chromium and tungsten additions for improved wear resistance. Aogami #1 is prized by professional Japanese chefs for single-bevel knives like Yanagiba and Deba, where precision sharpening and edge quality are paramount.',
    'Aogami #2': 'Aogami #2 (Blue Steel #2) is the most widely used blue paper steel in Japanese knife-making. It offers an excellent balance of sharpness, edge retention, and ease of sharpening. Slightly more forgiving than Aogami #1, it is the steel of choice for many traditional Sakai and Echizen smiths. Knives in Aogami #2 develop a beautiful patina over time.',
    'Shirogami #1': 'Shirogami #1 (White Steel #1) is the purest form of high-carbon steel used in Japanese knives, containing very few alloying elements. This purity allows it to reach extreme hardness and take the sharpest possible edge, but it requires more careful maintenance. Shirogami #1 is considered the benchmark steel for traditional Japanese knife-making and is favored by master smiths.',
    'Shirogami #2': 'Shirogami #2 (White Steel #2) is slightly softer than Shirogami #1, making it more durable and easier to sharpen while still achieving excellent sharpness. It is the entry point into traditional Japanese carbon steel and a popular choice for both professional chefs and home cooks who want to experience authentic Japanese blade performance.',
    'Shirogami': 'Shirogami (White Steel) is the classic high-carbon steel of Japanese knife-making. It sharpens exceptionally easily, takes a very fine edge, and has a long history in Japanese bladesmithing. White steel knives require drying and occasional oiling to prevent rust, but reward proper care with outstanding cutting performance.',
    'R2/SG2': 'R2/SG2 (also called Super Gold 2) is a premium powder metallurgy stainless steel developed in Japan. It achieves hardness levels of 62–65 HRC, offering exceptional edge retention and corrosion resistance in a single package. R2/SG2 is a modern marvel — it holds an edge like a carbon steel but resists rust like stainless, making it ideal for professional kitchens.',
    'VG-10': 'VG-10 is a high-quality Japanese stainless steel developed specifically for kitchen knives. It contains cobalt for added hardness and excellent edge retention. VG-10 is one of the most popular knife steels in the world, offering an excellent balance of sharpness, corrosion resistance, and ease of maintenance. It is the choice of many premium Japanese brands.',
    'ZDP-189': 'ZDP-189 is one of the hardest stainless steels available, capable of reaching 67–69 HRC. Developed by Hitachi, it offers extraordinary edge retention and the ability to achieve an exceptionally fine edge. Knives in ZDP-189 are prized by collectors and serious enthusiasts, though the extreme hardness requires careful use to avoid chipping.',
    'HAP40': 'HAP40 is a high-speed tool steel offering exceptional hardness (65–68 HRC) and wear resistance. Originally developed for industrial cutting tools, it was adopted by Japanese knife-makers for its extraordinary edge retention. HAP40 knives are considered among the highest-performing kitchen knives available, holding an edge far longer than most other steels.',
    'Damascus': 'Damascus steel in modern Japanese knife-making refers to knives made from multiple layers of steel folded and welded together, creating a distinctive layered pattern on the blade. Beyond its visual appeal, Damascus construction can combine the properties of different steels. Japanese Damascus knives are prized both as functional tools and as works of art.',
    'SG2': 'SG2 (Super Gold 2) is Takefu Special Steel\'s premier powder metallurgy stainless steel. It achieves 62–65 HRC hardness with excellent edge retention and corrosion resistance. SG2 is the steel of choice for many of Japan\'s top bladesmiths who want modern performance characteristics without compromising on cutting ability.',
    'Ginsan (Silver #3)': 'Ginsan (Silver Paper #3, also called Gin-san or Gingami #3) is a semi-stainless steel that bridges the gap between traditional carbon steel and modern stainless. It takes an edge nearly as sharp as white steel but has significantly better rust resistance. Ginsan is increasingly popular among professional chefs who want traditional performance with reduced maintenance.',
    'Iron-clad': 'Iron-clad construction involves cladding a hard carbon steel core with softer iron. This technique protects the high-carbon core while providing a tough, durable exterior. The iron cladding develops a natural patina over time, while the core retains its superior edge. Iron-clad knives are traditional in style and beloved by enthusiasts who appreciate the aesthetic of natural aging.',
}

# ── 包丁種類説明 ──
KNIFE_TYPE_DESC = {
    'Gyuto': 'the Japanese chef\'s knife, suitable for meat, fish, and vegetables',
    'Yanagiba': 'the long, single-bevel sashimi knife essential for Japanese cuisine',
    'Deba': 'the heavy-duty fish butchering knife designed for breaking down whole fish',
    'Santoku': 'the versatile three-virtue knife excelling at meat, fish, and vegetables',
    'Nakiri': 'the double-bevel vegetable cleaver prized for clean, precise cuts',
    'Petty': 'the compact utility knife for detail work and small tasks',
    'Bunka': 'the multi-purpose knife with a distinctive reverse-tanto tip',
    'Sujihiki': 'the slicing knife ideal for carving roasts and fillets',
    'Usuba': 'the thin, single-bevel vegetable knife used in traditional Japanese cooking',
    'Kiritsuke': 'the all-purpose single-bevel knife, traditionally a mark of the head chef',
}

# ── 拡張コンテンツ生成 ──
def generate_rich_content(maker):
    name = maker['nameEn']
    region = maker['region']
    prefecture = maker['prefecture']
    maker_type_word = 'blacksmith' if maker['type'] == 'individual' else 'knife brand'
    desc = maker['description']
    specialties = maker['specialtyTypes']
    steels = maker['steelTypes']
    price_min = maker['priceMin']
    price_max = maker['priceMax']
    handle = maker['handleStyle']
    price_range = maker['priceRange']
    forge = maker['forge']

    # パラグラフ1: 概要
    para1 = f"""<p class="description-text">{desc}</p>
    <p class="description-text">{name} operates out of {region}, {prefecture} Prefecture — one of Japan's most respected knife-making regions.
    {'As an independent master blacksmith' if maker['type'] == 'individual' else f'As an established {maker_type_word}'},
    {name} represents the high standards of craftsmanship that have made Japanese knives sought after by professional chefs and collectors worldwide.
    The forge, known as {forge}, {'carries on a tradition of handcrafted excellence' if not maker.get('foundedYear') else f'has been producing exceptional blades since {maker["foundedYear"]}'}.</p>"""

    # パラグラフ2: 専門分野
    if len(specialties) > 1:
        spec_list = ', '.join([f'{s} ({KNIFE_TYPE_DESC.get(s, "a Japanese knife style")})' for s in specialties[:2]])
        other_specs = ', '.join(specialties[2:]) if len(specialties) > 2 else ''
        para2 = f"""<p class="description-text">The primary knife specialties at {name} include {spec_list}{(', as well as ' + other_specs) if other_specs else ''}.
        {'Japanese knife shapes carry centuries of culinary heritage, each designed for specific cutting tasks.' if maker['type'] == 'individual' else 'Each knife style is carefully engineered for its intended purpose, reflecting the depth of Japanese culinary tradition.'}
        {'Single-bevel knives like the Yanagiba and Deba are used exclusively by professional Japanese chefs and require mastery to use effectively.' if any(s in specialties for s in ['Yanagiba', 'Deba', 'Usuba']) else 'Double-bevel knives like the Gyuto and Santoku are accessible to both professional chefs and serious home cooks.'}
        </p>"""
    else:
        para2 = f"""<p class="description-text">The signature knife at {name} is the {specialties[0]} ({KNIFE_TYPE_DESC.get(specialties[0], 'a prized Japanese blade style')}).
        This specialization allows the smith to perfect every aspect of this particular knife style, from geometry to heat treatment to final polish.</p>"""

    # パラグラフ3: 鋼材
    primary_steel = steels[0]
    steel_explanation = STEEL_DESC.get(primary_steel, f'{primary_steel} is a high-quality steel chosen for its excellent performance characteristics.')
    para3 = f"""<p class="description-text">{name} works primarily with {primary_steel}. {steel_explanation}
    {f'Additional steel options include {", ".join(steels[1:])},' if len(steels) > 1 else ''}
    {'giving buyers the option to choose based on their maintenance preferences and intended use.' if len(steels) > 1 else ''}
    The choice of steel reflects the maker's philosophy: {'favoring high-performance carbon steels that reward proper care with outstanding cutting ability' if any('gami' in s.lower() or 'shirogami' in s.lower() for s in steels) else 'prioritizing modern stainless and powder steel technology for durability and low maintenance'}.</p>"""

    # パラグラフ4: ハンドルと価格
    handle_text = {
        'Wa': 'Traditional Japanese (Wa) handles are used exclusively — octagonal or D-shaped wooden handles that are lightweight, replaceable, and deeply rooted in Japanese culinary culture.',
        'Western': 'Western-style handles are used, offering a familiar grip for chefs transitioning from European knives. These full-tang handles provide balance and durability for heavy professional use.',
        'Both': 'Both traditional Japanese (Wa) and Western handle options are available, allowing buyers to choose based on their preference and cooking style.',
    }.get(handle, f'{handle} handles are used.')

    price_text = {
        'budget': f'Priced between ${price_min} and ${price_max}, these knives represent outstanding value — an accessible entry point into authentic Japanese blade-making without compromise on quality.',
        'mid': f'Priced in the ${price_min}–${price_max} range, these knives sit in the sweet spot of the market: genuinely professional-grade performance at a price that serious home cooks and working chefs can justify.',
        'high': f'Priced between ${price_min} and ${price_max}, these are premium-tier knives intended for serious collectors and professional chefs who demand the best.',
        'premium': f'Priced from ${price_min} to ${price_max}, these are elite, collectible-grade knives produced in limited quantities for the most discerning buyers.',
    }.get(price_range, f'Priced at ${price_min}–${price_max}.')

    para4 = f"""<p class="description-text">{handle_text} {price_text}</p>"""

    # パラグラフ5: 購入ガイド
    para5 = f"""<p class="description-text">For anyone looking to invest in a genuine Japanese knife from {region}, {name} is {'an essential name to consider' if maker['rating'] >= 4 else 'a reliable choice'}.
    {'These knives are especially well-suited to professional chefs, dedicated home cooks, and knife collectors who understand the value of traditional Japanese craftsmanship.' if price_range in ['high', 'premium'] else 'These knives offer an excellent starting point for anyone wanting to experience real Japanese blade-making tradition at an accessible price point.'}
    {'Carbon steel knives require drying after use and occasional light oiling to prevent rust — a simple routine that rewards the owner with exceptional performance.' if any('gami' in s.lower() or 'shirogami' in s.lower() for s in steels) else 'Stainless and semi-stainless blades are low-maintenance and ideal for busy kitchens or those new to Japanese knives.'}
    </p>"""

    return para1 + '\n    ' + para2 + '\n    ' + para3 + '\n    ' + para4 + '\n    ' + para5

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
        visit_html = '<div class="visit-badge exp">Workshop / Experience Available</div>'
    elif maker.get('canVisit'):
        visit_html = '<div class="visit-badge">Shop / Forge Visitable</div>'

    site_btn = ''
    if maker.get('url'):
        site_btn = f'<a class="btn-primary" href="{maker["url"]}" target="_blank" rel="noopener">Visit Official Site &#8599;</a>'

    related_cards = ''
    for r in related:
        rslug = slugify(r['nameEn'])
        rstars = stars_html(r['rating'])
        related_cards += f'''
        <a class="related-card" href="{rslug}.html">
          <div class="related-name">{r['nameEn']}</div>
          <div class="related-forge">{r['forge']}</div>
          <div class="related-stars">{rstars}</div>
          <div class="related-price">${r['priceMin']}&#8211;${r['priceMax']}</div>
        </a>'''

    maker_type = 'Blacksmith' if maker['type'] == 'individual' else 'Brand'
    title_seo = f"{maker['nameEn']} | {maker['region']} Japanese Knife {'Blacksmith' if maker['type']=='individual' else 'Maker'} | Japan Knife Makers Database"
    meta_desc = f"{maker['description'][:150]} Region: {maker['region']}, {maker['prefecture']}. Price: ${maker['priceMin']}&#8211;${maker['priceMax']}."

    rich_content = generate_rich_content(maker)

    # 鋼材ガイドセクション
    steel_guide_items = ''
    for steel in maker['steelTypes']:
        if steel in STEEL_DESC:
            steel_guide_items += f'<div class="steel-guide-item"><strong>{steel}</strong><p>{STEEL_DESC[steel][:200]}...</p></div>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-KP6TF8CM7B"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-KP6TF8CM7B');
  </script>
  <title>{title_seo}</title>
  <meta name="description" content="{meta_desc}"/>
  <meta property="og:title" content="{maker['nameEn']} &#8212; Japan Knife Makers Database"/>
  <meta property="og:description" content="{maker['description']}"/>
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
    :root{{--bg:#F7F5F0;--surface:#FFF;--navy:#1C2340;--gold:#B8933F;--gold-lt:#F0E6CC;--red:#8C2020;--text:#2A2A2A;--muted:#6B6B6B;--border:#E0DDD6;--radius:8px}}
    body{{font-family:'Georgia','Times New Roman',serif;background:var(--bg);color:var(--text);line-height:1.6}}
    a{{color:var(--navy);text-decoration:none}}
    a:hover{{text-decoration:underline}}
    nav{{background:var(--navy);padding:14px 24px;display:flex;align-items:center;gap:8px;font-family:'Helvetica Neue',Arial,sans-serif;font-size:.82rem}}
    nav a{{color:#8A90A8}}
    nav a:hover{{color:#fff;text-decoration:none}}
    nav .sep{{color:#3A4060}}
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
    .main{{max-width:860px;margin:0 auto;padding:32px 24px 64px}}
    .specs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;margin-bottom:28px}}
    .spec-item{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px 16px}}
    .spec-label{{display:block;font-family:'Helvetica Neue',Arial,sans-serif;font-size:.7rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:4px}}
    .spec-val{{font-family:'Helvetica Neue',Arial,sans-serif;font-size:.95rem;font-weight:600;color:var(--navy)}}
    .section{{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:24px;margin-bottom:20px}}
    .section h2{{font-size:1rem;font-family:'Helvetica Neue',Arial,sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid var(--border)}}
    .description-text{{font-size:.95rem;line-height:1.75;color:var(--text);margin-bottom:12px}}
    .description-text:last-child{{margin-bottom:0}}
    .pill-list{{display:flex;flex-wrap:wrap;gap:6px}}
    .pill{{padding:4px 12px;background:var(--bg);border:1px solid var(--border);border-radius:20px;font-family:'Helvetica Neue',Arial,sans-serif;font-size:.8rem;color:var(--text)}}
    .pill.steel{{background:#F0F5F0;border-color:#C0D4C0;color:#2A4A2A}}
    .tag-list{{display:flex;flex-wrap:wrap;gap:6px}}
    .tag{{padding:3px 10px;border-radius:4px;font-size:.73rem;font-family:'Helvetica Neue',Arial,sans-serif;background:#F2F0EB;color:#5A5550;border:1px solid #E0DDD6}}
    .visit-badge{{display:inline-block;padding:6px 14px;border-radius:var(--radius);font-family:'Helvetica Neue',Arial,sans-serif;font-size:.82rem;color:#2A7A4A;background:#E8F5EE;border:1px solid #B8DFC8;margin-bottom:16px}}
    .visit-badge.exp{{color:#7A4A2A;background:#F5EEE8;border-color:#DFC8B8}}
    .region-box{{background:#F0F5FF;border:1px solid #C0D0E8;border-radius:var(--radius);padding:16px 20px;font-family:'Helvetica Neue',Arial,sans-serif;font-size:.85rem;line-height:1.7;color:#2A3A5A}}
    .steel-guide-item{{margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid var(--border)}}
    .steel-guide-item:last-child{{margin-bottom:0;padding-bottom:0;border-bottom:none}}
    .steel-guide-item strong{{font-family:'Helvetica Neue',Arial,sans-serif;font-size:.9rem;color:var(--navy);display:block;margin-bottom:4px}}
    .steel-guide-item p{{font-size:.88rem;line-height:1.6;color:var(--muted)}}
    .btn-primary{{display:inline-block;padding:12px 28px;background:var(--navy);color:#fff;border-radius:var(--radius);font-family:'Helvetica Neue',Arial,sans-serif;font-size:.9rem;transition:background .2s}}
    .btn-primary:hover{{background:var(--gold);text-decoration:none;color:#fff}}
    .btn-back{{display:inline-block;padding:8px 18px;border:1.5px solid var(--border);border-radius:var(--radius);font-family:'Helvetica Neue',Arial,sans-serif;font-size:.82rem;color:var(--muted);transition:all .2s}}
    .btn-back:hover{{border-color:var(--navy);color:var(--navy);text-decoration:none}}
    .actions{{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-top:4px}}
    .related-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}}
    .related-card{{background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:14px;display:block;transition:transform .2s,box-shadow .2s}}
    .related-card:hover{{transform:translateY(-2px);box-shadow:0 4px 16px rgba(0,0,0,.1);text-decoration:none}}
    .related-name{{font-weight:bold;font-size:.88rem;color:var(--navy);margin-bottom:2px}}
    .related-forge{{font-size:.75rem;color:var(--muted);font-family:'Helvetica Neue',Arial,sans-serif;margin-bottom:4px}}
    .related-stars{{font-size:.75rem;color:var(--gold);margin-bottom:2px}}
    .related-price{{font-size:.75rem;color:var(--muted);font-family:'Helvetica Neue',Arial,sans-serif}}
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
  <a href="../index.html">Japan Knife Makers</a>
  <span class="sep">&#8250;</span>
  <a href="../index.html?region={maker['region']}">{maker['region']}</a>
  <span class="sep">&#8250;</span>
  <span style="color:#fff">{maker['nameEn']}</span>
</nav>

<div class="hero">
  <div class="kamon">&#9876;</div>
  <h1>{maker['nameEn']}</h1>
  <div class="name-ja">{maker['nameJa']} &middot; {maker['forge']}</div>
  <div class="badges">
    <span class="badge badge-region">{maker['region']} &middot; {maker['prefecture']}</span>
    <span class="badge badge-type">{maker_type}</span>
    {f'<span class="badge badge-est">Est. {maker["foundedYear"]}</span>' if maker.get('foundedYear') else ''}
  </div>
  <div class="stars">{stars}</div>
</div>

<div class="main">

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
      <span class="spec-val">${maker['priceMin']}&#8211;${maker['priceMax']}</span>
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

  <div class="section">
    <h2>About {maker['nameEn']}</h2>
    {visit_html}
    {rich_content}
  </div>

  <div class="section">
    <h2>Specialty Knife Types</h2>
    <div class="pill-list">{specialty_pills}</div>
  </div>

  <div class="section">
    <h2>Steel Types Used</h2>
    <div class="pill-list" style="margin-bottom:16px">{steel_pills}</div>
    {f'<div class="steel-guide">{steel_guide_items}</div>' if steel_guide_items else ''}
  </div>

  <div class="section">
    <h2>Tags</h2>
    <div class="tag-list">{tag_spans}</div>
  </div>

  <div class="section">
    <h2>About the {maker['region']} Region</h2>
    <div class="region-box">{region_desc}</div>
  </div>

  <div class="actions" style="margin-bottom:32px">
    {site_btn}
    <a class="btn-back" href="../index.html">&#8592; Back to All Makers</a>
  </div>

  {'<div class="section"><h2>Other ' + maker["region"] + ' Makers</h2><div class="related-grid">' + related_cards + '</div></div>' if related_cards else ''}

</div>

<footer>
  <strong>Japan Knife Makers Database</strong>
  <p>An independent guide to Japanese knife-making traditions. &middot; <a href="../index.html" style="color:#8A90A8">&#8592; All Makers</a></p>
  <p style="margin-top:8px"><a href="../about.html" style="color:#8A90A8">About</a> &middot; <a href="../privacy.html" style="color:#8A90A8">Privacy Policy</a></p>
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

    print(f"\nDone: {len(makers)} HTML files generated in items/")
    print("\n--- slug map ---")
    for mid, slug in slug_map.items():
        print(f"  {mid}: '{slug}'")

if __name__ == '__main__':
    main()
