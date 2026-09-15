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

## [9/12/2026] — Persistent API key with .env

- Installed `python-dotenv` inside the venv specifically (had it in anaconda base, but venv needed its own copy)
- Created `.env` file with `ANTHROPIC_API_KEY=...`, confirmed `.gitignore` already excludes it from git
- Added `load_dotenv()` to the top of the script — no more manually exporting the key every new terminal session
- Verified it works in a completely fresh terminal with no manual export
- Tested a couple more questions — noticed the agent consistently declines to guess at unstated facts (like years of experience) rather than making things up, which is exactly the behavior I want for a portfolio agent
- Next: start thinking about turning this into an actual web app

## [9/13/2026] — First working web version (Flask)

- Built a Flask backend (`app.py`) with two routes: `/` serves the chat page, `/chat` handles the actual API call to Claude
- Created `templates/index.html` — plain HTML/JS chat interface, no styling yet
- Learned Flask's template folder convention (`templates/`) and hit a `TemplateNotFound` error from skipping that step — good reminder to actually run every setup command, not just the ones that feel important
- This version doesn't yet keep conversation history between messages (each request is independent) — that's next
- Milestone: agent is now usable in an actual browser, not just the terminal
- Next: bring back conversation memory in the web version, then start the visual design phase (playful character, Afghan/Dari-Farsi visual motifs)

## [9/14/2026] — Conversation memory in the web app

- Added a `conversation_history` list outside the `chat()` route so it persists across requests (Flask handles each request independently, unlike my terminal script's single continuous loop)
- Bug I hit: appended to `conversation_history` correctly but forgot to actually pass it to `client.messages.create()` — was still sending only the latest message. Fixed by changing `messages=[...]` to `messages=conversation_history`
- Tested with a direct memory check ("what did I just ask you?") — worked correctly
- Known limitation to fix later: `conversation_history` is global, shared across all visitors, and resets on server restart. Fine for solo testing now, not fine once this is public — will need per-visitor sessions
- Also noticed: across several tricky questions (ML projects, personal interests), the agent consistently refused to fabricate details it didn't have, instead pointing to real sources. This is exactly the trust behavior I want
- Next: start the design phase — playful character, Afghan/Dari-Farsi visual motifs

## [9/14/2026] — Real bio + conversational personality

- Replaced the placeholder system prompt with a full bio (`about_ali.py`), pulled from my actual LinkedIn export — all work history, technical skills, certifications, languages, projects, and career goals
- Kept the LinkedIn PDF itself (`Profile.pdf`) out of the repo via `.gitignore` since it has personal contact info — only the extracted bio content in `about_ali.py` is tracked
- Rewrote the system prompt instructions to make the agent talk like a real person in first-person conversation instead of dumping bullet lists — short, natural answers, only answering what's actually asked
- Tested with casual questions ("what do you do for work," "do you know Python," "what languages do you speak") — tone landed exactly right, felt like a real conversational reply instead of a chatbot readout
- Next: visual design phase — playful character, Afghan/Dari-Farsi visual motifs

## [9/14/2026] — Full UI styling pass

- Restyled the entire page: dark navy background, gold/maroon jewel-tone accents matching the avatar
- Added chat bubbles (user messages right-aligned teal, replies left-aligned navy/gold) instead of plain text lines
- Added a "thinking" indicator — animated bouncing dots that show while waiting for the API response, replaced with the real reply once it arrives
- Wired in the custom avatar with a soft glow effect
- Started (not finished) a resume download button — paused to find/prepare an actual resume PDF first
- Prototype is now genuinely demo-ready to show friends

## [9/15/2026] — Resume download button

- Added my actual resume PDF to static/files/
- Added a "View full résumé (PDF)" button below the subtitle, opens in a new tab via url_for
- Tested that it opens correctly in the browser

## [9/15/2026] — Fixed shared session bug

- Replaced the global conversation_history list with a conversations dictionary keyed by a per-visitor session_id (using Flask's session + secrets.token_hex)
- Hit a naming bug — declared the dict as conversation_history but referenced conversations everywhere else; renamed to match
- Tested with two simulated recruiter conversations in parallel — confirmed each stayed isolated and coherent, no cross-contamination
- Agent handled realistic recruiter Q&A well — conversational tone, relevant detail pulled from bio, asked good follow-up questions
- Noted a watch-item: first-person phrasing can read as more confident than intended when asked about specific unstated experience — worth monitoring, not an immediate fix
- Next: deploy online so this is accessible via a real URL, not just localhost