def doc_to_text(doc):
    question = doc["question"].strip()
    choices_label = doc["choices"]["label"]
    choices_text = doc["choices"]["text"]

    text = f"Spurning: {question}\n"
    for choice_label, choice_text in zip(choices_label, choices_text):
        text += f"{choice_label}: {choice_text}\n"

    text += (
        "Hvaða svar er réttast? Skrifaðu eitt af "
        + ", ".join([f"'{label}'" for label in choices_label])
        + " hér að neðan. Ekki skrifa neitt annað. Svar:"
    )
    return text
