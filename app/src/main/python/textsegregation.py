import nltk
import numpy

#nltk.download('wordnet')
#nltk.download('stopwords')
from nltk.corpus import wordnet as wn, stopwords
from nltk import tokenize
from nltk.tokenize import word_tokenize
from operator import itemgetter
from inflection import singularize
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def segregation(input):
	food = wn.synset('food.n.02')
	food_items = list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))
	for i in range(0, len(food_items)):
		food_items[i] = food_items[i].replace('_',' ')
	foodlist = [food for item in food_items for food in item.split()]
	#Defining stopwords
	stop_words = set(stopwords.words('english'))
	#stop_words
	input_text_words = input.split()
	query_words = []
	for word in input_text_words:
		word = singularize(word)
		query_words.append(word)

	'''Modified Word2number package below to accept strings'''
	american_number_system = {
		'zero': 0,
		'one': 1,
		'two': 2,
		'three': 3,
		'four': 4,
		'five': 5,
		'six': 6,
		'seven': 7,
		'eight': 8,
		'nine': 9,
		'ten': 10,
		'eleven': 11,
		'twelve': 12,
		'thirteen': 13,
		'fourteen': 14,
		'fifteen': 15,
		'sixteen': 16,
		'seventeen': 17,
		'eighteen': 18,
		'nineteen': 19,
		'twenty': 20,
		'thirty': 30,
		'forty': 40,
		'fifty': 50,
		'sixty': 60,
		'seventy': 70,
		'eighty': 80,
		'ninety': 90,
		'hundred': 100,
		'thousand': 1000,
		'million': 1000000,
		'billion': 1000000000,
		'point': '.'
	}

	decimal_words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


	def number_formation(number_words):
		numbers = []
		for number_word in number_words:
			numbers.append(american_number_system[number_word])
		if len(numbers) == 4:
			return (numbers[0] * numbers[1]) + numbers[2] + numbers[3]
		elif len(numbers) == 3:
			return numbers[0] * numbers[1] + numbers[2]
		elif len(numbers) == 2:
			if 100 in numbers:
				return numbers[0] * numbers[1]
			else:
				return numbers[0] + numbers[1]
		else:
			return numbers[0]

	def get_decimal_sum(decimal_digit_words):
		decimal_number_str = []
		for dec_word in decimal_digit_words:
			if(dec_word not in decimal_words):
				return 0
			else:
				decimal_number_str.append(american_number_system[dec_word])
		final_decimal_string = '0.' + ''.join(map(str,decimal_number_str))
		return float(final_decimal_string)

	def word_to_num(number_sentence):
		if type(number_sentence) is not str:
			return None

		number_sentence = number_sentence.replace('-', ' ')
		number_sentence = number_sentence.lower()  # converting input to lowercase

		if(number_sentence.isdigit()):  # return the number if user enters a number string
			return int(number_sentence)

		split_words = number_sentence.strip().split()  # strip extra spaces and split sentence into words

		clean_numbers = []
		clean_decimal_numbers = []
		for word in split_words:
			if word in american_number_system:
				clean_numbers.append(word)
		if len(clean_numbers) == 0:
			return None

		# Error if user enters million,billion, thousand or decimal point twice
		if clean_numbers.count('thousand') > 1 or clean_numbers.count('million') > 1 or clean_numbers.count('billion') > 1 or clean_numbers.count('point')> 1:
			raise ValueError("Redundant number word! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

		# separate decimal part of number (if exists)
		if clean_numbers.count('point') == 1:
			clean_decimal_numbers = clean_numbers[clean_numbers.index('point')+1:]
			clean_numbers = clean_numbers[:clean_numbers.index('point')]

		billion_index = clean_numbers.index('billion') if 'billion' in clean_numbers else -1
		million_index = clean_numbers.index('million') if 'million' in clean_numbers else -1
		thousand_index = clean_numbers.index('thousand') if 'thousand' in clean_numbers else -1

		if (thousand_index > -1 and (thousand_index < million_index or thousand_index < billion_index)) or (million_index>-1 and million_index < billion_index):
			raise ValueError("Malformed number! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

		total_sum = 0  # storing the number to be returned

		if len(clean_numbers) > 0:
			if len(clean_numbers) == 1:
				total_sum += american_number_system[clean_numbers[0]]

			else:
				if billion_index > -1:
					billion_multiplier = number_formation(clean_numbers[0:billion_index])
					total_sum += billion_multiplier * 1000000000

				if million_index > -1:
					if billion_index > -1:
						million_multiplier = number_formation(clean_numbers[billion_index+1:million_index])
					else:
						million_multiplier = number_formation(clean_numbers[0:million_index])
					total_sum += million_multiplier * 1000000

				if thousand_index > -1:
					if million_index > -1:
						thousand_multiplier = number_formation(clean_numbers[million_index+1:thousand_index])
					elif billion_index > -1 and million_index == -1:
						thousand_multiplier = number_formation(clean_numbers[billion_index+1:thousand_index])
					else:
						thousand_multiplier = number_formation(clean_numbers[0:thousand_index])
					total_sum += thousand_multiplier * 1000

				if thousand_index > -1 and thousand_index != len(clean_numbers)-1:
					hundreds = number_formation(clean_numbers[thousand_index+1:])
				elif million_index > -1 and million_index != len(clean_numbers)-1:
					hundreds = number_formation(clean_numbers[million_index+1:])
				elif billion_index > -1 and billion_index != len(clean_numbers)-1:
					hundreds = number_formation(clean_numbers[billion_index+1:])
				elif thousand_index == -1 and million_index == -1 and billion_index == -1:
					hundreds = number_formation(clean_numbers)
				else:
					hundreds = 0
				total_sum += hundreds

		# adding decimal part to total_sum (if exists)
		if len(clean_decimal_numbers) > 0:
			decimal_sum = get_decimal_sum(clean_decimal_numbers)
			total_sum += decimal_sum

		return total_sum
	'''End of Word2number package'''

	for words in query_words:
		print(words)

	#Extracting numbers from strings
	numbers = []

	for words in query_words:
		if(word_to_num(words) is not None):
			number = word_to_num(words)
			numbers.append(number)
		else:
			continue
	foods = []
	for word in query_words:
		if word not in stop_words:
			if word in foodlist:
				foods.append(word)
	#Linking words to quantity
	result = {foods[i]:numbers[i] for i in range(len(numbers))}
	return result

def search_query(query):
	return "Search Query: "+query

def tfidf(query):
	food = wn.synset('food.n.02')
	food_items = list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))
	for i in range(0, len(food_items)):
		food_items[i] = food_items[i].replace('_',' ')
	tf = TfidfVectorizer()
	tf_idf_matrix = tf.fit_transform(food_items)
	df = pd.DataFrame(tf_idf_matrix.toarray(), columns = tf.get_feature_names())
	word = query.split()
	for i in range(0,len(word)):
		word[i]=singularize(word[i])
	query=' '.join(word)
	query_vector = tf.transform([query]).toarray()
	df_query = pd.DataFrame(query_vector)

	#Cosine Similarity
	results = cosine_similarity(df, df_query)
	results_list=[]
	for i in range(0,len(results)):
		if results[i]>0:
			results_list.append(results[i][0])
	#results_list.sort(reverse=True)
	food_item_result={}
	for i in range(0, len(results)):
		if results[i]>0:
			food_item_result[i]=food_items[i]

	return food_item_result




