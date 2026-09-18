# Mushu — Technical Validation Record

An AI-powered system that turns the gap between a technical validation call and Commercial
Negotiation from an unowned silence into a living, accruing record — visible to the AE, the SC,
and Customer Success at handoff, in the Slack channel the deal already lives in.

Built for the Applied AI Architect, GTM assessment (Braze).

**→ Full system design: [`docs/design-doc.md`](docs/design-doc.md)** — who uses it, when, what
triggers it, what the output looks like, what data it needs, and what was actually built vs.
described.

## Repo map

```
docs/
  design-doc.md               # the full system design (start here)
  build-plan.md               # original planning doc — the problem, the field spec, the five-day plan
  record-contract.md          # authoritative schema for the Validation Record — the "exactly what"
  enforcement-layer-spec.md   # stage-exit criteria, closure tracking, two-stage escalation, dashboard
  corrections.md              # running log of every correction made to the pipeline, and why
  deal-spec.md                # the six synthetic deals and what each one tests
  transcript-generation-process.md
prompts/                      # the three-pass extraction chain, as separate iterable .md files
scripts/                      # seeding, extraction, closure checks, escalation, demo scripts
sql/schema.sql                # the Supabase schema
transcripts/                  # nine hand-QA'd synthetic call transcripts
scratch/                      # rendered record text used in the demo
```

## Running the demo

See `docs/design-doc.md` §7 for what's actually built, and the individual scripts in `scripts/`
for how to run the extraction chain and the demo sequence against the Meridian Health deal.

## Note on data

Everything in this repo — accounts, transcripts, deals, people — is 100% synthetic, generated for
this assessment. No real customer data of any kind appears anywhere in this repository.
