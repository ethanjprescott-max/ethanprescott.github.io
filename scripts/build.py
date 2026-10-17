#!/usr/bin/env python3
"""Generate the static portfolio from content/portfolio.json. Standard library only."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'content' / 'portfolio.json').read_text())
PROFILE = DATA['profile']
PROJECTS = DATA['projects']

def e(value):
    return escape(str(value), quote=True)

def icon(name, size=18):
    paths = {
        'image': '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/>',
        'arrow': '<path d="M5 12h14m-5-5 5 5-5 5"/>',
        'back': '<path d="M19 12H5m5-5-5 5 5 5"/>',
        'external': '<path d="M14 3h7v7m0-7L10 14"/><path d="M10 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-5"/>',
        'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
        'menu': '<path d="M5 7h14M5 12h14M5 17h14"/>',
        'file': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6M8 13h8M8 17h6"/>',
    }
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'

def asset_path(path, base):
    if not path:
        return ''
    asset = ROOT / path
    if not asset.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError('Assets must be inside the project directory')
    if not asset.is_file():
        raise ValueError(f'Missing asset: {path}')
    return base + path

def photo(src='', label='Project photo', number='', base='', gallery=False):
    if src:
        target = asset_path(src, base)
        img = f'<img class="project-photo" src="{e(target)}" alt="{e(label)}" loading="lazy" decoding="async">'
        if gallery:
            return f'<a href="{e(target)}" data-gallery data-caption="{e(label)}" aria-label="Enlarge {e(label)}">{img}</a>'
        return img
    code = f'<span class="photo-no">{e(number)}</span>' if number else ''
    return f'<div class="photo-placeholder" role="img" aria-label="{e(label)} placeholder">{code}{icon("image",30)}<span>Photo to be added</span></div>'

def sidebar(base='', project=False):
    avatar = (f'<img src="{e(asset_path(PROFILE["portrait"],base))}" alt="{e(PROFILE["name"])}">' if PROFILE['portrait'] else '<strong>EP</strong><span>Portrait</span>')
    home = base + 'index.html'
    nav = ''.join(f'<a href="{home}#{key}"{ " aria-current=\"page\"" if project and key == "projects" else ""}>{label}</a>' for key,label in [('about','About'),('projects','Projects'),('experience','Experience'),('skills','Skills'),('contact','Contact')])
    if PROFILE['resume']:
        nav += f'<a href="{base}resume.html">Résumé</a>'
    return f'''<aside class="sidebar" aria-label="Profile and navigation">
      <div class="identity"><a class="avatar" href="{e(home)}" aria-label="Ethan Prescott home">{avatar}</a><div><a class="sidebar-name" href="{e(home)}">{e(PROFILE['name'])}</a><p class="sidebar-degree">{e(PROFILE['degree'])}<br>{e(PROFILE['school'])}</p><p class="sidebar-school">{e(PROFILE['graduation'])}</p></div></div>
      <button class="menu-toggle" type="button" aria-label="Open navigation" aria-controls="main-navigation" aria-expanded="false">{icon('menu')}</button>
      <div class="sidebar-rule"></div><nav class="sidebar-nav" id="main-navigation" aria-label="Main navigation">{nav}</nav>
      <div class="sidebar-bottom"><div class="sidebar-links"><a href="{e(PROFILE['github'])}" target="_blank" rel="noopener noreferrer">GitHub</a><a href="{e(PROFILE['linkedin'])}" target="_blank" rel="noopener noreferrer">LinkedIn</a><a href="mailto:{e(PROFILE['email'])}">Email</a></div><p class="sidebar-footer">Mechanical engineering · Robotics · Design</p></div>
    </aside>'''

def page(title, description, body, base='', project=False):
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="{e(description)}">
  <meta name="theme-color" content="#153049">
  <title>{e(title)} | Ethan Prescott</title>
  <link rel="icon" type="image/svg+xml" href="{base}assets/favicon.svg">
  <link rel="stylesheet" href="{base}assets/css/style.css">
  <script src="{base}assets/js/site.js" defer></script>
</head>
<body id="top">
  <a class="skip-link" href="#main">Skip to content</a>
  {sidebar(base,project)}
  <main class="main" id="main">{body}<footer class="site-footer"><span>© 2026 Ethan Prescott</span><a href="#top">Back to top ↑</a></footer></main>
  <dialog class="lightbox" aria-label="Project image"><button class="close-dialog" type="button" aria-label="Close image">×</button><img alt=""><p></p></dialog>
</body>
</html>
'''

def status(project):
    value = project['status']
    class_name = 'progress' if value == 'In progress' else ('draft' if not value else '')
    return f'<span class="status {class_name}">{e(value or "Details to come")}</span>'

def card(project, number):
    link = 'projects/' + project['id'] + '.html'
    summary = f'<p class="project-summary">{e(project["summary"])}</p>' if project['summary'] else '<div class="empty-summary"><span></span><span></span><span></span><p class="sr-only">Project description to be added.</p></div>'
    tags = ''.join(f'<span class="tag">{e(tag)}</span>' for tag in project['tags'])
    cover_class = 'cover-link contain' if project.get('cover_layout') == 'portrait' else 'cover-link'
    return f'''<article class="project-card">
      <a class="{cover_class}" href="{link}" aria-label="View {e(project['title'])}">{photo(project['cover'],project['title'],f'{number:02d}')}</a>
      <p class="project-category">{e(project['category'])}</p><h3 class="project-title"><a href="{link}">{e(project['title'])}</a></h3><p class="project-subtitle">{e(project['subtitle'])}</p>{summary}
      {f'<div class="tags">{tags}</div>' if tags else ''}
      <div class="card-status">{status(project)}<a class="text-link" href="{link}" aria-label="View {e(project['title'])} project">View project {icon('arrow',13)}</a></div>
    </article>'''

def build_home():
    cards = ''.join(card(project,i+1) for i,project in enumerate(PROJECTS))
    skills = ''.join(f'<div class="skill-group"><h3>{e(group["title"])}</h3><p>{" · ".join(e(item) for item in group["items"])}</p></div>' for group in PROFILE['skills'])
    experience = ''.join(f'<article class="experience-item"><p class="experience-label">{e(item["when"])}</p><div><h3>{e(item["title"])}</h3><p class="organization">{e(item["organization"])}</p><p>{e(item["description"])}</p></div></article>' for item in PROFILE['experience'])
    resume = (f'<a class="button" href="{e(asset_path(PROFILE["resume"],""))}" download>{icon("file",14)} Download résumé</a>' if PROFILE['resume'] else f'<span class="button" aria-disabled="true">{icon("file",14)} Résumé · coming soon</span>')
    body = f'''
    <section id="about" aria-labelledby="intro-title"><div class="about-layout"><img class="about-art about-freedom" src="assets/images/freedom-removebg.png?v=full" alt="FREEDOM combat robot"><div class="about-text"><h1 class="intro-title" id="intro-title">About Me</h1><p class="intro-copy">{e(PROFILE['intro'])}</p><div class="intro-actions"><a class="button resume-button" href="resume.html">-Resume-</a></div></div><img class="about-art about-villanova" src="assets/images/Villanova-Wildcats-Emblem.png" alt="Villanova Wildcats emblem"></div></section>
    <section class="section" id="projects" aria-labelledby="projects-title"><div class="section-head"><h2 id="projects-title">Projects</h2><p>01 — 07</p></div><div class="project-grid">{cards}</div></section>
    <section class="section" id="skills" aria-labelledby="skills-title"><div class="section-head"><h2 id="skills-title">Tools & skills</h2></div><div class="skills-grid">{skills}</div></section>
    <section class="section" id="experience" aria-labelledby="experience-title"><div class="section-head"><h2 id="experience-title">Experience & education</h2></div><div class="experience-list">{experience}</div></section>
    <section class="section" id="contact" aria-labelledby="contact-title"><div class="section-head"><h2 id="contact-title">Let’s connect</h2></div><p class="contact-copy">{e(PROFILE['interests'])}</p><div class="contact-links"><a href="mailto:{e(PROFILE['email'])}">{icon('mail',16)} Email</a><a href="{e(PROFILE['linkedin'])}" target="_blank" rel="noopener noreferrer">{icon('external',14)} LinkedIn</a><a href="{e(PROFILE['github'])}" target="_blank" rel="noopener noreferrer">{icon('external',14)} GitHub</a></div></section>
    '''
    (ROOT / 'index.html').write_text(page('Engineering Portfolio','Ethan Prescott — Villanova mechanical engineering student. Projects in combat robotics, mechanical design, drone systems, entrepreneurship, and community service.',body))

def detail_content(title, key, project, number):
    copy = f'<p class="detail-copy">{e(project[key])}</p>' if project[key] else '<div class="empty-content" aria-label="Content to be added"></div>'
    comparison = ''
    if key == 'design' and project.get('design_images'):
        figures = ''.join(f'<figure>{photo(image["src"],image["caption"],base="../",gallery=True)}<figcaption>{e(image["caption"])}</figcaption></figure>' for image in project['design_images'])
        comparison = f'<div class="design-comparison"><h3>From CAD to prototype</h3><div class="gallery-grid gallery-pair">{figures}</div></div>'
    return f'<section class="detail-section" aria-labelledby="{key}-title"><div class="detail-heading"><span>{number:02d}</span><h2 id="{key}-title">{title}</h2></div>{copy}{comparison}</section>'

def video_player(video, base):
    src = e(asset_path(video['src'],base))
    poster = e(asset_path(video['poster'],base)) if video.get('poster') else ''
    width = int(video.get('width',540))
    height = int(video.get('height',1174))
    return f'''<figure class="project-video"><div class="video-shell"><video controls playsinline preload="metadata" width="{width}" height="{height}" poster="{poster}" aria-label="{e(video['title'])}" aria-describedby="video-caption"><source src="{src}" type="video/mp4">Your browser does not support embedded video. <a href="{src}">Download the recording</a>.</video></div><figcaption id="video-caption"><span>{e(video['caption'])}</span><a href="{src}" download>Download video</a></figcaption></figure>'''

def hero_media(project, index, base):
    video = project.get('video')
    if video and video.get('placement','hero') == 'hero':
        return video_player(video,base)
    class_name = 'hero-photo portrait-media' if project.get('cover_layout') == 'portrait' else 'hero-photo'
    return f'<div class="{class_name}">{photo(project["cover"],project["title"],f"{index+1:02d}",base)}</div>'

def build_project(project, index):
    base = '../'
    tags = ' · '.join(e(tag) for tag in project['tags'])
    blank = '<span class="meta-blank" aria-label="To be added"></span>'
    metadata = ''.join(f'<div><dt>{label}</dt><dd>{value or blank}</dd></div>' for label,value in [('When',e(project['date'])),('My role',e(project['role'])),('Tools & skills',tags)])
    detail = ''.join(detail_content(title,key,project,i+1) for i,(title,key) in enumerate([('Overview','overview'),('My contribution','contribution'),('Design & build','design'),('Results & lessons','results')]))
    gallery = ''.join(f'<figure>{photo(image["src"],image["caption"],f"{i+1:02d}",base,True)}<figcaption>{e(image["caption"])}</figcaption></figure>' for i,image in enumerate(project['images']))
    gallery_class = 'gallery-grid gallery-pair' if len(project['images']) == 2 else 'gallery-grid'
    extra_video = ''
    if project.get('video',{}).get('placement') == 'gallery':
        extra_video = f'<section class="video-section" aria-labelledby="event-video-title"><h2 id="event-video-title">{e(project["video"].get("heading","Project video"))}</h2>{video_player(project["video"],base)}</section>'
    resources = ''.join(f'<a class="button" href="{e(link["url"])}" target="_blank" rel="noopener noreferrer">{e(link["label"])} {icon("external",13)}</a>' for link in project['links'])
    previous = PROJECTS[(index-1) % len(PROJECTS)]
    following = PROJECTS[(index+1) % len(PROJECTS)]
    body = f'''
    <a class="breadcrumb" href="../index.html#projects">{icon('back',14)} All projects</a>
    <header class="project-header"><div class="project-header-top"><p class="eyebrow">{e(project['category'])}</p>{status(project)}</div><h1>{e(project['title'])}</h1><p class="subtitle">{e(project['subtitle'])}</p><dl class="project-meta">{metadata}</dl></header>
    {hero_media(project,index,base)}
    {detail}
    <section class="gallery-section" aria-labelledby="gallery-title"><h2 id="gallery-title">Project gallery</h2><div class="{gallery_class}">{gallery}</div></section>
    {extra_video}
    {f'<div class="project-resources">{resources}</div>' if resources else ''}
    <nav class="project-navigation" aria-label="More projects"><a href="{previous['id']}.html"><span>← Previous project</span><strong>{e(previous['title'])}</strong></a><a href="{following['id']}.html"><span>Next project →</span><strong>{e(following['title'])}</strong></a></nav>
    '''
    (ROOT / 'projects' / (project['id'] + '.html')).write_text(page(project['title'],project['summary'] or f'{project["title"]} — a project by Ethan Prescott.',body,base,True))


def build_profile_pages():
    back = '<a class="breadcrumb" href="index.html">← Back to portfolio</a>'
    resume = e(asset_path(PROFILE['resume'], ''))
    body = back + f'''<section aria-labelledby="resume-title"><h1 id="resume-title">Résumé</h1><p class="page-intro">Mechanical engineering, robotics, and hands-on project experience.</p><div class="intro-actions"><a class="button" href="{resume}" download>Download PDF</a><a class="button" href="{resume}" target="_blank" rel="noopener">Open PDF</a></div><object class="resume-embed" data="{resume}" type="application/pdf" aria-label="Ethan Prescott résumé"><p><a href="{resume}">Open the résumé PDF</a> to view it on your device.</p></object></section>'''
    (ROOT / 'resume.html').write_text(page('Résumé', 'Ethan Prescott — résumé.', body))

def main():
    ids = [project['id'] for project in PROJECTS]
    if len(set(ids)) != len(ids):
        raise ValueError('Project IDs must be unique')
    for project_id in ids:
        if not project_id or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in project_id):
            raise ValueError(f'Invalid project ID: {project_id}')
    (ROOT / 'projects').mkdir(exist_ok=True)
    build_home()
    build_profile_pages()
    for index,project in enumerate(PROJECTS):
        build_project(project,index)
    print(f'Built homepage and {len(PROJECTS)} project pages.')

if __name__ == '__main__':
    main()
