# SEO Best Practices for This Blog

## Front Matter SEO Checklist

These are the fields that directly affect search engine visibility:

| Field | Requirement | Example |
| ----- | ----------- | ------- |
| `title` | Primary keyword near start, under 60 chars | `"Setting Up Prometheus Monitoring for MariaDB"` |
| `description` | Compelling summary, under 160 chars | `"Step-by-step guide to monitoring MariaDB Galera Cluster with Prometheus and Grafana using Docker Compose"` |
| `categories` | 1–2 broad groupings | `[Tech, Monitoring]` |
| `tags` | 3–5 specific lowercase topics | `[prometheus, grafana, mariadb, docker]` |

## In-Content SEO

### Keywords
- Include the primary keyword in the first H2 heading and the first paragraph
- Use related keywords naturally in subsequent H2 headings
- Don't force keywords — readability comes first

### Headings
- H2 (`##`) for main sections — these are picked up by search engines
- H3 (`###`) for subsections within a section
- Make headings descriptive: "Configuring HAProxy for Load Balancing" not "Step 3"

### Internal Linking
- Link to other posts in the same series
- Link to related posts on the same blog when relevant
- Use descriptive anchor text (not "click here")

### Images
- Use descriptive filenames: `mariadb-cluster-architecture.png` not `screenshot1.png`
- Always include alt text: `![MariaDB Galera Cluster architecture diagram](/assets/img/...)`
- Store in `assets/img/`

### Content Length
- Technical tutorials: aim for 800–2000 words
- Deep dives: can go longer if the content warrants it
- Every section should add value — don't pad for length
