import io
import os
from os.path import exists
from subprocess import Popen, PIPE
import logging
# https://www.geeksforgeeks.org/broken-pipe-error-in-python/
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

from elg import FlaskService
from elg.model import TextRequest, AnnotationsResponse, Failure
from elg.model.base import StandardMessages, StatusMessage


logging.basicConfig(level=logging.DEBUG)
MAX_CHAR = 15000
MAX_TOKEN_LENGTH = 100


class LVTagger(FlaskService):

    def convert_outputs(self, outputs, content, endpoint):
        annotations = {}
        offset = 0
        tokens = [x for x in outputs.split("\n") if x != ""]
        pos_dict = {"n": "Noun", "v": "Verb", "a": "Adjective", "p": "Pronoun", "r": "Adverb",\
                    "s": "Preposition", "c": "Conjunction", "m": "Numeral", "i": "Interjection",\
                    "y": "Abbreviation", "q": "Particle", "z": "Punctuation", "x": "Residual"}
        for token in tokens:
            token_split = [x for x in token.split("\t") if x != ""]
            word = token_split[1]
            features = token_split[3:]
            found_index = content.find(word)
            start = found_index + offset
            end = start + len(word)
            content = content[end - offset:]
            offset = end
            feature_dict = {}
            tag1 = features[0]
            feature_dict["tag1"] = tag1
            feature_dict["tag2"] = features[1]
            pos = tag1[0]
            if pos in pos_dict:
                pos = pos_dict[pos]
            if len(features) > 2:
                features_split = features[2].split("|")
                for x in features_split:
                    [k, v] = x.split("=")
                    if v != "":
                        feature_dict[k.replace(" ", "_")] = v
            annot = {
                "start": start,
                "end": end,
                "features": feature_dict}
            annotations.setdefault(pos, []).append(annot)
        return AnnotationsResponse(annotations=annotations)

    def process_text(self, request: TextRequest):
        content = request.content + "\n"
        if content == "\n":
            emptyInput_warning_msg = StatusMessage(
                code='lingsoft.input.empty',
                params=[],
                text='Input text is empty'
            )
            return AnnotationsResponse(annotations={}, warnings=[emptyInput_warning_msg])
        if len(content) > MAX_CHAR:
            error = StandardMessages.generate_elg_request_too_large()
            return Failure(errors=[error])

        longest = 0
        if content.strip():
            longest = max(len(token) for token in content.split())
        if longest > MAX_TOKEN_LENGTH:
            error = StatusMessage(
                    code="lingsoft.token.too.long",
                    text="Given text contains too long tokens",
                    params=[])
            return Failure(errors=[error])

        if any(ord(ch) > 0xffff for ch in content):
            error = StatusMessage(
                    code="lingsoft.character.invalid",
                    text="Given text contains unsupported characters",
                    params=[])
            return Failure(errors=[error])

        endpoint = self.url_param('endpoint')
        if endpoint == "tagger":
            try:
                app.logger.debug("Content: %s", content)
                process.stdin.write(content)
                process.stdin.flush()
                lines = []
                previous_empty = False
                while True:
                    line = process.stdout.readline().rstrip('\n')
                    lines.append(line)
                    if previous_empty and not line:
                        break
                    if not line:
                        previous_empty = True
                    else:
                        previous_empty = False
                output = "\n".join(lines)
                app.logger.debug("Output: %s", output)
                return self.convert_outputs(output, content, endpoint)
            except Exception as err:
                error = StandardMessages.\
                        generate_elg_service_internalerror(params=[str(err)])
                return Failure(errors=[error])
        else:
            error = StandardMessages.generate_elg_service_not_found(
                    params=[endpoint])
            return Failure(errors=[error])



flask_service = LVTagger(name="LVTagger", path="/process/<endpoint>")
app = flask_service.app
process = None


@app.before_first_request
def setup():
    global process
    java_call = ["/java/bin/java", "-cp", "tagger-2.2.1-jar-with-dependencies.jar", "-Xmx2048m",
                 "lv.lumii.morphotagger.MorphoPipe"]
    process = Popen(java_call, stdin=PIPE, stdout=PIPE, text=True)
