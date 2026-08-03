# Negotiation Agent

Negotiation Agent is a FastAPI application that negotiates data-sharing terms between a data consumer and a data provider. It evaluates both parties' preferences and exchanges proposals until the agents reach an agreement, reject a proposal, repeat a previous state, or reach the 25-round limit.

The negotiated terms include:

- Dataset fields
- Price
- Permission or prohibition rules
- Usage duration
- ODRL actions
- Data Privacy Vocabulary (DPV) purposes
- Third-party access

## Requirements

- Python 3.10 or newer
- `pip`

## Installation

Clone the repository and create a virtual environment:

```bash
git clone git@github.com:DIPS-Tools/Negotiation-Agent.git
cd Negotiation-Agent
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
pip install uvicorn
```

## Running the application

Start the API and web interface:

```bash
python main.py
```

Then open:

- Web interface: <http://127.0.0.1:9000>
- Interactive API documentation: <http://127.0.0.1:9000/docs>

The development server reloads automatically when source files change.

## API

### `POST /NegotiationRequest`

Starts a negotiation using a dataset and the preferences of the consumer and provider. The response is the agreed proposal, or `null` if the agents do not reach an agreement.

Example request:

```bash
curl -X POST http://127.0.0.1:9000/NegotiationRequest \
  -H 'Content-Type: application/json' \
  --data @sample.json
```

A complete example payload is available in [`sample.json`](sample.json). Its top-level structure is:

```json
{
  "dataset": {
    "name": "mydataset",
    "items": ["name", "age", "job", "salary", "address"]
  },
  "consumer_preference": {
    "...": "consumer preference fields"
  },
  "providor_preference": {
    "...": "provider preference fields"
  }
}
```

> **Note:** The API currently uses the field name `providor_preference` (including that spelling), so clients must use it exactly as shown.

## Negotiation flow

1. The consumer agent generates an initial proposal.
2. The provider accepts, rejects, or returns a counterproposal.
3. The consumer evaluates any counterproposal and may accept, reject, or counter again.
4. Negotiation continues for up to 25 rounds.
5. Repeated proposals terminate the negotiation to prevent cycles.

## Project structure

| File | Purpose |
| --- | --- |
| `main.py` | FastAPI application and negotiation loop |
| `consumer_agent.py` | Consumer proposal generation and evaluation |
| `provider_agent.py` | Provider proposal generation and evaluation |
| `preference.py` | Consumer and provider preference model |
| `proposal.py` | Proposal model and utility calculation |
| `rule.py` | Data-usage rule model |
| `dataset.py` | Dataset model |
| `negotiation_request.py` | API request model |
| `dpv.py` | DPV purpose hierarchy helpers |
| `odrl.py` | ODRL action hierarchy helpers |
| `index.html` | Browser-based user interface |
| `sample.json` | Example negotiation request |

## Development

The API is built with FastAPI and Pydantic. Ontology relationships are handled with RDFLib and NetworkX.

To perform a quick syntax check:

```bash
python -m compileall .
```
