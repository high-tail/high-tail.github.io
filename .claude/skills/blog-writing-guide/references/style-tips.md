# Writing Style Guide

## Voice & Tone

This blog uses a professional but approachable voice:
- Speak directly to the reader: "we'll set up", "you can connect"
- Use contractions naturally: "we'll", "you're", "don't"
- Be concise — explain what's needed, skip what's obvious
- When introducing a technology, link to its official docs on first mention

## Formatting Rules

### Paragraphs
- Max 3–5 sentences per paragraph
- Use active voice over passive
- Lead with the key information, then elaborate

### Technical Terms
- Link to official documentation on first use: `[Prometheus](https://prometheus.io/docs/introduction/overview/)`
- For tools with specific concepts (e.g., "Galera Cluster", "write splitting"), define briefly on first use

### Code References
- Use backticks for filenames, commands, config keys: `` `_config.yml` ``, `` `docker-compose up` ``
- Use bold backticks for filenames in section headers: `#### **\`compose.yml\`**`

## Blog-Specific Patterns

### Numbered Lists for Capabilities
When describing what a tool provides, use a brief numbered list:
```markdown
Prometheus provides three main things:
1. Metrics Collection
2. Time-Series Database
3. Querying and Alerting
```

### Verification Checklists
Use checkbox syntax for verification steps:
```markdown
- [x] Does the sidebar show your avatar?
- [x] Are the title and tagline correct?
```

### Service URL Tables
When multiple services are running, present access URLs in a table:
```markdown
| Service    | WebUI                      |
| ---------- | -------------------------- |
| Grafana    | http://localhost:3000       |
| Prometheus | http://localhost:9090/query |
```
