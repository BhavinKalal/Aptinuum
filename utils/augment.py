import pandas as pd
import random
import re
import os

def load_data(filepath):
    """Load the raw CSV file."""
    return pd.read_csv(filepath)

def is_numerical_question(text):
    """Check if question likely involves numerical data."""
    return bool(re.search(r'\d+', text))

def extract_numbers(text):
    """Extract all integers from the question text."""
    return [int(n) for n in re.findall(r'\d+', text)]

def replace_numbers_in_text(text, old_numbers, new_numbers):
    """Replace old numbers with new numbers in the text."""
    new_text = text
    for old, new in zip(old_numbers, new_numbers):
        new_text = new_text.replace(str(old), str(new), 1)
    return new_text

def numerical_augment(row):
    """
    Replace numeric values in the question.
    Recalculation of options is skipped (for now).
    """
    question = row['question']
    numbers = extract_numbers(question)
    if not numbers:
        return None  # No numbers to augment

    # Change each number by ±10–30%
    new_numbers = [max(1, int(n * random.uniform(0.7, 1.3))) for n in numbers]
    new_question = replace_numbers_in_text(question, numbers, new_numbers)

    # Clone row and update question (answer stays same if options unchanged)
    new_row = row.copy()
    new_row['question'] = new_question
    return new_row

def option_shuffle(row):
    """Shuffle answer options and update answer key accordingly."""
    options = ['option_a', 'option_b', 'option_c', 'option_d']
    correct_option = row['answer']

    # Map old options to their values
    option_values = {opt: row[opt] for opt in options}

    # Shuffle the option values
    shuffled_items = list(option_values.items())
    random.shuffle(shuffled_items)

    # Reassign options
    new_row = row.copy()
    new_answer = ''
    for i, (original_opt, value) in enumerate(shuffled_items):
        new_opt = options[i]
        new_row[new_opt] = value
        if original_opt == correct_option:
            new_answer = new_opt
    new_row['answer'] = new_answer
    return new_row

def apply_augmentation(df):
    """Apply all augmentations to the dataframe."""
    augmented_rows = []

    for _, row in df.iterrows():
        # Original (unaltered)
        augmented_rows.append(row)

        # Numerical augmentation (if applicable)
        if is_numerical_question(row['question']):
            num_aug = numerical_augment(row)
            if num_aug is not None:
                augmented_rows.append(num_aug)

        # Option shuffling
        opt_aug = option_shuffle(row)
        augmented_rows.append(opt_aug)

    return pd.DataFrame(augmented_rows)

def run_augmentation():
    """Main function to run everything."""
    input_path = "data/raw/aptitude_questions_complete.csv"
    output_path = "data/processed/augmented_questions.csv"

    if not os.path.exists(input_path):
        print(f"[ERROR] Input file not found at: {input_path}")
        return

    print("[INFO] Loading data...")
    df = load_data(input_path)

    print("[INFO] Applying augmentation...")
    augmented_df = apply_augmentation(df)

    print(f"[INFO] Saving augmented data to: {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    augmented_df.to_csv(output_path, index=False)
    print("[SUCCESS] Augmentation complete.")

if __name__ == "__main__":
    run_augmentation()
