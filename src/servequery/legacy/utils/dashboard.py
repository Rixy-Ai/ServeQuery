import base64
import dataclasses
import html
import json
import os
import shutil
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional

import servequery
from servequery.legacy.model.dashboard import DashboardInfo
from servequery.legacy.utils import NumpyEncoder

STATIC_PATH = os.path.join(servequery.__path__[0], "nbextension", "static")


class SaveMode(Enum):
    SINGLE_FILE = "singlefile"
    FOLDER = "folder"
    SYMLINK_FOLDER = "symlink_folder"


SaveModeMap = {v.value: v for v in SaveMode}


@dataclasses.dataclass()
class TemplateParams:
    dashboard_id: str
    dashboard_info: DashboardInfo
    additional_graphs: Dict
    embed_font: bool = True
    embed_lib: bool = True
    embed_data: bool = True
    font_file: Optional[str] = None
    include_js_files: List[str] = dataclasses.field(default_factory=list)


def save_lib_files(filename: str, mode: SaveMode):
    if mode == SaveMode.SINGLE_FILE:
        return None, None
    parent_dir = os.path.dirname(filename)
    if not os.path.exists(os.path.join(parent_dir, "js")):
        os.makedirs(os.path.join(parent_dir, "js"), exist_ok=True)
    font_file = os.path.join(parent_dir, "js", "material-ui-icons.woff2")
    lib_file = os.path.join(parent_dir, "js", f"servequery.{servequery.__version__}.js")

    if mode == SaveMode.SYMLINK_FOLDER:
        if os.path.exists(font_file):
            os.remove(font_file)
        os.symlink(os.path.join(STATIC_PATH, "material-ui-icons.woff2"), font_file)
        if os.path.exists(lib_file):
            os.remove(lib_file)
        os.symlink(os.path.join(STATIC_PATH, "index.js"), lib_file)
    else:
        shutil.copy(os.path.join(STATIC_PATH, "material-ui-icons.woff2"), font_file)
        shutil.copy(os.path.join(STATIC_PATH, "index.js"), lib_file)
    return font_file, lib_file


def save_data_file(
    filename: str,
    mode: SaveMode,
    dashboard_id,
    dashboard_info: DashboardInfo,
    additional_graphs: Dict,
):
    if mode == SaveMode.SINGLE_FILE:
        return None
    parent_dir = os.path.dirname(filename)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)
    base_name = os.path.basename(filename)
    data_file = os.path.join(parent_dir, "js", f"{base_name}.data.js")
    with open(data_file, "w", encoding="utf-8") as out_file:
        out_file.write(
            f"""
    var {dashboard_id} = {dashboard_info_to_json(dashboard_info)};
    var additional_graphs_{dashboard_id} = {json.dumps(additional_graphs, cls=NumpyEncoder)};"""
        )
    return data_file


def dashboard_info_to_json(dashboard_info: DashboardInfo):
    asdict_result = dashboard_info.dict()
    for widget in asdict_result["widgets"]:
        widget.pop("additionalGraphs", None)
    return json.dumps(asdict_result, cls=NumpyEncoder)


def file_html_template(params: TemplateParams):
    lib_block = f"""<script>{__load_js()}</script>""" if params.embed_lib else "<!-- no embedded lib -->"

    data_block = (
        f"""<script>
    var {params.dashboard_id} = {dashboard_info_to_json(params.dashboard_info)};
    var additional_graphs_{params.dashboard_id} = {json.dumps(params.additional_graphs, cls=NumpyEncoder)};
</script>"""
        if params.embed_data
        else "<!-- no embedded data -->"
    )

    js_files_block = "\n".join([f'<script src="{file}"></script>' for file in params.include_js_files])

    style = f"""
        <style>
        /* fallback */
        @font-face {{
        font-family: 'Material Icons';
        font-style: normal;
        font-weight: 400;
        src: {f"url(data:font/ttf;base64,{__load_font()}) format('woff2');" if params.embed_font else
            f"url({params.font_file});"}
        }}

        .center-align {{
        text-align: center;
        }}

        .material-icons {{
        font-family: 'Material Icons';
        font-weight: normal;
        font-style: normal;
        font-size: 24px;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        display: inline-block;
        white-space: nowrap;
        word-wrap: normal;
        direction: ltr;
        text-rendering: optimizeLegibility;
        -webkit-font-smoothing: antialiased;
        }}
        </style>
    """

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {style}
        {data_block}
    </head>
    <body>
    <div id="root_{params.dashboard_id}">
    </div>
    <script>var global = globalThis</script>
    {lib_block}
    {js_files_block}
    <script>
    window.drawDashboard({params.dashboard_id},
        new Map(Object.entries(additional_graphs_{params.dashboard_id})),
        "root_{params.dashboard_id}"
    );
    </script>

    </body>
    </html>
"""


def inline_iframe_html_template(params: TemplateParams):
    resize_script = """
        <script type="application/javascript">
            ;(function () {
              const main = () => {
                window.servequeryResizeTargetAndIframePair ??= []
                window.servequeryResizeObserver ??= createObserver()

                document.querySelectorAll('iframe.servequery-ui-iframe').forEach((iframe) => {
                  iframe.onload = () => {
                    const targetToObserveResize = iframe.contentWindow.document.body

                    window.servequeryResizeTargetAndIframePair.push([targetToObserveResize, iframe])
                    window.servequeryResizeObserver.observe(targetToObserveResize)
                  }
                })
              }

              const createObserver = () =>
                new ResizeObserver((entities) => {
                  for (const entity of entities) {
                    const resizeTargetAndIframePair = window.servequeryResizeTargetAndIframePair.find(
                      ([target]) => entity.target.isSameNode(target)
                    )

                    if (!resizeTargetAndIframePair) {
                      break
                    }

                    const [, iframe] = resizeTargetAndIframePair

                    const iframeHeight = iframe.contentWindow.document.body.scrollHeight
                    const newHeight = iframeHeight + 2.5

                    if (iframeHeight === 0 || Number(iframe.height) === newHeight) {
                      break
                    }

                    // set new height
                    iframe.height = newHeight
                  }
                })

              main()
            })()
        </script>
    """

    html_doc = file_html_template(params)

    return f"""
    {resize_script}
    <iframe class='servequery-ui-iframe' width="100%" frameborder="0" srcdoc="{html.escape(html_doc)}">
    """


def __load_js():
    with open(os.path.join(STATIC_PATH, "index.js"), encoding="utf-8") as f:
        return f.read()


def __load_font():
    with open(os.path.join(STATIC_PATH, "material-ui-icons.woff2"), "rb") as f:
        return base64.b64encode(f.read()).decode()
