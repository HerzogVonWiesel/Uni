from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForMaskedLM  # hint for steps 2 and 5
from transformers import DataCollatorForLanguageModeling  # hint for step 4
from transformers import TrainingArguments, Trainer


if __name__ == '__main__':
    mlm_probability = 0.1


    dropout_probability = 0.15
    # model.roberta.encoder.layer[i].output.dropout = ?

    #### Inference
    text = "E-mail scam targets police chief Wiltshire Police warns about <mask> after its fraud squad chief was targeted."

