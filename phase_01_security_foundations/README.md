# Phase 1: Security Foundations for AI Engineers (Days 9-16)

You can't secure agents if you can't secure an API. This phase gives you the classic AppSec and
cloud-security vocabulary that AI-security work builds on: OAuth, SSRF, IDOR, supply chain and threat modeling.
These are the concepts interviewers probe when your resume says "AI security".

## Days

- **Day 9: Security mindset & threat modeling.** CIA triad, attack surface, trust boundaries, data-flow
  diagrams, **STRIDE**. Exercise: threat-model a "chat with your docs" bot (assets, entry points, threats, mitigations).
- **Day 10: Web & API security.** [OWASP Top 10 (2025)](https://owasp.org/Top10/) + [OWASP API Security Top 10](https://owasp.org/API-Security/):
  injection, broken access control, BOLA/IDOR, SSRF, security misconfiguration, supply-chain failures.
- **Day 11: AuthN / AuthZ.** OAuth 2.1 (auth code + PKCE, client credentials), OIDC, JWT pitfalls (`alg=none`,
  key confusion, missing `aud` checks), API keys vs tokens, RBAC/ABAC/ReBAC, least privilege.
  *Build:* FastAPI service with JWT auth and per-route scopes.
- **Day 12: Applied cryptography.** Hashing vs HMAC vs encryption, AEAD (AES-GCM), public-key crypto, TLS
  handshake, digital signatures, password hashing (argon2), key rotation, secrets managers.
  You'll reuse signatures in Phase 4 (model signing) and Phase 5 (signed agent manifests).
- **Day 13: Networking & cloud security.** DNS, HTTP, TLS, proxies; **SSRF → cloud metadata endpoints**;
  IAM, managed identities, private endpoints, egress control, zero trust.
- **Day 14: Secure SDLC & software supply chain.** SAST/DAST ([Semgrep](https://semgrep.dev/), Bandit),
  dependency scanning, secret scanning ([gitleaks](https://github.com/gitleaks/gitleaks)), SBOMs (CycloneDX),
  [SLSA](https://slsa.dev/), typosquatting and **slopsquatting** (LLMs hallucinating package names that attackers register).
- **Day 15: Detection & response.** Structured audit logs (who/what/when/on-whose-behalf), SIEM basics, alert
  design, incident response lifecycle, [MITRE ATT&CK](https://attack.mitre.org/), the bridge to MITRE ATLAS in Phase 4.
- **Day 16: 🎯 Ship + SD #2.** **Secure LLM API gateway skeleton** (FastAPI): JWT auth, per-tenant rate limits,
  input size/schema validation, audit logging, secrets from env/Key Vault, Semgrep + gitleaks in pre-commit.
  **SD #2:** *Design a secure multi-tenant LLM API gateway.*

## Resources

- [PortSwigger Web Security Academy](https://portswigger.net/web-security) (free and the best hands-on resource)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [oauth.net/2.1](https://oauth.net/2.1/)
- Adam Shostack, *Threat Modeling: Designing for Security* (STRIDE)

## Deliverables

- `gateway/`: the secure gateway skeleton. You'll extend it in Phases 2-6 and the capstone.
- `threat_models/chatbot_stride.md`
- SD #2 write-up
