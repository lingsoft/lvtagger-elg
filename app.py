from elg import FlaskService
from elg.model import AnnotationsResponse, TextsResponse
import subprocess
import io
import os
from os.path import exists

class LVTagger(FlaskService):
    
    def convert_outputs(self, outputs, content, endpoint, incorrect_result):
        if endpoint in ["word_analysis", "wordforms"]:
            texts = []
            lines = [x for x in outputs.split("\n") if x != ""]
            groups = []
            group = []
            for line in lines:
                if line.startswith("\t\t"):
                    group.append(line[2:]) # this is morpho-feature
                elif group == []:
                    group.append(line[1:]) # this is the first tag
                else:
                    groups.append(group)
                    group = [line[1:]] # this is the next tag 
            groups.append(group)
            for group in groups:
                feature_dict = {}
                for x in group[1:]: # the first element is tag
                    [k,v] = x.split(" = ")
                    if v != "":
                        feature_dict[k.replace(" ", "_")] = v
                text = {"role":"alternative",
                        "content": group[0], # tag
                        "features": feature_dict}
                texts.append(text)
            if exists("inputfile.txt"):
                os.remove("inputfile.txt")
            return TextsResponse(texts = texts)
        else:
            annotations = {}
            offset = 0
            tokens = [x for x in outputs.split("\n") if x != ""]
            for token in tokens:
                token_split = [x for x in token.split("\t") if x != ""]
                if endpoint == "tagger":
                    word = token_split[1]
                elif endpoint == "ner":
                    word = token_split[0]
                features = token_split[3:]
                found_index = content.find(word)
                if found_index == -1 and incorrect_result == False:
                    print("The input contains unsupported characters (probably smileys), \
                           and the results might be incorrect.")
                    incorrect_result = True
                start = found_index + offset
                end = start + len(word)
                content = content[end - offset:]
                offset = end
                if endpoint == "tagger":
                    feature_dict = {}
                    tag1 = features[0]
                    feature_dict["tag1"] = tag1
                    feature_dict["tag2"] = features[1]
                    pos = tag1[0]
                    if len(features) > 2:
                        features_split = features[2].split("|")
                        for x in features_split:
                            [k,v] = x.split("=")
                            if v != "":
                                feature_dict[k.replace(" ", "_")] = v
                    annot = {
                        "start": start,
                        "end": end,
                        "features": feature_dict
                        }
                    annotations.setdefault(pos, []).append(annot)
                elif endpoint == "ner":
                    label = token_split[2]
                    if label != "O":
                        annot = {
                                    "start": start,
                                    "end": end,
                                }
                        annotations.setdefault(label, []).append(annot)
            if exists("inputfile.txt"):
                os.remove("inputfile.txt")
            if exists("outputfile.txt"):
                os.remove("outputfile.txt")
            return AnnotationsResponse(annotations = annotations)

    def process_text(self, content):
        incorrect_result = False
        with io.open("inputfile.txt",'w',encoding='utf8') as f:
            f.write(content.content)
        endpoint = self.url_param('endpoint')
        if endpoint == "tagger":
            p = subprocess.Popen('java -cp "tagger-2.2.1-jar-with-dependencies.jar" \
                                  -Xmx2048m lv.lumii.morphotagger.MorphoPipe <inputfile.txt', 
                                  shell=True, stdout=subprocess.PIPE)
        elif endpoint == "ner":
            p = subprocess.Popen('java -cp "tagger-2.2.1-jar-with-dependencies.jar" \
                                  -Xmx2048m lv.lumii.morphotagger.MorphoPipe <inputfile.txt \
                                  >outputfile.txt', shell=True, stdout=subprocess.PIPE)
            p.wait() # without this the second subprocess starts too early and returns nothing
            p = subprocess.Popen('java -mx1g -Dfile.encoding=utf-8 -cp \
                                  "tagger-2.2.1-jar-with-dependencies.jar" \
                                  edu.stanford.nlp.ie.crf.CRFClassifier -prop lv-ner.prop', \
                                  shell=True, stdout=subprocess.PIPE)
        elif endpoint == "word_analysis":
            p = subprocess.Popen('java -jar morphology-2.2.5-SNAPSHOT.jar "analysis" "' + \
                                 content.content + '"', shell=True, stdout=subprocess.PIPE)
        else:
            p = subprocess.Popen('java -jar morphology-2.2.5-SNAPSHOT.jar "wordforms" "' + \
                                 content.content + '"', shell=True, stdout=subprocess.PIPE)
        output, errors = p.communicate()
        output_utf8 = output.decode("utf-8")
        return self.convert_outputs(output_utf8, content.content, endpoint, incorrect_result)

flask_service = LVTagger(name = "LVTagger", path = "/process/<endpoint>")
app = flask_service.app
