---
name: redis-cloud-console-login-spinner
description: Use when a Redis Cloud user can enter credentials but the Console stays on a loading spinner, especially around SSO, MFA, browser cookies, blocked redirects, VPNs, corporate firewalls, browser extensions, stale session data, or HAR/console-log evidence collection for support.
---

# Redis Cloud Console Login Spinner

Use this skill to isolate Redis Cloud Console login flows that hang after credentials are submitted. Treat the spinner as a client, browser-session, identity-provider, or network-path problem until evidence points elsewhere.

## Triage Order

1. Ask whether the user reaches the login page, completes credentials, and then sees the spinner.
2. Check whether the issue reproduces in:
   - an incognito or private window
   - a different browser
   - a clean browser profile or guest profile
   - a different network, such as hotspot versus corporate network
3. If any clean path works, classify the issue as local to the failing browser profile, extension set, site data, or network policy.
4. If every path fails, check Redis Cloud status and collect support evidence.

## Browser Fixes

Guide the user through these fixes in order:

1. Open an incognito/private window or another browser.
2. Allow cookies, pop-ups, and redirects for Redis Cloud and the identity provider.
3. For SSO, explicitly allow cross-site cookies and redirects for providers such as Google or GitHub.
4. Disable ad blockers, privacy tools, script blockers, and other browser extensions.
5. Clear Redis Cloud site data only: cookies, local storage, and cached files.
6. Close all Redis Cloud tabs, restart the browser, and retry.
7. If using Chromium browsers, try an empty-cache hard reload from DevTools after clearing site data.

## Network Checks

If browser cleanup does not resolve the spinner:

1. Disable VPN, proxy, DNS filtering, or corporate security extensions temporarily where policy allows.
2. Try another network to distinguish local network policy from account or service behavior.
3. Confirm system date and time are correct, because secure session flows can fail when clocks drift.
4. For corporate networks, ask IT to allow authentication redirects, Redis Cloud Console domains, and the configured identity provider domains.

## Support Evidence

If escalation is needed, collect:

- browser name and exact version
- identity method used, such as password, Google SSO, GitHub SSO, or enterprise SSO
- whether incognito, a different browser, device, or network worked
- steps already attempted
- screenshot of the spinner state
- HAR file and browser console logs showing failed, blocked, or redirected requests

## Response Pattern

When answering, give the user a compact isolation plan:

1. Fastest clean-session test.
2. Cookie, redirect, pop-up, and extension checks.
3. Network comparison.
4. Evidence to gather if the problem persists.
