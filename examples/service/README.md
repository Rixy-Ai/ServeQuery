# ServeQuery UI Demo: Remote Project Example

This example demonstrates how to run an **ServeQuery UI service** and connect to it remotely to upload and monitor a demo project using ServeQuery's Python API.

---

## 📦 Contents

- `run_service.sh` — Script to start the ServeQuery UI service in Docker.
- `remote_demo_project.py` — Python script that uploads a demo bike rentals monitoring project to the running ServeQuery service.
- `workspace_tutorial.ipynb` — Jupyter notebook with ServeQuery UI API tutorial
- `README.md` — (this file) instructions on how to set up and run the example.

---

## 🚀 How to Run the ServeQuery UI Service

You have two options for running the ServeQuery UI service:

### 🔸 Option 1: Using Docker (recommended)

1. Make sure you have [Docker](https://www.docker.com/get-started) installed.
2. Run the service using the provided script:

```bash
bash run_service.sh
```

This will start the ServeQuery UI at:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### 🔸 Option 2: Run Locally without Docker

Alternatively, you can start the ServeQuery UI service directly in your terminal (if ServeQuery is installed in your Python environment):

```bash
servequery ui
```

The service will be available at:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📊 Upload the Demo Project

Once the UI service is running, you can upload a demo project by running:

```bash
python remote_demo_project.py
```

This script will:

- Connect to the ServeQuery service at `http://127.0.0.1:8000`
- Create a sample project for bike rental monitoring
- Upload a few simulated data runs
- Add a dashboard panel to visualize metrics

You can then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to explore the project and its reports.

---

## 📚 More Information

For detailed documentation and configuration options, visit:  
[ServeQuery AI Documentation](https://docs.servequery.com)

---

## ✅ Requirements

- Python 3.8+
- `servequery` Python package  
  Install it via:

```bash
pip install servequery
```

- (Optional) Docker, if using the Docker-based option.

---

Enjoy exploring your
