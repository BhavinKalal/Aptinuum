import pandas as pd
from transformers import T5Tokenizer, T5ForConditionalGeneration
from tqdm import tqdm
import os

def load_model(model_name="t5-base"):
    print("[INFO] Loading T5 model and tokenizer...")
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    return tokenizer, model

def rephrase_question(question, tokenizer, model, max_length=64):
    input_text = f"paraphrase: {question} </s>"
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=max_length, truncation=True)
    outputs = model.generate(
        inputs,
        max_length=max_length,
        num_beams=4,
        early_stopping=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def rephrase_questions_in_df(df, tokenizer, model):
    new_questions = []
    print("[INFO] Rephrasing questions...")
    for question in tqdm(df['question']):
        try:
            new_q = rephrase_question(question, tokenizer, model)
        except Exception as e:
            print(f"[WARNING] Skipping question due to error: {e}")
            new_q = question
        new_questions.append(new_q)
    df['question'] = new_questions
    return df

def run_rephrasing():
    input_path = "data/processed/augmented_questions.csv"
    output_path = "data/processed/rephrased_questions.csv"

    if not os.path.exists(input_path):
        print(f"[ERROR] Input file not found at: {input_path}")
        return

    df = pd.read_csv(input_path)

    tokenizer, model = load_model()
    updated_df = rephrase_questions_in_df(df, tokenizer, model)

    print(f"[INFO] Saving rephrased dataset to: {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    updated_df.to_csv(output_path, index=False)
    print("[SUCCESS] Rephrasing complete.")

if __name__ == "__main__":
    run_rephrasing()
