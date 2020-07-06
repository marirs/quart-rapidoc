"""Quart-Rapidoc Module.

Description: Rapidoc docs for API documentation
Rapidocs: https://mrin9.github.io/RapiDoc/
Author: Sriram (https://github.com/marirs/
"""
import os
import json
import yaml

from quart import render_template_string, send_file, Blueprint

from .htmls import rapidoc_html


def parse_bool(val) -> str:
    """Parse a bool into string-ish bool - crazy; i know."""
    return str(val).lower() if isinstance(val, bool) else val


class Rapidoc(object):
    """Rapidoc object."""

    _doc_url: str = '/docs/'
    _jsfile_url: str = '/rapidoc-min.js'
    _js_url: str = 'https://unpkg.com/rapidoc/dist/rapidoc-min.js'
    _openapi_json_url: str = '/openapi.json'
    _openapi_json = {}
    _rapidoc_conf_dafaults = {
        "allow-server-selection": True,
        "allow-try": True,
        "theme": "dark",
        "show-header": False,
        "schema-description-expanded": True,
        "default-schema-tab": "example",
        "schema-style": "tree",
        "render-style": "read",
        "nav-item-spacing": "compact",
        "font-size": "default",
    }

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            app=None,
            doc_spec_file: str = None,
            doc_spec_json: json = None,
            doc_spec_yml: yaml = None,
            docs_url: str = None,
            use_jscdn: bool = False
    ):
        """Init the Rapidoc object."""
        self.app = app
        self.use_jscdn = use_jscdn
        if app is not None:
            self.init_app(
                app, doc_spec_file, doc_spec_json, doc_spec_yml, docs_url, use_jscdn
            )

    # pylint: disable=too-many-arguments
    def init_app(
            self,
            app,
            doc_spec_file: str = None,
            doc_spec_json: json = None,
            doc_spec_yml: yaml = None,
            docs_url: str = None,
            use_jscdn: bool = False
    ):
        """Initialize this :class:`Rapidoc` for use.

        In the following scenarios:
        1) if ``doc_endpoint`` is ``None``, pass the ``doc_endpoint`` and 
        any other positional keyword arguments. 
        2) if ``doc_endpoint`` is ``None`` and a Quart config variable named
           ``DOC_URL`` exists, use that as the ``doc_endpoint`` as above
        3) if ``doc_spec_file`` or ``doc_spec_json`` or ``doc_spec_yml`` is ``None`` and a Quart
        config variable named ``DOC_FILE`` or ``DOC_JSON`` or ``DOC_YML`` exists, use that appropriately
        4) use_jscdn is default where the rapidoc javascript is fetched from cdn
        5) use ``RAPIDOC_CONFIG`` dict in the config file to import configurations for rapidoc rendering
        The Config doc is available here: https://mrin9.github.io/RapiDoc/api.html
        :param app: Quart App
        :param doc_spec_file: openapi 3 spec from file
        :param doc_spec_json: openapi 3 spec from json
        :param doc_spec_yml: openapi 3 spec from yml
        :param docs_url: url/endpoint to serve the doc
        :param use_jscdn: use rapidoc javascript from cdn if not use local copy
        :return:
        """
        self.app = app
        self.use_jscdn = use_jscdn
        if not doc_spec_file:
            doc_spec_file = app.config.get('DOC_FILE', None)
            if doc_spec_file:
                if os.path.exists(doc_spec_file):
                    self._load_spec_file(doc_spec_file)
                else:
                    raise FileNotFoundError(
                        f"{doc_spec_file} not found!"
                    )
        if not doc_spec_json:
            doc_spec_json = app.config.get('DOC_JSON', None)
            if doc_spec_json:
                self._openapi_json = json.loads(doc_spec_json)
        if not doc_spec_yml:
            doc_spec_yml = app.config.get('DOC_YML', None)
            if doc_spec_yml:
                self._openapi_json = yaml.safe_load(doc_spec_yml)

        if not any([doc_spec_file, doc_spec_yml, doc_spec_json]):
            raise ValueError(
                "You must specify a DOC_FILE or DOC_JSON or DOC_YML in config or "
                "set them as Quart config variable",
            )
        rapidoc_conf = app.config.get('RAPIDOC_CONFIG', {})
        if isinstance(rapidoc_conf, dict):
            self._rapidoc_conf_dafaults.update(rapidoc_conf)
        else:
            raise ValueError(
                "RAPIDOC_CONFIG must be a dict!"
            )

        self._doc_url = docs_url or self._doc_url
        self._doc_url = self._doc_url.rstrip('/')

        doc_route = Blueprint('doc', __name__, url_prefix=self._doc_url)
        doc_route.add_url_rule('/', view_func=self.doc_view)
        doc_route.add_url_rule(self._openapi_json_url, view_func=self.openapi_view)
        if not use_jscdn:
            doc_route.add_url_rule(self._jsfile_url, view_func=self.jsfile_view)

        self.app.register_blueprint(doc_route)

    async def doc_view(self):
        """Render the HTML."""
        title = self._openapi_json.get('info', 'Api documentation')
        if isinstance(title, dict):
            title = title.get('title', 'Api documentation')
        config = [f'{k}="{parse_bool(v)}"' for k, v in self._rapidoc_conf_dafaults.items()]
        context = {
            "title": title,
            "js": self._js_url if self.use_jscdn else self._doc_url+self._jsfile_url,
            "openapi_url": self._doc_url+self._openapi_json_url,
            "config": config,
        }
        return await render_template_string(
            rapidoc_html, **context
        )

    async def openapi_view(self):
        """Render the openapi 3 json."""
        return self._openapi_json

    async def jsfile_view(self):
        """Render the Rapidoc Javascript file."""
        file = os.path.join(os.path.dirname(os.path.realpath(__file__)),  self._jsfile_url[1:])
        return await send_file(
            file,
            mimetype="text/javascript"
        )

    def _load_spec_file(self, filename):
        """Load the spec file.

        :param filename: spec file to read and load
        :return: none
        """
        if not filename.startswith('/'):
            filename = os.path.join(
                self.app.root_path,
                filename
            )
        with open(filename) as file:
            if filename.endswith(".yml") or filename.endswith(".yaml"):
                spec = yaml.safe_load(file)
            else:
                spec = json.load(file)

        self._openapi_json = spec

