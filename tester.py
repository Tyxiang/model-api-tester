#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import json
import time
import argparse
import csv
import requests
from datetime import datetime

CONFIG_FILE = "config.json"
LIST_FILE = "list.csv"
TEST_FILE = "test.csv"
LOG_FILE = "tester.log"
VERSION = "1.6.3"

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
	
	if api_type == "gemini":
		gemini_base = url.rstrip("/")
		if "googleapis.com" in gemini_base:
			models_url = f"{gemini_base}?key={api_key}"
		else:
			models_url = f"{gemini_base}/models?key={api_key}"
		try:
			resp = requests.get(models_url, timeout=30)
			if resp.status_code == 200:
				data = resp.json()
				models = sorted([m["name"].replace("models/", "") for m in data.get("models", [])])
				for m in models:
					print(f"{m}")
				list_path = os.path.join(get_script_dir(), LIST_FILE)
				with open(list_path, "w", encoding="utf-8") as f:
					f.write("\n".join(models))
			else:
				print("FAILED")
				write_log(f"[{datetime.now().isoformat()}] ERROR: List models failed, status: {resp.status_code}, body: {resp.text}")
		except Exception as e:
			print("FAILED")
			write_log(f"[{datetime.now().isoformat()}] ERROR: List models exception: {e}")
		return
	
	if api_type == "anthropic":
		anthropic_base = url.rstrip("/")
		models_url = f"{anthropic_base}/models"
		headers = {
			"x-api-key": api_key,
			"anthropic-version": "2023-06-01"
		}
		try:
			resp = requests.get(models_url, headers=headers, timeout=30)
			if resp.status_code == 200:
				data = resp.json()
				models = sorted([m["id"] for m in data.get("data", [])])
				for m in models:
					print(f"{m}")
				list_path = os.path.join(get_script_dir(), LIST_FILE)
				with open(list_path, "w", encoding="utf-8") as f:
					f.write("\n".join(models))
			else:
				print("FAILED")
				write_log(f"[{datetime.now().isoformat()}] ERROR: List models failed, status: {resp.status_code}, body: {resp.text}")
		except Exception as e:
			print("FAILED")
			write_log(f"[{datetime.now().isoformat()}] ERROR: List models exception: {e}")
		return
	
	if api_type == "anthropic":
		anthropic_base = url.rstrip("/")
		models_url = f"{anthropic_base}/models"
		headers = {
			"x-api-key": api_key,
			"anthropic-version": "2023-06-01"
		}
		try:
			resp = requests.get(models_url, headers=headers, timeout=30)
			if resp.status_code == 200:
				data = resp.json()
				models = sorted([m["id"] for m in data.get("data", [])])
				for m in models:
					print(f"{m}")
				list_path = os.path.join(get_script_dir(), LIST_FILE)
				with open(list_path, "w", encoding="utf-8") as f:
					f.write("\n".join(models))
			else:
				print("FAILED")
				write_log(f"[{datetime.now().isoformat()}] ERROR: List models failed, status: {resp.status_code}, body: {resp.text}")
		except Exception as e:
			print("FAILED")
			write_log(f"[{datetime.now().isoformat()}] ERROR: List models exception: {e}")
		return
	
	headers = {
		"Authorization": f"Bearer {api_key}",
		"Content-Type": "application/json"
	}
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
				f.write("\n".join(models))
		else:
			print("FAILED")
			write_log(f"[{datetime.now().isoformat()}] ERROR: List models failed, status: {resp.status_code}, body: {resp.text}")
	except Exception as e:
		print("FAILED")
		write_log(f"[{datetime.now().isoformat()}] ERROR: List models exception: {e}")

def test_model(model_name, config, csv_file=None):
	url = config["base-url"]
	api_key = config["api-key"]
	api_type = config.get("api-type", "openai").lower()
	
	status = "FAILED"
	time_val = ""
	
	if api_type == "gemini":
		gemini_base = url.rstrip("/")
		gemini_url = f"{gemini_base}/{model_name}:generateContent?key={api_key}"
		payload = {
			"contents": [{"parts": [{"text": "Hello, test speed."}]}],
			"generationConfig": {
				"temperature": 0.5,
				"topP": 1,
				"maxOutputTokens": 32
			}
		}
		start = time.time()
		try:
			resp = requests.post(gemini_url, headers={"Content-Type": "application/json"}, json=payload, timeout=60)
			elapsed = time.time() - start
			if resp.status_code == 200:
				print(f"{model_name.ljust(65)} OK\t{elapsed:.2f}s")
				status = "OK"
				time_val = round(elapsed, 2)
			else:
				print(f"{model_name.ljust(65)} FAILED")
				write_log(f"[{datetime.now().isoformat()}] ERROR: Test model {model_name} failed, status: {resp.status_code}, body: {resp.text}")
		except Exception as e:
			print(f"{model_name.ljust(65)} FAILED")
			write_log(f"[{datetime.now().isoformat()}] ERROR: Test model {model_name} exception: {e}")
	
	elif api_type == "anthropic":
		anthropic_base = url.rstrip("/")
		anthropic_url = f"{anthropic_base}/messages"
		headers = {
			"x-api-key": api_key,
			"anthropic-version": "2023-06-01",
			"Content-Type": "application/json"
		}
		payload = {
			"model": model_name,
			"max_tokens": 32,
			"messages": [{"role": "user", "content": "Hello, test speed."}]
		}
		start = time.time()
		try:
			resp = requests.post(anthropic_url, headers=headers, json=payload, timeout=60)
			elapsed = time.time() - start
			if resp.status_code == 200:
				print(f"{model_name.ljust(65)} OK\t{elapsed:.2f}s")
				status = "OK"
				time_val = round(elapsed, 2)
			else:
				print(f"{model_name.ljust(65)} FAILED")
				write_log(f"[{datetime.now().isoformat()}] ERROR: Test model {model_name} failed, status: {resp.status_code}, body: {resp.text}")
		except Exception as e:
			print(f"{model_name.ljust(65)} FAILED")
			write_log(f"[{datetime.now().isoformat()}] ERROR: Test model {model_name} exception: {e}")
	
	else:
		headers = {
			"Authorization": f"Bearer {api_key}",
			"Content-Type": "application/json"
		}
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
				status = "OK"
				time_val = round(elapsed, 2)
			else:
				print(f"{model_name.ljust(65)} FAILED")
				write_log(f"[{datetime.now().isoformat()}] ERROR: Test model {model_name} failed, status: {resp.status_code}, body: {resp.text}")
		except Exception as e:
			print(f"{model_name.ljust(65)} FAILED")
			write_log(f"[{datetime.now().isoformat()}] ERROR: Test model {model_name} exception: {e}")
	
	if csv_file:
		csv_file.write(f'{model_name},{status},{time_val}\n')
		csv_file.flush()

def load_models():
	list_path = os.path.join(get_script_dir(), LIST_FILE)
	if not os.path.exists(list_path):
		return []
	with open(list_path, "r", encoding="utf-8") as f:
		return [line.strip() for line in f if line.strip()]

def test_all(config, filter_status=None):
	models = load_models()
	if not models:
		print("ERROR: No models found, run 'tester list' first")
		write_log(f"[{datetime.now().isoformat()}] ERROR: No models found, run list first")
		return
	
	test_path = os.path.join(get_script_dir(), TEST_FILE)
	if os.path.exists(test_path):
		os.remove(test_path)
	
	with open(test_path, "w", encoding="utf-8") as f:
		f.write("model,status,time\n")
		for model in models:
			test_model(model, config, f)
	
	if filter_status:
		filter_status = filter_status.upper()
		results = []
		with open(test_path, "r", encoding="utf-8") as f:
			reader = csv.DictReader(f)
			results = [row for row in reader if row["status"].upper() == filter_status]
		with open(test_path, "w", encoding="utf-8") as f:
			f.write("model,status,time\n")
			for r in results:
				f.write(f'{r["model"]},{r["status"]},{r["time"]}\n')

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
	gemini_template = {
		"name": "Gemini API",
		"api-type": "gemini",
		"base-url": "https://generativelanguage.googleapis.com/v1beta/models",
		"api-key": "your-gemini-api-key-here"
	}
	anthropic_template = {
		"name": "Anthropic API",
		"api-type": "anthropic",
		"base-url": "https://api.anthropic.com/v1",
		"api-key": "your-anthropic-api-key-here"
	}
	print("Choose config template:")
	print("  1. OpenAI (default)")
	print("  2. Gemini")
	print("  3. Anthropic")
	choice = input("Enter choice [1/2/3]: ").strip()
	if choice == "2":
		with open(config_path, "w", encoding="utf-8") as f:
			json.dump(gemini_template, f, ensure_ascii=False, indent=2)
		print(f"Created {CONFIG_FILE} for Gemini at {config_path}")
	elif choice == "3":
		with open(config_path, "w", encoding="utf-8") as f:
			json.dump(anthropic_template, f, ensure_ascii=False, indent=2)
		print(f"Created {CONFIG_FILE} for Anthropic at {config_path}")
	else:
		with open(config_path, "w", encoding="utf-8") as f:
			json.dump(template, f, ensure_ascii=False, indent=2)
		print(f"Created {CONFIG_FILE} at {config_path}")
	write_log(f"[{datetime.now().isoformat()}] INFO: Created new config file")

def print_version():
	print(f"tester {VERSION}")

def main():
	parser = argparse.ArgumentParser(prog="tester", description="Model API Tester")
	parser.add_argument("-v", "--version", action="store_true", help="Show version")
	subparsers = parser.add_subparsers(dest="command", required=True)
	
	init_parser = subparsers.add_parser("init", help="Generate config.json template")
	
	list_parser = subparsers.add_parser("list", help="List available models")
	
	test_parser = subparsers.add_parser("test", help="Test models")
	test_parser.add_argument("-f", choices=["OK", "FAILED", "ok", "failed"], help="Filter results saved to test.csv")
	test_parser.add_argument("models", nargs="*", help="Specific model(s) to test")
	
	args = parser.parse_args()
	
	if args.version:
		print_version()
		return
	
	if args.command == "init":
		init_config()
		return
	
	config = load_config()
	
	if args.command == "list":
		print_name(config)
		list_models(config)
	elif args.command == "test":
		print_name(config)
		if args.models:
			for model in args.models:
				test_model(model, config)
		else:
			test_all(config, args.f)

if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1] in ("-v", "--version"):
		print_version()
	else:
		main()
