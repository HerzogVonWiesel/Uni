"""
This is a .py created from a .ipynb notebook. 
It is a little messy, the notebook is a lot more organized, but this is what the task requested. 
Oh well.
"""

from datasets import load_dataset
import datasets
from typing import Dict, Any
import matplotlib.pyplot as plt
import random
from transformers import AutoTokenizer
import torch
from transformers import T5ForConditionalGeneration
import wandb
import os


SEED = 42

dataset = load_dataset("allenai/qasper")

print(dataset['train'][0])

# draw bar plot of the number of questions

num_questions = [len(dataset['train'][i]['qas']['question']) for i in range(len(dataset['train']))]
plt.hist(num_questions, bins=12, range=(0.5, 12.5))
plt.title('Number of questions per article')
plt.xlabel('Number of questions')
plt.ylabel('Number of article')
plt.show()

# draw histogram of average number of answers per question
num_avgs = []
all_answer_counts = []
num_free_form_answers = 0
num_extractive_answers = 0
num_unanswerable = 0
abstract_lengths = []
for article in dataset['train']:
    abstract_lengths.append(len(article['abstract'].split(' ')))
    for answers in article['qas']['answers']:
        for answer_dict in answers['answer']:
            if answer_dict['free_form_answer'] != '':
                num_free_form_answers += 1
            if len(answer_dict['extractive_spans']) != 0:
                num_extractive_answers += 1
            if answer_dict['unanswerable'] == True:
                num_unanswerable += 1
    answer_counts = [len(answers['answer']) for answers in article['qas']['answers']]
    num_avgs.append(sum(answer_counts) / len(answer_counts))
    all_answer_counts.extend(answer_counts)

print('Number of answers: ', sum(all_answer_counts))
print('Number of free form answers: ', num_free_form_answers)
print('Number of extractive answers: ', num_extractive_answers)
print('Number of unanswerable questions: ', num_unanswerable)
print('Average number of answers per question: ', sum(all_answer_counts) / len(all_answer_counts))
plt.hist(num_avgs)
plt.title('Average number of answers per question')
plt.xlabel('Average number of answers')
plt.ylabel('Number of articles')
plt.show()

# draw histogram of abstract lengths
plt.hist(abstract_lengths, bins=50, range=(0, 300))
plt.title('Abstract lengths in words')
plt.xlabel('Abstract length (in words)')
plt.ylabel('Number of articles')
plt.show()

num_questions = [len(dataset['test'][i]['qas']['question']) for i in range(len(dataset['test']))]
print('Number of questions in test set: ', sum(num_questions)) 
plt.hist(num_questions, bins=12, range=(0.5, 12.5))
plt.title('Number of questions per article')
plt.xlabel('Number of questions')
plt.ylabel('Number of article')
plt.show()

# draw histogram of average number of answers per question
num_avgs = []
all_answer_counts = []
num_free_form_answers = 0
num_extractive_answers = 0
num_unanswerable = 0
abstract_lengths = []
for article in dataset['test']:
    abstract_lengths.append(len(article['abstract'].split(' ')))
    for answers in article['qas']['answers']:
        for answer_dict in answers['answer']:
            if answer_dict['free_form_answer'] != '':
                num_free_form_answers += 1
            if len(answer_dict['extractive_spans']) != 0:
                num_extractive_answers += 1
            if answer_dict['unanswerable'] == True:
                num_unanswerable += 1
    answer_counts = [len(answers['answer']) for answers in article['qas']['answers']]
    num_avgs.append(sum(answer_counts) / len(answer_counts))
    all_answer_counts.extend(answer_counts)

print('Number of answers: ', sum(all_answer_counts))
print('Number of free form answers: ', num_free_form_answers)
print('Number of extractive answers: ', num_extractive_answers)
print('Number of unanswerable questions: ', num_unanswerable)
print('Average number of answers per question: ', sum(all_answer_counts) / len(all_answer_counts))
plt.hist(num_avgs)
plt.title('Average number of answers per question')
plt.xlabel('Average number of answers')
plt.ylabel('Number of articles')
plt.show()

# draw histogram of abstract lengths
plt.hist(abstract_lengths, bins=50, range=(0, 300))
plt.title('Abstract lengths in words')
plt.xlabel('Abstract length (in words)')
plt.ylabel('Number of articles')
plt.show()

# train_sample = {
#     'question': xxx,
#     'context': xxx,
#     'answer': xxx (randomly selected of the possible answers)
# }

train_samples = []
for article in dataset['train']:
    for i, question in enumerate(article['qas']['question']):
        answers = article['qas']['answers'][i]['answer']
        # shuffle answers
        random.shuffle(answers)
        for answer_dict in answers:
            if answer_dict['free_form_answer'] != '':
                train_samples.append({
                    'question': question,
                    'context': article['abstract'],
                    'answer': answer_dict['free_form_answer']
                })
                break
            elif len(answer_dict['extractive_spans']) != 0:
                train_samples.append({
                    'question': question,
                    'context': article['abstract'],
                    'answer': answer_dict['extractive_spans'][0]
                })
                break
print("Example train sample:")
print(train_samples[0])

test_samples = []
for article in dataset['test']:
    for i, question in enumerate(article['qas']['question']):
        answers = article['qas']['answers'][i]['answer']
        # shuffle answers
        random.shuffle(answers)
        for answer_dict in answers:
            if answer_dict['free_form_answer'] != '':
                test_samples.append({
                    'question': question,
                    'context': article['abstract'],
                    'answer': answer_dict['free_form_answer']
                })
                break
            elif len(answer_dict['extractive_spans']) != 0:
                test_samples.append({
                    'question': question,
                    'context': article['abstract'],
                    'answer': answer_dict['extractive_spans'][0]
                })
                break

print("Example test sample:")
print(test_samples[0])

train_abstracts = [sample['context'] for sample in train_samples]
train_questions = [sample['question'] for sample in train_samples]
train_answers = [sample['answer'] for sample in train_samples]

test_abstracts = [sample['context'] for sample in test_samples]
test_questions = [sample['question'] for sample in test_samples]
test_answers = [sample['answer'] for sample in test_samples]

train = {'abstract': train_abstracts, 'question': train_questions, 'answer': train_answers}
test = {'abstract': test_abstracts, 'question': test_questions, 'answer': test_answers}

train_dataset = datasets.Dataset.from_dict(train)
test_dataset = datasets.Dataset.from_dict(test)

flattened_dataset = datasets.DatasetDict({'train': train_dataset, 'test': test_dataset})

assert len(train_abstracts) == len(train_questions) == len(train_answers)
assert len(test_abstracts) == len(test_questions) == len(test_answers)

print("Example flattened train sample:")
print(flattened_dataset['train'][0])

# randomly choose 10% of the training data as validation data from flattened dataset
temp = flattened_dataset["train"].train_test_split(test_size=0.1, shuffle=True, seed=SEED)
flattened_dataset["train"] = temp["train"]
flattened_dataset["val"] = temp["test"]

tokenizer = AutoTokenizer.from_pretrained("t5-base")

def preprocess_function(sample: Dict, max_qc_len: int, max_ans_len: int):
    """
    Preprocesses a single sample dictionary, each containing:
        'question': question,
        'abstract': article['abstract'],
        'answer': answer

    Tokenizes the question and context, and truncates the concatenation to max_qc_len.
    Tokenizes the answer and truncates to max_ans_len.
    """

    # Tokenize the question and context pair
    qc_pair = tokenizer(
        sample["question"],
        sample["abstract"],
        max_length=max_qc_len,
        truncation=True,
        padding="max_length",
    )

    # Tokenize the answer
    ans = tokenizer(
        sample["answer"],
        max_length=max_ans_len,
        truncation=True,
        padding="max_length",
    )

    return {
        "input_ids": qc_pair.input_ids,
        "attention_mask": qc_pair.attention_mask,
        "labels": ans.input_ids,
        "decoder_attention_mask": ans.attention_mask,
    }

encoded_ds = flattened_dataset.map(
    preprocess_function,
    batched=True,
    fn_kwargs={"max_qc_len": 128, "max_ans_len": 32},
)


model = T5ForConditionalGeneration.from_pretrained("google/t5-efficient-mini")

# set the wandb project where this run will be logged
os.environ["WANDB_PROJECT"]="my-awesome-project"

# save your trained model checkpoint to wandb
os.environ["WANDB_LOG_MODEL"]="true"

# turn off watch to log faster
os.environ["WANDB_WATCH"]="false"

from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments

training_args = Seq2SeqTrainingArguments(
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    learning_rate=5e-4,
    weight_decay=0.001,
    # prediction_loss_only=True,
    lr_scheduler_type="cosine",
    output_dir="./results_scratch",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    seed=SEED,
    num_train_epochs=5,
    logging_dir='./logs',
    report_to="wandb",
    logging_steps=10,
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=encoded_ds['train'],
    eval_dataset=encoded_ds['val'],
)

# start wandb run
wandb.init()

trainer.train()

trainer.evaluate()

# end wandb run
wandb.finish()

# run inference on a sample from the test split of flattened dataset
sample = flattened_dataset['test'][9]

# preprocess the sample
preprocessed_sample = preprocess_function(sample, max_qc_len=128, max_ans_len=32)

# move the sample to the device (GPU, if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# run inference
# model_base = T5ForConditionalGeneration.from_pretrained("google/t5-efficient-mini")
# model_base.to(device)
generated_answer_ids = model.generate(
    input_ids=torch.tensor([preprocessed_sample['input_ids']]).to(device),
    attention_mask=torch.tensor([preprocessed_sample['attention_mask']]).to(device),
)

# decode the generated answer ids
generated_answer = tokenizer.decode(generated_answer_ids[0], skip_special_tokens=True)

print("Question:", sample['question'])
print("Context:", sample['abstract'])
print("Generated Answer:", generated_answer)
print("Actual Answer:", sample['answer'])