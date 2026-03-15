---
name: create-post
description: Create a new blog post draft with specified topic and structure
---

Create a new blog post by following these steps:

1. **Read the skill guide** at `.claude/skills/blog-writing-guide/SKILL.md` for structure and standards.

2. **Check existing posts** in `_posts/` to understand series context and avoid duplicates.

3. **Generate the filename**: `_posts/YYYY-MM-DD-kebab-case-title.md` using today's date.

4. **Create front matter** with all required fields:
   ```yaml
   ---
   title: "Post Title"
   date: YYYY-MM-DD HH:MM:SS +0900
   description: "SEO summary under 160 characters"
   comments: true
   mermaid: true  # only if using diagrams
   categories: [Main, Sub]
   tags: [tag1, tag2]
   ---
   ```

5. **Write the post** following the standard section flow:
   Objective → Prerequisites → Overview → Implementation → Verification → Conclusion → Footnotes

6. **Apply theme features**:
   - Chirpy callouts: `> content {: .prompt-tip }`, `{: .prompt-info }`, etc.
   - Environment version tables in `{: .prompt-tip }`
   - Mermaid diagrams for system architecture
   - Footnotes for source repos: `[^fn-nth-1]`

7. **Validate**: `python3 .claude/skills/blog-writing-guide/tools/validate_blog_post.py _posts/YOUR_POST.md`

## Usage

- `/create-post "How to Set Up Prometheus Monitoring"`
- `/create-post "Docker Networking Basics" --audience "beginners"`
- `/create-post "Kubernetes Pod Security" --structure "tutorial"`

## Arguments

- `topic` (required): The main topic or title
- `--audience` (optional): Target audience (beginners, intermediate, advanced)
- `--structure` (optional): Content structure (tutorial, listicle, deep-dive, comparison)
- `--series` (optional): Series name if this post is part of a series
