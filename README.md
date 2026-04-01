# Model API Tester

A simple CLI tool for testing OpenAI-compatible AI API endpoints.

## Features

- List available models from an API endpoint
- Test individual models or batch test all models
- Measure response times
- Log results to JSON files
- Supports frozen executables (PyInstaller)

## Installation

```bash
pip install requests
```

## Usage

### Initialize Config

```bash
python tester.py init
```

Generates a `config.json` template. Edit it with your API details:

```json
{
  "name": "Your API Name",
  "api-type": "openai",
  "base-url": "https://api.example.com/v1",
  "api-key": "your-api-key-here"
}
```

### List Models

```bash
python tester.py list
```

Fetches and saves available models to `list.json`.

### Test Models

```bash
# Test all models from list.json
python tester.py test

# Test specific model(s)
python tester.py test <model_name>
python tester.py test <model1> <model2>
```

Results are saved to `test.json`, sorted by response time.

### Other Commands

```bash
python tester.py --help     # Show help
python tester.py --version  # Show version
```

## Build Executable

```bash
pyinstaller --onefile tester.py
```

Output is placed in `dist/tester.exe`.

## Files

| File | Description |
|------|-------------|
| `tester.py` | Main CLI tool |
| `config.json` | API configuration |
| `list.json` | Cached model list |
| `test.json` | Test results |
| `tester.log` | Error log |

## License

MIT
