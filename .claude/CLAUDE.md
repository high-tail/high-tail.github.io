# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll-based static site generator for a personal blog hosted on GitHub Pages. 
The site uses the Chirpy theme and is configured for local development with Docker Compose.

## Key Technologies

- Jekyll static site generator (Ruby-based)
- Chirpy theme (jekyll-theme-chirpy)
- GitHub Pages deployment
- Docker Compose for local development

## Development Setup

### Docker-based Development (Recommended)

The preferred method for local development is using Docker Compose:

1. Build and run the site:
   ```
   docker compose up
   ```

2. The site will be available at http://localhost:4000

### Docker Commands

- `docker compose up` – build and start the Jekyll server with auto-reload
- `docker compose down` – stop and remove containers
- `docker compose run --rm app bundle exec jekyll build` – build the site
- `docker compose exec app bundle exec jekyll serve` – run server in container

## Site Structure

- `_posts/` - Blog posts in Jekyll format
- `_tabs/` - Tab pages (about, archives, categories, tags)
- `_config.yml` - Main configuration
- `Gemfile` - Ruby gem dependencies
- `Dockerfile` - Container configuration
- `compose.yml` - Docker Compose configuration

## Deployment

The site is deployed to GitHub Pages. Configuration in `_config.yml` specifies the base URL and other deployment settings.

## Architecture

- Built with Chirpy theme providing responsive design and dark/light mode
- Uses Jekyll for static site generation
- Docker containerizes the Jekyll environment
- Posts use Markdown format with YAML front matter

## Rules & Guidelines

Strictly adhere to the rules defined in `.claude/rules/`:
- **Files**: See `.claude/rules/files.md` for naming conventions (`YYYY-MM-DD-...`) and directory structures (`_posts/`, `assets/img/`).

## Available Commands

- `/create-post "topic" [--audience "target"] [--structure "type"]`
  Create a new blog post draft with the correct filename and Front Matter.
- `/generate-content "prompt" [--section "intro|body|conclusion"]`
  Generate specific sections for a post.
- `/review-content "content_or_file" [--focus "structure|style|seo"]`
  Analyze existing posts for improvements.

## Available Agents

- **`@blog-post-generator`**
  *Expert at writing full posts.*
  Usage: "Write a blog post about X"
  Tools: Read, Write, Grep
- **`@content-improver`**
  *Expert at auditing and refining content.*
  Usage: "Improve this draft"
  Tools: Read, Grep
- **`@content-organizer`**
  *Expert at structuring messy notes.*
  Usage: "Organize these notes into a post"
  Tools: Read, Grep

## Project Constraints

- **Filenames**: Blog posts MUST be in `_posts/` and follow `YYYY-MM-DD-kebab-case-title.md`.
- **Front Matter**: MUST include `title`, `date`, `categories`, and `tags`.
- **Images**: Store in `assets/img/`.
- **Theme Features**:
  - Use `{: .prompt-tip }`, `{: .prompt-info }`, `{: .prompt-warning }`, `{: .prompt-danger }` for callouts.
  - Use `mermaid: true` in front matter for diagrams.

