# scripts/extract_diff.py
import subprocess
import requests
import os
import sys



def get_latest_diff():
    """Returns the latest commit hash and diff text"""
    commit_hash = subprocess.check_output(
        ["git", "rev-parse", "HEAD"]
    ).decode("utf-8").strip()

    diff = subprocess.check_output(
        ["git", "show", commit_hash, "--no-color"],
        stderr=subprocess.STDOUT
    ).decode("utf-8")

    return commit_hash, diff

def send_to_summarizer(commit_hash, diff):
    url = os.getenv("SUMMARIZER_URL")
    groq_api_key = os.getenv("GROQ_API_KEY")
    payload = {
        "commit_hash": commit_hash,
        "diff": diff ,
        "groq_api_key": groq_api_key
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Error:", response.text, file=sys.stderr)
        sys.exit(1)

    print("Summary:")
    print(response.json()["summary"])

if __name__ == "__main__":
    commit_hash, diff = get_latest_diff()
    send_to_summarizer(commit_hash, diff)
