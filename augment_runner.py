from utils.augment import augment_questions

augment_questions(
    input_csv_path="data/raw/aptitude_questions_complete.csv",
    output_csv_path="data/processed/augmented_questions.csv"
)