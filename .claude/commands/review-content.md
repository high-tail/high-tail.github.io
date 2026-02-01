---
name: review-content
description: Analyze existing blog content for improvements in structure, style, and SEO
---

To review existing blog content, follow these steps:

1. **Receive Content**: Get the blog post content to analyze from the user.

2. **Analyze Structure**: Check if the content follows proper blog post structure using the Blog Writing Guide skill.

3. **Evaluate Style**: Assess writing style, tone, and readability.

4. **Check SEO**: Review for keyword usage, meta elements, and technical SEO factors.

5. **Provide Recommendations**: Offer specific suggestions for improvement.

## Usage Examples

- `/review-content "My existing blog post about Jekyll"`
- `/review-content --file="posts/2023-01-01-jekyll-tips.md"`

## Command Arguments

- `content` (required): The blog post content to review (can be pasted directly or file path)
- `--file` (optional): Path to a file containing the blog post content
- `--focus` (optional): Specific area to focus on (structure, style, SEO)

## Implementation Notes

When using this command:
1. Apply the Blog Writing Guide skill to evaluate content quality
2. Check for proper heading hierarchy and content organization
3. Assess writing style and readability
4. Review SEO elements including keywords and meta tags
5. Provide actionable improvement suggestions
6. Highlight strengths as well as areas for improvement