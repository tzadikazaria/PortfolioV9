#!/usr/bin/env python3
"""Generates the V9 pages from one shared template so every page stays consistent."""
import os
from PIL import Image

import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
A = ROOT + '/assets/'

# ---------------------------------------------------------------- helpers
def dims(name):
    with Image.open(A + name + '.webp') as im:
        return im.size

def img(name, alt, sizes='(max-width:700px) 92vw, 50vw', eager=False, cls=''):
    w, h = dims(name)
    ss = []
    for v in (480, 960):
        if os.path.exists(A + f'{name}-{v}.webp') and v < w:
            ss.append(f'assets/{name}-{v}.webp {v}w')
    ss.append(f'assets/{name}.webp {w}w')
    srcset = ', '.join(ss)
    load = 'loading="eager"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ''
    return (f'<img src="assets/{name}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{alt}"{c} {load} decoding="async">')

def fig(name, alt, cap=None, num=None, sizes=None, zoom=True, style=''):
    sz = sizes or '(max-width:700px) 92vw, 40vw'
    im = img(name, alt, sz)
    inner = (f'<button class="zoom" data-lightbox aria-label="Enlarge: {alt}">{im}</button>'
             if zoom else im)
    c = ''
    if cap:
        n = f'<b>{num}</b>' if num else ''
        c = f'<figcaption>{n}<span>{cap}</span></figcaption>'
    st = f' style="{style}"' if style else ''
    return f'<figure class="fg"{st}>{inner}{c}</figure>'

def note(label, text, n=None):
    num = f'<b>{n}</b> ' if n else ''
    return (f'<div class="note wrap"><p class="lab">{num}{label}</p><p class="txt">{text}</p></div>')

def gal(figs, n=3, bg=None, cls='', wide=False):
    body = f'<div class="gal n{n} {cls}">' + ''.join(figs) + '</div>'
    if bg:
        return f'<div class="panel {"wide" if wide else "wrap"}" style="--bg:{bg}">{body}</div>'
    return f'<div class="{"wide" if wide else "wrap"}">{body}</div>'

# ---------------------------------------------------------------- shared chrome
def head(title, desc, body_class):
    return f'''<!doctype html><html lang="en" id="top"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#F3F3F2"><meta name="description" content="{desc}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><title>{title}</title><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="theme.css"><link rel="stylesheet" href="v9.css"><script src="app.js" defer></script></head><body class="{body_class}"><a class="skip" href="#main">Skip to content</a>
'''

def header(current):
    def cur(k):
        return ' aria-current="page"' if k == current else ''
    return f'''<header class="site-header" id="siteheader"><div class="hdr"><a class="brand" href="index.html" aria-label="Tzadik Azaria home"><img src="assets/logo.svg" width="117" height="35" alt="Tzadik"></a><nav class="nav" id="navigation" aria-label="Main navigation"><div class="nav-main"><a href="index.html#work"{cur('work')}>Projects</a><a href="about.html"{cur('about')}>About</a><a href="#contact">Contact</a></div><div class="nav-side"><a class="pill" href="assets/TzadikAzaria_CV.pdf" download="Tzadik-Azaria-CV.pdf">Download CV</a></div></nav><button class="menu-toggle" aria-expanded="false" aria-controls="navigation">Menu</button></div></header>
'''

FOOTER = '''<footer class="footer" id="contact"><div class="wrap"><div class="footer-top"><p class="eyebrow">Have something in mind?</p><p class="availability">Open to full-time opportunities</p></div><a class="footer-title" href="mailto:tzadikazaria@gmail.com">Let’s work <em>together.</em></a><div class="footer-bottom"><span class="mail"><a href="mailto:tzadikazaria@gmail.com">tzadikazaria@gmail.com</a><button class="copy" type="button" data-copy="tzadikazaria@gmail.com" aria-label="Copy email address">Copy</button></span><div class="footer-links"><a href="https://www.linkedin.com/in/tzadik-azaria" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a><a href="assets/TzadikAzaria_CV.pdf" download="Tzadik-Azaria-CV.pdf">Download CV ↓</a></div><span class="copyright">© 2026 Tzadik Azaria · <a href="#top">Back to top ↑</a></span></div></div></footer>
<dialog class="lightbox" aria-label="Project image viewer"><button class="lightbox-close" aria-label="Close image viewer">Close ×</button><button class="lb-nav prev" aria-label="Previous image">←</button><button class="lb-nav next" aria-label="Next image">→</button><div class="lightbox-inner"><img alt=""><p></p></div></dialog></body></html>'''

# ---------------------------------------------------------------- projects
PROJECTS = [
    dict(slug='campaign', n='01', title='Campaign &amp; <em>digital design.</em>', short='Campaign &amp; Digital Design',
         kind='real', kind_label='Commercial work', bg='#171719',
         tag='Campaigns · Social · E-commerce · Email',
         blurb='Connected campaign creative for beauty and lifestyle brands — one visual direction carried across social, web, email and paid media.',
         desc='Commercial campaign design across social, web, email and paid media for beauty and lifestyle brands.',
         lead='One idea. Many moments. A connected visual language across the places a brand shows up.',
         detail='Commercial campaign design for beauty and lifestyle brands. My work covered campaign concepting, visual design and execution, balancing expressive imagery with clear promotional hierarchy across formats.',
         meta=[('Role', 'Digital Designer'), ('Context', 'Multi-brand retail'), ('Scope', 'Concepting &amp; visual design'), ('Channels', 'Social · Web · Email · Paid media')]),
    dict(slug='marketplace', n='02', title='Marketplace<br><em>product visuals.</em>', short='Marketplace Product Visuals',
         kind='real', kind_label='Commercial work', bg='#E8E4DE',
         tag='E-commerce · Infographics · Systems',
         blurb='Scalable listing systems that make product benefits clear at a glance.',
         desc='Product visuals and scalable listing systems for beauty and wellness brands on Asian e-commerce marketplaces.',
         lead='Make the benefit clear. Make the brand recognizable. Make the system repeatable.',
         detail='Product visuals for beauty and wellness brands across Asian e-commerce marketplaces. The challenge was to organize benefits, product photography and usage information into adaptable layouts that stay clear at different sizes.',
         meta=[('Role', 'Digital Designer'), ('Focus', 'Scalable product listings'), ('Markets', 'Asian e-commerce'), ('Output', 'Product visual systems')]),
    dict(slug='hatachana', n='03', title='Hatachana', short='Hatachana',
         kind='acad', kind_label='Academic concept', bg='#ECBA40',
         tag='Identity · Illustration · Mobile UI',
         blurb='Identity, illustration and a mobile tour experience for a complex urban landmark.',
         desc='Academic concept: identity, illustration and a mobile tour experience for the Tel Aviv Central Bus Station.',
         lead='A complex place. A clear way in. An identity that invites people to explore.',
         detail='The Central Bus Station is layered and overwhelming. This academic concept combines a distinct visual identity, character illustration and guided mobile flows to make discovery feel more approachable.',
         meta=[('Project', 'Academic concept'), ('Scope', 'Identity · UI · Illustration'), ('Focus', 'Guided urban tours'), ('Place', 'Tel Aviv Central Bus Station')]),
    dict(slug='sambusak', n='04', title='Give Me<br><em>Sambusak.</em>', short='Give Me Sambusak',
         kind='acad', kind_label='Academic concept', bg='#DDDADF',
         tag='Identity · Packaging · Spatial',
         blurb='A loud, friendly street-food identity — from packaging to a stand you can step into, and a self-ordering screen.',
         desc='Academic concept: a street-food identity across packaging, signage, space and a self-ordering interface.',
         lead='A street-food brand with an appetite for personality. Built to be seen, held and stepped into.',
         detail='The aim was to create a complete, recognizable identity for a busy public environment. Bold typography, playful food icons and a warm palette carry the same character from takeaway packaging to signage and digital ordering.',
         meta=[('Project', 'Academic concept'), ('Focus', 'Street-food experience'), ('Scope', 'Identity · Packaging · Space'), ('Digital', 'Self-ordering flow')]),
]
BY = {p['slug']: p for p in PROJECTS}

# thumbnails for the "next project" card
NEXT_THUMB = {
    'campaign': ('#171719', 'campaign-04', 'Fine Rituals Tax Free campaign'),
    'marketplace': ('#E8E4DE', 'marketplace-09', 'Beauty product listing with benefit icons'),
    'hatachana': ('#ECBA40', 'hatachana-00', 'Hatachana identity and app overview'),
    'sambusak': ('#DDDADF', 'home-07-cut', 'Give Me Sambusak packaging'),
}

# ---------------------------------------------------------------- case-study body per project
def body_campaign():
    out = []
    out.append(f'<div class="cover wide dark" style="--bg:#171719;--ar:2.05"><div class="trio">'
               + img('campaign-04', 'Fine Rituals Tax Free campaign', '(max-width:700px) 40vw, 26vw', True)
               + img('campaign-01', 'Beauty serum product campaign', '(max-width:700px) 40vw, 26vw', True)
               + img('campaign-03', 'Fine Rituals Mystery Box campaign', '(max-width:700px) 40vw, 26vw', True)
               + '</div></div>')
    out.append(note('Different moods, same intention', 'Seasonal campaigns, launches and promotional moments each need their own tone. A consistent hierarchy keeps the message clear while colour, imagery and composition give each campaign its character.', '01'))
    out.append(gal([
        fig('campaign-16', 'Cleansing mousse campaign — pink product composition', 'Cleansing mousse', sizes='(max-width:700px) 92vw, 34vw'),
        fig('campaign-02', 'Plenaire skincare promotional design', 'Plenaire skincare', sizes='(max-width:700px) 92vw, 34vw'),
        fig('campaign-20', 'Fine Rituals candle campaign — green composition', 'Candle campaign', sizes='(max-width:700px) 92vw, 34vw'),
    ], 3))
    out.append(note('One campaign, a wider canvas', 'The Flame Sale direction carries warm, atmospheric product imagery across email, web and social. Layout and scale change; the identity and core message stay connected.', '02'))
    flame = ('<div class="panel wide" style="--bg:#E4DDD6"><div class="flame">'
             + fig('campaign-07', 'Flame Sale email campaign, full layout', 'Email', sizes='(max-width:700px) 92vw, 30vw')
             + '<div class="col">'
             + fig('campaign-08', 'Flame Sale website banner', 'Website banner', sizes='(max-width:700px) 92vw, 52vw')
             + fig('campaign-09', 'Flame Sale social campaign', 'Social', sizes='(max-width:700px) 92vw, 52vw')
             + '</div></div></div>')
    out.append(flame)
    out.append(note('Built to travel', 'From the product-led hero to the supporting social asset, a visual system has to flex without losing recognition.', '03'))
    out.append(gal([
        fig('campaign-11', 'Beauty serum hero visual', 'Product-led hero', sizes='(max-width:700px) 92vw, 46vw'),
        fig('campaign-14', 'Skincare campaign — product in use', 'Product in use', sizes='(max-width:700px) 92vw, 46vw'),
    ], 2))
    out.append('<p class="sublab wrap">More from the collection</p>')
    out.append(gal([
        fig('campaign-15', 'Skincare supporting campaign imagery'),
        fig('campaign-17', 'Beauty promotional campaign on red'),
        fig('campaign-21', 'Fine Rituals beauty promotion'),
        fig('campaign-23', 'Signature skincare bundle campaign'),
    ], 4, cls='sm'))
    return out

def body_marketplace():
    out = []
    out.append('<div class="cover wide" style="--bg:#E8E4DE;--ar:2.05"><div class="trio flat">'
               + img('marketplace-09', 'Beauty product listing with benefit icons', '(max-width:700px) 40vw, 26vw', True)
               + img('marketplace-02', 'Lip product benefit listing', '(max-width:700px) 40vw, 26vw', True)
               + img('marketplace-11', 'Razor product visual', '(max-width:700px) 40vw, 26vw', True)
               + '</div></div>')
    out.append(note('A product story, at a glance', 'A simple benefit hierarchy helps the shopper find what matters. Product photography, textures and concise iconography work together rather than competing for attention.', '01'))
    out.append(gal([
        fig('marketplace-03', 'Mascara ingredient benefit layout', 'Mascara — ingredients', sizes='(max-width:700px) 92vw, 46vw'),
        fig('marketplace-16', 'Skincare active ingredient visual', 'Skincare — active ingredient', sizes='(max-width:700px) 92vw, 46vw'),
    ], 2, bg='#E8E4DE'))
    out.append(note('First the product, then the details', 'A listing unfolds in layers: introduce the product, explain what makes it different, then show how it fits into a routine.', '02'))
    out.append(gal([
        fig('marketplace-06', 'Razor hero product image', 'Product', '01', sizes='(max-width:700px) 92vw, 34vw'),
        fig('marketplace-04', 'Razor product benefit layout', 'Benefits', '02', sizes='(max-width:700px) 92vw, 34vw'),
        fig('marketplace-08', 'Razor usage demonstration', 'Use', '03', sizes='(max-width:700px) 92vw, 34vw'),
    ], 3, bg='#E8E4DE', wide=True))
    out.append(note('The structure stays, the character shifts', 'Reusable modules make it possible to move between product families without flattening their identities. The information stays consistent while photography, colour and tone belong to each brand.', '03'))
    out.append(gal([
        fig('marketplace-14', 'Mascara hydrating ingredient visual', 'Mascara', sizes='(max-width:700px) 92vw, 34vw'),
        fig('marketplace-18', 'Eyeliner thin and flat applicator comparison', 'Eyeliner — applicator comparison', sizes='(max-width:700px) 92vw, 34vw'),
        fig('marketplace-12', 'Razor feature overview', 'Razor — features', sizes='(max-width:700px) 92vw, 34vw'),
    ], 3))
    out.append(gal([
        fig('marketplace-17', 'Product photography in warm light', 'Product photography', sizes='(max-width:700px) 92vw, 46vw'),
        fig('marketplace-15', 'Mascara revitalizing ingredients', 'Mascara — revitalizing', sizes='(max-width:700px) 92vw, 46vw'),
    ], 2, cls='tight'))
    return out

def body_hatachana():
    out = []
    out.append('<div class="cover wide" style="--bg:#ECBA40;--ar:2.165"><div class="full">'
               + img('hatachana-00', 'Hatachana identity and app overview', '(max-width:700px) 100vw, 1360px', True)
               + '</div></div>')
    out.append(note('The people make the place', 'Playful characters soften the industrial setting. A vivid yellow acts as a signal, with black and white creating a clear, direct framework around the illustrations.', '01'))
    out.append('<div class="panel wide" style="--bg:#ECBA40"><div class="chars">'
               + img('hatachana-01', 'Female urban explorer illustration', '(max-width:700px) 40vw, 300px')
               + img('hatachana-02', 'Male urban explorer illustration', '(max-width:700px) 40vw, 300px')
               + '</div><p class="cap-in">Character illustrations</p></div>')
    out.append(note('A little orientation, a lot to discover', 'The mobile experience connects registration, tour discovery and booking. The same colour and illustration language carries through the interface, keeping brand and digital experience connected.', '02'))
    out.append(gal([
        fig('home-05', 'Hatachana mobile introduction', 'Introduction', sizes='(max-width:700px) 60vw, 20vw'),
        fig('hatachana-07', 'Hatachana sign-in screen', 'Join', sizes='(max-width:700px) 60vw, 20vw'),
        fig('hatachana-06', 'Hatachana tour discovery screen', 'Explore &amp; choose', sizes='(max-width:700px) 60vw, 20vw'),
        fig('home-06', 'Hatachana tour detail mobile screen', 'Tour details', sizes='(max-width:700px) 60vw, 20vw'),
        fig('hatachana-05', 'Hatachana tour details and booking screen', 'Book', sizes='(max-width:700px) 60vw, 20vw'),
    ], 5, bg='#F1EEE6', cls='phones', wide=True))
    return out

def body_sambusak():
    out = []
    out.append('<div class="cover wide" style="--bg:#DDDADF;--ar:2.05"><div class="one">'
               + img('home-07-cut', 'Give Me Sambusak paper bag, box, wrapping and cup packaging', '(max-width:700px) 90vw, 760px', True)
               + '</div></div>')
    out.append(note('Loud. Friendly. A little hungry.', 'A playful Hebrew wordmark anchors the identity. Simple food icons and a compact colour palette create a flexible language that can grow from a small sticker to a large environmental graphic.', '01'))
    out.append('<div class="panel wide dark" style="--bg:#27272B"><div class="sys">'
               + fig('sambusak-02', 'Give Me Sambusak Hebrew wordmark', 'Wordmark', sizes='(max-width:700px) 92vw, 44vw')
               + fig('sambusak-01', 'Give Me Sambusak typography, palette and food icon system', 'Typography, palette and icons', sizes='(max-width:700px) 92vw, 44vw')
               + '</div></div>')
    out.append(gal([
        fig('sambusak-03', 'Branded kraft paper bag on a café table', 'Paper bag', sizes='(max-width:700px) 92vw, 46vw'),
        fig('sambusak-04', 'Physical Give Me Sambusak packaging samples', 'Packaging samples', sizes='(max-width:700px) 92vw, 46vw'),
    ], 2, cls='tight'))
    out.append('<div class="wrap tightwrap">' + fig('sambusak-05', 'Yellow and blue branded takeaway cups', 'Takeaway cups', sizes='(max-width:700px) 92vw, 1100px') + '</div>')
    out.append(note('Beyond the bag, into the street', 'Oversized graphics and strong colour make the physical stand part of the identity. The system moves from handheld packaging to a space people can recognize and enter.', '02'))
    out.append(gal([
        fig('sambusak-06', 'Branded street-food stand front', 'Stand — front', sizes='(max-width:700px) 60vw, 28vw'),
        fig('sambusak-07', 'Give Me Sambusak branded environmental panels', 'Environmental panels', sizes='(max-width:700px) 92vw, 44vw'),
        fig('sambusak-08', 'Street-food stand side with oversized graphics', 'Stand — side', sizes='(max-width:700px) 60vw, 28vw'),
    ], 3, cls='spat'))
    out.append(note('Same appetite, a digital order', 'The self-ordering concept brings the brand into the interface, using its visual language to keep the experience friendly and the choices clear.', '03'))
    out.append('<div class="panel wide" style="--bg:#EEEBE7"><div class="one tab">' + fig('sambusak-09', 'Give Me Sambusak self-ordering tablet interface', 'Self-ordering interface', sizes='(max-width:700px) 92vw, 1000px') + '</div></div>')
    return out

BODIES = dict(campaign=body_campaign, marketplace=body_marketplace, hatachana=body_hatachana, sambusak=body_sambusak)

def case_page(i):
    p = PROJECTS[i]
    nxt = PROJECTS[(i + 1) % 4]
    prv = PROJECTS[(i - 1) % 4]
    meta = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in p['meta'])
    badge_cls = 'real' if p['kind'] == 'real' else 'acad'
    note_txt = '' if p['kind'] == 'real' else '<span class="acad-note">Self-initiated study — not a client project</span>'
    nbg, nimg, nalt = NEXT_THUMB[nxt['slug']]
    nxt_img = img(nimg, nalt, '(max-width:700px) 80vw, 380px')
    html = head(f"{p['short'].replace('&amp;','&amp;')} — Tzadik Azaria", p['desc'], 'inner case')
    html += header('work')
    html += f'''<main id="main">
<section class="ch wrap">
<div class="ch-top"><a class="back-link" href="index.html#work">← Selected work</a><span class="kind {badge_cls}">{p['kind_label']}</span></div>
<div class="ch-main"><h1 class="ct">{p['title']}</h1><div class="ci"><p class="cl">{p['lead']}</p><p class="cd">{p['detail']}</p>{note_txt}</div></div>
<dl class="cm">{meta}</dl>
</section>
'''
    html += '\n'.join(BODIES[p['slug']]())
    html += f'''
<section class="nx wrap" aria-label="Next project"><div class="nx-top"><span class="lab">Project {p['n']} of 04</span><a class="prev-link" href="{prv['slug']}.html">← {prv['short']}</a></div>
<a class="nx-a" href="{nxt['slug']}.html"><div class="nx-t"><span class="lab">Next project</span><span class="nx-h">{nxt['short']}</span><span class="nx-k"><span class="kind {'real' if nxt['kind']=='real' else 'acad'}">{nxt['kind_label']}</span></span></div><span class="nx-m" style="--bg:{nbg}">{nxt_img}<span class="go" aria-hidden="true">↗</span></span></a></section>
</main>
'''
    html += FOOTER
    open(f"{ROOT}/{p['slug']}.html", 'w').write(html)

# ---------------------------------------------------------------- home
def home():
    feat = BY['campaign']
    def tile_media(slug):
        if slug == 'campaign':
            return ('<span class="pj-m feat-m" style="--bg:#171719"><span class="trio3">'
                    + img('campaign-04', 'Fine Rituals Tax Free campaign', '(max-width:700px) 40vw, 28vw', True)
                    + img('campaign-16', 'Cleansing mousse campaign', '(max-width:700px) 40vw, 28vw', True)
                    + img('campaign-09', 'Flame Sale social campaign', '(max-width:700px) 40vw, 28vw', True)
                    + '</span><span class="go" aria-hidden="true">↗</span></span>')
        if slug == 'marketplace':
            return ('<span class="pj-m" style="--bg:#E8E4DE"><span class="mk">'
                    + img('marketplace-09', 'Beauty product listing with benefit icons', '(max-width:700px) 60vw, 24vw')
                    + img('marketplace-02', 'Lip product benefits and features', '(max-width:700px) 60vw, 24vw')
                    + '</span><span class="go" aria-hidden="true">↗</span></span>')
        if slug == 'hatachana':
            return ('<span class="pj-m" style="--bg:#ECBA40"><span class="ht">'
                    + img('hatachana-01', 'Illustrated urban explorer', '(max-width:700px) 40vw, 14vw')
                    + img('home-05', 'Hatachana mobile tour experience', '(max-width:700px) 40vw, 16vw')
                    + '</span><span class="go" aria-hidden="true">↗</span></span>')
        return ('<span class="pj-m" style="--bg:#DDDADF"><span class="sb">'
                + img('home-07-cut', 'Give Me Sambusak brand packaging', '(max-width:700px) 90vw, 32vw')
                + '</span><span class="go" aria-hidden="true">↗</span></span>')
    def tile(p, featured=False):
        cls = 'pj feat' if featured else 'pj'
        k = 'real' if p['kind'] == 'real' else 'acad'
        extra = '<span class="pj-star">Featured</span>' if featured else ''
        return (f'<a class="{cls} rv" href="{p["slug"]}.html">{tile_media(p["slug"])}'
                f'<span class="pj-c"><span class="pj-n">{p["n"]}</span><span class="pj-t"><h3>{p["short"]}</h3><p>{p["blurb"]}</p></span>'
                f'<span class="pj-k"><span class="kind {k}">{p["kind_label"]}</span><span class="pj-tags">{p["tag"]}</span><span class="pj-cta">View case study <i aria-hidden="true">→</i></span></span></span></a>')
    stk = ('<img class="stk" src="assets/hatachana-01-cut.webp" alt="" aria-hidden="true" draggable="false" style="--x:7%;--y:52%;--h:190px;--r:-5deg;--mx:5%;--my:13%;--d:.5s">'
           '<img class="stk" src="assets/hatachana-02.webp" alt="" aria-hidden="true" draggable="false" style="--x:90%;--y:50%;--h:190px;--r:5deg;--mx:74%;--my:12%;--d:.6s">'
           '<img class="stk" src="assets/home-07-cut.webp" alt="" aria-hidden="true" draggable="false" style="--x:78%;--y:84%;--h:104px;--r:6deg;--mx:58%;--my:88%;--d:.8s">')
    h = head('Tzadik Azaria — Visual &amp; Creative Designer', 'Brand identities, digital campaigns and visual experiences by Tzadik Azaria. Based in Israel.', 'home')
    h += header('work')
    h += f'''<main id="main">
<section class="hero2" id="hero" aria-labelledby="hero-title">
<div class="hero2-in"><p class="eyebrow"><i aria-hidden="true"></i>Tzadik Azaria — Visual &amp; Creative Designer</p>
<h1 id="hero-title"><span>Design with clarity.</span><span class="l2">And a <b class="sel">point of view.<i class="hd tl"></i><i class="hd tr"></i><i class="hd bl"></i><i class="hd br"></i><em class="dim" aria-hidden="true">W 0 × H 0</em></b></span></h1>
<svg class="vec" aria-hidden="true" focusable="false"><path class="vp" d=""/><path class="vh" d=""/><g class="vpts"></g></svg>
<p class="sub">Brand identities, digital campaigns and visual experiences. Thoughtfully made to connect across every touchpoint.</p>
<div class="actions"><a class="cta" href="#work">Selected projects <span aria-hidden="true">↓</span></a><a class="ghost" href="about.html">About me <span aria-hidden="true">→</span></a></div></div>
{stk}
<p class="hint" aria-hidden="true">Drag the middle point of the curve — it reshapes the type</p></section>

<section class="work wrap" id="work" aria-labelledby="work-title"><div class="work-head"><p class="kicker" id="work-title">Selected Projects</p><h2 class="lede rv">Brand, campaigns and digital design — led by clarity, craft and a point of view.</h2><p class="work-key rv"><span class="kind real">Commercial work</span><span class="kind acad">Academic concept</span></p></div>
<div class="pj-grid">
{tile(PROJECTS[0], True)}
{tile(PROJECTS[1])}
{tile(PROJECTS[2])}
{tile(PROJECTS[3])}
</div></section>

<section class="about-strip wrap"><h2 class="rv">A thoughtful approach.<br><em>A versatile perspective.</em></h2><p class="rv">I’m a designer working across brands, campaigns and digital experiences. I combine a strong eye for typography and composition with the practical care it takes to bring an idea into the world.</p><a class="text-link rv" href="about.html">More about me <span aria-hidden="true">→</span></a></section></main>
'''
    h += FOOTER
    open(f'{ROOT}/index.html', 'w').write(h)
    # legacy URL: keep old home.html working
    open(f'{ROOT}/home.html', 'w').write('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=index.html"><link rel="canonical" href="index.html"><title>Tzadik Azaria</title></head><body><a href="index.html">Continue to the portfolio</a></body></html>')

# ---------------------------------------------------------------- about
def about():
    h = head('About — Tzadik Azaria', 'Tzadik Azaria is a visual and digital designer working across branding, campaigns, e-commerce and digital experiences.', 'inner about')
    h += header('about')
    exp = [
        ('OG Brands Ltd.', 'Digital and print design for international beauty and wellness brands, across e-commerce, social media, campaigns and retail. Product visuals, banners, newsletters, marketplace content and promotional materials, in collaboration with marketing, sales, operations and external suppliers.'),
        ('Freelance', 'Branding, brochures, signage, presentations and digital marketing materials for clients across different industries. Projects managed from the initial brief through feedback, revisions and final delivery.'),
        ('ORT Hermelin College', 'Posters, educational publications and marketing materials for college initiatives, alongside support for students in design principles and creative software.'),
    ]
    xp = ''.join(f'<article class="xp"><span class="xn">0{i+1}</span><h2>{o}</h2><p>{d}</p></article>' for i, (o, d) in enumerate(exp))
    h += f'''<main id="main"><div class="about-page wrap">
<section class="about-hero"><div><p class="eyebrow">About Tzadik</p><h1>Thoughtful design.<br><em>From idea<br>to execution.</em></h1></div><p class="about-intro">I’m Tzadik Azaria, a visual and digital designer based in Israel. I work across branding, campaigns, e-commerce and digital experiences, with an eye for typography, layout and the details that hold a brand together.</p></section>
<section class="about-story"><p class="eyebrow">Perspective</p><div><p>My experience spans in-house and freelance work — from product visuals and digital campaigns to web, print and retail materials. I enjoy taking a project from its first brief through concept, refinement and final production.</p><p>I’m looking for my next full-time opportunity in a studio, agency or in-house creative team, where I can contribute, keep learning and grow toward creative design and art direction.</p><div class="about-actions"><a class="text-link" href="assets/TzadikAzaria_CV.pdf" download="Tzadik-Azaria-CV.pdf">Download CV <span>↓</span></a><a class="text-link ghost-l" href="mailto:tzadikazaria@gmail.com">Get in touch <span>→</span></a></div></div></section>
<section class="experience-section"><p class="eyebrow">Experience</p><div class="experience-list">{xp}</div></section>
<section class="about-lists"><div><h2>Capabilities</h2><ul><li>Brand identity</li><li>Digital campaigns</li><li>E-commerce &amp; product visuals</li><li>Web &amp; UI design</li><li>Print &amp; packaging</li><li>Presentations &amp; video editing</li></ul></div><div><h2>Tools</h2><ul><li>Figma · Wix Studio</li><li>Photoshop · Illustrator</li><li>InDesign · Premiere Pro</li><li>Shopify · Blender</li></ul></div><div><h2>Education</h2><p>ORT Hermelin College<br>Practical Engineer Diploma<br>in Media Design</p><p class="education-note">Graduated with Distinction</p></div></section></div></main>
'''
    h += FOOTER
    open(f'{ROOT}/about.html', 'w').write(h)

home(); about()
for i in range(4):
    case_page(i)
print('built')
