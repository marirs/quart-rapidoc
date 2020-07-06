import os
import json
import yaml
import pytest
from quart import Quart
from quart_rapidoc import Rapidoc


class TestQuartRapidoc:
    cwd = os.path.dirname(os.path.relpath(__file__))

    @pytest.mark.asyncio
    async def test_rapidoc_yml_file(self):
        app = Quart(__name__)
        client = app.test_client()
        Rapidoc(app, doc_spec_file='petstore.yml')
        resp = await client.get('/docs/')
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_rapidoc_json_file(self):
        app = Quart(__name__)
        client = app.test_client()
        Rapidoc(app, doc_spec_file='petstore.json')
        resp = await client.get('/docs/')
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_rapidoc_json_string(self):
        file = os.path.join(self.cwd, 'petstore.json')
        with open(file, 'r') as f:
            spec_json = json.load(f)
        app = Quart(__name__)
        client = app.test_client()
        Rapidoc(app, doc_spec_json=spec_json)
        resp = await client.get('/docs/')
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_rapidoc_yml_string(self):
        file = os.path.join(self.cwd, 'petstore.yml')
        with open(file, 'r') as f:
            spec_yml = yaml.safe_load(f)
        app = Quart(__name__)
        client = app.test_client()
        Rapidoc(app, doc_spec_json=spec_yml)
        resp = await client.get('/docs/')
        assert resp.status_code == 200

