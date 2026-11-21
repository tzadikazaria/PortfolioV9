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

def fig(name, alt, cap=None, num=None, sizes=None, zoom=True, style='', eager=False):
    sz = sizes or '(max-width:700px) 92vw, 40vw'
    im = img(name, alt, sz, eager)
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


def band(num, label, text, inner, bg='#F3F3F2', mode='side', dark=False, cls=''):
    """Full-bleed colour band. mode 'side': sticky text column + large images. mode 'top': text row above a wide gallery."""
    lab = f'<p class="lab"><b>{num}</b>{label}</p>' if label else ''
    txt = f'<p class="txt">{text}</p>' if text else ''
    head_ = f'<div class="band-txt">{lab}{txt}</div>' if (label or text) else ''
    d = ' dark' if dark else ''
    return (f'<section class="band {mode}{d} {cls}" style="--bg:{bg}"><div class="band-in">{head_}<div class="band-body">{inner}</div></div></section>')

def g(figs, n=3, cls=''):
    return f'<div class="gal n{n} {cls}">' + ''.join(figs) + '</div>'

# ---------------------------------------------------------------- shared chrome
def head(title, desc, body_class):
    return f'''<!doctype html><html lang="en" id="top"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#F3F3F2"><meta name="description" content="{desc}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><title>{title}</title><link rel="icon" href="favicon-tz-light.svg" type="image/svg+xml" media="(prefers-color-scheme: light)"><link rel="icon" href="favicon-tz-dark.svg" type="image/svg+xml" media="(prefers-color-scheme: dark)"><link rel="apple-touch-icon" href="apple-touch-icon-v94.png"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="theme.css"><link rel="stylesheet" href="v9.css"><script src="app.js" defer></script></head><body class="{body_class}"><a class="skip" href="#main">Skip to content</a>
'''

def header(current):
    def cur(k):
        return ' aria-current="page"' if k == current else ''
    return f'''<header class="site-header" id="siteheader"><div class="hdr"><a class="brand" href="index.html" aria-label="Tzadik Azaria — home"><svg class="logo" role="img" aria-label="Tzadik" viewBox="0 0 117 35" fill="currentColor" xmlns="http://www.w3.org/2000/svg"> <path d="M37.1564 4.64562L37.1545 4.65131L28.2211 28.5096H32.526L30.4352 34.5H19.3094L21.0225 29.9664L24.1695 21.6005L25.112 19.0617L25.1129 19.0589L29.9721 6.03693H21.3063V0H38.8818L37.1564 4.64562Z" /> <path d="M19.3892 5.90406H12.797V34.4943H6.59402V5.90406H0V0.000949054H19.3892V5.90406Z" /> <path fill-rule="evenodd" clip-rule="evenodd" d="M49.2473 0.000949054H51.3106L64.2339 34.4943H57.5146L54.563 26.5631H42.8536L39.9011 34.4943H33.1799L46.1534 0.000949054H48.2233L48.7368 0L49.2473 0.000949054ZM45.0649 20.622H52.3593L48.7235 10.8401L45.0649 20.622Z" /> <path d="M102.191 9.38994L108.365 0.000949054H116.034L104.317 17.2861L116.101 34.4943H108.37L102.191 25.1822V34.4943H95.9863V0.000949054H102.191V9.38994Z" /> <path d="M92.5897 34.4934H86.3867V0H92.5897V34.4934Z" /> <path fill-rule="evenodd" clip-rule="evenodd" d="M65.9497 0.00474527C69.5105 0.00483633 72.6817 0.639252 75.3492 1.93512C81.1321 4.70135 84.0614 10.2331 84.0615 17.2946C84.0615 17.7243 84.0494 18.1661 84.0245 18.5977L84.0235 18.6214L84.0207 18.6451L83.9941 19.0295C83.9836 19.1686 83.9687 19.3233 83.9523 19.467C83.7431 21.7793 83.1843 23.9159 82.2687 25.8114L82.2621 25.8238L82.2573 25.8361L81.9954 26.3334C81.9095 26.4908 81.8259 26.6386 81.7524 26.77L81.1422 27.8623H81.0406C79.8883 29.4922 78.4177 30.8483 76.657 31.9005L76.6465 31.9062L76.0543 32.2403C75.45 32.5647 74.8076 32.8605 74.1249 33.1144L74.1239 33.1134C73.0869 33.5118 71.9676 33.8349 70.7795 34.0568L70.5859 34.0938H67.3221L66.8077 32.6987L66.5401 31.9765L57.4102 7.74333L57.4083 7.73858L56.2514 4.64467L56.2504 4.64372L54.5174 0.00474527H65.9497ZM68.293 19.0523L68.2939 19.056L69.2363 21.5948L71.5425 27.7266C71.8018 27.6319 72.0504 27.5306 72.2875 27.421L72.2951 27.4172C72.9233 27.1299 73.4905 26.789 74.0157 26.4008C74.6381 25.9278 75.1645 25.4215 75.5997 24.8586L75.6007 24.8576C75.7712 24.6373 75.9121 24.4431 76.0268 24.2607L76.0391 24.2426L76.0505 24.2236C76.9368 22.8759 77.5154 21.1668 77.7123 19.0646L77.7161 19.0285L77.7199 18.9934C77.7447 18.7997 77.7624 18.5925 77.7712 18.3841L77.7731 18.3367L77.7778 18.2902C77.8022 18.0079 77.8034 17.7005 77.8034 17.2946C77.8034 13.8413 76.9242 11.2344 75.3985 9.426C73.9038 7.6545 71.5868 6.41146 68.2047 6.03124H63.4366L68.293 19.0523Z" /> </svg> </a><nav class="nav" id="navigation" aria-label="Main navigation"><div class="nav-main"><a href="index.html#work"{cur('work')}>Projects</a><a href="about.html"{cur('about')}>About</a><a href="#contact">Contact</a></div><div class="nav-side"><a class="pill" href="assets/TzadikAzaria_CV.pdf" download="Tzadik-Azaria-CV.pdf">Download CV</a></div></nav><button class="menu-toggle" aria-expanded="false" aria-controls="navigation">Menu</button></div></header>
'''

FOOTER = '''<footer class="footer" id="contact"><div class="wrap"><div class="footer-top"><p class="eyebrow">Have something in mind?</p><p class="availability">Open to full-time opportunities</p></div><a class="footer-title" href="mailto:tzadikazaria@gmail.com">Let’s work <em>together.</em></a><div class="footer-bottom"><span class="mail"><a href="mailto:tzadikazaria@gmail.com">tzadikazaria@gmail.com</a><button class="copy" type="button" data-copy="tzadikazaria@gmail.com" aria-label="Copy email address">Copy</button></span><div class="footer-links"><a href="https://www.linkedin.com/in/tzadik-azaria" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a><a href="assets/TzadikAzaria_CV.pdf" download="Tzadik-Azaria-CV.pdf">Download CV ↓</a></div><span class="copyright">© 2026 Tzadik Azaria · <a href="#top">Back to top ↑</a></span></div></div></footer>
<dialog class="lightbox" aria-label="Project image viewer"><button class="lightbox-close" aria-label="Close image viewer">Close ×</button><button class="lb-nav prev" aria-label="Previous image">←</button><button class="lb-nav next" aria-label="Next image">→</button><div class="lightbox-inner"><img alt=""><p></p></div></dialog></body></html>'''

# ---------------------------------------------------------------- projects
PROJECTS = [
    dict(slug='campaign', n='01', title='Campaign &amp; <em>digital design.</em>', short='Campaign &amp; Digital Design',
         kind='real', kind_label='Commercial work', bg='#171719',
         tag='Campaigns · Social · Email · Banners',
         blurb='Campaign and promotional visuals for beauty and wellness brands, adapted for social, web and email.',
         desc='Commercial campaign and promotional visuals for beauty and wellness brands, designed for social, web, email and banners.',
         lead='Campaign and promotional visuals for beauty and wellness brands.',
         detail='Commercial work designed for social, web, email and banners. The selection shows how promotional messages and product imagery are laid out for different brands and formats.',
         meta=[('Work', 'Commercial'), ('Scope', 'Visual design &amp; adaptation'), ('Formats', 'Social · Web · Email · Banners'), ('Sector', 'Beauty &amp; wellness')]),
    dict(slug='marketplace', n='02', title='Marketplace<br><em>product visuals.</em>', short='Marketplace Product Visuals',
         kind='real', kind_label='Commercial work', bg='#E8E4DE',
         tag='E-commerce · Infographics · Systems',
         blurb='Product listing visuals that make benefits clear at a glance.',
         desc='Product listing visuals for beauty and wellness brands on Asian e-commerce marketplaces.',
         lead='Product listing visuals for beauty and wellness brands on Asian e-commerce marketplaces.',
         detail='Benefits, product photography and usage information organized into layouts that stay clear at different sizes.',
         meta=[('Work', 'Commercial'), ('Focus', 'Product listing visuals'), ('Markets', 'Asian e-commerce'), ('Output', 'Benefit layouts &amp; icons')]),
    dict(slug='hatachana', n='03', title='Hatachana', short='Hatachana',
         kind='acad', kind_label='Academic concept', bg='#ECBA40',
         tag='Identity · Illustration · Mobile UI',
         blurb='An identity and mobile app that present Tel Aviv’s Central Bus Station as a place to explore.',
         desc='Academic concept: an identity, character illustrations and a mobile app for guided tours of Tel Aviv’s Central Bus Station.',
         lead='An identity and mobile app that invite people to rediscover Tel Aviv’s Central Bus Station.',
         detail='Hatachana is Hebrew for “the station”. The concept presents the Central Bus Station as a place to explore through guided tours. A yellow, black and white palette and illustrated explorer characters carry from the identity into the app.',
         meta=[('Project', 'Academic concept'), ('Scope', 'Identity · Illustration · Mobile UI'), ('Subject', 'Tel Aviv Central Bus Station'), ('Focus', 'Guided tours')]),
    dict(slug='sambusak', n='04', title='Give Me<br><em>Sambusak.</em>', short='Give Me Sambusak',
         kind='acad', kind_label='Academic concept', bg='#DDDADF',
         tag='Identity · Packaging · Spatial',
         blurb='A street-food identity applied to packaging, a stand and a self-ordering screen.',
         desc='Academic concept: a street-food identity applied to packaging, a physical stand and a self-ordering interface.',
         lead='A street-food identity applied to packaging, a physical stand and a self-ordering screen.',
         detail='Hebrew lettering, playful food icons and a bright palette carry one character from takeaway packaging to environmental graphics and a digital ordering interface.',
         meta=[('Project', 'Academic concept'), ('Scope', 'Identity · Packaging · Space · UI'), ('Subject', 'Street food'), ('Digital', 'Self-ordering interface')]),
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
def cover(bg, ar, inner, cls=''):
    return f'<div class="cover {cls}" style="--bg:{bg};--ar:{ar}">{inner}</div>'

def M(*items, cls=''):
    """12-column editorial grid. items are fig() strings."""
    return f'<div class="mx {cls}">' + ''.join(items) + '</div>'

def F(name, alt, cap, cols, row=None, pct=40, num=None, extra=''):
    st = f'grid-column:{cols};' + (f'grid-row:{row};' if row else '') + extra
    return fig(name, alt, cap, num, sizes=f'(max-width:700px) 92vw, {pct}vw', style=st)

def body_campaign():
    out = []
    out.append(cover('#171719', '2.05', '<div class="trio">'
               + img('campaign-04', 'Fine Rituals Tax Free campaign', '(max-width:700px) 40vw, 26vw', True)
               + img('campaign-01', 'Beauty serum product campaign', '(max-width:700px) 40vw, 26vw', True)
               + img('campaign-03', 'Fine Rituals Mystery Box campaign', '(max-width:700px) 40vw, 26vw', True)
               + '</div>'))
    out.append(band('01', 'Offers and products', 'Promotions and product highlights for different brands, laid out so the message and the product stay easy to read.',
        M(F('campaign-16', 'Cleansing mousse campaign — pink product composition', 'Cleansing mousse', '1/9', '1/3', 62),
          F('campaign-02', 'Plenaire skincare promotional design', 'Plenaire skincare', '9/13', '1/2', 31),
          F('campaign-20', 'Fine Rituals candle campaign — green composition', 'Candle campaign', '9/13', '2/3', 31)),
        '#F3F3F2', 'top'))
    out.append(band('02', 'One campaign, three formats', 'The Flame Sale as an email, a website banner and a social post, each laid out for its own format.',
        M(F('campaign-07', 'Flame Sale email campaign, full layout', 'Email', '1/5', '1/3', 26),
          F('campaign-08', 'Flame Sale website banner', 'Website banner', '5/13', '1/2', 52),
          F('campaign-09', 'Flame Sale social campaign', 'Social', '6/12', '2/3', 40)),
        '#E4DDD6', 'side'))
    out.append(band('03', 'In context', 'A product page on the web and a social feed with campaign posts.',
        M(F('campaign-06', 'Website product page shown on a laptop', 'Website product page', '1/9', None, 62, extra='align-self:center'),
          F('campaign-00-cut', 'Social feed and campaign post shown on two phones', 'Social feed and campaign post', '9/13', None, 31, extra='align-self:center')),
        '#171719', 'top', True))
    out.append(band('04', 'Product-led visuals', 'Skincare and beauty layouts that put the product first.',
        M(F('campaign-14', 'Skincare campaign — product in use', 'Product in use', '1/9', '1/3', 62),
          F('campaign-11', 'Beauty serum hero visual', 'Product-led hero', '9/13', '1/2', 31),
          F('campaign-23', 'Signature skincare bundle campaign', 'Product bundle', '9/13', '2/3', 31)),
        '#F3F3F2', 'side'))
    out.append(band('05', 'More from the collection', '',
        M(F('campaign-15', 'Skincare supporting campaign imagery', None, '1/5', None, 31),
          F('campaign-17', 'Beauty promotional campaign on red', None, '5/9', None, 31, extra='margin-top:clamp(32px,5vw,80px)'),
          F('campaign-21', 'Fine Rituals beauty promotion', None, '9/13', None, 31)),
        '#E9E7E4', 'top'))
    return out

def body_marketplace():
    out = []
    out.append(cover('#E8E4DE', '2.05', '<div class="trio flat">'
               + img('marketplace-09', 'Beauty product listing with benefit icons', '(max-width:700px) 40vw, 26vw', True)
               + img('marketplace-02', 'Lip product benefit listing', '(max-width:700px) 40vw, 26vw', True)
               + img('marketplace-11', 'Razor product visual', '(max-width:700px) 40vw, 26vw', True)
               + '</div>'))
    out.append(band('01', 'Benefits at a glance', 'Product photography, textures and concise icons share one hierarchy, so the main benefit reads quickly.',
        M(F('marketplace-03', 'Mascara ingredient benefit layout', 'Mascara — ingredients', '1/8', None, 56),
          F('marketplace-16', 'Skincare active ingredient visual', 'Skincare — active ingredient', '8/13', None, 40, extra='margin-top:clamp(48px,8vw,128px)')),
        '#F0EDE8', 'top'))
    out.append(band('02', 'Product, benefits, use', 'A listing set moves from the product to its benefits to how it is used.',
        M(F('marketplace-06', 'Razor hero product image', 'Product', '1/9', '1/3', 62, num='01'),
          F('marketplace-04', 'Razor product benefit layout', 'Benefits', '9/13', '1/2', 31, num='02'),
          F('marketplace-08', 'Razor usage demonstration', 'Use', '9/13', '2/3', 31, num='03')),
        '#E8E4DE', 'top'))
    out.append(band('03', 'Benefit icons', 'Icons for product benefits.',
        M(F('marketplace-01', 'Set of benefit icons with labels', None, '1/13', None, 92)),
        '#F7F6F3', 'top'))
    out.append(band('04', 'Across product families', 'The same structure adapts to different products, while photography, colour and tone follow each one.',
        M(F('marketplace-14', 'Mascara hydrating ingredient visual', 'Mascara', '1/5', None, 31),
          F('marketplace-18', 'Eyeliner thin and flat applicator comparison', 'Eyeliner — applicator comparison', '5/9', None, 31, extra='margin-top:clamp(32px,5vw,80px)'),
          F('marketplace-12', 'Razor feature overview', 'Razor — features', '9/13', None, 31))
        + M(F('marketplace-05', 'Deodorant ingredient and benefit layout on stone', 'Ingredient story', '1/8', '1/3', 56),
            F('marketplace-19', 'Skincare benefits layout with portrait photography', 'Skincare — benefits', '8/13', '1/2', 40),
            F('marketplace-07', 'Razor refills with sustainability icons', 'Razor — refills', '9/13', '2/3', 31), cls='again'),
        '#F0EDE8', 'top'))
    out.append(band('', 'Photography', '',
        M(F('marketplace-17', 'Product photography in warm light', 'Product photography', '2/8', None, 50),
          F('marketplace-15', 'Mascara revitalizing ingredients', 'Mascara — revitalizing', '8/12', None, 31, extra='margin-top:clamp(40px,6vw,96px)')),
        '#E8E4DE', 'top'))
    return out

def body_hatachana():
    out = []
    out.append(cover('#ECBA40', '2.165', '<div class="full">' + img('hatachana-00', 'Hatachana identity and app overview', '100vw', True) + '</div>', 'fullimg'))
    out.append(band('01', 'Explorers, not commuters', 'Characters with cameras and phones set the tone: visitors discovering the station, not just passing through it. Yellow, black and white keep the identity simple and direct.',
        '<div class="chars three">' + img('hatachana-01', 'Female urban explorer illustration', '(max-width:700px) 30vw, 300px')
        + img('hatachana-02', 'Male urban explorer illustration', '(max-width:700px) 30vw, 300px') + '</div>',
        '#ECBA40', 'side'))
    out.append(band('02', 'From identity to app', 'The app uses the same palette and illustration style for sign-in, tour discovery and booking. Tour screens show duration, price, date, guide and group size.',
        '<div class="gal n5 phones stagger">'
        + fig('home-05', 'Hatachana mobile introduction', 'Introduction', sizes='(max-width:700px) 46vw, 20vw', eager=True)
        + fig('hatachana-07', 'Hatachana sign-in screen', 'Join', sizes='(max-width:700px) 46vw, 20vw', eager=True)
        + fig('hatachana-06', 'Hatachana tour discovery screen', 'Explore &amp; choose', sizes='(max-width:700px) 46vw, 20vw', eager=True)
        + fig('home-06', 'Hatachana tour detail mobile screen', 'Tour details', sizes='(max-width:700px) 46vw, 20vw', eager=True)
        + fig('hatachana-05', 'Hatachana tour details and booking screen', 'Book', sizes='(max-width:700px) 46vw, 20vw', eager=True)
        + '</div>',
        '#F1EEE6', 'top'))
    return out

def body_sambusak():
    out = []
    out.append(cover('#DDDADF', '2.05', '<div class="one">' + img('home-07-cut', 'Give Me Sambusak paper bag, box, wrapping and cup packaging', '(max-width:700px) 90vw, 760px', True) + '</div>'))
    out.append(band('01', 'Wordmark and system', 'A Hebrew wordmark, food icons and a compact palette form the core of the identity.',
        '<div class="stack">' + fig('sambusak-02', 'Give Me Sambusak Hebrew wordmark', 'Wordmark', sizes='(max-width:700px) 92vw, 60vw')
        + fig('sambusak-01', 'Give Me Sambusak typography, palette and food icon system', 'Typography, palette and icons', sizes='(max-width:700px) 92vw, 60vw') + '</div>',
        '#27272B', 'side', True))
    out.append(band('02', 'Packaging to space', 'The identity extends from handheld packaging to the stand and its oversized graphics.',
        M(F('sambusak-03', 'Branded kraft paper bag on a café table', 'Paper bag', '1/8', None, 56),
          F('sambusak-04', 'Physical Give Me Sambusak packaging samples', 'Packaging samples', '6/13', '2/3', 50, extra='margin-top:calc(-1 * clamp(24px,5vw,80px));z-index:2'))
        + M(F('sambusak-05', 'Yellow and blue branded takeaway cups', 'Takeaway cups', '3/11', None, 66), cls='again'),
        '#F3F3F2', 'top'))
    out.append(band('03', 'Stand', 'The stand carries the identity through environmental panels and oversized graphics.',
        M(F('sambusak-06', 'Branded street-food stand front', 'Stand — front', '1/4', None, 24, extra='align-self:end'),
          F('sambusak-07', 'Give Me Sambusak branded environmental panels', 'Environmental panels', '4/10', None, 46, extra='align-self:center'),
          F('sambusak-08', 'Street-food stand side with oversized graphics', 'Stand — side', '10/13', None, 24, extra='margin-top:clamp(40px,6vw,96px)')),
        '#F1EFF4', 'top'))
    out.append(band('04', 'Self-ordering', 'The same identity continues into a tablet ordering interface.',
        M(F('sambusak-09', 'Give Me Sambusak self-ordering tablet interface', 'Self-ordering interface', '1/13', None, 92)),
        '#EEEBE7', 'top'))
    return out

BODIES = dict(campaign=body_campaign, marketplace=body_marketplace, hatachana=body_hatachana, sambusak=body_sambusak)

def case_page(i):
    p = PROJECTS[i]
    nxt = PROJECTS[(i + 1) % 4]
    prv = PROJECTS[(i - 1) % 4]
    meta = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in p['meta'])
    badge_cls = 'real' if p['kind'] == 'real' else 'acad'
    note_txt = '' if p['kind'] == 'real' else '<span class="acad-note">Academic concept — not a client project</span>'
    nbg, nimg, nalt = NEXT_THUMB[nxt['slug']]
    nxt_img = img(nimg, nalt, '(max-width:700px) 80vw, 380px')
    html = head(f"{p['short'].replace('&amp;','&amp;')} — Tzadik Azaria", p['desc'], 'inner case')
    html += header('work')
    html += f'''<main id="main">
<section class="ch wrap">
<div class="ch-top"><a class="back-link" href="index.html#work">← Selected work</a><span class="kind {badge_cls}">{p['kind_label']}</span></div>
<div class="ch-main"><h1 class="ct">{p['title']}</h1><div class="ci"><p class="cl">{p['lead']}</p>{note_txt}</div></div>
<dl class="cm">{meta}</dl>
</section>
'''
    html += '\n'.join(BODIES[p['slug']]())
    nfg = ' dark' if nbg in ('#171719',) else ''
    html += f'''
<section class="nxb{nfg}" style="--bg:{nbg}" aria-label="Next project"><div class="nxb-top wide"><span class="lab">Project {p['n']} of 04</span><a class="prev-link" href="{prv['slug']}.html">← {prv['short']}</a></div>
<a class="nxb-a wide" href="{nxt['slug']}.html"><div class="nxb-t"><span class="lab">Next project</span><span class="nx-h">{nxt['short']}</span><span class="kind {'real' if nxt['kind']=='real' else 'acad'}">{nxt['kind_label']}</span></div><span class="nxb-m">{nxt_img}<span class="go" aria-hidden="true">↗</span></span></a></section>
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
        cls = ('pj feat' if featured else 'pj') + ' pj--' + p['slug']
        k = 'real' if p['kind'] == 'real' else 'acad'
        extra = '<span class="pj-star">Featured</span>' if featured else ''
        return (f'<a class="{cls} rv" href="{p["slug"]}.html">{tile_media(p["slug"])}'
                f'<span class="pj-c"><span class="pj-n">{p["n"]}</span><span class="pj-t"><h3>{p["short"]}</h3><p>{p["blurb"]}</p></span>'
                f'<span class="pj-k"><span class="kind {k}">{p["kind_label"]}</span><span class="pj-tags">{p["tag"]}</span><span class="pj-cta">View case study <i aria-hidden="true">→</i></span></span></span></a>')
    h = head('Tzadik Azaria — Visual &amp; Creative Designer', 'Portfolio of Tzadik Azaria, a digital designer with in-house and freelance experience in e-commerce, campaigns, branding and print.', 'home')
    h += header('work')
    h += f'''<main id="main">
<section class="hero2" id="hero" aria-labelledby="hero-title">
<div class="hero2-in wide"><p class="eyebrow"><i aria-hidden="true"></i>Visual &amp; Creative Designer</p>
<h1 id="hero-title"><span>Design with clarity.</span><span class="l2">And a <b class="sel">point of view.<i class="hd tl"></i><i class="hd tr"></i><i class="hd bl"></i><i class="hd br"></i><em class="dim" aria-hidden="true">W 0 × H 0</em></b></span></h1>
<svg class="vec" role="group" aria-label="Interactive curve that reshapes the headline type"><path class="vp" d=""/><path class="vh" d=""/><g class="vpts"></g></svg>
<div class="hero-row"><p class="sub">Digital designer with in-house and freelance experience across e&#8209;commerce, campaigns, branding and print.</p>
<div class="actions"><a class="cta" href="#work">Selected projects <span aria-hidden="true">↓</span></a><a class="ghost" href="about.html">About me <span aria-hidden="true">→</span></a></div></div>
<div class="hero-foot"><span>Tzadik Azaria</span><p class="hint">Drag the middle point of the curve, or focus it and use the arrow keys, to reshape the type.</p><span>Open to full-time roles</span></div></div></section>

<section class="work wrap" id="work" aria-labelledby="work-title"><div class="work-head"><p class="kicker" id="work-title">Selected Projects</p><h2 class="lede rv">Commercial campaign and e-commerce work, alongside two academic concepts. Each one is labelled.</h2><p class="work-key rv"><span class="kind real">Commercial work</span><span class="kind acad">Academic concept</span></p></div>
<div class="pj-grid">
{tile(PROJECTS[0], True)}
{tile(PROJECTS[1])}
{tile(PROJECTS[2])}
{tile(PROJECTS[3])}
</div></section>

<section class="about-strip wrap"><h2 class="rv">From product pages<br><em>to brand identities.</em></h2><p class="rv">I’m a digital designer with in-house and freelance experience. I’ve created e-commerce content, campaign and social visuals, and promotional materials for beauty and wellness brands, and branding, signage and print for freelance clients. I care about typography, layout and consistency, and I like seeing a project through from brief to final delivery.</p><a class="text-link rv" href="about.html">More about me <span aria-hidden="true">→</span></a></section></main>
'''
    h += FOOTER
    open(f'{ROOT}/index.html', 'w').write(h)
    # legacy URL: keep old home.html working
    open(f'{ROOT}/home.html', 'w').write('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=index.html"><link rel="canonical" href="index.html"><title>Tzadik Azaria</title></head><body><a href="index.html">Continue to the portfolio</a></body></html>')

# ---------------------------------------------------------------- about
def about():
    h = head('About — Tzadik Azaria', 'Tzadik Azaria is a digital designer with in-house and freelance experience in e-commerce content, digital campaigns, social media, web visuals and print.', 'inner about')
    h += header('about')
    exp = [
        ('OG Brands Ltd.', 'Designed digital and print assets for international beauty and wellness brands across e-commerce, social media, campaigns and retail. Created product visuals, banners, newsletters, marketplace content and promotional materials, working with marketing, sales, operations and external suppliers.'),
        ('Freelance', 'Designed branding, brochures, signage, presentations and digital marketing materials for clients across different industries. Developed visual solutions around each client’s needs and managed projects from the initial brief through feedback, revisions and final delivery.'),
        ('ORT Hermelin College', 'Designed posters, educational publications and marketing materials for college initiatives. Created digital and print assets and assisted students with design principles and creative software.'),
    ]
    xp = ''.join(f'<article class="xp"><span class="xn">0{i+1}</span><h2>{o}</h2><p>{d}</p></article>' for i, (o, d) in enumerate(exp))
    h += f'''<main id="main"><div class="about-page wrap">
<section class="about-hero"><div><p class="eyebrow">About Tzadik</p><h1>Thoughtful design.<br><em>From idea<br>to execution.</em></h1></div><p class="about-intro">I’m Tzadik Azaria, a digital designer with in-house and freelance experience. I create e-commerce content, digital campaigns, social media assets, web visuals and print materials, with an eye for typography, layout and brand consistency.</p></section>
<section class="about-story"><p class="eyebrow">Background</p><div><p>I’ve worked in-house on e-commerce and campaign content for beauty and wellness brands, and as a freelancer on branding, signage, brochures and presentations for clients in different industries. I’m used to taking a project from the brief and concept through to final production.</p><p>I studied media design at ORT Hermelin College, and I’m looking for a full-time role in a design studio, agency or in-house creative team.</p><div class="about-actions"><a class="text-link" href="assets/TzadikAzaria_CV.pdf" download="Tzadik-Azaria-CV.pdf">Download CV <span aria-hidden="true">↓</span></a><a class="text-link ghost-l" href="mailto:tzadikazaria@gmail.com">Get in touch <span aria-hidden="true">→</span></a></div></div></section>
<section class="experience-section"><p class="eyebrow">Experience</p><div class="experience-list">{xp}</div></section>
<section class="about-lists"><div><h2>Skills</h2><ul><li>Brand identity</li><li>Campaigns &amp; social visuals</li><li>E-commerce, product visuals &amp; marketplaces</li><li>Shopify &amp; email</li><li>Web design, landing pages &amp; responsive</li><li>Print, packaging &amp; production</li><li>Presentations &amp; video editing</li></ul></div><div><h2>Tools</h2><ul><li>Figma · Wix Studio</li><li>Adobe Photoshop · Illustrator</li><li>Adobe InDesign · Premiere Pro</li><li>Shopify · Blender</li></ul></div><div><h2>Education</h2><p>ORT Hermelin College<br>Practical Engineer Diploma<br>in Media Design</p><p class="education-note">Graduated with Distinction</p></div></section></div></main>
'''
    h += FOOTER
    open(f'{ROOT}/about.html', 'w').write(h)

home(); about()
for i in range(4):
    case_page(i)
print('built')
