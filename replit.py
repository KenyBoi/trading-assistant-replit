run = "python main.py"
entrypoint = "main.py"
hidden = ["venv", ".config"]
modules = ["python-3.10"]

[nix]
channel = "stable-23_05"

[deployment]
run = ["python", "main.py"]
deploymentTarget = "cloudrun"

[[ports]]
localPort = 5000
externalPort = 80

[[ports]]
localPort = 8501
externalPort = 8501