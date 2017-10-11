Prototype backend code that will eventually become the full backend server.

To run the voice generation test, simply execute:

	$ python model.py
	
This will generate output.wav, which (for now) is a early version of our voice model saying "Hello Scott"

This will become much more advanced later on.

In addition to this, we also implemented the word-to-phoneme system, which is under CMUdict.py

CMUdict is currently able to sucessfully convert any of the 130,000 words in the dictionary into phonemes, which can then be taken in by the Voice model renderWord() method.