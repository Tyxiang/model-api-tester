# Model API Tester

A simple CLI tool for testing AI API endpoints (OpenAI, Gemini, Anthropic).

## Features

- Support multiple API protocols (OpenAI, Gemini, Anthropic)
- List available models from an API endpoint
- Test individual models or batch test all models
- Measure response times
- Results in CSV format
- Portable executable, no Python required

## Usage

Download `tester.exe` and place it in a folder.

### Initialize Config

```bash
tester.exe init
```

Choose API type (1: OpenAI, 2: Gemini, 3: Anthropic) and edit `config.json`:

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

Fetches and saves available models to `list.csv`.

### Test Models

```bash
# Test all models from list.csv
tester.exe test

# Test specific model(s)
tester.exe test <model_name>
tester.exe test <model1> <model2>

# Filter results (OK or FAILED)
tester.exe test -f OK
tester.exe test -f FAILED
```

Results are saved to `test.csv`, sorted by response time.

### Other Commands

```bash
tester.exe -v          # Show version
tester.exe list --help # Show list options
tester.exe test --help # Show test options
```

## Build from Source

```bash
pip install requests
pyinstaller --onefile --icon=NONE tester.py
```

Output is placed in `dist/tester.exe`.

## Files

| File       | Description                 |
|------------|----------------------------|
| `tester.exe`  | Main CLI tool           |
| `config.json` | API configuration       |
| `list.csv`    | Cached model list       |
| `test.csv`   | Test results             |
| `tester.log` | Error log (auto-generated) |

## License

MIT
