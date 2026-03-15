---
name: generate-content
description: Generate specific content sections for blog posts based on prompts
---

Generate a specific section for an existing or new blog post:

1. **Read the skill guide** at `.claude/skills/blog-writing-guide/SKILL.md` for style and formatting standards.

2. **Understand context**: If a post already exists, read it first to match tone and flow.

3. **Generate the requested section** following the blog's patterns:
   - **Objective**: State the goal, include series links if applicable
   - **Prerequisites**: Tools list + environment version table in `{: .prompt-tip }`
   - **Overview**: Key concepts + architecture diagram in `{: .prompt-info }`
   - **Implementation**: File structure tree + annotated code blocks
   - **Verification**: Commands, URLs table, expected output
   - **Conclusion**: Checklist of completed items + next steps

4. **Apply formatting**: Use Chirpy callouts, Mermaid diagrams, footnotes, and fenced code blocks with language identifiers as appropriate.

## Usage

- `/generate-content "Prerequisites section for a post about Kubernetes"`
- `/generate-content "Architecture overview diagram for HAProxy setup" --section "overview"`
- `/generate-content "Conclusion for my Docker monitoring post" --section "conclusion"`

## Arguments

- `prompt` (required): What content to generate
- `--section` (optional): Which section type (objective, prerequisites, overview, implementation, verification, conclusion)
- `--file` (optional): Path to existing post to match context
