# brief-verify
Requirements-coverage verifier for hardware design-brief agents (natural-language
requirements to design briefs). Every requirement must be addressed by at least one brief
item, and every brief item must justify itself against a requirement - no orphaned
requirements, no unsupported design choices. Gates in `cases.json`; any agent callable via
`python run.py my_agent.py` (exposing `run(requirements)` returning brief items).
`python run.py` runs the naive demo agent, which the verifier blocks.
