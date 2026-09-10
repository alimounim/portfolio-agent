# Build Journal

Notes on building this portfolio agent — what I did, why, and what I learned.

---

## [9/10/2026] — Getting started

- Set up Python environment, installed `anthropic` SDK
- Wrote first script: single hardcoded question, system prompt with basic bio info
- Learned: response text comes back as `response.content[0].text`, not a plain string
- Hit a dependency bug (`httpx2` decompression error) in my anaconda base env — fixed by creating a clean virtualenv instead of fighting the base install
- Working result: agent correctly answered a question about my data science background

