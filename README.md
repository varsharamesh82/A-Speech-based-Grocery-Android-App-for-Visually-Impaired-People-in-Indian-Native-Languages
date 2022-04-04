# A-Speech-based-Grocery-Android-App-for-Visually-Impaired-People-in-Indian-Native-Languages

## About the App:

The ubiquitous usage of online shopping over time has increased its prominence. However, the lack of user-friendly UI for visually impaired people hinders the e-commerce shopping facility. Although assistive technology has become more available for the visually impaired, some features like a smooth UI and descriptions of products are not compatible with such. We propose a total voice-based implementation of online shopping using Indian languages like Hindi and Tamil using CNN (convolutional neural network model). Our proposed model is a speech-based classification model of grocery items using CNN. A comparison of our proposed CNN models (Hindi and Tamil) are made using three different activation functions, namely relu, sigmoid, and softplus functions. We found that our proposed CNN model using relu activation function gives the highest training accuracy of 100% for both Hindi and Tamil languages. Also, it gives the highest testing accuracy of 94.5% for Hindi and 81% for Tamil languages. A comparison is done between our proposed CNN model and the open-source speech-to-text Google API merged with TF-IDF using our dataset. Our proposed CNN model outperforms the Google API approach while translating the voice based requests of the grocery items.

## Dataset:
A novel dataset was prepared for the purpose of this paper where five distinct speakers recorded their own voices. Each voice recording is of a person asking for a certain amount of a grocery item, for example “500-gram vasant pyaz daal do” in Hindi will correspond to the English grocery item “onion”. All the sentences cover almost all the grocery items and if two sentences share the same grocery item then they are framed differently. Hence various sentences were recorded for the purpose of the model and no two sentences were the same. A total of four hundred voice recordings were collected for Hindi (200 recordings) and Tamil (200 recordings) respectively for the purpose of building the model and for calculating the accuracy. For each grocery item, 5 audio recordings were prepared, out of which 4 were used for training and 1 was used for testing. It is similar for Tamil and this will be used for classification through our proposed CNN model.
A python package (Natural Language Toolkit WordNet database) was used for creating the database of all grocery items. We have taken 40 grocery items for training and made it into a 1-D array

## Implementation of Proposed Model :

1. Through the Google API which uses Connectionist Temporal Classification algorithm (CTC), the user specifies his grocery request through voice. For example, the user can say ‘mujhe 2-kilogram seb chahiye’ (I want 2 kilograms of apples) and the API will recognize this sentence and convert it into the text format.

2. The language - Tamil or Hindi gets converted to English. ML kit in Android is used for this purpose.

3. Using TF-IDF, the keyword (grocery item) is searched and matched.
TF-IDF is a technique to quantify a word in documents, it computes a weight to each word which signifies the importance of the word in the corpus.

4. When you search with a query, the database will find the relevance of the query with all of the documents, ranks them in the order of relevance and shows you the top k documents. This process is done using the vectorised form of query and documents. 

5. Once the top k documents, in this proposed work, the top 5 documents are displayed and they are told out loud in the specific language.

6. The user has five options to choose from, which will be read out using Google’s Text-To-Speech API. The user will give a voice command regarding his preference among them.

7. The keyword will be matched in the database and will be confirmed with the user. Fig. 3 depicts a block diagram of the above process.


## Text Classification for Google API: 
For the purpose of text classification, TF-IDF (Term Frequency - Inverse Document Frequency) is used.
It measures the uniqueness of a word by comparing the number of times a word appears in a document along with the number of documents the word appears in. It is calculated as shown in Equation(1).

TF-IDF=TFt,d*IDFt		    (1)

Where TF (t,d) stands for Term frequency where ‘t’ stands for the number of times the term appears in the document, ‘d’.

And IDF stands for Inverse Document frequency.  It is calculated as shown in Equation (2).

IDFt=log⁡(NDF+1) 			(2)

Where N stands for the number of documents and DF stands for the document frequency of the term ‘t’.

Using the NLTK WordNet database to serve as the primary general database, the transcribed text is retrieved as input string to extract the keywords. 
Next step is to remove the stop words present in the input string. Using the inflection string transformation library, it is mandatory to singularize the text. 
Using the corpus of grocery items as reference, the keywords which represent the items are matched. The grocery items extracted are segregated, mapped and returned as a key-value pair in the form of a dictionary for calculating associated costs.
The initial step is to consider each grocery item as a distinct document, the following step is the TF scores are calculated for every based on the given word’s frequency.  
We then multiply TF with IDF scores using sklearn’s “TfIdfTransformer '' and store it as a dataframe. The segregated input string is used as a query to retrieve related documents (food items). 
The TF-IDF scores are then calculated for the query term and stored as a dataframe. To rank the documents, the matching scores need to be calculated. 
The query is converted to a vector and then the pairwise cosine similarity score with each document is computed. Based on the cosine similarity scores, the maximum k documents are returned in descending order of scores to retrieve most relevant grocery items first.
