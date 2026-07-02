# Codex Instructions

This repository contains a Skill Poster Workflow for generating social-media-ready knowledge posters.

## Goal

Help the user turn a topic, keyword, or structured JSON/CSV content into a clean 1080×1440 knowledge-card poster.

## Main files

- `poster_generator.py`: Python poster renderer using Pillow.
- `content_template.json`: Single-poster example content.
- `topics.csv`: Batch generation template.
- `prompt_template.md`: Prompt for generating poster-ready JSON copy.
- `requirements.txt`: Python dependencies.

## How to run

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate one poster:

```bash
python poster_generator.py --json content_template.json
```

Generate posters in batch:

```bash
python poster_generator.py --csv topics.csv
```

Output files are saved in `output/`.

## Style rules

Keep the poster style simple, clean, educational, and suitable for Xiaohongshu, WeChat public account images, LinkedIn, and personal-brand content.

Use short Chinese copy, strong headings, three key points, and a final memorable sentence.

## When editing

Preserve compatibility with Python 3.10+ and Pillow. Avoid adding unnecessary heavy dependencies.
