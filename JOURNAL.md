# Build Journal

Notes on building this portfolio agent — what I did, why, and what I learned.

---

## [9/10/2026] — Getting started

- Set up Python environment, installed `anthropic` SDK
- Wrote first script: single hardcoded question, system prompt with basic bio info
- Learned: response text comes back as `response.content[0].text`, not a plain string
- Hit a dependency bug (`httpx2` decompression error) in my anaconda base env — fixed by creating a clean virtualenv instead of fighting the base install
- Working result: agent correctly answered a question about my data science background

## [9/11/2026] — Conversational loop with memory

- Extended the single-question script into a real back-and-forth loop using `input()`
- Learned that the API has no memory between calls — you have to resend the full conversation history (`messages` list) every time, with each entry shaped as `{"role": ..., "content": ...}`
- Hit an auth error from a new terminal session — realized my API key export doesn't persist across sessions, and I wasn't in my virtual environment (`base` vs `agent_env`)
- Tested memory by asking a follow-up question referencing the previous one — worked correctly
- Noticed the agent stayed honest about not knowing things outside its system prompt (e.g. specific tools/languages) instead of making things up — good sign for reliability
- Next: make the API key persist automatically instead of re-exporting every session (probably via `.env`)


