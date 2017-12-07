# Iteration 3

We have reorganized the backend to be much closer to the final architecture.

drivertest.py contains a sketch to the workflow and is used for our testing.

flaskserver.py is the flask server for the backend, and will be responsible to handling the requests for training, tts, and login.

test.py is the test code for the entire voice model system. This currently contains tests for many of the major components of the model, and will be later expanded to be much more comprehensive.

# Iteration 2

Prototype backend code that will eventually become the full backend server.

To run the voice generation test, simply execute:

	$ python model.py
	
This will generate output.wav, which (for now) is a early version of our voice model saying "Hello Scott"

This will become much more advanced later on.

In addition to this, we also implemented the word-to-phoneme system, which is under CMUdict.py

CMUdict is currently able to sucessfully convert any of the 130,000 words in the dictionary into phonemes, which can then be taken in by the Voice model renderWord() method.
