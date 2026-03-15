# Blog Post Template

Copy this template when starting a new post. Replace placeholders with actual content.

```markdown
---
title: "[Primary Keyword] [Descriptive Title]"
date: YYYY-MM-DD HH:MM:SS +0900
description: "[Compelling summary under 160 chars]"
comments: true
mermaid: true
categories: [Main, Sub]
tags: [tag1, tag2, tag3]
---

## Objective

[1-2 sentences: what this post achieves and why it matters.]

<!-- If part of a series, uncomment:
This is part N of the series:
1. [Part 1 Title](https://high-tail.github.io/posts/part-1-slug)
2. [Part 2 Title](https://high-tail.github.io/posts/part-2-slug) ← this post
-->

## Prerequisites

- [Required tool or knowledge]
- [Required tool or knowledge]

> My Environment
>
> | Software | Version |
> | :------- | :------ |
> | [Tool]   | [X.Y.Z] |
>
{: .prompt-tip }

## Overview

### [Key Concept 1]

[Brief explanation with link to official docs.]

### [Key Concept 2]

[Brief explanation.]

> Architecture
> ```mermaid
> architecture-beta
>     group system[System Name]
>     service svc1(server)[Service 1] in system
>     service svc2(database)[Service 2] in system
>     svc1:R -- L:svc2
> ```
{: .prompt-info }

## Implementation

### File Structure[^fn-nth-1]

```
.
├── file1.yml      # Update
└── directory/
    ├── new-file/  # New
    └── config.cfg # Update
```

### [Step or File Name]

[Explanation of what this step does.]

```yaml
# Code block with inline comments
key: value  # Explain this line
```

## How to Start

```bash
docker-compose build
docker-compose up -d
```

| Service | WebUI |
| ------- | ----- |
| [Name]  | http://localhost:[port] |

## Completed Plan

- [x] [What was accomplished]
- [x] [What was accomplished]

## Links

[^fn-nth-1]: [Repository Name](https://github.com/...) - Description of the source code.
```
