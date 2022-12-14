import os
import logging
from typing import Text

from transformers import AutoTokenizer, T5ForConditionalGeneration
import torch


class QuestionGenerator:
    def __init__(self):
        # TODO: на сервере сделать относительный
        logging.info(f'{os.getcwd()=}')
        model_path = 'resources/qgen_model'
        if os.path.exists(model_path):
            self.model = T5ForConditionalGeneration.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained('t5-base')
        self.max_len_input = 512
        self.max_len_output = 30
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def generate_question(self, text: Text, num_questions: int = 1):
        tokenized = self.tokenizer(text, return_tensors='pt',
                                   truncation=True,
                                   max_length=self.max_len_input).input_ids.to(self.device)

        output_tokens = self.model.generate(tokenized,
                                            do_sample=True,
                                            top_k=15,
                                            top_p=0.9,
                                            temperature=0.95,
                                            num_return_sequences=num_questions)
        return self.tokenizer.batch_decode(output_tokens, skip_special_tokens=True)

