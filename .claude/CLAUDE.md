# CLAUDE.md

## Project Overview

Jekyll-based personal blog hosted on GitHub Pages using the Chirpy theme. Local development uses Docker Compose.

## Development

```bash
docker compose up          # Start dev server at http://localhost:4000 (auto-reload)
docker compose down        # Stop containers
docker compose build       # Rebuild after Gemfile changes
```

## Deployment

Pushes to `main` trigger automatic deployment via `.github/workflows/jekyll-gh-pages.yml`:
- Builds with `bundle exec jekyll b` in production mode (Ruby 3.3)
- Deploys to GitHub Pages at https://high-tail.github.io

## Site Structure

```
_posts/           Blog posts (YYYY-MM-DD-kebab-case-title.md)
_tabs/            Tab pages (about, archives, categories, tags)
_config.yml       Main site configuration
_data/            Site data files
_plugins/         Custom Jekyll plugins
assets/img/       Images referenced in posts
compose.yml       Docker Compose configuration
Dockerfile        Container configuration (Ruby 3.3)
.claude/skills/   Blog writing skill and tools
.claude/agents/   Agent definitions (blog-post-generator, content-improver, content-organizer)
.claude/commands/ Slash commands (create-post, generate-content, review-content)
.claude/rules/    Project rules (file naming, directory structure)
```

## Rules & Guidelines

Strictly adhere to the rules defined in `.claude/rules/`:
- **Files**: See `.claude/rules/files.md` for naming conventions (`YYYY-MM-DD-...`) and directory structures (`_posts/`, `assets/img/`).

## Blog Post Requirements

- **Filenames**: `_posts/YYYY-MM-DD-kebab-case-title.md`
- **Front Matter**: Must include `title`, `date`, `description`, `comments`, `categories`, and `tags`.
- **Images**: Store in `assets/img/`.
- **Headings**: Use `##` (H2) for body sections — Chirpy renders `title` as H1.
- **Theme Features**:
  - Callouts: `{: .prompt-tip }`, `{: .prompt-info }`, `{: .prompt-warning }`, `{: .prompt-danger }`
  - Diagrams: `mermaid: true` in front matter for Mermaid diagrams
  - Footnotes: `[^fn-nth-1]` for source repos and references

### Validation

```bash
python3 .claude/skills/blog-writing-guide/tools/validate_blog_post.py _posts/YOUR_POST.md
```

## Available Commands

- `/create-post "topic" [--audience "target"] [--structure "type"] [--series "name"]`
  Create a new blog post draft with correct filename and front matter.
- `/generate-content "prompt" [--section "objective|prerequisites|overview|implementation|verification|conclusion"]`
  Generate specific sections for a post.
- `/review-content "path" [--focus "structure|style|seo"]`
  Analyze existing posts for improvements.

## Content Conventions

- Posts are primarily technical (DevOps, databases, infrastructure) and typically form multi-part series.
- Use Mermaid `architecture-beta` syntax for system diagrams (not basic flowcharts).
- Standard section flow: Objective → Prerequisites → Overview → Implementation → Verification → Conclusion → Footnotes.

## Gotchas

- **Timezone**: Front matter `date` must use `+0900` (JST).
- **Permalinks**: `_config.yml` sets `/posts/:title/`, so series links use `https://high-tail.github.io/posts/slug-name` — not date-based URLs.
- **`Gemfile.lock` is gitignored**: GitHub Pages uses its own gems. Don't commit lock changes.
- **No test suite**: No `bundle exec rake` or similar. Post validation is via the Python script only.
- **Docker service name**: The compose service is `app` (e.g., `docker compose exec app ...`).

## Available Agents

- **`@blog-post-generator`** — Write full posts from scratch.
  Tools: Read, Write, Grep, Glob
- **`@content-improver`** — Audit and fix existing content.
  Tools: Read, Write, Grep, Glob
- **`@content-organizer`** — Turn messy notes into structured posts.
  Tools: Read, Write, Grep, Glob
