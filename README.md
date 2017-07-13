# Text-Classification-using-NaiveBayes-
- LANGUAGE/PACKAGE REQUIREMENTS : Python 3.0; No other packages required. 
- Implementation of a Naive Bayes classifier to classify hotel reviews in English as positive/negative and truthful/deceptive. 
- The classifier was fully implemented using Python 3.0 Standard Libraries and makes no use of external Python packages.

- Feature Selection techniques used : Stop Word removal, Normalizing punctuations
- Stop word removal : 'stopWords.py' finds frequently occuring tokens ( > 200 occurrences) and such tokens are not used in training the model.
- Handling unseen tokens in test data : 'Add-one smoothing' technique was used to handle unseen tokens during classification. 
- F1 score - 91.8%. 

FILE INFORMATION:
Model training - nblearn3.py
Training Dataset Files - train-text.txt train-labels.txt

Model testing - nbclassify3.py
Development Dataset Files - test-text3.txt test-label3.txt

Model parameters (Probability of occurance of tokens and classes) are stored in 'nbmodel.txt'
Classifier output on test dataset is stored in 'nboutput.txt'

INSTRUCTIONS TO RUN CODE FROM COMMAND LINE: 
python nblearn3.py train-text.txt train-labels.txt
Output file(s) : nbmodel.txt

python nbclassify3.py nbmodel.txt
Output file(s) : nboutput.txt 




