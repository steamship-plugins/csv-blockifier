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

Tests are located in the `test/test_api.py` file. You can run them with:

```bash
pytest
```

We have provided sample data in the `test_data/` folder.

## Deploying

Deploy your converter to Steamship by running:

```bash
ship deploy --register-plugin
```

That will deploy your app to Steamship and register it as a plugin for use.

The first time, you will be asked a few questions:
* What to name your plugin
* What handle to give your plugin

Your answers will be saved in the `steamship.json` file of this project.