#!/usr/bin/env python3
"""
PRC Setup Verification Script

Run this script to verify that all components are properly configured.
Usage: python verify_setup.py
"""

import subprocess
import sys
from pathlib import Path

def check_command(cmd: str, name: str) -> bool:
    """Check if a command is available."""
    try:
        result = subprocess.run(
            [cmd, "--version"] if cmd != "checkov" else [cmd, "-v"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def check_python_module(module: str) -> bool:
    """Check if a Python module is installed."""
    try:
        __import__(module)
        return True
    except ImportError:
        return False

def main():
    print("=" * 60)
    print("PRC Setup Verification")
    print("=" * 60)

    # Check Python version
    print(f"\nPython Version: {sys.version}")
    if sys.version_info < (3, 9):
        print("  [WARNING] Python 3.9+ is recommended")
    else:
        print("  [OK] Python version is compatible")

    # Check required Python packages
    print("\n--- Required Python Packages ---")
    required_packages = [
        ("click", "click"),
        ("rich", "rich"),
    ]

    for package_name, import_name in required_packages:
        if check_python_module(import_name):
            print(f"  [OK] {package_name} installed")
        else:
            print(f"  [MISSING] {package_name} - install with: pip install {package_name}")

    # Check optional Python packages
    print("\n--- Optional Python Packages ---")
    optional_packages = [
        ("reportlab", "reportlab", "PDF report generation"),
        ("openai", "openai", "AI-powered insights"),
    ]

    for package_name, import_name, description in optional_packages:
        if check_python_module(import_name):
            print(f"  [OK] {package_name} - {description}")
        else:
            print(f"  [OPTIONAL] {package_name} - {description}")
            print(f"             Install with: pip install {package_name}")

    # Check external scanning tools
    print("\n--- External Scanning Tools ---")
    external_tools = [
        ("trivy", "Trivy", "Vulnerability scanner", "https://trivy.dev/latest/getting-started/installation/"),
        ("checkov", "Checkov", "IaC scanner", "pip install checkov"),
        ("gitleaks", "Gitleaks", "Secret detection", "https://github.com/gitleaks/gitleaks#installing"),
    ]

    tools_available = 0
    for cmd, name, description, install_info in external_tools:
        if check_command(cmd, name):
            print(f"  [OK] {name} - {description}")
            tools_available += 1
        else:
            print(f"  [NOT INSTALLED] {name} - {description}")
            print(f"                  Install: {install_info}")

    # Built-in scanner
    print("\n--- Built-in Scanner ---")
    print("  [ALWAYS AVAILABLE] Built-in Secret Scanner")
    print("                     Detects hardcoded passwords, API keys, K8s secrets")

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    if tools_available == 0:
        print("\n[INFO] No external tools installed.")
        print("       PRC will use the built-in secret scanner only.")
        print("       For comprehensive scanning, install Trivy, Checkov, or Gitleaks.")
    else:
        print(f"\n[OK] {tools_available} external tool(s) available + built-in scanner")

    # Check environment variables
    print("\n--- Environment Variables ---")
    import os
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print("  [OK] OPENAI_API_KEY is set (AI insights enabled)")
    else:
        print("  [NOT SET] OPENAI_API_KEY - AI insights will use fallback mode")
        print("            Set with: export OPENAI_API_KEY=your-key")

    print("\n" + "=" * 60)
    print("To run a scan:")
    print("  python -m src.cli.main scan /path/to/project")
    print("=" * 60)

if __name__ == "__main__":
    main()
