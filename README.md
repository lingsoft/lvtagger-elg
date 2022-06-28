# ELG API for LV Tagger – Latvian morphological tagger and named entity recognition module

This git repository contains [ELG compatible](https://european-language-grid.readthedocs.io/en/stable/all/A3_API/LTInternalAPI.html) Flask based REST API for [LV Tagger](https://github.com/PeterisP/LVTagger) – morphological tagger and named entity recognition module for the Latvian language (v. 2.2.1). LV Tagger is licensed under the [full GPL](https://github.com/PeterisP/LVTagger/blob/master/LICENSE.txt). The software was developed by Pēteris Paikens from the University of Latvia, Institute of Mathematics and Computer science.

You can call two endpoints: `tagger` and `ner`. `tagger` groups tokens by their part of speech, which is the first letter of the morphological tag, shows their starting and ending indexes, lemma ('Pamatforma') and other morphological information depending on the part of speech (e.g. 'Skaitlis' (number), 'Locījums' (case), 'Dzimte' (gender), etc.) `ner` groups tokens by their named entity label (person, organization, location, event, product, profession) and shows their starting and ending indexes.

This ELG API was developed in EU's CEF project [Microservices at your service](https://www.lingsoft.fi/en/microservices-at-your-service-bridging-gap-between-nlp-research-and-industry).

## Obtaining the jar

Download [tagger-2.2.1-jar-with-dependencies.jar](https://search.maven.org/remotecontent?filepath=lv/ailab/morphology/tagger/2.2.1/tagger-2.2.1-jar-with-dependencies.jar) or build using Maven from the [source](https://github.com/PeterisP/LVTagger) and copy the jar to the project directory.

## Local development

Setup virtualenv, dependencies
```
python -m venv spacy-lt-elg-venv
source spacy-lt-elg-venv/bin/activate
python -m pip install -r requirements.txt
```

Run the development mode flask app
```
FLASK_ENV=development flask run --host 0.0.0.0 --port 8000
```

## Building the docker image

```
docker build -t lvtagger .
```

Or pull directly ready-made image `docker pull lingsoft/lvtagger:2.2.1-elg`.

## Deploying the service

```
docker run -d -p <port>:8000 --init --memory="2g" --restart always lvtagger
```

## Example call

```
curl -H "Content-Type: application/json" -d @text-request.json -X POST http://localhost:<port>/process/<endpoint_name>
```
`endpoint_name` can be `tagger` or `ner`. 


### Text request

```
{
    "type": "text",
    "content": text to be analyzed
}
```

### Response

Tagger

```
{
  "response": {
    "type": "annotations",
    "annotations": {
      "<POS tag>": [ // list of tokens that were recognized
        {
          "start":number,
          "end":number,
          "features": {"Pamatforma": str, …}
        },
      ],
    }
  }
}
```

NER

```
{
  "response": {
    "type": "annotations",
    "annotations": {
      "<NER label>": [ // list of tokens that were recognized
        {
          "start":number,
          "end":number
        },
      ],
    }
  }
}
```
