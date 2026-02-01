---
name: create-post
description: Create a new blog post draft with specified topic and structure
---

To create a new blog post draft, follow these steps:

1. **Gather Information**: Ask the user for the blog post topic, target audience, and any specific requirements or constraints.

2. **Determine Filename**: Generate a filename following the pattern `_posts/YYYY-MM-DD-kebab-case-title.md` using the current date.

3. **Generate Front Matter**: Create the YAML front matter with the following fields:
   - `title`: The post title
   - `date`: Current date and time (e.g., `2025-04-27 10:00:00 +0900`)
   - `categories`: [Main Category, Sub Category]
   - `tags`: [tag1, tag2]
   - `mermaid`: true (if diagrams are needed)

4. **Create Outline**: Based on the topic, create a logical outline using the Blog Writing Guide skill.

5. **Generate Content**: Write the content sections following the structure and style guidelines.
   - Use Chirpy theme callouts like `> content {: .prompt-tip }` or `> content {: .prompt-info }` where appropriate.
   - Use Mermaid diagrams if technical concepts need visualization.

6. **Format Content**: Apply proper formatting including headings, lists, and other structural elements.

7. **Review and Save**: Review the draft for clarity and completeness, then save it to the `_posts/` directory.

## Usage Examples

- `/create-post "How to Build a Blog with Jekyll"`
- `/create-post "SEO Tips for Technical Writers" --audience="technical"`
- `/create-post "Getting Started with Docker" --structure="tutorial"`

## Command Arguments

- `topic` (required): The main topic or title of the blog post
- `--audience` (optional): Target audience (technical, general, beginners, etc.)
- `--structure` (optional): Content structure type (tutorial, listicle, opinion, etc.)
- `--keywords` (optional): Keywords to include in the post

## Implementation Notes

When using this command:
1. **Filename**: ALWAYS use `_posts/YYYY-MM-DD-topic-slug.md`.
2. **Front Matter**: Strictly follow the project's schema (title, date, categories, tags).
3. **Style**: Use the Blog Writing Guide skill.
4. **Theme Features**: Utilize Chirpy specific syntax (prompts, mermaid).