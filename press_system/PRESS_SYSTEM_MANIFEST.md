# DEIOM PRESS System Integration

This directory is the automation layer for the supplied DEIOM PRESS ERP package.

## Source package
- `DEIOM_PRESS_ERP.html`: single-file ERP reference supplied by the owner.
- `DEIOM_PRESS_MASTER_REFERENCE.docx`: business/engineering master reference.
- `CLAUDE.md`: engineering rules for safely modifying the ERP.
- `Azure_Enterprise_AI_Platform_Design.md`: enterprise AI architecture reference.

The ERP philosophy is intentionally lightweight: browser-first, localStorage-backed, no build step required. The automation layer must not break that property.

## Five bounded GEN agents
1. **ERP QA Agent**: validates HTML structure, script-load-order hazards, and basic runtime checks.
2. **Operations Agent**: maps ERP modules to workflow improvements, bottlenecks, inventory/QC/production opportunities.
3. **Revenue Agent**: identifies legitimate productized services, quotation opportunities, and B2B monetization paths from the ERP capabilities.
4. **AI Upgrade Agent**: proposes bounded AI features such as forecasting, document generation, demand analysis, and approved API integrations.
5. **Security & Reliability Agent**: checks secrets, unsafe external calls, dependency failures, data persistence risks, and regression risks.

The agents run in parallel on a five-minute schedule. They do **not** recursively spawn more agents. Each cycle produces isolated JSON reports and a deterministic aggregate. This keeps the system scalable without creating an uncontrolled process explosion.

## Account-ready design
No payment credentials, OTPs, passwords, API keys, or account tokens belong in this repository. When the owner later connects an approved account, the corresponding GitHub secret/environment credential can activate that integration without changing the agent architecture.

## Revenue boundary
Before account authorization, the system may research, validate, prepare assets, score opportunities, and generate drafts. Actual publishing, outbound messaging, payments, and account changes remain gated by explicit authorization and the relevant platform APIs.
