# Speech-Recognition-Bar-Scenario

## Introduction
Project was built to realize bar tender and customer conversation scenario in any bar. There are some default data that is needed to be modified through the source code such as refusal messages and menu.

## Working principle
Following figure represents the working principle of the project. You can find configuration of the microphone, text to speech and speech to text modules in [src/get_message.py](src/get_message.py)

### default_settings.py

_It involves related default speech recognition functions for initializing microphone, setting the recognizer and transforming
the text to the speech._

### natural_language_settings.py

_It involves functions which are related to natural language and dependency parsing. Tokenization of the sentences, extracting
convenient patterns, nouns are done in this file._

### main.py

_This file is the main file that, menu and some default initializations can be changed or resetted. Order is asked from the 
user in here, checking the emptyness and convenience of the order has been done in the main while loop. _

_**Note:**_ 

_**If you want to terminate the code, you can use one of the keywords from the list of rejection while bot is asking you  
to give an order. This will make the project terminate.**_
  
###


_**Best Regards**_

_**Mahammad Namazov**_

24.02.2020
