import math
import json
import os
import pickle
from nltk.tokenize import TweetTokenizer
import emoji
import html
import re

FILES_PER_JSON = 10

input_dir = '../data/raw/'
ouput_dir = '../data/realworld_json'


URL_TOKEN = '<URL>'
URL_REGEX = r'http\S+'

def clean_sentence(sentence):
	tknzr = TweetTokenizer()

	sentence = emoji.demojize(sentence)
	
	new_body = html.unescape(sentence)

	# remove extraneous whitespace.
	new_body = new_body.replace('\n', ' ')
	new_body = new_body.replace('\t', ' ')
	new_body = new_body.replace('<num>', ' ')
	new_body = re.sub(r'\s+', ' ', new_body).strip()
	new_body = re.sub(r'\:.*\:', ' ', new_body).strip()

	# remove non-ascii symbols.
	new_body = new_body.encode('ascii', errors='ignore').decode()

	# replace URLS with a special token.
	new_body = re.sub(URL_REGEX, URL_TOKEN, new_body)

	# lowercase the text
	new_body = new_body.casefold()

	# Could be done in addition:
	# get rid of comments with quotes

	# tokenize the text
	new_body = tknzr.tokenize(new_body)

	return ' '.join(new_body)


def main():
	if not os.path.exists(ouput_dir):
		os.makedirs(ouput_dir)

	files = [f for f in os.listdir(input_dir)]
	files.sort()
	
	for file in files:
		with open(os.path.join(input_dir, file), 'r') as f:
			raw_data = json.load(f)

			leaf_json = {'users': [], 'num_samples': [], 'user_data': {}}
			cnt = 0
			total = len(raw_data)
			for guid, sentences in raw_data.items():
				if cnt % 1000 == 0:
					print('{}/{}'.format(cnt, total))
				cnt += 1
				leaf_json['users'].append(guid)
				leaf_json['num_samples'].append(len(sentences))
				
				x = []
				y = []
				for s in sentences:
					s = clean_sentence(s)
					
					c_x = s
					c_y = {}

					x.append(c_x)
					y.append(c_y)

				user_data = {'x': x, 'y': y}
				leaf_json['user_data'][guid] = user_data

		with open(os.path.join(ouput_dir, file), 'w') as f:
			json.dump(leaf_json, f, indent=2)



if __name__ == '__main__':
    main()



