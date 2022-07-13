# ELG API for LV Tagger – Latvian morphological tagger and named entity recognition module

This git repository contains
[ELG compatible](https://european-language-grid.readthedocs.io/en/stable/all/A3_API/LTInternalAPI.html)
Flask based REST API for [LV Tagger](https://github.com/PeterisP/LVTagger) – morphological
tagger and named entity recognition module for the Latvian language (v. 2.2.1).
LV Tagger is licensed under the
[full GPL](https://github.com/PeterisP/LVTagger/blob/master/LICENSE.txt).
The software was developed by Pēteris Paikens from the University of Latvia,
Institute of Mathematics and Computer science.

You can call two endpoints: `tagger` and `ner`.
`tagger` groups tokens by their part of speech, which is the first letter of
the morphological tag, shows their starting and ending indexes, lemma ('Pamatforma')
and other morphological information depending on the part of speech
(e.g. 'Skaitlis' (number), 'Locījums' (case), 'Dzimte' (gender), etc).
`ner` groups tokens by their named entity label (person, organization, location,
event, product, profession) and shows their starting and ending indexes.

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
docker build -t lvtagger .
```

Or pull directly ready-made image `docker pull lingsoft/lvtagger:2.2.1-elg`.

## Deploying the service

```
docker run -d -p <port>:8000 --init lvtagger
```

## Example call

```
curl -X POST -H 'Content-Type: application/json' http://localhost:8000/process/<endpoint> -d '{"type":"text","content":"Sofija dzīvo Rīgā."}'
```

`endpoint` can be `tagger` or `ner`.

### Response

Tagger

```json
{
  "response": {
    "type": "annotations",
    "annotations": {
      "n": [
        {
          "start": 0,
          "end": 6,
          "features": {
            "tag1": "npfsn_",
            "tag2": "npfsn4",
            "Īpašvārda_veids": "Priekšvārds",
            "Skaitlis": "Vienskaitlis",
            "Vārds": "Sofija",
            "Leksēmas_nr": "1034177",
            "Skaits": "5422",
            "Lietvārda_tips": "Īpašvārds",
            "Pamatforma": "Sofija",
            "Galotnes_nr": "75",
            "Avots": "VVC_paplašinātais_vārdadienu_saraksts_2014-10-31",
            "Nobīde_rindkopā": "0",
            "Vārdšķira": "Lietvārds",
            "Mija": "0",
            "Minēšana": "Nav",
            "Lielo_burtu_lietojums": "Sākas_ar_lielo_burtu",
            "Locījums": "Nominatīvs",
            "Dzimte": "Sieviešu",
            "Vārdgrupas_nr": "7",
            "Deklinācija": "4"
          }
        },
        {
          "start": 13,
          "end": 17,
          "features": {
            "tag1": "npfsl_",
            "tag2": "npfsl4",
            "Īpašvārda_veids": "Vietvārds",
            "Skaitlis": "Vienskaitlis",
            "Vārds": "Rīgā",
            "Leksēmas_nr": "1101861",
            "Lietvārda_tips": "Īpašvārds",
            "Atstarpes_pirms": "_",
            "Pamatforma": "Rīga",
            "Galotnes_nr": "79",
            "Avots": "LĢIS",
            "Nobīde_rindkopā": "13",
            "Vārdšķira": "Lietvārds",
            "Mija": "0",
            "Minēšana": "Nav",
            "Lielo_burtu_lietojums": "Sākas_ar_lielo_burtu",
            "Locījums": "Lokatīvs",
            "Dzimte": "Sieviešu",
            "Vārdgrupas_nr": "7",
            "Deklinācija": "4"
          }
        }
      ],
      "v": [
        {
          "start": 7,
          "end": 12,
          "features": {
            "tag1": "vm_ip__30__",
            "tag2": "vmnipi230an",
            "Laiks": "Tagadne",
            "Konjugācija": "2",
            "Skaitlis": "Nepiemīt",
            "Šķirkļa_ID": "79002",
            "Vārds": "dzīvo",
            "Persona": "3",
            "Darbības_vārda_tips": "Patstāvīgs_darbības_vārds",
            "Šķirkļa_cilvēklasāmais_ID": "dzīvot:1",
            "Atgriezeniskums": "Nē",
            "Leksēmas_nr": "81176",
            "Atstarpes_pirms": "_",
            "Pamatforma": "dzīvot",
            "FreeText": "-oju,_-o,_-o,_pag._-oju;_intrans.",
            "Galotnes_nr": "228",
            "Noliegums": "Nē",
            "Transitivitāte": "Intransitīvs",
            "Nobīde_rindkopā": "7",
            "Vārdšķira": "Darbības_vārds",
            "Mija": "0",
            "Minēšana": "Nav",
            "Vārdgrupas_nr": "16",
            "Izteiksme": "Īstenības",
            "Kārta": "Darāmā"
          }
        }
      ],
      "z": [
        {
          "start": 17,
          "end": 18,
          "features": {
            "tag1": "zs",
            "tag2": "zs",
            "Galotnes_nr": "2092",
            "Vārds": ".",
            "Nobīde_rindkopā": "17",
            "Vārdšķira": "Pieturzīme",
            "Pieturzīmes_tips": "Punkts",
            "Mija": "0",
            "Minēšana": "Nav",
            "Vārdgrupas_nr": "37",
            "Leksēmas_nr": "1101217",
            "Pamatforma": "."
          }
        }
      ]
    }
  }
}
```

NER

```json
{
  "response": {
    "type": "annotations",
    "annotations": {
      "location": [
        {
          "start": 0,
          "end": 6
        },
        {
          "start": 13,
          "end": 17
        }
      ]
    }
  }
}
```

## Warning

Some characters (e.g. smileys) are not supported and may result into incorrect output. 
