#!/usr/bin/env python
# coding: utf-8

import os
from pathlib import Path
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
nb_path = os.path.join(HERE, "src", "servequery", "nbextension", "static")

# Targets for JS build
jstargets = [
    os.path.join(nb_path, "index.js"),
]

package_data_spec = {
    "servequery": [
        "nbextension/static/*.*js*",
        "nbextension/static/*.*woff2*",
        "legacy/ui/assets/*",
        "legacy/ui/assets/static/css/*",
        "legacy/ui/assets/static/js/*",
        "legacy/ui/assets/static/img/*",
        "ui/service/assets/*",
        "ui/service/assets/static/css/*",
        "ui/service/assets/static/js/*",
        "ui/service/assets/static/img/*",
    ]
}

data_files_spec = [
    ("share/jupyter/nbextensions/servequery", nb_path, "*.js*"),
    ("share/jupyter/nbextensions/servequery", nb_path, "*.woff2"),
    ("etc/jupyter/nbconfig/notebook.d", HERE, "servequery.json"),
]

# Custom command to handle JS dependencies
def install_npm(path, build_cmd="build"):
    def _install(self):
        os.system(f"cd {path} && npm {build_cmd}")
    return _install

def ensure_targets(targets):
    def _ensure(self):
        for target in targets:
            if not os.path.exists(target):
                raise ValueError(f"Target {target} does not exist")
    return _ensure

from setuptools.command.develop import develop

class JSCommand(develop):
    def run(self):
        install_npm(os.path.join(HERE, "ui"), build_cmd="build")(self)
        ensure_targets(jstargets)(self)

setup(
    name="servequery",
    version="0.1.0",
    description="An open-source ML & LLM observability platform",
    author="Your Name",
    author_email="support@servequery.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "plotly>=5.10.0,<6",
        "statsmodels>=0.12.2",
        "scikit-learn>=1.0.1",
        "pandas[parquet]>=1.3.5",
        "numpy>=1.22.0",
        "nltk>=3.6.7",
        "scipy>=1.10.0",
        "requests>=2.32.0",
        "PyYAML>=5.4",
        "pydantic>=1.10.16",
        "litestar>=2.8.3",
        "typing-inspect>=0.9.0",
        "uvicorn[standard]>=0.22.0",
        "watchdog>=3.0.0",
        "typer>=0.3",
        "rich>=13",
        "iterative-telemetry>=0.0.5",
        "dynaconf>=3.2.4",
        "certifi>=2024.7.4",
        "urllib3>=1.26.19",
        "fsspec>=2024.6.1",
        "ujson>=5.4.0",
        "deprecation>=2.1.0",
        "uuid6>=2024.7.10",
        "cryptography>=43.0.1",
    ],
    extras_require={
        "dev": [
            "pip-audit>=2.7.2",
            "wheel==0.38.1",
            "setuptools==65.5.1; python_version < '3.12'",
            "setuptools==68.2.2; python_version >= '3.12'",
            "jupyter==1.0.0",
            "mypy==1.1.1",
            "pandas-stubs>=1.3.5",
            "pytest==7.4.4",
            "types-PyYAML==6.0.1",
            "types-requests==2.26.0",
            "types-dataclasses==0.6",
            "types-python-dateutil==2.8.19",
            "types-ujson>=5.4.0",
            "pillow>=10.3.0",
            "httpx==0.27.0",
            "ruff==0.3.7",
            "pre-commit==3.5.0",
            "pytest-asyncio==0.23.7",
            "pytest-mock==3.14.0",
        ],
        "llm": [
            "openai>=1.16.2",
            "evaluate>=0.4.1",
            "transformers[torch]>=4.39.3",
            "sentence-transformers>=2.7.0",
            "sqlvalidator>=0.0.20",
            "litellm>=1.60.4",
        ],
        "spark": [
            "pyspark>=3.4.0,<4",
        ],
        "fsspec": [
            "s3fs>=2024.9.0",
            "gcsfs>=2024.9.0",
        ],
    },
    entry_points={"console_scripts": ["servequery=servequery.cli:app"]},
    long_description=(Path(__file__).parent / "README.md").read_text("utf8"),
    long_description_content_type="text/markdown",
    cmdclass={"jsdeps": JSCommand},
)