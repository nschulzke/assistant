from transformers import AutoTokenizer
from core.prompt_grammar import parse_prompts
from datasets import Dataset
from transformers import TokenClassificationPipeline
import torch
from transformers import TrainingArguments, Trainer
from transformers import AutoModelForTokenClassification
import os

BASE_MODEL = "bert-base-uncased"


def load_tokenizer():
    return AutoTokenizer.from_pretrained(BASE_MODEL, add_prefix_space=True)


def train_classifier():
    tokenizer = load_tokenizer()

    def tokenize_and_align_labels(examples):
        tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True)
        labels = []

        for i, label in enumerate(examples[f"tags"]):
            word_ids = tokenized_inputs.word_ids(batch_index=i)  # Map tokens to their respective word.
            previous_word_idx = None
            label_ids = []

            for word_idx in word_ids:  # Set the special tokens to -100.
                if word_idx is None:
                    label_ids.append(-100)
                elif word_idx != previous_word_idx:  # Only label the first token of a given word.
                    label_ids.append(label[word_idx])
                else:
                    label_ids.append(-100)
                previous_word_idx = word_idx
            labels.append(label_ids)
        tokenized_inputs["labels"] = labels
        return tokenized_inputs

    with open("prompts.txt") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    prompts = parse_prompts(lines)

    dataset = Dataset.from_list(prompts['data'])

    dataset = dataset.map(tokenize_and_align_labels, batched=True)

    model = AutoModelForTokenClassification.from_pretrained(
        BASE_MODEL,
        id2label=prompts['unique_tags'],
    )

    training_args = TrainingArguments(
        output_dir="classifier_trainer",
        per_gpu_eval_batch_size=1,
        per_gpu_train_batch_size=1,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )

    trainer.train()

    classifier = TokenClassificationPipeline(
        model=model,
        tokenizer=tokenizer,
        device=torch.cuda.current_device(),
    )
    try:
        os.makedirs("tmp/classifier_model")
    except FileExistsError:
        pass
    model.save_pretrained("tmp/classifier_model")
    return classifier


def load_classifier():
    model = AutoModelForTokenClassification.from_pretrained("tmp/classifier_model")
    classifier = TokenClassificationPipeline(
        model=model,
        tokenizer=load_tokenizer(),
        device=torch.cuda.current_device(),
    )
    return classifier


if __name__ == '__main__':
    train_classifier()
