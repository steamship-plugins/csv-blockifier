# Developing

## First Time Setup

We recommend using Python virtual environments for development.
To set one up, run the following command from this directory:

```bash
python3 -m venv .venv
```

Activate your virtual environment by running:

```bash
source .venv/bin/activate
```

Your first time, install the required dependencies with:

```bash
python -m pip install -r requirements.dev.txt
python -m pip install -r requirements.txt
```

## Implementation

All the code for this plugin is located in the `src/api.py` file:

* The ConverterPlugin class
* The `/convert` endpoint

## Testing

See TESTING.md for details

## Deploying

See DEPLOYING.md for details.