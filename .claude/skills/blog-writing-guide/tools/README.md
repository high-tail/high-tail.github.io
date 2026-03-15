# Validation Tool

## validate_blog_post.py

Validates blog posts against the project's standards.

### Usage

```bash
python3 .claude/skills/blog-writing-guide/tools/validate_blog_post.py _posts/YYYY-MM-DD-your-post.md
```

### What It Checks

| Check | Severity | Details |
| ----- | -------- | ------- |
| Filename format | FAIL | Must match `YYYY-MM-DD-kebab-case.md` |
| Required front matter | FAIL | `title`, `date`, `categories`, `tags` must be present |
| Recommended front matter | FAIL | `description`, `comments` should be present |
| Description length | FAIL | Must be under 160 characters |
| Title length | FAIL | Recommended under 60 characters |
| H1 in body | FAIL | Chirpy uses `title` as H1 — use `##` for body sections |
| Image paths | FAIL | Must use `/assets/img/` prefix |
| Callout usage | SUGGEST | Recommends adding `{: .prompt-tip }` etc. if none found |
| Footnotes | SUGGEST | Recommends adding footnotes for source references |

### Example Output

```
Validating _posts/2025-04-27-my-post.md...

[PASS] Filename: Filename format correct
[PASS] Front Matter: Front matter looks good
[PASS] Content: Content structure looks good

[SUGGESTIONS]
  - Consider adding footnotes for source references

========================================
SUCCESS: Post meets all requirements!
```
