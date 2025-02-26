# bpmn-converter
convertion of .signavio-bpmn models (signavio academic) into .signavio-json, minimal json, yaml or mermaid.js.

bpmn\_shema\_helper.py and sapsam\_mapping.py are part of the 'llm-round-trip-correctness' implementation (see https://github.com/SAP-samples/llm-round-trip-correctness/).

Before using the service please go to /source and fill the .env\_template file with your data. Then, rename the file to .env.
To find your tenant ID (i.e., workspace ID) go to your signavio account, 'Help' (?) -> 'Workspace ID'.

To start the service locally:
cd bpmn-converter
pipenv install -r requirements.txt
cd source
pipenv run gunicorn -c gunicorn.cong.py run:app --daemon

to kill the service use:
netstat -antp | grep <PORT>
kill <PID>

to convert particula model use /model/<model\_format>?id=<model\_ID>, where:
model\_format: string, possible values: json, minijson, yaml, mermaid;
id: string, model id provided in signavio

to convert all models in a particular directory use /directory/<model\_format>?id=<directory\_ID>, where:
model\_format: string, possible values: json, minijson, yaml, mermaid;
id: string, directory id provided in signavio


