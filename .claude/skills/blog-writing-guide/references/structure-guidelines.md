# Blog Post Structure Guidelines

## Front Matter Schema

Every post requires this front matter block:
```yaml
---
title: "Primary Keyword Near Start, Under 60 Chars"
date: YYYY-MM-DD HH:MM:SS +0900
description: "Compelling SEO summary under 160 characters"
comments: true
mermaid: true  # only when using diagrams
categories: [Main, Sub]
tags: [tag1, tag2, tag3]
---
```

**Field details:**
- `title`: Include the primary keyword near the start. Keep under 60 chars for optimal SEO display.
- `date`: Use JST timezone (`+0900`).
- `description`: This becomes the meta description. Make it compelling — it shows in search results.
- `categories`: Broad groupings like `[Tech, DevOps]` or `[Tech, Monitoring]`. Check existing posts for consistency.
- `tags`: Specific, lowercase topics like `[docker, prometheus, grafana]`. Reuse existing tags when possible.

## Section-by-Section Guide

### Objective
- 2–3 sentences: what will be built/explained and why it matters
- For series posts, include a numbered list of all parts with links
- Mark the current post with `← this post`

### Prerequisites
- Bullet list of required tools and knowledge
- Always include an environment version table inside a `{: .prompt-tip }` callout
- Use a table format: `| Software | Version |`

### Overview
- Explain 2–3 key concepts the reader needs to understand
- Use H3 (`###`) for each concept
- Include a Mermaid `architecture-beta` diagram inside `{: .prompt-info }` for system-level overviews
- Link to official documentation for each technology mentioned

### Implementation
- Start with a file structure tree showing all files, annotated with `# New` or `# Update`
- Walk through each file using H4 (`####`) with the filename in bold backticks: `#### **\`filename.ext\`**`
- Use fenced code blocks with language identifiers (`yaml`, `bash`, `conf`, `Dockerfile`, etc.)
- Add inline comments in code blocks explaining key lines

### Verification / How to Start
- Show exact commands to run (typically `docker-compose build` + `docker-compose up -d`)
- Show expected output
- Provide a table of service URLs: `| Service | WebUI |`

### Conclusion / Completed Plan
- Use a checklist format with `- [x]` for completed items
- Link each item to its official documentation
- Mention what comes next (next post in series, future improvements)

### Footnotes
- Place footnote definitions at the bottom of the post
- Use for linking to source code repositories and external references
- Format: `[^fn-nth-N]: [Display Text](URL) - Brief description`

## Content Patterns

### Code Blocks
Always specify the language:
- `yaml` for config files
- `bash` for shell commands
- `conf` for configuration files (HAProxy, ProxySQL)
- `Dockerfile` for Dockerfiles
- `sql` for database queries

### Callout Usage
| Callout | Use For |
| ------- | ------- |
| `{: .prompt-tip }` | Environment tables, helpful hints, version info |
| `{: .prompt-info }` | Architecture diagrams, key concepts, context |
| `{: .prompt-warning }` | Caveats, things that might confuse readers |
| `{: .prompt-danger }` | Breaking changes, data loss risks, destructive commands |
