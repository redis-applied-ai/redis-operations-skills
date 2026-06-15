---
name: redis-login-429-triage
description: Use when Redis Cloud, Redis Insight, or Redis Support portal login returns HTTP 429 Too Many Requests, especially after repeated login attempts, Captcha failures, SSO retry loops, browser blockers, privacy extensions, corporate proxy filtering, concurrent sessions, automated Redis Insight sign-ins, or when distinguishing login throttling from Redis Cloud API quota 429s.
---

# Redis Login 429 Triage

Use this skill for interactive login 429 responses in Redis Cloud, Redis Insight, or related Redis portals. Do not treat login 429s as Redis database throughput errors.

## First Distinction

Classify the 429:

- Interactive login 429: browser, SSO, Captcha, bot protection, repeated retries, concurrent sessions.
- API quota 429: non-interactive Redis Cloud API calls are too frequent and need API backoff/rate limiting.

Use the rest of this skill for interactive login 429s.

## Immediate Recovery

1. Stop retrying for a short cooldown period.
2. Retry once in a private or incognito browser window.
3. Close extra login tabs and stop simultaneous login attempts from other devices.
4. Complete any Captcha or anti-bot challenge.
5. If Captcha does not load, disable ad blockers, privacy extensions, script blockers, or corporate proxy filtering for the login flow.
6. Try a different browser, device, or network to isolate local blockers.

## Redis Insight Specifics

If Redis Insight or scripts trigger login attempts:

- remove automation from interactive login endpoints
- add backoff and retry limits
- use supported API authentication paths for non-interactive workflows
- avoid tight loops after failed authentication

## Browser And Network Checks

Ask for:

- browser and version
- whether private browsing works
- whether another network works
- SSO provider involved
- Captcha visibility and completion behavior
- extensions or corporate security tools in the path
- number of concurrent sessions or retrying devices

## Support Evidence

If throttling persists after cooldown and clean-session tests, collect:

- screenshot of the 429 or Captcha state
- browser and OS version
- login method, such as password or SSO
- approximate time and timezone of attempts
- whether another browser, device, or network worked
- steps already tried
- HAR file or console logs if requested by support

## Prevention

- Avoid rapid manual retry loops.
- Do not automate interactive login pages.
- Whitelist required login and Captcha domains in browser privacy tools or corporate filters.
- For API workloads, implement backoff and respect current API quota guidance.

## Response Pattern

Answer with:

1. Whether this is interactive login throttling or API quota throttling.
2. A cooldown and clean-session retry plan.
3. Browser/network blocker checks.
4. Automation/backoff guidance when Redis Insight or scripts are involved.
5. Evidence to collect if support escalation is needed.
