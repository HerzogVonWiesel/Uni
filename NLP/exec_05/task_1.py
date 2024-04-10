"""
This is a .py created from a .ipynb notebook. 
It is a little messy, the notebook is a lot more organized, but this is what the task requested. 
Oh well.
"""

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForMaskedLM  # hint for steps 2 and 5
from transformers import DataCollatorForLanguageModeling  # hint for step 4
from transformers import TrainingArguments, Trainer
from typing import Dict, Any
from math import exp
import torch

SEED = 42
dataset = load_dataset("ag_news")
dataset = dataset.shuffle(SEED)

temp = dataset["train"].train_test_split(test_size=0.1, shuffle=True, seed=SEED)
dataset["train"] = temp["train"]
dataset["val"] = temp["test"]

MAX_SEQ_LENGTH = 256

tokenizer = AutoTokenizer.from_pretrained("distilroberta-base")

def preprocess_function(sample: Dict[str, Any], seq_len: int):
    """
    Function applied to all the examples in the Dataset (individually or in batches). 
    It accepts as input a sample as a dictionary and return a new dictionary with the BERT tokens for that sample

    Args:
        sample Dict[str, Any]:
            Dictionary of sample
            
    Returns:
        Dict: Dictionary of tokenized sample in the following style:
        {
          "input_ids": list[int] # token ids
          "attention_mask": list[int] # Mask for self-attention (padding tokens are ignored).
        }
        Hint: if your are using the Huggingface tokenizer implementation, this is the default output format but check it yourself to be sure!
    """
    # set pad to eos
    # tokenizer.pad_token = tokenizer.eos_token
    Dict = tokenizer(sample["text"], truncation=True, padding="max_length", max_length=seq_len)
    return Dict

encoded_ds = dataset.map(
    preprocess_function, batched=True, fn_kwargs={"seq_len": MAX_SEQ_LENGTH}, remove_columns=["label"]
)

MLM_PROBABILITY = 0.1

collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=MLM_PROBABILITY)


DROPOUT_PROBABILITY = 0.15

model = AutoModelForMaskedLM.from_pretrained("distilroberta-base")

# change dropout rate of the output layer in each of the encoder layers

for i in range (0, 6):
    model.roberta.encoder.layer[i].output.dropout.p = DROPOUT_PROBABILITY
print(model)

trainingArgs = TrainingArguments(
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    learning_rate=5e-5,
    weight_decay=0.001,
    # prediction_loss_only=True,
    lr_scheduler_type="cosine",
    output_dir="./results_scratch",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    seed=43,
    num_train_epochs=5,
)

trainer = Trainer(
    model=model,
    args=trainingArgs,
    train_dataset=encoded_ds["train"],
    eval_dataset=encoded_ds["val"],
    data_collator=collator,
)

trainer.train()

trainer.evaluate()

# calculate perplexity on validation and test splits
# Perplexity is the exponentiation of the cross-entropy loss

test_loss = trainer.evaluate(eval_dataset=encoded_ds["test"])["eval_loss"]
test_perplexity = exp(test_loss)
print(f"Test Perplexity: {test_perplexity}")

val_loss = trainer.evaluate()["eval_loss"]
val_perplexity = exp(val_loss)
print(f"Validation Perplexity: {val_perplexity}")

#### Inference
text = "E-mail scam targets police chief Wiltshire Police warns about <mask> after its fraud squad chief was targeted."

# compute top 5 most probable tokens for the masked token
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

input_ids = tokenizer.encode(text, return_tensors='pt').to(device)
mask_token_index = torch.where(input_ids == tokenizer.mask_token_id)[1]

outputs = model(input_ids)
mask_logits = outputs.logits[0, mask_token_index, :]
top_5_tokens = torch.topk(mask_logits, 5, dim=1).indices[0].tolist()

print("Predicted tokens:")
for token in top_5_tokens:
    print(tokenizer.decode([token]))