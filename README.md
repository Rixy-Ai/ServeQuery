<h1 align="center">ServeQuery</h1>

<p align="center"><b>An open-source framework to evaluate, test and monitor ML and LLM-powered systems.</b></p>

# :bar_chart: What is ServeQuery?

ServeQuery is an open-source Python library to evaluate, test, and monitor ML and LLM systems—from experiments to production.

* 🔡 Works with tabular and text data.
* ✨ Supports evals for predictive and generative tasks, from classification to RAG.
* 📚 100+ built-in metrics from data drift detection to LLM judges.
* 🛠️ Python interface for custom metrics.
* 🚦 Both offline evals and live monitoring.
* 💻 Open architecture: easily export data and integrate with existing tools.

ServeQuery is very modular. You can start with one-off evaluations or host a full monitoring service.

## 1. Reports and Test Suites

**Reports** compute and summarize various data, ML and LLM quality evals.

* Start with Presets and built-in metrics or customize.
* Best for experiments, exploratory analysis and debugging.
* View interactive Reports in Python or export as JSON, Python dictionary, HTML, or view in monitoring UI.

Turn any Report into a **Test Suite** by adding pass/fail conditions.

* Best for regression testing, CI/CD checks, or data validation.
* Zero setup option: auto-generate test conditions from the reference dataset.
* Simple syntax to set test conditions as `gt` (greater than), `lt` (less than), etc.

| Reports |

## 2. Monitoring Dashboard

**Monitoring UI** service helps visualize metrics and test results over time.

# :woman_technologist: Install ServeQuery

To install from PyPI:

```sh
pip install servequery
```

To install ServeQuery using conda installer, run:

```sh
conda install -c conda-forge servequery
```

# :arrow_forward: Getting started

## Reports

### LLM evals

Import the necessary components:

```python
import pandas as pd
from servequery import Report
from servequery import Dataset, DataDefinition
from servequery.descriptors import Sentiment, TextLength, Contains
from servequery.presets import TextEvals
```

Create a toy dataset with questions and answers.

```python
eval_df = pd.DataFrame([
    ["What is the capital of Japan?", "The capital of Japan is Tokyo."],
    ["Who painted the Mona Lisa?", "Leonardo da Vinci."],
    ["Can you write an essay?", "I'm sorry, but I can't assist with homework."]],
                       columns=["question", "answer"])
```

Create an ServeQuery Dataset object and add `descriptors`: row-level evaluators. We'll check for sentiment of each response, its length and whether it contains words indicative of denial.

```python
eval_dataset = Dataset.from_pandas(pd.DataFrame(eval_df),
data_definition=DataDefinition(),
descriptors=[
    Sentiment("answer", alias="Sentiment"),
    TextLength("answer", alias="Length"),
    Contains("answer", items=['sorry', 'apologize'], mode="any", alias="Denials")
])
```

You can view the dataframe with added scores:

```python
eval_dataset.as_dataframe()
```

To get a summary Report to see the distribution of scores:

```python
report = Report([
    TextEvals()
])

my_eval = report.run(eval_dataset)
my_eval
# my_eval.json()
# my_eval.dict()
```

You can also choose other evaluators, including LLM-as-a-judge and configure pass/fail conditions.

### Data and ML evals

Import the Report, evaluation Preset and toy tabular dataset.

```python
import pandas as pd
from sklearn import datasets

from servequery import Report
from servequery.presets import DataDriftPreset

iris_data = datasets.load_iris(as_frame=True)
iris_frame = iris_data.frame
```

Run the **Data Drift** evaluation preset that will test for shift in column distributions. Take the first 60 rows of the dataframe as "current" data and the following as reference.  Get the output in Jupyter notebook:

```python
report = Report([
    DataDriftPreset(method="psi")
],
include_tests="True")
my_eval = report.run(iris_frame.iloc[:60], iris_frame.iloc[60:])
my_eval
```

You can also save an HTML file. You'll need to open it from the destination folder.

```python
my_eval.save_html("file.html")
```

To get the output as JSON or Python dictionary:

```python
my_eval.json()
# my_eval.dict()
```

You can choose other Presets, create Reports from indiviudal Metrics and configure pass/fail conditions.

## Monitoring dashboard

Recommended step: create a virtual environment and activate it.

```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

After installing ServeQuery (`pip install servequery`), run the ServeQuery UI with the demo projects:

```
servequery ui --demo-projects all
```

Visit **localhost:8000** to access the UI.

# 🚦 What can you evaluate?

ServeQuery has 100+ built-in evals. You can also add custom ones.

Here are examples of things you can check:

|                           |                          |
|:-------------------------:|:------------------------:|
| **🔡 Text descriptors**   | **📝 LLM outputs**       |
| Length, sentiment, toxicity, language, special symbols, regular expression matches, etc. | Semantic similarity, retrieval relevance, summarization quality, etc. with model- and LLM-based evals. |
| **🛢 Data quality**       | **📊 Data distribution drift** |
| Missing values, duplicates, min-max ranges, new categorical values, correlations, etc. | 20+ statistical tests and distance metrics to compare shifts in data distribution. |
| **🎯 Classification**     | **📈 Regression**        |
| Accuracy, precision, recall, ROC AUC, confusion matrix, bias, etc. | MAE, ME, RMSE, error distribution, error normality, error bias, etc. |
| **🗂 Ranking (inc. RAG)** | **🛒 Recommendations**   |
| NDCG, MAP, MRR, Hit Rate, etc. | Serendipity, novelty, diversity, popularity bias, etc. |
