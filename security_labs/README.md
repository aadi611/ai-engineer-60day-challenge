# 🔐 Security Labs Track (Track A, even days)

~45 min of hands-on offense on every even day. You learn defense fastest by breaking things.
All labs below are **legal, intentionally vulnerable targets**. Never point tools at systems you don't own or
aren't authorized to test.

## Progression

| Days | Lab | Skill |
|---|---|---|
| 2 | Burp Suite Community setup + [PortSwigger](https://portswigger.net/web-security) HTTP basics | Intercepting proxy, reading raw HTTP |
| 4, 6 | [OverTheWire Bandit](https://overthewire.org/wargames/bandit/) 0-20 | Linux, permissions, networking basics |
| 8, 24 | [Gandalf](https://gandalf.lakera.ai/) levels 1-8 | Prompt injection intuition |
| 10 | PortSwigger: SQL injection | Injection (the ancestor of prompt injection) |
| 12 | PortSwigger: JWT attacks | Token validation bugs |
| 14 | PortSwigger: SSRF | SSRF → cloud metadata (critical for agents with fetch tools) |
| 16 | PortSwigger: Access control / IDOR | Authorization bugs |
| 18, 26 | [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) | Full-app web exploitation |
| 20, 22, 42 | [PortSwigger: Web LLM attacks](https://portswigger.net/web-security/llm-attacks) | Excessive agency, indirect injection, insecure output handling |
| 28, 30, 40 | Dreadnode Crucible (AI red-team CTF) | Prompt injection, jailbreaks, model evasion |
| 32, 34, 44 | Damn Vulnerable MCP Server (open source, run locally) | Tool poisoning, rug pulls, token theft |
| 36 | TryHackMe AI/LLM security rooms | Guided AI security |
| 46 | Pickle payload vs safetensors (local, your own files) | Model supply chain |
| 48 | Write an AI incident post-mortem | Incident response |
| 52, 54 | OAuth / JWT misconfiguration labs (PortSwigger OAuth) | Delegation & identity bugs |
| 56 | PortSwigger: Business logic vulnerabilities | Payment/flow abuse |
| 58 | Audit a real open-source MCP server (read-only review) | Code review for agent tools |
| 60 | Threat-model your marketplace | Design review |
| 62-68 | Cloud misconfig, rate-limit bypass, detection engineering, CTF of choice | Ops security |
| 70 | Re-do weakest lab category | Gap-fill |

> Tool/lab availability changes. If one is gone, swap in an equivalent and note it in your daily log.

## How to log

One line per lab in `security_labs/log.md`: date · lab · solved? · **the one trick** · "how would this
show up in an AI agent?" The last column is what turns a web-security lab into AI-security intuition.
