import subprocess
import io
import os
from os.path import exists

from elg import FlaskService
from elg.model import TextRequest, AnnotationsResponse


class LVTagger(FlaskService):
    
    def convert_outputs(self, outputs, content, endpoint, incorrect_result):
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
                    "features": feature_dict}
                annotations.setdefault(pos, []).append(annot)
            elif endpoint == "ner":
                label = token_split[2]
                if label != "O":
                    annot = {
                                "start": start,
                                "end": end,}
                    annotations.setdefault(label, []).append(annot)
        if exists("inputfile.txt"):
            os.remove("inputfile.txt")
        if exists("outputfile.txt"):
            os.remove("outputfile.txt")
        return AnnotationsResponse(annotations = annotations)

    def process_text(self, request: TextRequest):
        incorrect_result = False
        content = request.content
        with io.open("inputfile.txt",'w',encoding='utf8') as f:
            f.write(content)
        endpoint = self.url_param('endpoint')
        if endpoint == "tagger":
            p = subprocess.Popen('/java/bin/java -cp "tagger.jar" \
                                  -Xmx2048m lv.lumii.morphotagger.MorphoPipe <inputfile.txt', 
                                  shell=True, stdout=subprocess.PIPE)
        elif endpoint == "ner":
            p = subprocess.Popen('/java/bin/java -cp "tagger.jar" \
                                  -Xmx2048m lv.lumii.morphotagger.MorphoPipe <inputfile.txt \
                                  >outputfile.txt', shell=True, stdout=subprocess.PIPE)
            p.wait() # without this the second subprocess starts too early and returns nothing
            p = subprocess.Popen('/java/bin/java -mx1g -Dfile.encoding=utf-8 -cp \
                                  "tagger.jar" \
                                  edu.stanford.nlp.ie.crf.CRFClassifier -prop lv-ner.prop', \
                                  shell=True, stdout=subprocess.PIPE)
        else:
            print("TODO return failure")
        output, errors = p.communicate()
        output_utf8 = output.decode("utf-8")
        return self.convert_outputs(output_utf8, content, endpoint, incorrect_result)


flask_service = LVTagger(name = "LVTagger", path = "/process/<endpoint>")
app = flask_service.app
