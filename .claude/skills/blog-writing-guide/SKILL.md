---
name: blog-writing-guide
description: Create, structure, and improve blog posts following Jekyll Chirpy theme standards. Use for writing new posts, auditing drafts, or organizing content.
---

# Blog Writing Guide

This skill guides you in creating high-quality blog posts that adhere to the project's Jekyll Chirpy theme standards.

## Critical Constraints (MUST Follow)

1.  **File Naming**: ALWAYS use `_posts/YYYY-MM-DD-kebab-case-title.md`.
2.  **Front Matter**: MUST include `title`, `date`, `categories` (list), and `tags` (list).
3.  **Theme Features**: Use Chirpy callouts for emphasis:
    *   `{: .prompt-tip }` (Green)
    *   `{: .prompt-info }` (Blue)
    *   `{: .prompt-warning }` (Yellow)
    *   `{: .prompt-danger }` (Red)
4.  **Diagrams**: Use `mermaid: true` in front matter if using Mermaid diagrams.

## Workflow: Creating a New Post

Follow this sequence to ensure quality and consistency.

### 1. Planning & Structure
*   **Analyze**: Identify the target audience and key takeaways.
*   **Structure**:
    1.  **Introduction**: Hook the reader, state the problem/goal.
    2.  **Prerequisites**: Define needed environment/knowledge (use `.prompt-info`).
    3.  **Body**: Logical steps/sections using H2 (`##`) and H3 (`###`).
    4.  **Conclusion**: Summary and actionable next steps.
*   *Reference*: See `examples/blog-outline-template.md` for a concrete outline structure.

### 2. Drafting Content
*   **Tone**: Professional yet conversational. Speak directly to the reader ("You can...").
*   **Readability**:
    *   Max 3-5 sentences per paragraph.
    *   Use bullet points for lists.
    *   Use active voice.
*   **SEO**: Include keywords naturally in H2 headers and the first paragraph.
*   *Reference*: See `references/style-tips.md` for detailed voice/tone guidelines.

### 3. Formatting & Refinement
*   **Images**: Use `![Alt text](/assets/img/path/to/image.png)`.
*   **Code**: Use fenced code blocks with language identifiers (e.g., ````bash`).
*   **Links**: Use internal links to other posts where relevant.
*   *Reference*: See `references/seo-best-practices.md` for optimization details.

### 4. Validation
*   **Run Tool**: Execute the validation script to check for common errors.
    *   Command: `python3 ./tools/validate_blog_post.py _posts/YOUR_POST.md`

## Workflow: Improving Existing Content

When asked to "improve" or "review" a post:

1.  **Audit Structure**: Check against the "Critical Constraints" and "Structure" above.
2.  **Check Formatting**: Ensure headers are hierarchical (no H1 in body) and code blocks are clear.
3.  **Enhance Features**: Suggest adding Callouts (`{: .prompt-tip }`) or Mermaid diagrams where they add value.
4.  **Optimize**: Check for keyword usage and sentence length.
5.  **Validate**: Run `python3 ./tools/validate_blog_post.py <path>` to ensure compliance.

## Available Resources

*   **`examples/blog-outline-template.md`**: Standard structure template.
*   **`examples/seo-optimized-post.md`**: Example of a fully polished post.
*   **`references/structure-guidelines.md`**: Deep dive on post components.
*   **`references/style-tips.md`**: Writing style guide.
*   **`references/seo-best-practices.md`**: SEO checklist.
*   **`tools/validate_blog_post.py`**: Python script to validate filename, front matter, and structure.
