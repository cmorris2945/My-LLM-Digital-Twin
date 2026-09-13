# MVP plan

## Phase 0: safe foundation

Status: implemented in this branch.

- Replaceable Ollama model adapter
- Local web interface
- Public seed profile
- Persistent conversation turns
- Human reviewed long term memory
- No action taking tools

## Phase 1: private corpus

- Export selected conversations and documents
- Retain Chris-authored material separately from assistant output
- Classify records as fact, preference, belief, hypothesis, decision, correction, or writing example
- Add timestamps, source identifiers, confidentiality labels, and supersession links
- Keep Apex, UF, clinical, and personal collections isolated

## Phase 2: evaluation

- Create held-out questions that are not stored in the retrieval index
- Score factual recall and citation correctness
- Compare predicted decisions with Chris's actual choices
- Score writing style separately from factual accuracy
- Require uncertainty when the record does not establish Chris's view

## Phase 3: cautious adaptation

- Run semantic retrieval in shadow mode beside the deterministic retriever
- Review proposed automatic memories before promotion
- Consider preference tuning only after enough approved examples exist
- Keep changing facts and beliefs in memory, not model weights

## Phase 4: tools and embodiment

- Begin with read-only research and calendar tools
- Add explicit approval for drafts before sending or publishing
- Add speech recognition, a selected voice, and a rendered avatar
- Preserve a visible label that the system is an AI proxy for Chris

