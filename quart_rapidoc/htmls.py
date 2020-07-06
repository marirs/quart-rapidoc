"""Rapidoc Html Template."""


rapidoc_html = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{{title}}</title>
  <link href="https://fonts.googleapis.com/css2?family=Play&display=swap" rel="stylesheet">
</head>
<body>
  <rapi-doc id="rapidoc" spec-url = "{{openapi_url}}"
  {% for conf in config %}
   {{conf | safe}} 
  {% endfor %}
   allow-spec-url-load="false"
   allow-spec-file-load="false"
   regular-font="Play"
  > </rapi-doc>
  <script type="module" src="{{js}}"></script>
</body> 
</html>
"""