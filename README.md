# Model API Tester

A simple CLI tool for testing OpenAI-compatible AI API endpoints.

## Features

- List available models from an API endpoint
- Test individual models or batch test all models
- Measure response times
- Log results to JSON files
- Portable executable, no Python required

## Usage

Download `tester.exe` and place it in a folder.

### Initialize Config

```bash
tester.exe init
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
tester.exe list
```

Fetches and saves available models to `list.json`.

### Test Models

```bash
# Test all models from list.json
tester.exe test

# Test specific model(s)
tester.exe test <model_name>
tester.exe test <model1> <model2>
```

Results are saved to `test.json`, sorted by response time.

### Other Commands

```bash
tester.exe --help     # Show help
tester.exe --version  # Show version
```

## Build from Source

```bash
pip install requests
pyinstaller --onefile --icon=NONE tester.py
```

Output is placed in `dist/tester.exe`.

## Files

| File | Description |
|------|-------------|
| `tester.exe` | Main CLI tool |
| `config.json` | API configuration |
| `list.json` | Cached model list |
| `test.json` | Test results |
| `tester.log` | Error log (auto-generated) |

## License

MIT
