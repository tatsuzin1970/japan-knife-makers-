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

# ── 鍛冶師経歴 ──
BIOGRAPHY = {
    "Yu Kurosaki": "Yu Kurosaki trained at Takefu Knife Village in Echizen under legendary master Hiroshi Kato before establishing his own forge, Kurosaki Hamono. He became the youngest blacksmith in Japan to receive the government title of 'Master Blacksmith' (伝統工芸士), awarded to artisans who preserve Japan's cultural heritage. Kurosaki is celebrated for his distinctive hammered (tsuchime) finishes and hand-engraved ornate blade patterns — including the iconic FUJIN (Wind God) and SENKO (Flash) designs. His knives feature unusually tall blade heights, ultra-thin grinds, and steels pushed to the limits of hardness. Limited-run series often sell out within hours of release, reflecting the fierce worldwide demand from collectors and professional chefs alike.\n\nHis primary steel is Aogami Super, a blue carbon steel containing tungsten and molybdenum that achieves extraordinary edge retention and sharpness. Kurosaki also works in R2/SG2, a premier powder metallurgy stainless steel reaching 62–65 HRC with excellent corrosion resistance, and ZDP-189, one of the hardest stainless steels available at 67–69 HRC. Each steel choice represents a different balance of edge performance and maintenance requirements, allowing collectors to select based on their priorities.\n\nThe forge's signature series — FUJIN, SENKO, and SHIZUKU — have become some of the most coveted limited releases in the Japanese knife world. FUJIN knives are named for the Shinto wind god, featuring explosive tsuchime textures and dramatic blade heights. The SENKO (Flash) series showcases finely hand-engraved patterns alongside ultra-thin edge geometry. Both Wa and Western handle options are available, finished to a standard that reflects Kurosaki's position as one of the most celebrated active smiths in Japan today.",
    "Yoshimi Kato": "Yoshimi Kato is the son of the legendary Hiroshi Kato, one of Takefu Knife Village's founding masters. Having grown up in the forge, Yoshimi took over Kato Hamono in 2017 and has since proven himself a worthy heir to the tradition, continuing his father's acclaimed multi-layer Damascus forging methods while developing his own refined aesthetic. His knives are known for exceptionally thin grinds, clean heat treatment, and beautiful Damascus patterns in Aogami Super and SG2. Yoshimi has earned recognition as one of Echizen's leading smiths, attracting an international collector community that follows every new release.\n\nHis work spans two primary steel directions. The Aogami Super Damascus line features multi-layer carbon steel forged to 63–64 HRC, offering exceptional sharpness with a reactive surface that develops a beautiful working patina over time. The R2/SG2 Nashiji series uses a pear-skin surface texture over premium powder stainless steel, delivering near-carbon cutting performance with stainless convenience — a popular choice for professional kitchens.\n\nSignature series include the Super Blue Damascus Gyuto, widely regarded as one of the finest handmade chef's knives available at its price, and the Nashiji SG2 line prized for its subdued elegance and easy maintenance. Handles are typically Wa-style in quality hardwoods. Yoshimi Kato knives occupy a rarefied position: handmade by a second-generation master in one of Japan's most respected knife-making villages, yet still accessible enough that serious enthusiasts can realistically acquire one.",
    "Hideo Kitaoka": "Born in 1950, Hideo Kitaoka is widely regarded as one of Japan's finest living traditional blacksmiths. A founding member of Takefu Knife Village, he has spent over 50 years mastering the art of single-bevel knives — the Yanagiba, Deba, and Usuba that define professional Japanese cooking. Kitaoka works exclusively in traditional white and blue steel (Shirogami and Aogami), hand-finishing every blade in his Echizen workshop. His knives are used by top sushi chefs in Japan and are considered benchmark references for single-bevel performance. His forge remains one of the few where every stage of production is entirely by hand.\n\nKitaoka's steel choices reflect a deep reverence for Japanese tradition. His Shirogami #1 blades represent the purest high-carbon steel in Japanese knife-making — minimally alloyed, capable of taking an impossibly fine edge, and sharpening with a feedback and feel unmatched by modern steels. His Aogami #1 work adds chromium and tungsten for improved wear resistance, making it the preferred steel for heavy-duty fish work in Deba applications.\n\nThe signature Yanagiba in Shirogami #1 is considered a benchmark tool for professional sushi chefs — its geometry, balance, and edge-holding ability have been refined through five decades of iteration. The Deba in Aogami #1 is equally celebrated among chefs who break down whole fish daily. Each knife is individually inspected and finished by Kitaoka himself, making every piece a direct expression of one of Japan's greatest living craftsmen.",
    "Takeshi Saji": "Takeshi Saji co-founded Takefu Knife Village in 1973 and his forge has been a cornerstone of the village for over 50 years. He pioneered the use of rainbow Damascus — applying controlled heat to create vivid natural color gradients in layered steel patterns — giving his knives a visual identity recognized worldwide. With decades of forging experience, Saji represents the original spirit of Takefu Village: collaboration, innovation, and uncompromising craftsmanship. Both professional chefs and serious collectors seek out his work.\n\nHis primary steel work centers on R2/SG2 powder stainless steel, hardened to 63–65 HRC for exceptional edge retention. The rainbow Damascus construction involves forge-welding multiple layers of steel then applying controlled heat oxidation to the surface, creating naturally occurring color gradients — golds, blues, purples — that are unique to each blade. VG-10 serves as the core for his more accessible Black Damascus series, offering reliable corrosion resistance at a mid-range price.\n\nSignature series include the R2 Rainbow Damascus Gyuto — the knife that first made Saji famous internationally — and the VG-10 Black Damascus Santoku, an entry point for collectors attracted to his aesthetic. The Rainbow Damascus Nakiri has become a beloved choice for vegetable work, combining Saji's artistic signature with the clean-cutting geometry of a dedicated vegetable knife. Both Wa and Western handle options are available, crafted from natural hardwoods and stabilized materials that complement the blade's dramatic surface.",
    "Katsushige Anryu": "Katsushige Anryu co-founded Takefu Knife Village in 1973 and is one of Echizen's most respected traditional smiths. He is celebrated for his signature copper-clad Damascus construction, in which a reactive copper layer is forge-welded into the cladding, creating a warm earth-toned texture. Anryu's knives are forged in traditional carbon steel (Aogami #2 and Shirogami) at remarkably accessible prices for handmade Echizen work, making them a top recommendation for enthusiasts entering the world of Japanese carbon steel.\n\nThe copper-clad construction is Anryu's most distinctive technical contribution to Japanese knife-making. By incorporating copper into the forge-welded cladding, the exterior develops a warm, slightly oxidized appearance that changes with use — no two knives age identically. The Aogami #2 core is the most widely used blue paper steel in Japanese knife-making, offering excellent sharpness with good toughness and relative ease of sharpening. It reaches 61–63 HRC in Anryu's hands, striking a balance that professional chefs find ideal for daily use. Shirogami #2 versions are also available for those wanting the classic Japanese white steel experience.\n\nThe Copper Clad Damascus Gyuto is consistently cited as one of the finest-value handmade knives in the Japanese market, delivering genuine Takefu Village craftsmanship at an accessible price. The matching Nakiri and Santoku have developed their own followings. Handles are traditional Wa-style in magnolia or ho wood, keeping the overall package simple, authentic, and focused entirely on performance. Katsushige Anryu's knives are a compelling argument for the enduring relevance of traditional Japanese carbon steel.",
    "Isamu Takamura": "Isamu Takamura runs a family workshop in Echizen that has become legendary among professional chefs worldwide. The forge is best known for its R2/SG2 Migaki series — a knife combining an almost impossibly thin grind with SG2 powder steel hardened to 64 HRC, producing one of the most cutting-edge-performance blades available at its price. Takamura also works in a proprietary steel called HSPS achieving exceptional hardness. Despite elite status among professionals, Takamura knives remain relatively accessible in price, reflecting the workshop's commitment to making top-tier performance available to serious cooks.\n\nThe R2/SG2 Migaki Gyuto is the knife that established Takamura's global reputation. SG2 powder metallurgy stainless steel achieves 62–65 HRC hardness with excellent edge retention and corrosion resistance — ideal for professional kitchens where both performance and convenience are required. The Migaki (mirror-polished) finish reveals the exceptional geometry: the grind is among the thinnest available in any production knife, resulting in cutting performance that approaches custom handmade standards. HSPS, Takamura's proprietary high-speed powder steel, pushes hardness even further for collectors seeking maximum edge retention.\n\nThe workshop also produces knives in VG-10, offering the same ultra-thin Takamura geometry at more accessible prices — an ideal introduction for chefs new to Japanese knives. The HSPS series, hardened to 66–67 HRC, represents the frontier of kitchen knife steel performance. Both Wa and Western handles are available, and the forge's Echizen location connects it to a tradition of knife-making excellence stretching back centuries.",
    "Nao Yamamoto": "Nao Yamamoto trained under the late master Masami Azai, one of Echizen's most respected blacksmiths, before establishing his own forge. He is considered one of the finest smiths of the new Echizen generation, and his iron-clad carbon steel knives have attracted an intensely loyal following. Yamamoto specializes in Aogami Super and Shirogami #1 blades clad in soft iron — a construction that develops a beautiful, protective patina over time. His knives are characterized by refined simplicity: clean geometry, precise heat treatment, and octagonal Wa handles that reflect his deep training in the traditional Echizen style.\n\nThe iron-clad construction is central to Yamamoto's philosophy. By encasing a high-carbon steel core in soft, reactive iron rather than stainless steel, the knife's exterior develops a natural patina that actually protects the blade from deep oxidation — a technique rooted in centuries of Japanese smithing tradition. The Aogami Super core offers outstanding edge retention at 64–65 HRC, while Shirogami #1, the purest high-carbon steel in Japanese knife-making, achieves exceptional sharpness and a sharpening feel that enthusiasts describe as unmatched.\n\nThe Iron Clad Aogami Super Gyuto is Yamamoto's most celebrated knife, praised consistently for its balance of cutting performance, aesthetic beauty, and honest craftsmanship. The Nakiri and smaller utility knives follow the same principles. Octagonal Wa handles in Japanese magnolia or walnut complete knives that are both tools and objects of beauty — a defining achievement of the contemporary Echizen tradition.",
    "Shungo Ogata": "Shungo Ogata is a rising Echizen blacksmith who has built a significant international following through the consistency and refinement of his work. His knives are known for excellent fit and finish, clean geometry, and a polished aesthetic that appeals to the modern collector. Working primarily in R2/SG2 and Aogami Super, both heat-treated to high hardness with careful attention to the balance between hardness and toughness, Ogata represents the next generation of Echizen smiths: classical training combined with contemporary sensibility.\n\nOgata's R2/SG2 knives are hardened to 63–65 HRC, offering outstanding edge retention and corrosion resistance that professional kitchens value. The mirror polish (Migaki) finish allows the precise geometry to be fully appreciated — Ogata's grinds are notably even and refined, reflecting the attention to detail that distinguishes his work from less carefully finished competitors. The Aogami Super Tsuchime line offers a visually contrasting option with hammered surface texture that provides food release benefits alongside the exceptional edge performance of carbon steel.\n\nThe SG2 Mirror Polish Gyuto has become Ogata's signature knife — a clean, elegant tool that serious cooks find ideal as both an everyday workhorse and a collector piece. The Aogami Super Bunka, with its distinctive reverse-tanto tip and hammered finish, has developed an enthusiastic following. Petty knives in R2/SG2 complete the range, offering Ogata's refined geometry in a compact size ideal for detail work. Handles are Wa-style in quality hardwoods, completing knives that represent the best of Echizen's modern generation.",
    "Makoto Kurosaki": "Makoto Kurosaki is an Echizen smith gaining international recognition for sharp, elegantly finished knives at accessible prices. Producing knives in Aogami Super, SG2, and VG-10, his work offers collectors entry points at multiple price levels. His Gyuto knives are praised for clean geometry, thin grinds, and attractive handle pairings. Makoto represents the dynamic energy of Echizen's new generation — smiths who have learned from the village masters and are now building their own international reputations.\n\nWorking in the same Echizen region that produced his more famous namesake Yu Kurosaki, Makoto has developed a distinct voice. His SG2 knives achieve 63–64 HRC, providing excellent edge retention and corrosion resistance in a package priced more accessibly than comparable Echizen output. The Aogami Super Bunka — which gained early attention from the international knife community — demonstrates his confidence with reactive carbon steel: the combination of Aogami Super's edge performance and the Bunka's distinctive tip geometry creates a versatile kitchen companion that many cooks find becomes their most-used knife.\n\nFit and finish standards are notably high for the price — Makoto's knives punch above their tier in terms of edge consistency, handle quality, and overall presentation. Wa handles in Japanese hardwoods are standard, occasionally paired with octagonal ho wood for a traditional aesthetic. For collectors looking to build a well-rounded Japanese knife collection, Makoto Kurosaki represents excellent value from one of Japan's most storied knife-making regions.",
    "Sakai Takayuki": "Sakai Takayuki was established in 1932 and works with some of Sakai's finest craftsmen, including legendary smith Itsuo Doi and master sharpeners from the Yamatsuka family. The brand produces an exceptionally wide range — from entry-level everyday knives to professional single-bevel tools used in Michelin-starred restaurants. Their Ginga series in Swedish steel is among the most highly regarded professional knives in Japan. The brand's ability to collaborate with top-tier craftspeople while maintaining accessible pricing has made it one of the most trusted names in the Sakai tradition.\n\nThe Ginga series represents the brand's most critical contribution to professional kitchens: made from Swedish Sandvik stainless steel, these knives combine exceptional thinness, hardness, and edge retention with low-maintenance stainless convenience. Professional chefs across Japan consider the Ginga Gyuto a benchmark tool for Western cooking in Japanese restaurant environments. The 45-Layer Damascus VG-10 series offers striking visual aesthetics alongside VG-10 core performance — cobalt-enhanced hardness reaching 61–62 HRC with excellent corrosion resistance. The Itsuo Doi collaboration produces limited single-bevel Yanagiba and Deba knives combining Doi's legendary heat treatment with Sakai Takayuki's distribution reach.\n\nSakai Takayuki maintains the traditional Sakai division of labor — separate specialists for forging, sharpening, and handle fitting — ensuring that each stage of production receives focused expertise. This approach, developed over six centuries in Sakai, produces results that vertically integrated manufacturers cannot replicate. The brand occupies an enviable position: authentic Sakai heritage, wide availability, and pricing that spans every budget tier.",
    "Itsuo Doi": "Itsuo Doi is the son of the legendary Keijiro Doi, widely considered one of the greatest Japanese blacksmiths in history. Itsuo carries on his father's tradition of forging at unusually low temperatures — a technique producing superior grain structure in the steel and exceptional edge quality. His Yanagiba and Deba knives in Aogami #2 are benchmark tools for Japan's top professional sushi and kaiseki chefs. Doi's blades are produced in very limited quantities, and acquiring one often requires patience and dedication. For collectors seeking the pinnacle of Sakai's traditional single-bevel craft, Itsuo Doi represents an uncompromised standard.\n\nThe low-temperature forging technique practiced by Itsuo and inherited from Keijiro Doi is the defining technical characteristic of their work. By forging at temperatures below conventional practice, the steel's grain structure remains tighter and more uniform — a difference that manifests as superior edge quality and cutting feel in use. Aogami #2 is the primary steel, containing chromium and tungsten for improved wear resistance, reaching 62–64 HRC. Shirogami #1 is also used for Yanagiba work demanding the ultimate edge refinement.\n\nThe Yanagiba in Aogami #2 is a professional standard among Japan's most demanding sushi chefs. Its single-bevel geometry, hand-ground to exacting specifications, cuts sashimi with a pull stroke that minimizes cell disruption — a quality judges and masters describe as having a fundamentally different feel from ordinary knives. The Deba, used for breaking down whole fish, achieves the same standard in a heavier profile. These are tools that professional chefs build entire careers around.",
    "Yasuhiro Hirakawa (Sasuke)": "Yasuhiro Hirakawa is the 22nd-generation head of the Sasuke forge — a lineage of blacksmiths stretching back over 400 years in Sakai. He is one of only five remaining craftsmen in Japan who produce both knives and scissors, a combination once common in traditional Sakai that has nearly vanished due to specialization. Hirakawa's work is museum-quality: every blade individually forged and finished using techniques passed down through generations. His Yanagiba and Deba knives in Aogami #1 and Shirogami are among the finest available, and his scissor-and-knife combinations are extraordinary collector pieces.\n\nThe Aogami #1 steel at the heart of Hirakawa's finest Yanagiba knives is among the most demanding to work with: a high-carbon steel requiring precise temperature control to achieve its potential. In skilled hands, Aogami #1 reaches 62–64 HRC with chromium and tungsten additions for superior wear resistance — the ideal steel for single-bevel knives subjected to the exacting demands of professional sushi preparation. Shirogami options offer a slightly softer alternative with a different sharpening character favored by some chefs for its tactile feedback.\n\nThe Yanagiba represents the apex of Hirakawa's craft — 400 years of family knowledge applied to a knife that professional sushi chefs use as a primary tool for slicing sashimi. Every aspect, from the geometry of the single bevel to the weight distribution of the handle, reflects generations of refinement. The scissor-and-knife combination pieces are unique in the contemporary market — living examples of traditional Sakai's full range of cutlery arts, available from one of the last craftsmen maintaining both traditions simultaneously.",
    "Satoshi Nakagawa": "Satoshi Nakagawa trained for 16 years under master blacksmith Kenichi Shiraki before establishing Nakagawa Hamono in Sakai. That lengthy apprenticeship is evident in the consistency and quality of his work — Nakagawa is considered one of Sakai's finest active smiths for traditional single-bevel knives. His Yanagiba and Deba blades in Aogami #2 and Shirogami #2 are prized for exceptional heat treatment consistency and a level of fit and finish that reflects years of patient mastery.\n\nThe 16-year apprenticeship Nakagawa served under Kenichi Shiraki is unusually long even by Sakai's demanding standards, and the depth of training is apparent in every aspect of his finished knives. Aogami #2 is his primary steel — the most widely used blue paper steel in Japanese knife-making, offering excellent sharpness, edge retention, and ease of sharpening at 62–64 HRC. Shirogami #2 provides a slightly softer alternative that sharpens with exceptional ease, ideal for chefs who sharpen daily and value the tactile experience of white steel. Both steels develop a beautiful working patina over time.\n\nThe Yanagiba is Nakagawa's most celebrated work — praised in knife enthusiast communities for heat treatment consistency that rivals smiths commanding far higher collector premiums. The Kiritsuke, a single-bevel all-purpose knife traditionally reserved for head chefs, showcases Nakagawa's ability to work across different geometry requirements. The Deba in Shirogami #2 is an ideal entry point — genuine Sakai single-bevel craftsmanship at a price accessible to serious home cooks and developing professionals.",
    "Sakai Kikumori": "Sakai Kikumori is a respected Sakai brand known for consistent quality across both traditional Japanese and Western-style knife production. Working within Sakai's traditional division of labor — collaborating with specialist smiths, sharpeners, and handle-makers — Kikumori produces knives reflecting the full depth of Sakai's craft tradition. Their Nihonko carbon steel series and Gyuto offerings are particularly well-regarded by professional chefs who want authentic Sakai quality at reasonable prices. Kikumori occupies a trusted middle ground: serious enough for professionals, accessible enough for dedicated home cooks who understand what Sakai knives represent.\n\nThe Nihonko (Japanese steel) carbon series represents Kikumori's deepest connection to Sakai's heritage. These knives use traditional high-carbon steel processed by Sakai's specialist craftsmen — forged, shaped, and sharpened by separate artisans who have devoted their careers to their specific role. The result is a knife whose every stage has received focused expert attention. Aogami #1 Yanagiba represents the brand's premium single-bevel offering — one of the finest professional sashimi knives available at its price. The NK Stainless Gyuto provides modern low-maintenance performance within the same Sakai quality framework.\n\nThe traditional Sakai division of labor that Kikumori maintains is increasingly rare — most modern manufacturers have consolidated production for efficiency. By preserving this separation, Kikumori ensures that each specialized step receives undivided expert attention: the forging specialist focuses entirely on steel, the sharpener on edge geometry, the handle craftsman on fit and finish. For buyers who understand and value this tradition, Kikumori represents an authentic and accessible entry into genuine Sakai craftsmanship.",
    "Konosuke": "Konosuke is a boutique Sakai brand with a cult following among the world's most dedicated knife enthusiasts. The brand is known for extraordinarily thin grinds — some of the thinnest in production knives — combined with proprietary stainless steel formulations (HD2 and GS+) that achieve near-carbon-steel sharpness without maintenance requirements. The Fujiyama series, a premium line using traditional Sakai white steel construction, is one of the most coveted knife collections in the world. Long waiting lists for popular models are common, and the brand's uncompromising quality has cemented its status as a benchmark in the global knife community.\n\nThe HD2 steel is Konosuke's most discussed proprietary formulation — a semi-stainless steel achieving carbon-level sharpness with significantly better rust resistance than pure carbon steel. It occupies the niche between traditional carbon steel and fully stainless modern alloys: close enough to stainless for professional kitchen use, sharp enough to satisfy enthusiasts who have used the finest carbon steel knives. GS+ offers similar characteristics with refined properties. The Fujiyama series, built on traditional Sakai white steel (Shirogami) construction, represents the ultimate expression of Konosuke's thin-grind philosophy.\n\nProduction quantities remain deliberately limited — Konosuke's commitment to hand-finishing and quality inspection at every stage creates natural constraints. The result is that acquiring specific models, especially in Fujiyama white steel, often requires patience and persistence. For enthusiasts who have worked through entry and mid-range Japanese knives and are ready for the finest available, Konosuke HD2 and Fujiyama series represent a genuine destination. Few knives in the world generate the same level of community reverence.",
    "Jikko (Sakai Jikko)": "Jikko Cutlery was established in 1926 and has built a reputation as one of the most accessible authentic Sakai experiences for international visitors and buyers. The brand offers genuine Sakai-made knives at entry to mid-range prices, making it an ideal introduction to the tradition for new enthusiasts. Jikko's Sakai shop offers knife-sharpening experiences and forge visits — a rarity among Sakai producers — and the brand's English-friendly website has helped introduce many international customers to Sakai's unique knife culture.\n\nThe Honkasumi Yanagiba in Aogami #2 is Jikko's classic professional offering — a genuine Sakai single-bevel sashimi knife produced through the traditional division of labor, at a price accessible to developing professionals and serious home cooks. Aogami #2 offers excellent sharpness and edge retention at 62–64 HRC, with a characteristic blue paper steel feel when sharpening that many chefs find deeply satisfying. The VG-10 Gyuto and Santoku series bring Sakai quality to double-bevel Western-influenced shapes, with VG-10's cobalt-enhanced hardness providing exceptional edge retention and corrosion resistance for everyday professional use.\n\nWhat distinguishes Jikko beyond the quality of its knives is its commitment to accessibility and education. The workshop visit and sharpening experience programs have introduced thousands of international visitors to the living craft of Sakai knife-making — something most Sakai producers do not offer. The staff's willingness to engage with non-Japanese-speaking customers, combined with well-produced English product descriptions, makes Jikko one of the best entry points for anyone wanting to meaningfully connect with Sakai's tradition rather than simply purchase a product.",
    "Ichimonji Mitsuhide": "Ichimonji Mitsuhide is a well-established Sakai brand and retailer with one of the most comprehensive English-language knife websites in Japan. Working with multiple Sakai smiths, the brand offers a wide range from professional single-bevel knives to Western-influenced stainless options. Their Mizu Yaki (water-quench) line uses traditional quenching techniques for superior edge quality. Ichimonji's physical store in Sakai is visitable and staffed with knowledgeable experts, making it a popular destination for knife enthusiasts visiting the Osaka area.\n\nThe Mizu Yaki (water-quench) technique is the defining specialty of Ichimonji's premium line. Traditional water quenching — submerging a heated blade rapidly in water rather than oil — creates a harder, more brittle steel structure requiring exceptional skill to control. When executed correctly, it produces an edge quality and feel that oil-quenched knives cannot achieve. Applied to Aogami steel, the result is a Yanagiba or Deba with edge qualities that professional Japanese chefs describe as distinctively alive. The technique's difficulty means that water-quenched knives command a premium and are produced in smaller quantities.\n\nThe Honyaki (full-hardened) Kiritsuke represents Ichimonji's most technically demanding product: a single-steel, single-bevel knife hardened throughout its body rather than using a softer cladding. Honyaki knives are the rarest and most respected type in Japanese knife-making — demanding to produce, demanding to maintain, and producing an edge quality that only the finest carbon steel monosteel can achieve. For collectors who have worked through the hierarchy of Japanese knife acquisition, an Ichimonji Honyaki represents a meaningful milestone.",
    "MAC Knife": "MAC Knife was founded in 1964 in Seki and has become one of the most successful Japanese knife brands in North America, particularly popular in professional kitchens and culinary schools. The brand's success is built on a simple formula: thin, lightweight blades from high-quality Japanese steel at accessible prices. The Pro series and Chef's series are widely used in restaurant kitchens and taught in culinary programs across the United States. MAC's Western-style handles make the knives immediately approachable for chefs transitioning from European blade traditions.\n\nMAC's proprietary steel blend — a high-carbon, high-molybdenum stainless alloy — achieves hardness levels of 59–61 HRC, noticeably harder than typical German kitchen knives while remaining within a range where professional maintenance is straightforward. The thin blade geometry, closer to Japanese blade standards than European, creates cutting performance that surprises chefs accustomed to heavier Western knives. The Pro Series MSK-65 (8.5-inch Gyuto) is arguably the most recommended single knife for culinary students and restaurant professionals seeking Japanese-style performance without the learning curve of a Wa-handle knife or the maintenance requirements of carbon steel.\n\nThe Chef's series provides an entry tier maintaining the same thin-blade philosophy at lower price points, while the Superior Series adds bread knives and utility blades that complete a professional kitchen set. What distinguishes MAC is the consistency of manufacturing — each knife produced to identical specifications, which matters considerably in high-volume professional kitchen environments where knives are subjected to daily heavy use. Few brands achieve MAC's combination of Japanese blade engineering and reliable professional-grade production standards at its price tier.",
    "Miyabi (by Zwilling)": "Miyabi was launched in 2004 through a collaboration between German knife giant Zwilling J.A. Henckels and Japan's Seki knife-making tradition. Made in Seki using Japanese blade-making techniques — including ice-hardening and hand-honing — combined with German quality control standards, the result combines Japanese thinness and hardness with the consistency of German manufacturing. The 5000MCD Birchwood and Kaizen II series in SG2/R2 have been particularly successful among home cooks seeking premium Japanese performance with a Western aesthetic.\n\nThe Friodur ice-hardening process, applied to Miyabi's SG2 and R2 cores, achieves hardness levels of 63 HRC — significantly harder than most German knives and comparable to the finest Japanese handmade work. SG2 powder stainless steel offers exceptional edge retention and corrosion resistance in a package that handles the demands of modern restaurant and home kitchen use. The 100-layer Damascus cladding on the 5000MCD is both aesthetically stunning and technically meaningful, providing contrast between the performance core and a tougher exterior. VG-10 cores in the Kaizen II line deliver reliable performance at a more accessible price.\n\nThe 5000MCD Birchwood series — featuring SG2 core, 100-layer Damascus, and a distinctive birchwood handle — is Miyabi's most recognized knife, achieving premium Japanese performance standards within the Zwilling distribution network. This distribution reach is significant: Miyabi is available in department stores and kitchen specialty shops worldwide, making genuine Japanese SG2 performance accessible to buyers who might not otherwise encounter it. For home cooks wanting to upgrade from European knives without abandoning familiar handle ergonomics, Miyabi represents an elegant bridge.",
    "Kai Group (Shun / Kershaw)": "Kai Corporation was founded in 1908 in Seki and has grown into one of Japan's largest and most internationally recognized knife manufacturers. The Shun brand is the most widely recognized Japanese knife label in the United States, stocked in major department stores and cooking supply chains. Shun Classic and Shun Premier offer an accessible entry to Japanese knife ownership for Western consumers, combining Damascus aesthetics with VG-10 and VG-MAX cores. For enthusiasts, the Shun Kaji and limited special editions offer premium performance using SG2 steel and more traditional construction.\n\nVG-MAX, Kai's proprietary steel developed from VG-10, forms the core of most Shun knives. It contains added tungsten and cobalt over VG-10, achieving 60–61 HRC with improved edge retention and a finer grain structure that allows a sharper initial edge. The 68-layer Damascus cladding provides both aesthetic appeal and practical function — the layered steel exterior contrasts with the polished core and reduces friction during cutting. For the premium Kaji series, SG2 powder metallurgy stainless steel pushes performance significantly further, achieving 63–65 HRC for collectors wanting the finest cutting edge within the Shun lineup.\n\nShun Classic — the brand's bestselling knife — has introduced more North American home cooks to Japanese knife ownership than any other product. Its familiar Western handle shape combined with Japanese blade geometry and VG-MAX steel represents a carefully calculated bridge between culinary traditions. The distribution reach of Kai/Shun, available through major retailers internationally, means that these knives serve as millions of people's first experience with authentic Japanese blade manufacturing.",
    "Tojiro": "Tojiro (Fujitora) was established in 1955 in Sanjo, Niigata, and has become one of the most universally recommended knife brands for beginners and professionals seeking outstanding value. The DP Cobalt series — VG-10 core, clad in softer stainless, Western handle — offers professional-grade cutting performance at prices accessible to nearly everyone. Few brands match Tojiro's combination of authentic Japanese manufacturing, real professional performance, and honest pricing that democratizes access to quality Japanese blades.\n\nThe DP Cobalt series uses VG-10 as its core — a high-quality Japanese stainless steel containing cobalt for additional hardness, achieving 60–62 HRC. This hardness level, significantly exceeding typical German kitchen knives, produces edge retention that professional chefs notice in daily use. The softer stainless cladding protects the core during heavy use while keeping the knife easy to maintain. Triple-rivet Western handles provide familiar ergonomics for chefs transitioning from European knives. The F-807 8.2-inch Gyuto is the specific model most frequently cited as the world's best-value beginner Japanese knife — a designation earned through years of consistent positive experiences from both professional and home cook communities.\n\nThe Senkou series represents a meaningful upgrade — hammered tsuchime finish, improved handle materials, and refined geometry — while the traditional Shirogami Gyuto introduces authentic carbon steel at accessible prices. For professional kitchens equipping entire teams, Tojiro offers a compelling combination: genuine Japanese manufacturing, VG-10 performance, and prices that allow purchasing quality tools across an entire brigade. The brand demonstrates that outstanding Japanese knife-making need not carry an exclusionary price tag.",
    "Tamahagane": "Tamahagane is a Sanjo-based brand named after the legendary steel used in traditional Japanese swords. The brand's signature offering is its 3-layer San Mai construction, in which a high-carbon core is clad between layers of stainless steel, combining the edge quality of carbon with improved resistance and easier maintenance. The Tsubame series, featuring distinctive hammered finishes and refined Wa handles, has found a loyal following among enthusiasts seeking a sophisticated knife at a mid-range price.\n\nThe San Mai (three-layer) construction central to Tamahagane's identity addresses one of the main challenges in knife design: balancing cutting performance with durability and maintenance. A hard high-carbon steel core provides the sharpness and edge retention enthusiasts demand, while outer stainless steel layers protect the core during lateral stress and reduce the risk of corrosion on the non-cutting parts of the blade. This construction, common in traditional Japanese sword-making, produces a knife combining the best qualities of both material types. Hardness typically reaches 61–63 HRC in Tamahagane's implementation.\n\nThe Tsubame series, named after a city in Niigata Prefecture with centuries of quality metalwork tradition, is the flagship line. Hammered tsuchime finishes provide visual distinction and practical food release benefits — the indentations create air pockets between food and blade that reduce suction during cutting. Wa handles in natural hardwoods complete a package that presents as a premium product at a price point that dedicated home cooks find reasonable. The San Mai Sujihiki and Nakiri extend the range for chefs building a complete Japanese knife collection around Tamahagane's distinctive aesthetic.",
    "Nigara Hamono": "Nigara Hamono traces its origins to 1598, when the family was involved in sword-making during Japan's feudal period — one of the oldest lineages in Japanese blade-making. The forge transitioned from swords to kitchen knives in the modern era, bringing centuries of metallurgical knowledge to bear on contemporary design. Nigara is best known for its extraordinary Anmon (twisted) Damascus patterns, in which steel layers are twisted during forging to create a distinctive spiral texture on the blade surface. The combination of 400-year heritage and exceptional Aogami Super and SG2 craftsmanship has made Nigara one of the most exciting brands in the current collector market.\n\nThe Anmon (twisted) Damascus technique is Nigara's defining visual and technical contribution. During the forge-welding process, bundles of layered steel are twisted before being flattened, creating a spiral grain pattern that appears on the blade surface after etching. The effect is unlike any other Damascus pattern available — immediately identifiable as Nigara's work and technically demanding to execute consistently. Aogami Super forms the core of Nigara's most celebrated knives, hardened to 64–65 HRC for exceptional edge performance. SG2 powder steel provides a corrosion-resistant option with comparable edge retention for professional applications.\n\nThe Anmon Twisted Damascus Gyuto is the knife that established Nigara's international reputation — a combination of 400-year heritage aesthetics and thoroughly modern steel performance. The Aogami Super Tsuchime Bunka and SG2 Damascus Kiritsuke extend the range for collectors building comprehensive Nigara sets. For enthusiasts who value both historical depth and technical excellence in their knives, Nigara Hamono represents an unparalleled combination of antiquity and innovation.",
    "Hokiyama": "Hokiyama Hamono is a Tosa-based brand that has earned recognition for producing thin-ground, reactive carbon steel knives at prices that punch above their weight. The two flagship lines — Sakon and Hamokyu — are well-regarded by the knife community for their combination of traditional Aogami carbon steel performance and the Tosa tradition of jiyuu-tanzo (free-form forging). The Ginsan (Silver #3) option provides professionals with a semi-stainless alternative maintaining much of carbon steel's sharpness while significantly reducing maintenance requirements.\n\nThe Tosa tradition of jiyuu-tanzo, or free-form forging, allows smiths to adapt their technique to each individual piece rather than following rigid production specifications. In Hokiyama's hands, this approach produces knives with notably thin grinds and consistent heat treatment — qualities that enthusiast communities consistently highlight in reviews of the Sakon series. Aogami #2 steel, the primary choice for the Sakon line, achieves 62–64 HRC with excellent edge retention and the engaging sharpening feedback that carbon steel enthusiasts prize. The Ginsan (Silver #3) option bridges carbon and stainless performance — taking an edge approaching carbon steel sharpness while resisting rust significantly better.\n\nThe Sakon Aogami #2 Gyuto is consistently cited as one of the finest-value Japanese knives for enthusiasts exploring carbon steel for the first time. Its thin grind, food-release properties, and honest pricing create a combination that rewards the investment in developing a maintenance routine. The Hamokyu Ginsan series serves professional kitchens where carbon steel maintenance is impractical but performance remains the priority. The Nakiri completes a range that covers the most common kitchen cutting needs with consistent Tosa-tradition quality.",
    "Hatsukokoro": "Hatsukokoro is a newer Tosa brand that has rapidly built an international following for its clean aesthetic and high-quality heat treatment. Working with skilled Tosa smiths, the brand produces knives characterized by refined geometry, attractive Wa handles, and careful attention to fit and finish. Their Komorebi series in Aogami Super and the Shirogami #1 offerings have attracted positive reviews from professional chefs and collectors alike. Hatsukokoro represents the evolution of the Tosa tradition: maintaining the region's emphasis on performance and value while adding a more refined aesthetic appeal.\n\nThe Komorebi series — named after the Japanese word for sunlight filtering through leaves — is Hatsukokoro's most celebrated line. Aogami Super core hardened to 64–65 HRC delivers outstanding edge retention alongside the sharpness that carbon steel allows at its finest. The series is distinguished by careful attention to handle pairing and blade geometry refinement, producing knives that compare favorably to Echizen output at Tosa pricing. Shirogami #1 offerings push edge potential to the maximum, providing the purest high-carbon steel experience for enthusiasts who want to explore white steel's unique sharpening feel and edge quality.\n\nThe stainless-clad carbon steel range adds practical convenience — a high-carbon cutting core protected by stainless outer layers reduces maintenance requirements while preserving most of the edge performance. This construction has proven particularly popular with professional chefs and serious home cooks who want Japanese carbon steel performance without full commitment to a carbon steel maintenance routine. Hatsukokoro's willingness to develop multiple product lines at different maintenance and price levels reflects a sophisticated understanding of the contemporary knife enthusiast market.",
    "Harukaze": "Harukaze is a Tosa brand that has found its niche specializing in Ginsan (Silver Steel #3) — the semi-stainless option preferred by professional chefs who want near-carbon performance with reduced maintenance. Ginsan takes an edge that approaches carbon steel sharpness while being significantly more rust-resistant, making it practical for commercial kitchen environments. Harukaze knives are characterized by thin grinds, clean Wa handles, and an unfussy aesthetic that prioritizes cutting performance — the ideal professional's everyday knife.\n\nGinsan (Gingami #3, also called Silver Paper #3) is the steel that defines Harukaze's identity. It contains enough chromium to provide meaningfully better corrosion resistance than pure carbon steels like Aogami or Shirogami, while its carbon content remains high enough to allow sharpening to genuine carbon steel sharpness levels. Professional chefs who have used both describe Ginsan as occupying a uniquely satisfying middle ground — not quite as reactive as pure carbon, not quite as maintenance-free as fully stainless, but combining the best qualities of each. Harukaze's implementation, hardened to 62–63 HRC using Tosa's free-form forging tradition, is widely regarded as one of the finest Ginsan knife makers available.\n\nThe Ginsan Gyuto is the core product — a knife that professional chefs and serious home cooks repeatedly cite as their most-used tool precisely because its performance-to-maintenance balance makes it ideal for daily use. The Aogami #2 alternative satisfies enthusiasts wanting full carbon steel reactivity, while the Ginsan Petty completes the range for detail work. Harukaze's Tosa-forged knives represent an honest, practical Japanese blade philosophy that prioritizes real-world performance over visual drama.",
    "Tsunehisa": "Tsunehisa is a budget-friendly Tosa brand that holds a special place in the Japanese knife community as the most-recommended entry point for enthusiasts wanting to experience authentic Japanese carbon steel without a significant financial commitment. Made in Tosa's tradition of free-form forging, Tsunehisa knives in Aogami #2 offer genuine carbon steel performance typically under $100. While lacking the refined finish of higher-tier makers, Tsunehisa knives are sharp, functional, and authentic — a perfect first Japanese knife for anyone ready to learn the joys and responsibilities of carbon steel care.\n\nAogami #2 (Blue Steel #2) is the primary steel for Tsunehisa's most popular series. At 62–64 HRC, it provides legitimate professional cutting performance — noticeably superior edge retention versus stainless steel at comparable prices, with the sharpening ease that makes blue steel forgiving for beginners developing their whetstone technique. The Migaki (mirror-polished) finish option makes Tsunehisa's budget Gyuto particularly appealing — a polished blade with clean lines that presents well above its price. The Tsuchime (hammered) Santoku adds visual texture and food release benefits.\n\nThe Ginsan option introduces semi-stainless performance to the budget tier — a genuine Ginsan knife at entry-level prices is rare and represents exceptional value for buyers who want low-maintenance convenience without spending on established premium brands. For knife enthusiasts recommending a first quality Japanese knife to someone new to the hobby, Tsunehisa is typically cited alongside Tojiro DP as one of the two most sensible starting points — offering authentic Japanese manufacturing and real performance at prices that make the decision to try carbon steel essentially risk-free.",
    "Chikamasa (Miki)": "Chikamasa was founded in 1977 in Miki City, Hyogo Prefecture, a region with a 500-year history of blade-making known as Banshu Hamono. The brand specializes in garden and craft knives alongside kitchen knives, and is particularly known for its fluorine-coated blades — a practical coating that reduces friction during cutting and improves food release. Chikamasa's kitchen knives represent the accessible end of the price spectrum, but the brand's commitment to functional quality and the Miki tradition of durable, honest blade-making makes it a reliable choice for utility-focused users.\n\nThe fluorine (PTFE) coating applied to Chikamasa's blade line provides a measurable practical benefit: reduced friction during cutting means less effort required for repetitive tasks, and improved food release means less sticking and dragging. While the coating is not indefinite — it will wear with use and sharpening — it adds meaningful value for everyday kitchen and garden use. The underlying steel is stainless, providing low-maintenance convenience appropriate for the brand's utility-focused positioning. Miki's Banshu Hamono tradition, while less internationally celebrated than Sakai or Echizen, represents genuine blade-making heritage dating back five centuries.\n\nChikamasa's kitchen knife range sits at entry-level pricing, making it accessible to buyers not yet ready to invest in premium Japanese blades. The brand's real strength is in its garden knife and utility blade categories, where the fluorine coating's friction-reducing properties are particularly valuable for repetitive agricultural cutting tasks. For buyers who need honest, functional knives at accessible prices with the backing of a real Japanese blade-making tradition, Chikamasa represents a dependable choice that Miki's 500-year heritage validates.",
    "Misono": "Misono was founded in 1935 in Seki and has built an enduring reputation as the premier Western-handle Japanese knife brand for professional kitchens. The Misono UX10 — a Gyuto in Swedish Sandvik stainless steel with a slim Western handle — is widely considered the gold standard for Japanese-style professional knives used in Western kitchen environments. Misono knives have been the choice of Japanese sushi restaurants in America and Europe for decades. For professional chefs coming from a European knife background who want Japanese geometry and edge quality, Misono is often the first and last brand they need.\n\nThe UX10 series uses Swedish Sandvik steel — a premium high-carbon stainless produced in Sweden specifically for cutting tool applications. Its hardness reaches 59–61 HRC, achieving better edge retention than typical German kitchen knives while remaining within a range where daily touch-up on a honing rod remains effective. The slim Western handle profile — narrower and lighter than European equivalents — accommodates both Western and pinch grips, making the transition from European to Japanese geometry intuitive. This combination of familiar ergonomics with superior Japanese blade geometry has made UX10 a go-to recommendation for professional chefs making their first step toward Japanese knife performance.\n\nThe 440 Series provides an accessible entry point in quality stainless at a lower price, while the Dragon Series adds iconic blade engraving for collectors attracted to visual distinction. Both Western and Japanese (Wa) handle options have been introduced across different series, giving buyers flexibility based on their background and preference. Misono's decades of presence in professional kitchens worldwide has established a trust that newer brands require years to develop.",
    "Ryusen": "Ryusen Hamono has been producing knives in Echizen since 1952 and has developed a reputation for bold steel choices and striking Damascus aesthetics. The flagship HAP40 Blazen series uses a high-speed tool steel achieving 67–68 HRC — among the hardest production kitchen knives available — producing extraordinary edge retention for demanding professional use. The Bonten Unryu (Cloud Dragon) Damascus series is one of the most visually distinctive knife lines in the Japanese market. Ryusen's willingness to experiment with exotic steels and bold aesthetics has earned it a loyal collector following worldwide.\n\nHAP40 is the steel that defines Ryusen's most celebrated work. Originally developed as an industrial high-speed tool steel, HAP40 achieves 65–68 HRC in Ryusen's implementation — hardness levels that produce edge retention far exceeding conventional kitchen knife steels. The tradeoff is increased brittleness: HAP40 knives reward careful cutting technique and proper board use, but chefs who adapt their technique find the edge-holding ability transformative for high-volume professional work. The SRS-15 powder stainless steel provides an alternative for chefs wanting extreme hardness with better corrosion resistance — a modern alloy achieving 65–67 HRC.\n\nThe Bonten Unryu 'Cloud Dragon' Damascus series represents Ryusen's visual signature — a flowing, cloud-like Damascus pattern created through careful control of the layering and etching process, making each blade's surface unique. The combination of technical ambition and aesthetic boldness distinguishes Ryusen from more conservative Echizen producers. For collectors and professional chefs who want knives that perform at the extreme end of what Japanese steel technology can achieve, combined with a visual presence that commands attention, Ryusen Hamono offers an essential perspective on what Echizen knife-making can produce.",
}

# ── 代表シリーズ ──
SIGNATURE_KNIVES = {
    "Yu Kurosaki": [
        {"name": "FUJIN Series (Gyuto)", "desc": "Kurosaki's signature hammered-pattern series with wind-god engraving. Aogami Super or ZDP-189 core with explosive tsuchime texture and extraordinary edge retention."},
        {"name": "SENKO Series", "desc": "Flash-themed line with finely hand-engraved blade designs. Renowned for ultra-thin edge geometry and excellent food release properties."},
        {"name": "SHIZUKU Series", "desc": "Droplet-pattern collection showcasing Kurosaki's refined hand-engraving alongside powder steel cores in R2/SG2."},
    ],
    "Yoshimi Kato": [
        {"name": "Super Blue Damascus Gyuto", "desc": "Multi-layer Damascus in Aogami Super. Continues Hiroshi Kato's signature layered forging tradition with a laser-thin grind that defines Echizen craftsmanship."},
        {"name": "R2 Nashiji Series", "desc": "Pear-skin (nashiji) surface finish over SG2 core — beautiful, functional, and low-maintenance. A favorite among professional chefs."},
        {"name": "Aogami Super Tsuchime", "desc": "Hammered carbon steel with stunning visual texture, excellent food release, and the reactive carbon edge performance collectors prize."},
    ],
    "Hideo Kitaoka": [
        {"name": "Wa Yanagiba (Shirogami #1)", "desc": "Single-bevel sashimi knife considered a benchmark by professional sushi chefs. Every detail hand-finished to traditional Sakai standards."},
        {"name": "Wa Deba (Aogami #1)", "desc": "Heavy fish-butchering knife used by top Japanese chefs for breaking down whole fish with precision and power."},
        {"name": "Kiritsuke Yanagiba", "desc": "Hybrid single-bevel knife — traditionally the mark of the head chef — forged to Kitaoka's exacting standards in premium blue steel."},
    ],
    "Takeshi Saji": [
        {"name": "R2 Rainbow Damascus Gyuto", "desc": "Saji's most celebrated work: SG2 core with rainbow-heat-treated layered Damascus cladding. Each blade is uniquely colored by natural heat oxidation."},
        {"name": "VG-10 Black Damascus Santoku", "desc": "Multi-layer VG-10 Damascus with dramatic black finish — striking visual aesthetics at an accessible mid-range price."},
        {"name": "Rainbow Damascus Nakiri", "desc": "Vegetable cleaver with Saji's full rainbow Damascus surface — visually extraordinary and excellent for clean cuts."},
    ],
    "Katsushige Anryu": [
        {"name": "Copper Clad Damascus Gyuto", "desc": "Signature construction with copper incorporated into the forge-welded cladding, producing a warm, unique visual texture unmatched among Echizen makers."},
        {"name": "Aogami #2 Tsuchime Santoku", "desc": "Hammered blue steel Santoku at an accessible price — frequently cited as one of the best-value handmade Japanese knives available."},
        {"name": "Copper Clad Nakiri", "desc": "Vegetable knife in Anryu's distinctive copper-clad style — excellent performance for dedicated vegetable prep with beautiful aesthetics."},
    ],
    "Isamu Takamura": [
        {"name": "R2 Migaki Gyuto", "desc": "Mirror-polished SG2 Gyuto with ultra-thin grind hardened to 64 HRC. Consistently rated one of the finest cutting-performance knives at its price point."},
        {"name": "HSPS Gyuto", "desc": "Proprietary high-speed powder steel offering extreme hardness and edge retention. A performance benchmark for professional chef applications."},
        {"name": "VG-10 Migaki Gyuto", "desc": "Entry-level Takamura in VG-10 — the same ultra-thin grind philosophy at a more accessible price, ideal for chefs new to Japanese knives."},
    ],
    "Nao Yamamoto": [
        {"name": "Iron Clad Aogami Super Gyuto", "desc": "Carbon steel core clad in reactive iron — develops a beautiful protective patina over time while maintaining superb edge quality and a reactive cutting feel."},
        {"name": "Shirogami #1 Gyuto", "desc": "Pure white steel Gyuto with Yamamoto's signature clean geometry, octagonal handle, and the exceptional sharpness of premium white steel."},
        {"name": "Iron Clad Nakiri", "desc": "Vegetable cleaver in Yamamoto's iron-clad construction — a beautiful everyday cooking companion that improves with use and care."},
    ],
    "Shungo Ogata": [
        {"name": "SG2 Mirror Polish Gyuto", "desc": "Powder steel with mirror finish — clean, refined aesthetics combined with excellent SG2 cutting performance at a competitive price."},
        {"name": "Aogami Super Tsuchime Bunka", "desc": "Hammered carbon steel Bunka with distinctive reverse-tanto tip. A collector favorite for its visual appeal and outstanding edge performance."},
        {"name": "R2 Petty", "desc": "Compact utility knife in SG2 — precise, sharp, and refined for detail work in professional and home kitchens."},
    ],
    "Makoto Kurosaki": [
        {"name": "SG2 Gyuto", "desc": "Clean, well-executed SG2 Gyuto with excellent fit and finish. A popular entry point into the Kurosaki family's work at an accessible price."},
        {"name": "Aogami Super Bunka", "desc": "Carbon steel Bunka with striking aesthetic and outstanding cutting performance — the knife that first caught international attention."},
        {"name": "VG-10 Damascus Sujihiki", "desc": "Slicing knife with beautiful Damascus patterning — ideal for carving and slicing proteins with precision."},
    ],
    "Sakai Takayuki": [
        {"name": "Ginga Series (Swedish Steel Gyuto)", "desc": "Professional workhorse in Swedish stainless. Used in top restaurants across Japan. Exceptional edge retention and a reliable first choice for working chefs."},
        {"name": "45-Layer Damascus Gyuto", "desc": "Multi-layer Damascus construction over VG-10 core — stunning visual aesthetics with genuine Sakai performance heritage."},
        {"name": "Itsuo Doi Aogami #2 Yanagiba", "desc": "Single-bevel sashimi knife forged by master Itsuo Doi for the Sakai Takayuki brand — restaurant-grade quality at a more accessible price."},
    ],
    "Itsuo Doi": [
        {"name": "Aogami #2 Yanagiba", "desc": "Doi's signature single-bevel sashimi knife, forged at low temperatures for superior steel structure. Used by Japan's top sushi chefs as their primary cutting tool."},
        {"name": "Aogami #2 Deba", "desc": "Heavy fish knife forged to the same low-temperature standard. An essential professional tool for breaking down whole fish with precision."},
        {"name": "Shirogami #1 Gyuto", "desc": "Double-bevel chef's knife in pure white steel — an exceptional carbon steel cutting tool representing the pinnacle of Sakai double-bevel craft."},
    ],
    "Yasuhiro Hirakawa (Sasuke)": [
        {"name": "Aogami #1 Yanagiba", "desc": "22nd-generation craftsmanship applied to the classic single-bevel sashimi knife. Museum-level quality with centuries of family forging knowledge in every blade."},
        {"name": "Aogami #2 Deba", "desc": "Traditional fish knife forged to Hirakawa's meticulous heritage standards — a collector's piece that functions as a working professional tool."},
        {"name": "Scissor-Knife Combination", "desc": "An extraordinary collector piece — one of the last craftsmen in Japan producing both scissors and knives in the traditional Sakai manner simultaneously."},
    ],
    "Satoshi Nakagawa": [
        {"name": "Aogami #2 Yanagiba", "desc": "Nakagawa's flagship single-bevel sashimi knife — praised for exceptional heat treatment consistency and clean geometry by professional sushi chefs."},
        {"name": "Shirogami #2 Deba", "desc": "White steel fish knife with Nakagawa's characteristic clean geometry and fine polish — a reliable professional tool with exceptional edge quality."},
        {"name": "Aogami #2 Kiritsuke", "desc": "All-purpose single-bevel knife in traditional Sakai style — traditionally the mark of the head chef, now a prized collector's piece."},
    ],
    "Sakai Kikumori": [
        {"name": "Nihonko Carbon Series", "desc": "Traditional carbon steel line offering authentic Sakai performance at accessible prices — an honest entry point into Sakai's knife-making heritage."},
        {"name": "NK Stainless Gyuto", "desc": "Professional-grade stainless Gyuto in Sakai's double-bevel tradition — reliable, sharp, and crafted with the attention to detail Sakai is known for."},
        {"name": "Aogami #1 Yanagiba", "desc": "High-end single-bevel sashimi knife using premium blue steel core — for professional chefs who demand the finest cutting edge in traditional Japanese cuisine."},
    ],
    "Konosuke": [
        {"name": "Fujiyama White #2 Gyuto", "desc": "Konosuke's premium line using traditional Sakai white steel construction. Ultra-thin grind and extraordinary sharpness — a benchmark in the enthusiast community."},
        {"name": "HD2 Gyuto", "desc": "Proprietary stainless steel achieving near-carbon sharpness. A cult-favorite among knife enthusiasts worldwide, often on extended wait lists."},
        {"name": "GS+ Petty", "desc": "Premium stainless compact utility knife — among the finest detail knives available at its price, pairing Konosuke's thin grind with a convenient size."},
    ],
    "Jikko (Sakai Jikko)": [
        {"name": "Honkasumi Aogami #2 Yanagiba", "desc": "Traditional Sakai-forged single-bevel sashimi knife — an authentic entry into professional Japanese knife use at a fair price."},
        {"name": "VG-10 Gyuto Series", "desc": "Stainless double-bevel line offering authentic Sakai quality at mid-range prices — ideal for home cooks wanting to upgrade to Japanese knives."},
        {"name": "Santoku (Aogami #2)", "desc": "Versatile carbon steel kitchen knife — an excellent everyday tool from a genuine Sakai producer with a long history."},
    ],
    "Ichimonji Mitsuhide": [
        {"name": "Mizu Yaki Aogami Yanagiba", "desc": "Water-quenched single-bevel sashimi knife using traditional hardening technique for superior edge quality and steel structure."},
        {"name": "Honyaki Kiritsuke", "desc": "Full-hardened (honyaki) single-bevel kiritsuke — an extremely rare and technically demanding construction for the most serious collectors."},
        {"name": "Shirogami #1 Deba", "desc": "Traditional Sakai fish knife in premium white steel — for professional chefs demanding precision in fish breakdown and butchery."},
    ],
    "MAC Knife": [
        {"name": "Pro Series MSK-65 Gyuto (8.5\")", "desc": "MAC's most popular professional knife — thin, light, and used in culinary schools and restaurant kitchens worldwide. The quintessential Japanese knife for Western chefs."},
        {"name": "Chef's Series HB-85 Bread Knife", "desc": "Valued by professionals for reliable serration and excellent edge retention. Widely used alongside the Pro Gyuto in professional kitchen environments."},
        {"name": "Superior Series Santoku", "desc": "Entry-level MAC line — outstanding value with the same thin Japanese blade geometry at lower prices, ideal for home cooks."},
    ],
    "Miyabi (by Zwilling)": [
        {"name": "5000MCD Birchwood (SG2)", "desc": "Miyabi's flagship: SG2 core, 100-layer Damascus, birchwood handle. Ice-hardened to 63 HRC. Visually stunning and high-performing."},
        {"name": "Kaizen II (VG-10 Damascus)", "desc": "65-layer Damascus over VG-10 core — an excellent balance of visual appeal and cutting performance at a competitive price."},
        {"name": "6000MCT Artisan (SG2)", "desc": "Hand-honed SG2 with traditional Micarta handle. Combines Japanese technique with accessible Seki manufacturing for premium home kitchen use."},
    ],
    "Kai Group (Shun / Kershaw)": [
        {"name": "Shun Classic Gyuto (VG-MAX)", "desc": "The entry point to premium Shun. VG-MAX core, 68-layer Damascus, PakkaWood handle. America's best-selling Japanese-style kitchen knife."},
        {"name": "Shun Premier Nakiri (VG-MAX)", "desc": "Hammered tsuchime finish with VG-MAX core and walnut-finished PakkaWood handle. Elegant aesthetics for dedicated vegetable work."},
        {"name": "Shun Kaji Gyuto (SG2)", "desc": "Premium Shun line in SG2 powder steel — the highest-performance option in the Kai lineup for serious cooks and collectors."},
    ],
    "Tojiro": [
        {"name": "DP Cobalt Gyuto F-807 (8.2\")", "desc": "The most recommended beginner Japanese knife in the world. VG-10 core, triple-rivet Western handle, professional performance at an unbeatable price."},
        {"name": "Senkou Hammered Gyuto", "desc": "Premium Tojiro line with hammered tsuchime finish and improved handle materials — a significant upgrade at a still-reasonable mid-range price."},
        {"name": "Shirogami Gyuto (Traditional Series)", "desc": "Authentic white steel carbon option from Tojiro — traditional performance at an accessible price, introducing carbon steel to new enthusiasts."},
    ],
    "Tamahagane": [
        {"name": "Tsubame San Mai Gyuto", "desc": "Tsubame series flagship: high-carbon steel core clad in stainless for the best of both materials — sharpness of carbon, ease of stainless."},
        {"name": "Tsubame Hammered Santoku", "desc": "Three-layer San Mai construction with distinctive hammered surface texture — beautiful and functional for everyday cooking."},
        {"name": "San Mai Sujihiki", "desc": "Slicing knife in Tamahagane's signature San Mai construction — excellent for carving roasts and slicing proteins with precision."},
    ],
    "Nigara Hamono": [
        {"name": "Anmon Twisted Damascus Gyuto", "desc": "Signature twisted Damascus pattern created by twisting steel layers during forging. Visually extraordinary — a direct link to the forge's 400-year sword-making heritage."},
        {"name": "Aogami Super Tsuchime Bunka", "desc": "Carbon steel Bunka with hammered finish — functional and visually striking, showcasing Nigara's centuries of metallurgical knowledge."},
        {"name": "SG2 Damascus Kiritsuke", "desc": "Powder steel head chef's knife with layered Damascus aesthetic from Japan's oldest continuously operating knife-making lineage."},
    ],
    "Hokiyama": [
        {"name": "Sakon Aogami #2 Gyuto", "desc": "Hokiyama's flagship carbon steel line — thin grinds and excellent edge quality at Tosa value pricing. Consistently praised for performance-to-price ratio."},
        {"name": "Hamokyu Ginsan Gyuto", "desc": "Semi-stainless Ginsan option delivering near-carbon performance with significantly reduced maintenance — ideal for busy professional kitchens."},
        {"name": "Sakon Nakiri", "desc": "Vegetable cleaver in Hokiyama's Tosa carbon steel tradition — clean cuts and honest performance for dedicated vegetable prep."},
    ],
    "Hatsukokoro": [
        {"name": "Komorebi Aogami Super Gyuto", "desc": "'Dappled Light' series — Hatsukokoro's signature line combining superb Aogami Super heat treatment with refined aesthetics and clean Wa handle pairing."},
        {"name": "Shirogami #1 Tsuchime Nakiri", "desc": "Pure white steel vegetable knife with hammered finish — exceptional edge quality and visual appeal for dedicated vegetable work."},
        {"name": "Stainless-Clad Santoku", "desc": "Carbon steel core with stainless cladding — high performance with added rust resistance for everyday use without sacrifice of cutting quality."},
    ],
    "Harukaze": [
        {"name": "Ginsan Gyuto", "desc": "Harukaze's core product: semi-stainless Silver #3 Gyuto with thin Tosa grind and practical Wa handle. The professional's low-maintenance everyday knife."},
        {"name": "Aogami #2 Gyuto", "desc": "Blue steel alternative for those wanting reactive carbon steel performance from Harukaze's thin Tosa geometry."},
        {"name": "Ginsan Petty", "desc": "Compact utility knife in Silver #3 — a practical, low-maintenance detail knife for precision work in professional and home kitchens."},
    ],
    "Tsunehisa": [
        {"name": "Aogami #2 Migaki Gyuto", "desc": "Mirror-finish carbon steel Gyuto — Tsunehisa's most recommended model for first-time Japanese knife buyers wanting authentic carbon steel at entry prices."},
        {"name": "Aogami #2 Tsuchime Santoku", "desc": "Hammered finish Santoku at budget price — authentic carbon steel performance with visual texture at an unbeatable price point."},
        {"name": "Ginsan Gyuto", "desc": "Semi-stainless option for buyers wanting Tsunehisa quality and Tosa forging with less maintenance than pure carbon steel."},
    ],
    "Chikamasa (Miki)": [
        {"name": "B-500SF Fluorine Gyuto", "desc": "Kitchen knife with fluorine coating for reduced friction and easy food release. Entry-level Japanese kitchen knife from Miki's 500-year blade-making tradition."},
        {"name": "Garden Knife Series (B-300)", "desc": "Miki-region utility and garden knives — the brand's core specialty alongside kitchen cutlery, using Banshu Hamono craftsmanship."},
        {"name": "Stainless Kitchen Series", "desc": "Everyday stainless kitchen knives made with Miki's traditional blade-making heritage — functional, durable, and honestly priced."},
    ],
    "Misono": [
        {"name": "UX10 Gyuto (Swedish Sandvik Steel)", "desc": "The gold standard for Western-handle Japanese knives. Used by sushi chefs worldwide. Slim, precise, extremely durable — a lifelong knife for serious professionals."},
        {"name": "440 Series Gyuto", "desc": "Entry-level Misono in high-quality stainless steel — the same slim Japanese geometry and professional feel at a more accessible price."},
        {"name": "Dragon Stainless Gyuto", "desc": "Premium Misono series with iconic dragon engraving on the blade. Swedish steel with beautiful blade road geometry and collector appeal."},
    ],
    "Ryusen": [
        {"name": "Blazen Series (HAP40 Steel)", "desc": "HAP40 high-speed tool steel at 67–68 HRC — extraordinary edge retention for the most demanding professional use. Among the hardest production kitchen knives available."},
        {"name": "Bonten Unryu 'Cloud Dragon' Damascus", "desc": "'Cloud Dragon' Damascus pattern — among the most visually dramatic and recognized knife designs in the Japanese market for collectors."},
        {"name": "SRS-15 Gyuto", "desc": "Exotic powder stainless steel offering extreme hardness and corrosion resistance — Ryusen's commitment to the frontier of steel technology in kitchen knives."},
    ],
}

# ── 購入先リンク ──
RETAILER_LINKS = {
    "Yu Kurosaki": [
        {"name": "Kurosaki Official Store", "url": "https://kurosaki-knife.com/", "note": "Official online shop"},
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/collections/yu-kurosaki", "note": "Canada / USA"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/yukurosaki.html", "note": "USA"},
        {"name": "Seisuke Knife", "url": "https://us.seisukeknife.com/collections/yu-kurosaki", "note": "Japan-based"},
    ],
    "Yoshimi Kato": [
        {"name": "Takefu Knife Village", "url": "https://en.takefu-knifevillage.jp/", "note": "Official Takefu Village shop"},
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/collections/yoshimi-kato", "note": "Canada / USA"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/yoshimikato.html", "note": "USA"},
    ],
    "Hideo Kitaoka": [
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/collections/hideo-kitaoka", "note": "Primary international retailer"},
        {"name": "Japanese Chef's Knife", "url": "https://japanesechefsknife.com/collections/hideo-kitaoka", "note": "Specialist Japan knife store"},
        {"name": "Tokushu Knife", "url": "https://tokushuknife.com/collections/hideo-kitaoka", "note": "USA curated selection"},
    ],
    "Takeshi Saji": [
        {"name": "Japanese Chef's Knife", "url": "https://japanesechefsknife.com/collections/takeshi-saji", "note": "Primary international retailer"},
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/collections/takeshi-saji", "note": "Canada / USA"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/takeshisaji.html", "note": "USA"},
    ],
    "Katsushige Anryu": [
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/blogs/articles/blacksmith-profile-katsushige-anryu", "note": "Profile + shop"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/katsushigeanryu.html", "note": "USA"},
        {"name": "Seisuke Knife", "url": "https://us.seisukeknife.com/collections/anryu", "note": "Japan-based"},
    ],
    "Isamu Takamura": [
        {"name": "Takamura Official", "url": "https://takamuraknife.com/", "note": "Official website"},
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/collections/takamura", "note": "Canada / USA"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/takamura.html", "note": "USA"},
    ],
    "Nao Yamamoto": [
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/collections/nao-yamamoto", "note": "Primary international retailer"},
        {"name": "Tokushu Knife", "url": "https://tokushuknife.com/collections/nao-yamamoto", "note": "USA curated"},
        {"name": "Seisuke Knife", "url": "https://us.seisukeknife.com/collections/nao-yamamoto", "note": "Japan-based"},
    ],
    "Shungo Ogata": [
        {"name": "Seisuke Knife", "url": "https://us.seisukeknife.com/collections/shungo-ogata", "note": "Primary international retailer"},
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/collections/shungo-ogata", "note": "Canada / USA"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/shungo-ogata.html", "note": "USA"},
    ],
    "Makoto Kurosaki": [
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/collections/makoto-kurosaki", "note": "Primary international retailer"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/makoto-kurosaki.html", "note": "USA"},
        {"name": "Seisuke Knife", "url": "https://us.seisukeknife.com/collections/makoto-kurosaki", "note": "Japan-based"},
    ],
    "Sakai Takayuki": [
        {"name": "Hocho-Knife.com", "url": "https://www.hocho-knife.com/sakai-takayuki/", "note": "Official international store"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/sakai-takayuki.html", "note": "USA"},
        {"name": "Korin", "url": "https://www.korin.com/Japanese-Knives-Sakai-Takayuki", "note": "USA Japanese culinary specialist"},
    ],
    "Itsuo Doi": [
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/collections/itsuo-doi", "note": "Primary international retailer"},
        {"name": "Korin", "url": "https://www.korin.com/Japanese-Knives-Itsuo-Doi", "note": "USA Japanese specialist"},
        {"name": "Seisuke Knife", "url": "https://us.seisukeknife.com/collections/itsuo-doi", "note": "Japan-based"},
    ],
    "Yasuhiro Hirakawa (Sasuke)": [
        {"name": "Sasuke Official", "url": "http://sasuke-smith.com/English_version/e-about-sasuke.html", "note": "Official workshop website"},
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/collections/sasuke", "note": "Canada / USA"},
        {"name": "Tokushu Knife", "url": "https://tokushuknife.com/collections/sasuke", "note": "USA curated"},
    ],
    "Satoshi Nakagawa": [
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/collections/satoshi-nakagawa", "note": "Primary international retailer"},
        {"name": "Seisuke Knife", "url": "https://us.seisukeknife.com/collections/satoshi-nakagawa", "note": "Japan-based"},
        {"name": "Tokushu Knife", "url": "https://tokushuknife.com/collections/satoshi-nakagawa", "note": "USA"},
    ],
    "Sakai Kikumori": [
        {"name": "Kikumori Official", "url": "https://www.kikumori.co.jp/", "note": "Official website"},
        {"name": "Hocho-Knife.com", "url": "https://www.hocho-knife.com/sakai-kikumori/", "note": "International Sakai specialist"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/sakai-kikumori.html", "note": "USA"},
    ],
    "Konosuke": [
        {"name": "Konosuke Official", "url": "https://konosukeknives.com/", "note": "Official Konosuke store (US-based)"},
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/collections/konosuke", "note": "Canada / USA"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/konosuke.html", "note": "USA"},
    ],
    "Jikko (Sakai Jikko)": [
        {"name": "Jikko Official", "url": "https://jikkocutlery.com/", "note": "Official Jikko store — English available"},
        {"name": "Hocho-Knife.com", "url": "https://www.hocho-knife.com/jikko/", "note": "Sakai specialist"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/jikko.html", "note": "USA"},
    ],
    "Ichimonji Mitsuhide": [
        {"name": "Ichimonji Mitsuhide Official", "url": "https://global.ichimonji.co.jp/", "note": "Official English global store"},
        {"name": "Hocho-Knife.com", "url": "https://www.hocho-knife.com/ichimonji-mitsuhide/", "note": "Sakai specialist"},
        {"name": "Korin", "url": "https://www.korin.com/Japanese-Knives", "note": "USA Japanese culinary specialist"},
    ],
    "MAC Knife": [
        {"name": "MAC Official", "url": "https://macknife.com/", "note": "Official MAC website (USA)"},
        {"name": "Cutlery and More", "url": "https://www.cutleryandmore.com/mac-knives", "note": "USA knife retailer"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/macknives.html", "note": "USA"},
    ],
    "Miyabi (by Zwilling)": [
        {"name": "Miyabi Official", "url": "https://www.miyabi-knives.com/", "note": "Official Miyabi website"},
        {"name": "Cutlery and More", "url": "https://www.cutleryandmore.com/miyabi", "note": "USA retailer"},
        {"name": "Williams Sonoma", "url": "https://www.williams-sonoma.com/shop/cutlery/miyabi/", "note": "Available at Williams Sonoma"},
    ],
    "Kai Group (Shun / Kershaw)": [
        {"name": "Shun Official", "url": "https://www.shuncutlery.com/", "note": "Official Shun website (USA)"},
        {"name": "Cutlery and More", "url": "https://www.cutleryandmore.com/shun", "note": "USA knife retailer"},
        {"name": "Williams Sonoma", "url": "https://www.williams-sonoma.com/shop/cutlery/shun/", "note": "Available at Williams Sonoma"},
    ],
    "Tojiro": [
        {"name": "Tojiro Official", "url": "https://tojiro.net/en/", "note": "Official website — English"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/tojiro.html", "note": "USA — wide selection"},
        {"name": "Korin", "url": "https://www.korin.com/Japanese-Knives-Tojiro", "note": "USA Japanese culinary specialist"},
    ],
    "Tamahagane": [
        {"name": "Tamahagane Official", "url": "https://tamahagane.jp/en/", "note": "Official website — English"},
        {"name": "Cutlery and More", "url": "https://www.cutleryandmore.com/tamahagane", "note": "USA retailer"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/tamahagane.html", "note": "USA"},
    ],
    "Nigara Hamono": [
        {"name": "Nigara Official", "url": "https://nigaraknives.com/", "note": "Official Nigara English store"},
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/collections/nigara", "note": "Canada / USA"},
        {"name": "Seisuke Knife", "url": "https://us.seisukeknife.com/collections/nigara-hamono", "note": "Japan-based"},
    ],
    "Hokiyama": [
        {"name": "Hokiyama Official", "url": "https://www.hokiyama.com/", "note": "Official website"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/hokiyama.html", "note": "USA"},
        {"name": "Tokushu Knife", "url": "https://tokushuknife.com/collections/hokiyama", "note": "USA curated"},
    ],
    "Hatsukokoro": [
        {"name": "Cutlery and More", "url": "https://cutleryandmore.com/collections/hatsukokoro", "note": "USA primary retailer"},
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/collections/hatsukokoro", "note": "Canada / USA"},
        {"name": "Tokushu Knife", "url": "https://tokushuknife.com/collections/hatsukokoro", "note": "USA curated"},
    ],
    "Harukaze": [
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/habl2kn.html", "note": "USA primary retailer"},
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/collections/harukaze", "note": "Canada / USA"},
        {"name": "Tokushu Knife", "url": "https://tokushuknife.com/collections/harukaze", "note": "USA curated"},
    ],
    "Tsunehisa": [
        {"name": "Tokushu Knife", "url": "https://tokushuknife.com/collections/tsunehisa-1", "note": "Primary international retailer"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/tsunehisa.html", "note": "USA"},
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/collections/tsunehisa", "note": "Canada / USA"},
    ],
    "Chikamasa (Miki)": [
        {"name": "Chikamasa Official", "url": "https://chikamasa.co.jp/", "note": "Official website (Japanese)"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/chikamasa.html", "note": "USA"},
        {"name": "Amazon", "url": "https://www.amazon.com/s?k=Chikamasa+knife", "note": "Widely available online"},
    ],
    "Misono": [
        {"name": "Misono Official", "url": "https://misonoknife.com/", "note": "Official English website"},
        {"name": "Korin", "url": "https://www.korin.com/Japanese-Knives-Misono", "note": "USA Japanese culinary specialist"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/misono.html", "note": "USA"},
    ],
    "Ryusen": [
        {"name": "Ryusen Official", "url": "https://www.ryusen-japan.com/", "note": "Official website"},
        {"name": "Chef Knives To Go", "url": "https://www.chefknivestogo.com/ryusen.html", "note": "USA"},
        {"name": "Knifewear", "url": "https://knifewear.com/en-us/collections/ryusen", "note": "Canada / USA"},
    ],
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
        url = maker['url']
        RETAILER_DOMAINS = ['knifewear.com', 'japanesechefsknife.com', 'seisukeknife.com',
                            'cutleryandmore.com', 'chefknivestogo.com', 'tokushuknife.com']
        if any(d in url for d in RETAILER_DOMAINS):
            btn_label = 'Browse Knives &#8599;'
        else:
            btn_label = 'Visit Official Site &#8599;'
        site_btn = f'<a class="btn-primary" href="{url}" target="_blank" rel="noopener">{btn_label}</a>'

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

    # Biography セクション
    bio_text = BIOGRAPHY.get(maker['nameEn'], '')
    if bio_text:
        bio_paras = ''.join(
            f'<p class="description-text">{p.strip()}</p>'
            for p in bio_text.split('\n\n') if p.strip()
        )
        biography_section = f'<div class="section"><h2>Biography</h2>{bio_paras}</div>'
    else:
        biography_section = ''

    # Signature Knives セクション
    sig_knives = SIGNATURE_KNIVES.get(maker['nameEn'], [])
    if sig_knives:
        knife_items_html = ''.join(
            f'<div class="knife-item"><strong>{k["name"]}</strong><p>{k["desc"]}</p></div>'
            for k in sig_knives
        )
        signature_section = f'<div class="section"><h2>Signature Knife Series</h2><div class="knife-guide">{knife_items_html}</div></div>'
    else:
        signature_section = ''

    # Where to Buy セクション
    retailers = RETAILER_LINKS.get(maker['nameEn'], [])
    if retailers:
        retailer_cards_html = ''.join(
            f'<a class="retailer-link" href="{r["url"]}" target="_blank" rel="noopener"><div class="retailer-name">{r["name"]}</div><div class="retailer-note">{r["note"]} &#8599;</div></a>'
            for r in retailers
        )
        retailer_section = f'<div class="section"><h2>Where to Buy</h2><div class="retailer-grid">{retailer_cards_html}</div></div>'
    else:
        retailer_section = ''

    # 鋼材ガイドセクション
    steel_guide_items = ''
    for steel in maker['steelTypes']:
        if steel in STEEL_DESC:
            steel_guide_items += f'<div class="steel-guide-item"><strong>{steel}</strong><p>{STEEL_DESC[steel][:200]}...</p></div>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon.ico" sizes="any">
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
  <link rel="canonical" href="https://japan-knife-makers.com/items/{slug}.html"/>
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
    .knife-item{{margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid var(--border)}}
    .knife-item:last-child{{margin-bottom:0;padding-bottom:0;border-bottom:none}}
    .knife-item strong{{font-family:'Helvetica Neue',Arial,sans-serif;font-size:.9rem;color:var(--navy);display:block;margin-bottom:4px}}
    .knife-item p{{font-size:.88rem;line-height:1.6;color:var(--muted)}}
    .retailer-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px}}
    .retailer-link{{display:block;padding:14px 16px;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);transition:border-color .2s,box-shadow .2s;text-decoration:none}}
    .retailer-link:hover{{border-color:var(--gold);box-shadow:0 2px 8px rgba(0,0,0,.08);text-decoration:none}}
    .retailer-name{{font-family:'Helvetica Neue',Arial,sans-serif;font-size:.88rem;font-weight:700;color:var(--navy);margin-bottom:4px}}
    .retailer-note{{font-family:'Helvetica Neue',Arial,sans-serif;font-size:.75rem;color:var(--muted)}}
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

  {biography_section}

  <div class="section">
    <h2>Specialty Knife Types</h2>
    <div class="pill-list">{specialty_pills}</div>
  </div>

  {signature_section}

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

  {retailer_section}

  <div class="actions" style="margin-bottom:32px">
    {site_btn}
    <a class="btn-back" href="../index.html">&#8592; Back to All Makers</a>
  </div>

  {'<div class="section"><h2>Other ' + maker["region"] + ' Makers</h2><div class="related-grid">' + related_cards + '</div></div>' if related_cards else ''}

</div>

<footer>
  <strong>Japan Knife Makers Database</strong>
  <p>An independent guide to Japanese knife-making traditions. &middot; <a href="../index.html" style="color:#8A90A8">&#8592; All Makers</a></p>
  <p style="margin-top:8px"><a href="../about.html" style="color:#8A90A8">About</a> &middot; <a href="../contact.html" style="color:#8A90A8">Contact</a> &middot; <a href="../privacy.html" style="color:#8A90A8">Privacy Policy</a></p>
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
