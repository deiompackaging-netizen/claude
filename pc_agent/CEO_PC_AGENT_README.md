# CEO PC Agent

This folder is the local-worker layer for the DEIOM CEO Money Engine.

## Target machine
- Windows 64-bit
- Intel Core i3-4160, 2 cores / 4 threads
- 16 GB RAM
- 256 GB-class SSD
- Intel HD Graphics 4400

The machine is suitable for lightweight automation, Python jobs, document generation, web/API work, and browser automation. It is **not** intended for local large-model inference or heavy video rendering.

## Operating model
1. GitHub Actions handles cloud scheduling and heavier CPU work.
2. This Windows PC handles local jobs that require the machine, local files, browser sessions, or long-running background work.
3. Revenue priorities:
   - sell digital products through Gumroad
   - generate qualified B2B solar leads
   - prepare personalized outreach drafts
   - generate useful IDE/developer content that drives traffic to products
   - track measurable conversions
4. Never use fake clicks, fake subscribers, spam, credential theft, deceptive reviews, or invented affiliate claims.

## Security
Never put passwords, OTPs, API keys, payment tokens, bank numbers, or recovery codes in this repository. Use Windows environment variables or GitHub Actions secrets.

## One-time setup
Run `install_ceo_agent.ps1` as the Windows user who owns the browser sessions. It creates a startup task and launches `worker.ps1`.

The worker is deliberately allow-listed. It does not execute arbitrary commands received from the internet.
