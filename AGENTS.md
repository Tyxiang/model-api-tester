# AGENTS.md

## Project Overview

This is a simple Python project for testing Cerebras AI API endpoints. It consists of:
- `tester.py` - CLI tool to list available models and test them
- `config.json` - Configuration file for API settings
- `readme.txt` - Rate limit documentation

## Build/Lint/Test Commands

### Running the Tester

```bash
# List available models
python tester.py list

# Test a specific model
python tester.py test <model_name>
```

### Dependencies

```bash
# Install required packages
pip install requests
```

### Packaging

```bash
pyinstaller --onefile tester.py
```

- No icon file exists in the project; do NOT add `--icon` flag
- Output is placed in `dist/tester.exe`

This project has no formal test suite or linting configuration. For any new code:
- Use `python -m py_compile <file>` to check syntax
- Manually test new functionality with `python tester.py test <model>`

## Code Style Guidelines

### General Style
- Use 4 spaces for indentation (no tabs)
- Use UTF-8 encoding for all files
- Maximum line length: 120 characters
- Use trailing commas in multi-line structures

### Imports
- Standard library imports first, then third-party, then local
- Group imports with blank lines between groups
- Use explicit relative imports for local modules

```python
import sys
import json
import time

import requests
```

### Formatting
- Use Black-style formatting when possible
- Add spaces around operators: `a = b + c`
- No spaces inside parentheses: `func(a, b)`
- Use f-strings for string formatting

### Types
- Use type hints for function signatures and return types
- Prefer primitive types over custom types when simple
- Use `Optional[T]` instead of `T | None` for Python 3.9 compatibility

```python
def load_config() -> dict:
    ...
```

### Naming Conventions
- `snake_case` for functions, variables, and methods
- `PascalCase` for classes
- `UPPER_SNAKE_CASE` for constants
- Descriptive names preferred over abbreviations
- Private functions prefixed with underscore: `_helper_func()`

### Error Handling
- Use specific exception types when possible
- Always include context in error messages
- Use try/except with specific exceptions, not bare `except:`
- Log errors appropriately for debugging

```python
try:
    resp = requests.get(url, timeout=30)
except requests.Timeout:
    print(f"Request timed out: {url}")
except requests.RequestException as e:
    print(f"Request failed: {e}")
```

### Function Design
- Keep functions small and focused
- Use early returns to reduce nesting
- Document complex logic with docstrings
- Avoid side effects where possible

### Strings
- Use double quotes for strings
- Use f-strings for interpolation
- Keep strings on one line when possible

### Configuration
- Store sensitive data in config files (already done)
- Never hardcode API keys or secrets
- Use environment variables for sensitive values in production

## Best Practices

1. **API Calls**: Always set reasonable timeouts (30-60s)
2. **JSON Handling**: Use `ensure_ascii=False` for non-ASCII content
3. **Config Loading**: Validate required fields exist
4. **Error Messages**: Make them actionable and user-friendly

## File Structure

```
.
├── AGENTS.md          # This file
├── config.json        # API configuration
├── readme.txt         # Rate limits
└── tester.py          # Main CLI tool
```

## Cursor/Copilot Rules

### Version Bumping
- Whenever code changes are made and the user asks to package/build, bump `VERSION` in `tester.py` before packaging
- Follow semantic versioning (MAJOR.MINOR.PATCH), increment PATCH for minor fixes/features