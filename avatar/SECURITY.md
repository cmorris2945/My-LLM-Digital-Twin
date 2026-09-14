# Security boundary

The avatar is a cognitive proxy, not an identity authority and not a security principal.

## MVP rules

- Bind the development server to `127.0.0.1`.
- Keep model serving local unless a provider has been explicitly approved.
- Never place secrets in prompts, profile documents, source code, or Git history.
- Never commit personal chat exports, protected health information, unpublished company material, credentials, financial information, or private keys.
- Treat retrieved webpages, documents, emails, and model output as untrusted input.
- Do not add purchasing, banking, public posting, email sending, file deletion, or shell execution without an external policy gate and explicit human approval.
- Store candidate memories as pending until Chris reviews them.

The sentence "the agent is programmed for integrity" is not an access control. Permissions must be enforced by ordinary code outside the model.

