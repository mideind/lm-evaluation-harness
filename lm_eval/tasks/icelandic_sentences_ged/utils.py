import datasets
from lm_eval.api.filter import Filter
import random
import re

def doc_to_target(doc):
    return "0" if doc["correct"] == "false" else "1"

def doc_to_choice(doc):
    return ["0", "1"]
