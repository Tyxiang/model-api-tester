#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import json
import time
import requests
from datetime import datetime

CONFIG_FILE = "config.json"
LIST_FILE = "list.json"
TEST_FILE = "test.json"
LOG_FILE = "tester.log"
VERSION = "1.1.10"

def get_script_dir():
	if getattr(sys, "frozen", False):
		return os.path.dirname(sys.executable)
	return os.path.dirname(os.path.abspath(__file__))

def get_config_path():
	return os.path.join(get_script_dir(), CONFIG_FILE)

def load_config():
	with open(get_config_path(), "r", encoding="utf-8") as f:
		return json.load(f)

def write_log(content):
	log_path = os.path.join(get_script_dir(), LOG_FILE)
	with open(log_path, "a", encoding="utf-8") as f:
		f.write(content + "\n")

def print_name(config):
	name = config.get("name", "")
	if name:
		print(f"{name}:")

def list_models(config):
	url = config["base-url"]
	api_key = config["api-key"]
	api_type = config.get("api-type", "openai").lower()
	headers = {
		"Authorization": f"Bearer {api_key}",
		"Content-Type": "application/json"
	}
	if api_type != "openai":
		print(f"ERROR: Only openai protocol supported, got {api_type}")
		write_log(f"[{datetime.now().isoformat()}] ERROR: Only openai protocol supported, got {api_type}")
		return
	models_url = url.rstrip("/") + "/models"
	try:
		resp = requests.get(models_url, headers=headers, timeout=30)
		if resp.status_code == 200:
			data = resp.json()
			models = sorted([m["id"] for m in data.get("data", [])])
			for m in models:
				print(f"{m}")
			list_path = os.path.join(get_script_dir(), LIST_FILE)
			with open(list_path, "w", encoding="utf-8") as f:
				json.dump(models, f, ensure_ascii=False, indent=2)
		else:
			print("FAILED")
			write_log(f"[{datetime.now().isoformat()}] ERROR: List models failed, status: {resp.status_code}, body: {resp.text}")
	except Exception as e:
		print("FAILED")
		write_log(f"[{datetime.now().isoformat()}] ERROR: List models exception: {e}")

def test_model(model_name, config, results=None):
	url = config["base-url"]
	api_key = config["api-key"]
	api_type = config.get("api-type", "openai").lower()
	headers = {
		"Authorization": f"Bearer {api_key}",
		"Content-Type": "application/json"
	}
	if api_type != "openai":
		print(f"ERROR: Only openai protocol supported, got {api_type}")
		write_log(f"[{datetime.now().isoformat()}] ERROR: Only openai protocol supported, got {api_type}")
		return
	payload = {
		"model": model_name,
		"messages": [{"role": "user", "content": "Hello, test speed."}],
		"temperature": 0.5,
		"top_p": 1,
		"max_tokens": 32
	}

	start = time.time()
	chat_url = url.rstrip("/") + "/chat/completions"
	try:
		resp = requests.post(chat_url, headers=headers, json=payload, timeout=60)
		elapsed = time.time() - start
		if resp.status_code == 200:
			print(f"{model_name.ljust(65)} OK\t{elapsed:.2f}s")
			if results is not None:
				results.append({"model": model_name, "status": "OK", "time": round(elapsed, 2)})
		else:
			print(f"{model_name.ljust(65)} FAILED")
			if results is not None:
				results.append({"model": model_name, "status": "FAILED", "code": resp.status_code})
			write_log(f"[{datetime.now().isoformat()}] ERROR: Test model {model_name} failed, status: {resp.status_code}, body: {resp.text}")
	except Exception as e:
		print(f"{model_name.ljust(65)} FAILED\t{e}")
		if results is not None:
			results.append({"model": model_name, "status": "FAILED", "error": str(e)})
		write_log(f"[{datetime.now().isoformat()}] ERROR: Test model {model_name} exception: {e}")

def load_models():
	list_path = os.path.join(get_script_dir(), LIST_FILE)
	if not os.path.exists(list_path):
		return []
	with open(list_path, "r", encoding="utf-8") as f:
		return json.load(f)

def test_all(config):
	models = load_models()
	if not models:
		print("ERROR: No models found, run 'python tester.py list' first")
		write_log(f"[{datetime.now().isoformat()}] ERROR: No models found, run list first")
		return
	results = []
	for model in models:
		test_model(model, config, results)
	results.sort(key=lambda r: r.get("time", float("inf")))
	test_path = os.path.join(get_script_dir(), TEST_FILE)
	with open(test_path, "w", encoding="utf-8") as f:
		json.dump(results, f, ensure_ascii=False, indent=2)

def init_config():
	config_path = get_config_path()
	if os.path.exists(config_path):
		print(f"ERROR: {CONFIG_FILE} already exists at {config_path}")
		write_log(f"[{datetime.now().isoformat()}] ERROR: Config file already exists")
		return
	template = {
		"name": "Your API Name",
		"api-type": "openai",
		"base-url": "https://api.example.com/v1",
		"api-key": "your-api-key-here"
	}
	with open(config_path, "w", encoding="utf-8") as f:
		json.dump(template, f, ensure_ascii=False, indent=2)
	print(f"Created {CONFIG_FILE} at {config_path}")
	write_log(f"[{datetime.now().isoformat()}] INFO: Created new config file")

def print_help():
	name = sys.argv[0]
	if getattr(sys, "frozen", False):
		name = os.path.basename(sys.executable)
	print(f"Usage: {name} list | test [model ...]")
	print("")
	print("Commands:")
	print("  init           Generate a config.json template")
	print("  list           List available models")
	print("  test           Test all models from list.json")
	print("  test <model>   Test specific model(s), space-separated")

def print_version():
	print(f"tester {VERSION}")

def main():
	if len(sys.argv) < 2:
		print_help()
		return
	cmd = sys.argv[1]
	if cmd in ("-h", "--help"):
		print_help()
		return
	if cmd in ("-v", "--version"):
		print_version()
		return
	if cmd == "init":
		init_config()
		return
	config = load_config()
	if cmd == "list":
		print_name(config)
		list_models(config)
	elif cmd == "test":
		print_name(config)
		if len(sys.argv) > 2:
			for model in sys.argv[2:]:
				test_model(model, config)
		else:
			test_all(config)
	else:
		print_help()

if __name__ == "__main__":
	main()
