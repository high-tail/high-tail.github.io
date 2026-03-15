---
name: blog-writing-guide
description: Create, structure, and improve blog posts following Jekyll Chirpy theme standards. Use this skill whenever the user mentions writing a blog post, creating content, drafting an article, reviewing a post, improving SEO, organizing notes into a post, or anything related to blog content on this Jekyll site. Even if they just say "write about X" or "I have some notes about Y", this skill applies.
---

# Blog Writing Guide

This skill guides blog post creation for a Jekyll Chirpy theme site. Posts are primarily technical (DevOps, databases, infrastructure) and often form multi-part series.

## Critical Constraints

1. **File Naming**: `_posts/YYYY-MM-DD-kebab-case-title.md` — use today's date.
2. **Front Matter** — all of these fields are required:
   ```yaml
   ---
   title: "Descriptive Title with Primary Keyword"
   date: YYYY-MM-DD HH:MM:SS +0900
   description: "SEO summary under 160 characters"
   comments: true
   mermaid: true  # include only when using diagrams
   categories: [Main, Sub]
   tags: [tag1, tag2, tag3]
   ---
   ```
   - `title`: primary keyword near the start, under 60 chars
   - `description`: meta description for SEO, under 160 chars
   - `categories`: broad groupings (e.g., `[Tech, DevOps]`)
   - `tags`: specific topics in lowercase (e.g., `[docker, prometheus, grafana]`)
3. **Headings**: Use `##` (H2) for top-level body sections. Chirpy renders `title` from front matter as H1 — never use `#` in the post body.
4. **Theme Callouts** — use these block-quote markers where they add value:
   - `{: .prompt-tip }` — environment info, version tables, helpful hints
   - `{: .prompt-info }` — architecture diagrams, key concepts, context
   - `{: .prompt-warning }` — cautions, caveats, gotchas
   - `{: .prompt-danger }` — breaking changes, destructive operations
5. **Images**: `![Alt text](/assets/img/path/to/image.png)` — store files in `assets/img/`.

## Post Structure (Follow This Flow)

Real posts on this blog follow a consistent section flow. Use this as the default structure:

### 1. Objective
State what the post achieves. If part of a series, link all parts here:
```markdown
## Objective
This is part 2 of the series:
1. [Part 1 Title](https://high-tail.github.io/posts/part-1-slug)
2. [Part 2 Title](https://high-tail.github.io/posts/part-2-slug) ← this post
3. [Part 3 Title](https://high-tail.github.io/posts/part-3-slug)
```

### 2. Prerequisites
List required tools/knowledge. Always include an environment version table in a callout:
```markdown
## Prerequisites
- Basic knowledge of Docker and docker-compose

> My Environment
>
> | Software       | Version |
> | :------------- | :------ |
> | colima         | 0.8.1   |
> | docker CLI     | 27.5.1  |
> | docker-compose | 2.33.0  |
>
{: .prompt-tip }
```

### 3. Overview
Explain key concepts. Use architecture diagrams for system overviews:
```markdown
> System Architecture
> ```mermaid
> architecture-beta
>     group cluster[System Name]
>     service svc1(server)[Service 1] in cluster
>     service svc2(database)[Service 2] in cluster
>     svc1:R -- L:svc2
> ```
{: .prompt-info }
```

### 4. Implementation
Show the work. Include a file structure tree with annotations, then walk through each file:
```
.
├── compose.yml        # Update
└── docker/
    ├── new-service/   # New
    │   └── Dockerfile
    └── existing/
        └── config.cfg # Update
```
Use fenced code blocks with language identifiers. Add inline comments explaining key lines.

### 5. Verification
Show how to confirm everything works — commands to run, URLs to visit, expected output:
```markdown
## How to Start
docker-compose up -d

| Service    | WebUI                          |
| ---------- | ------------------------------ |
| Grafana    | http://localhost:3000           |
| Prometheus | http://localhost:9090/query     |
```

### 6. Conclusion
Summarize with a checklist of completed items. Link to further resources:
```markdown
## Completed Plan
- [x] Set up MariaDB Galera Cluster
- [x] Added Prometheus monitoring
- [x] Configured Grafana dashboards
```

### 7. Footnotes & Links
Use Jekyll footnote syntax for source code repos and references:
```markdown
### File Structure[^fn-nth-1]
...
[^fn-nth-1]: [Link Text](https://github.com/...) - Description of the resource.
```

## Writing Style

- Professional yet conversational. Speak directly to the reader ("we'll", "you can").
- Max 3–5 sentences per paragraph.
- Use active voice.
- Define technical terms on first use with a link to official docs.
- Include keywords naturally in H2 headers and the first paragraph.

## Validation

Run the validation script after creating or editing a post:
```bash
python3 .claude/skills/blog-writing-guide/tools/validate_blog_post.py _posts/YOUR_POST.md
```

## Available Resources

Read these only when deeper guidance is needed for a specific area:
- `references/structure-guidelines.md` — Detailed breakdown of each section with examples
- `references/seo-best-practices.md` — Front matter SEO optimization checklist
- `examples/blog-outline-template.md` — Copy-paste starting template for new posts
- `examples/seo-optimized-post.md` — Complete example post with all patterns applied
