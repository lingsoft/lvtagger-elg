# ELG API for LV Tagger – Latvian morphological tagger

This git repository contains
[ELG compatible](https://european-language-grid.readthedocs.io/en/stable/all/A3_API/LTInternalAPI.html)
Flask based REST API for [LV Tagger](https://github.com/PeterisP/LVTagger) – a morphological
tagger for the Latvian language (v. 2.2.1).
LV Tagger is licensed under the
[full GPL](https://github.com/PeterisP/LVTagger/blob/master/LICENSE.txt).
The software was developed by Pēteris Paikens from the University of Latvia,
Institute of Mathematics and Computer science.

The tagger groups tokens by their part of speech, which is the first letter of
the morphological tag, shows their starting and ending indexes, lemma ('Pamatforma')
and other morphological information depending on the part of speech
(e.g. 'Skaitlis' (number), 'Locījums' (case), 'Dzimte' (gender), etc).

This ELG API was developed in EU's CEF project
[Microservices at your service](https://www.lingsoft.fi/en/microservices-at-your-service-bridging-gap-between-nlp-research-and-industry).

## Local development

Download [tagger-2.2.1-jar-with-dependencies.jar](https://search.maven.org/remotecontent?filepath=lv/ailab/morphology/tagger/2.2.1/tagger-2.2.1-jar-with-dependencies.jar)
or build using Maven from the [source](https://github.com/PeterisP/LVTagger)
and copy the jar to the project directory.

Setup virtualenv, dependencies
```
python -m venv lvtagger-venv
source lvtagger-venv/bin/activate
python -m pip install -r requirements.txt
```

Run the development mode flask app
```
FLASK_ENV=development flask run --host 0.0.0.0 --port 8000
```

## Building the docker image

```
docker build -t lv-tagger .
```

Or pull directly ready-made image `docker pull lingsoft/lv-tagger:2.2.1-elg`.

## Deploying the service

```
docker run -d -p <port>:8000 --init lv-tagger
```

## Example call

```
curl -H 'Content-Type: application/json' -d @sample.json http://localhost:8000/process/tagger
```

### sample.json

```json
{
    "type": "text",
    "content": "Mārtiņš Bondars ir dzimis 1971. gada 31. decembrī, Rīgā."
}
```

### Response

```json
{
  "response": {
    "type": "annotations",
    "annotations": {
      "n": [
        {
          "start": 0,
          "end": 7,
          "features": {
            "tag1": "npmsn_",
            "tag2": "npmsn1",
            "Īpašvārda_veids": "Priekšvārds",
            "Skaitlis": "Vienskaitlis",
            "Vārds": "Mārtiņš",
            "Leksēmas_nr": "1036923",
            "Skaits": "13954",
            "Lietvārda_tips": "Īpašvārds",
            "Pamatforma": "Mārtiņš",
            "Galotnes_nr": "14",
            "Avots": "VVC_paplašinātais_vārdadienu_saraksts_2014-10-31",
            "Nobīde_rindkopā": "0",
            "Vārdšķira": "Lietvārds",
            "Mija": "0",
            "Minēšana": "Nav",
            "Lielo_burtu_lietojums": "Sākas_ar_lielo_burtu",
            "Locījums": "Nominatīvs",
            "Dzimte": "Vīriešu",
            "Vārdgrupas_nr": "2",
            "Deklinācija": "1"
          }
        },
        ...
      ]
    }
  }
}
```

More information about
[part-of-speech tags](https://peteris.rocks/blog/latvian-part-of-speech-tagging/).

## Warning

Some characters (e.g. smileys) are not supported and may result into incorrect output. 
