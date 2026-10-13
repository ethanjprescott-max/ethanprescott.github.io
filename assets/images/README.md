# Portfolio images

Photos are intentionally blank in the first version.

Save a portrait as `assets/images/portrait.jpg`, then set `profile.portrait` in `content/portfolio.json` to that exact path.

For each project, create a subfolder inside `assets/images/projects/` using its project ID. For example, put FREEDOM photos in `assets/images/projects/freedom/`.

Set the project's `cover` and `images[].src` fields to paths from the repository root, for example:

```json
"cover": "assets/images/projects/freedom/cover.jpg"
```

The gallery supports click-to-enlarge images. Give each image a meaningful `caption` for its label and alternative text.

Run `python3 scripts/build.py` after changing content. Empty paths display the photo placeholders, with no missing-image icons.
