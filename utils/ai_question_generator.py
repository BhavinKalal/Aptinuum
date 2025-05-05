import csv
import os
import re
from tqdm import tqdm
import random

# --------------------------------------------
# Replace this with your actual model-based generation logic
# For now, this is a dummy function that returns hardcoded format
def generate_question(topic, difficulty):
    """
    Simulated AI-based question generation.
    Replace this with your transformer/OpenAI call.
    """
    return f"""What is 25% of 200?

A. 25
B. 50
C. 75
D. 100
Answer: B"""

# --------------------------------------------
def parse_question_output(raw_text, topic="unknown", difficulty="medium"):
    """
    Parses a generated multiple-choice question into structured fields.
    """

    lines = [line.strip() for line in raw_text.strip().split('\n') if line.strip()]

    question = ""
    options = {"A": "", "B": "", "C": "", "D": ""}
    answer = ""

    option_pattern = re.compile(r"^(A|B|C|D)[\.\:\)]?\s+(.*)", re.IGNORECASE)
    answer_pattern = re.compile(r"Answer\s*[:\-]?\s*(A|B|C|D)", re.IGNORECASE)

    for line in lines:
        if option_match := option_pattern.match(line):
            label, text = option_match.groups()
            options[label.upper()] = text.strip()
        elif answer_match := answer_pattern.match(line):
            answer = answer_match.group(1).upper()
        elif not question:
            question = line.strip()

    if not question or not answer or not all(options.values()):
        raise ValueError("Failed to parse question properly.")

    return {
        "topic": topic,
        "difficulty": difficulty,
        "question": question,
        "option_a": options["A"],
        "option_b": options["B"],
        "option_c": options["C"],
        "option_d": options["D"],
        "answer": answer
    }

# --------------------------------------------
def generate_questions_to_csv(topics, difficulties, num_per_combo=10, output_path="data/processed/generated_questions.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    all_data = []
    print("[INFO] Generating questions...")
    for topic in topics:
        for difficulty in difficulties:
            for _ in tqdm(range(num_per_combo), desc=f"{topic} - {difficulty}"):
                try:
                    raw = generate_question(topic, difficulty)
                    parsed = parse_question_output(raw, topic, difficulty)
                    all_data.append(parsed)
                except Exception as e:
                    print(f"[WARNING] Skipping one due to error: {e}")
                    continue

    print(f"[INFO] Saving to: {output_path}")
    with open(output_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "topic", "difficulty", "question", "option_a", "option_b", "option_c", "option_d", "answer"
        ])
        writer.writeheader()
        writer.writerows(all_data)

    print(f"[SUCCESS] {len(all_data)} questions saved to {output_path}")

# --------------------------------------------
if __name__ == "__main__":
    topics = ["probability", "percentages", "number series", "ratios", "verbal reasoning"]
    difficulties = ["easy", "medium", "hard"]
    generate_questions_to_csv(topics, difficulties, num_per_combo=5)
