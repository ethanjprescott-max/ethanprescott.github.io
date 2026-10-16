# Ethan Prescott — Engineering Portfolio

A static, responsive engineering portfolio with a fixed profile sidebar, project cards, and seven individual project pages. The layout is inspired by the supplied portfolio reference; its HTML, CSS, icons, and scripts are independently implemented.

## Included projects

1. FREEDOM — 3 lb NHRL combat robot
2. Class Beetlebot — Mechanical Engineering Analysis & Design
3. CTI Roller
4. LimbLet — Ireland summer project
5. Iris+ Drone — in progress
6. Eagle Scout Project — BioReserve conservation signs
7. App made with AI — Quest, a private birthday game

The CTI Roller and LimbLet summaries use information from Ethan's supplied résumé. The Eagle Scout page describes the BioReserve sign project, including planning, approval, material selection, fabrication, welding instruction, and team coordination, based on Ethan's project notes. The Quest page describes the private birthday game and Ethan’s independent creation and playtesting using Base44’s AI development tools. Details not supplied remain blank. The Iris+ project includes two supplied setup photos. Quest includes two app screenshots and a screen recording. FREEDOM includes six supplied photos/screenshots and an arena recording, and the Eagle Scout project includes three supplied photos. LimbLet includes an exercise-interface screenshot, a wearable concept render, a team photo, and an app walkthrough. The Class Beetlebot project includes two supplied photos and competition footage. All four videos use native playback controls. Other missing photos and the portrait remain placeholders. The original résumé PDF is available through the homepage download button and the navigation on every page. The drone page identifies the work as ongoing and does not claim a completed flight.

## Make edits

The editable source for all text, project details, image paths, and profile links is **`content/portfolio.json`**. Empty strings remain blank on the generated website.

After an edit, run:

```bash
python3 scripts/build.py
```

This regenerates `index.html` and `projects/*.html`. Commit the JSON changes and the generated pages together. CSS is in `assets/css/style.css`; browser interactions are in `assets/js/site.js`. No Node installation, framework, or package manager is required.

You can also edit the generated HTML directly for a quick change, but a later build will replace those edits. Keep lasting content changes in the JSON file.

## Add images and a résumé

See `assets/images/README.md` for image instructions. Add a PDF such as `assets/ethan-prescott-resume.pdf` and set `profile.resume` to the file's path. The builder checks that nonempty asset paths point to real files.

## Video media

The Quest video is a web-optimized MP4 at `assets/videos/quest-walkthrough.mp4`. The NHRL recording is at `assets/videos/nhrl-arena.mp4`. The LimbLet app recording is at `assets/videos/limblet-walkthrough.mp4`. The Class Beetlebot recording is at `assets/videos/beetlebot-competition.mp4`. Each has a poster image and a download link. Video sources, posters, titles, and captions are configured through the project’s optional `video` object in `content/portfolio.json`. The original uploaded MOV files are not included in the website repository. Videos appear at the top of a project by default; set `video.placement` to `gallery` to put a recording after the photo gallery, and use `video.width` / `video.height` to preserve its orientation.

## Preview locally

Open `index.html` in a browser, or use a simple local server:

```bash
python3 -m http.server 8000
```

Visit `http://localhost:8000`. Check the mobile navigation, all project links, and any newly added images.

## GitHub Pages publishing

This version is ready for branch-based GitHub Pages hosting. Public publication should be enabled only when Ethan chooses to make the website public.

When ready, open the repository's **Settings → Pages**, select **Deploy from a branch**, then **main** and **/(root)**, and save. No automated deployment workflow is installed in this draft.

The connected account is `ethanjprescott-max`, and this repository is named `ethanprescott.github.io`. Because the repository name differs from the account's `ethanjprescott-max.github.io` user-site name, its GitHub Pages address will normally be a project URL:

`https://ethanjprescott-max.github.io/ethanprescott.github.io/`

The exact live address should be taken from GitHub's Pages settings after publication. All internal links use relative paths so project-URL hosting works.

## Updating together

Future edits can be requested in the same conversation by naming the project and the change, or sharing new text and images. The repository keeps version history so changes can be reviewed and revised.

## Dependencies

The site uses standard HTML, CSS, and JavaScript. Optional Google Fonts load DM Sans and Manrope; Arial provides a fallback if they are unavailable. The build script uses only Python's standard library.
