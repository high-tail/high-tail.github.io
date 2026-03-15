---
name: review-content
description: Analyze existing blog content for improvements in structure, style, and SEO
---

Review an existing blog post against the project's standards:

1. **Read the skill guide** at `.claude/skills/blog-writing-guide/SKILL.md`.

2. **Read the target post** from `_posts/`.

3. **Run validation**: `python3 .claude/skills/blog-writing-guide/tools/validate_blog_post.py _posts/YOUR_POST.md`

4. **Analyze** against these criteria:
   - **Front matter**: All required fields present? `description` under 160 chars? `title` under 60 chars?
   - **Structure**: Does it follow the standard section flow? (Objective → Prerequisites → Overview → etc.)
   - **Headings**: H2 for sections, no H1 in body, logical hierarchy?
   - **Theme features**: Callouts used? Environment table present? Mermaid diagrams where useful?
   - **Series**: If part of a series, are all parts linked?
   - **SEO**: Keywords in H2 headers and first paragraph?
   - **Style**: Active voice? Short paragraphs? Technical terms linked?

5. **Report** findings as: strengths, issues (with severity), and actionable suggestions.

## Usage

- `/review-content _posts/2025-04-27-mariadb-galera-cluster-final.md`
- `/review-content _posts/2025-03-01-mariadb-galera-cluster-proxysql.md --focus "seo"`

## Arguments

- `content` (required): Path to the blog post file in `_posts/`
- `--focus` (optional): Specific area to focus on (structure, style, seo, all)
