---
name: "[EN] Security Report"
about: Report a vulnerability or security concern in the library
title: "[SECURITY]: "
labels: ["security"]
assignees: ""
---

## Responsible Disclosure Notice
If the discovered vulnerability is critical and poses an active threat to production systems, please consider contacting the maintainers privately before publishing an exploitable proof of concept.

## Vulnerability Description
A clear and concise description of the detected security weakness (e.g., attack vectors, authorization bypass, improper data exposure, etc.).

## Affected Component
- Module / Class / Route: [e.g., core/security, flask_ext/routes.py, MailDispatcher]
- Affected Versions: [e.g., all versions <= 1.2.0]

## Estimated Severity Level
- [ ] Critical (RCE, complete authentication bypass)
- [ ] High (Privilege escalation, wide credential exposure)
- [ ] Medium (User enumeration, missing CSRF protection on secondary actions)
- [ ] Low (Minor inconsistency without direct exploit impact)

## Proof of Concept (PoC) / Steps to Reproduce
Technical steps to demonstrate the vulnerability in a controlled environment:
1. Test configuration...
2. Specific request or execution...
3. Observed result or impact...

## Potential Impact
What could an attacker achieve by exploiting this vulnerability?

## Proposed Mitigation or Fix
Technical suggestions to resolve or mitigate the issue (code patches, HTTP headers, additional validations, etc.).
