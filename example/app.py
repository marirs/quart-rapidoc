import os

from quart import Quart
from quart_rapidoc import Rapidoc

cwd = os.path.dirname(os.path.relpath(__file__))

conf = {
    "allow-server-selection": True,
    "allow-try": True,
    "theme": "dark",
    "show-header": False,
    "schema-description-expanded": True,
    "default-schema-tab": "example",
    "schema-style": "table",
    "render-style": "view",
    "nav-item-spacing": "compact",
}

app = Quart(__name__)
app.config['DOC_FILE'] = os.path.join(cwd, 'petstore.yml')
app.config['RAPIDOC_CONFIG'] = conf
app.url_map.strict_slashes = False
redoc = Rapidoc(app)


@app.route('/')
def index():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
