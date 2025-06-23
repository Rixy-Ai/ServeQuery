from typer import Typer

app = Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.callback(no_args_is_help=True, invoke_without_command=True)
def servequery_callback():
    """\b
    ServeQuery is tool to help you evaluate, test and monitor your data and ML models.
    Documentation: https://docs.servequery.com
    """
