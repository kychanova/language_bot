import numpy as np

from transformers import pipeline
#from sentence_transformers import SentenceTransformer

# model = SentenceTransformer('all-MiniLM-L6-v2')
qa_pipeline = pipeline('question-answering')


# def check_sent_similarity(sent1, sent2):
#     emb1 = model.encode(sent1)
#     emb2 = model.encode(sent2)
#     cos_sym = np.dot(emb1, emb2)/(np.linalg.norm(emb1)*np.linalg.norm(emb2))
#     return cos_sym


def generate_answers(context, questions):
    answers = []
    for question in questions:
        output = qa_pipeline(question=question, context=context)
        answers.append(output['answer'])
    return answers