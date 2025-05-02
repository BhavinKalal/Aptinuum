from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import pandas as pd
import torch

# 1. Load the T5 paraphrasing model
def load_model():
    model_name = "ramsrigouthamg/t5_paraphraser"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

# 2. Paraphrase a single question
def paraphrase_question(question, tokenizer, model, max_len=256, top_k=2):
    # Format input text for paraphrasing
    text = f"paraphrase: {question} </s>"

    # Tokenize input text
    encoding = tokenizer.encode_plus(
        text,
        padding="max_length",
        return_tensors="pt",
        max_length=max_len,
        truncation=True
    )

    # Print the encoding output for debugging
    print(f"Encoding for question: {question}")
    print(encoding)

    # Ensure that the encoding has both input_ids and attention_mask
    if "input_ids" not in encoding or "attention_mask" not in encoding:
        raise ValueError(f"Tokenization failed for question: {question} - Encoding: {encoding}")

    input_ids = encoding["input_ids"]
    attention_masks = encoding["attention_mask"]

    # Generate paraphrases
    outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_masks,
        max_length=max_len,
        do_sample=True,
        top_k=120,
        top_p=0.98,
        early_stopping=True,
        num_return_sequences=top_k
    )

    return [
        tokenizer.decode(output, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        for output in outputs
    ]

# 3. Main function to augment a full CSV
def augment_questions(input_csv_path, output_csv_path):
    tokenizer, model = load_model()
    df = pd.read_csv(input_csv_path)
    augmented_rows = []

    for _, row in df.iterrows():
        try:
            question = row["question"]
            paraphrases = paraphrase_question(question, tokenizer, model)
            for para in paraphrases:
                new_row = row.copy()
                new_row["question"] = para
                augmented_rows.append(new_row)
        except Exception as e:
            print(f"Error: {e}")

    augmented_df = pd.concat([df, pd.DataFrame(augmented_rows)], ignore_index=True)
    augmented_df.to_csv(output_csv_path, index=False)
    print(f"Saved to {output_csv_path}")
