import requests
import csv
import os
import sys

from tqdm import tqdm

def send_request(sentence):
    http_request_url = 'http://127.0.0.1:5002/'
    data = {
        'sentence': sentence
    }
    header = {'Content-Type': 'application/json'}

    return requests.post(http_request_url, json=data, headers=header)

def process_pronunciation(pronunciation):
    # pronunciation = list of phonemes
    return " ".join(pronunciation).replace('\t', ' ')

def main():

    sentences_file = './sentence_list.txt'

    print('Sending requests...')
    num_lines = sum(1 for line in open(sentences_file))
    with open(sentences_file, 'r') as f:
        responses = [ send_request(line) for line in tqdm(f, total=num_lines) ]
    
    d = {}
    print('Processing results...')
    for r in tqdm(responses):
        for key, value in r.json()['lex'].items():
            d[key] = value

    ordered_dict = dict(sorted(d.items()))

    print('Writing csv...')
    with open('./lexicon.csv', 'w') as o:
        w = csv.writer(o)
        for k, v in tqdm(ordered_dict.items()):
            w.writerow((k, process_pronunciation(v), process_pronunciation(v), process_pronunciation(v)))

if __name__ == "__main__":
    main()
