def doc_to_target(doc):
    correct_answer_num = doc["correct_answer_num"]
    correct_idx = int(correct_answer_num) - 1
    return ["A", "B", "C", "D"][correct_idx]