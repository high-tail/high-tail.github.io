---
name: generate-content
description: Generate specific content sections for blog posts based on prompts
---

To generate specific content sections for blog posts, follow these steps:

1. **Receive Prompt**: Get the specific content request from the user.

2. **Determine Context**: Understand the existing blog post structure and context.

3. **Generate Content**: Create the requested content section following blog writing best practices.

4. **Format Content**: Apply appropriate formatting and structure.

5. **Review and Deliver**: Ensure the content fits seamlessly with existing content.

## Usage Examples

- `/generate-content "Introduction section for a post about Jekyll static sites"`
- `/generate-content "Benefits of using Docker for development" --section="main-body"`
- `/generate-content "Conclusion for a post about CSS frameworks" --style="professional"`

## Command Arguments

- `prompt` (required): Specific content request or topic
- `--section` (optional): Which section to generate (introduction, main-body, conclusion)
- `--style` (optional): Writing style (professional, casual, technical)
- `--length` (optional): Desired length (short, medium, long)
- `--audience` (optional): Target audience (technical, general, beginners)

## Implementation Notes

When using this command:
1. Use the Blog Writing Guide skill for consistent style and structure
2. Consider the existing content context when generating
3. Apply appropriate formatting for the requested section
4. Ensure generated content aligns with the overall blog post theme
5. Follow SEO best practices for keyword integration
6. Maintain consistent voice and tone with the rest of the blog