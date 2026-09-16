# AI Phone Agent Integration Layer

The uploaded `ai-phone-agent` project has been mapped into the DEIOM PRESS architecture as an **optional, account-gated voice capability**.

## Imported capabilities

- OpenAI Realtime voice sessions
- Twilio Media Streams phone path
- Amazon Connect + OpenAI SIP webhook path
- MCP tool integration
- Structured intake, human transfer, and call termination patterns
- Voice activity detection and realtime session lifecycle patterns

## DEIOM PRESS uses

1. AI receptionist for inbound business calls.
2. Lead qualification and structured customer intake.
3. Printing/packaging quotation requirement capture.
4. Solar quotation requirement capture.
5. Appointment/request routing.
6. Human handoff when a customer requires a person.

## Account gate

Nothing in this layer is permitted to place calls, send outbound messages, transfer calls, access customer accounts, or spend money until the owner explicitly configures the required secrets and integrations.

## Required future secrets

- `OPENAI_API_KEY`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER` / approved voice number configuration
- Amazon Connect/AWS credentials only if that channel is selected

Secrets belong in GitHub Secrets or a server-side secret manager, never in source control.

## Upgrade policy

The five-agent swarm may discover new AI capabilities, compare providers, prepare adapters, and run compatibility checks. It must not silently switch production providers, create paid accounts, change billing, or initiate external communications. Promotion requires a validated test and explicit account authorization.
