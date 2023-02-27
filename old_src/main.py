# The main file of the program is holding main loop which proceeds all checkings and answers.
# The program is operating the scenario of the service in bar. There are hot and cold, alcoholic and
# non-alcoholic drinks in the menu of the bar. The following properties are taken into consideration:
# 
# @ if tea is ordered but not specified by user, user will be asked to specify kind of the tea.
# @ if user cannot catch the time to give the order there will be 2 situations:
# ---> User did not tell anything, then virtual waitress will ask to repeat the order, kindly
# ---> User could say something, but the sentence does not consist any drink, it will ask do you want to order something else.
#      Then user can repeat again the order.
# @ if alcoholic drink was ordered by the user, then user will be asked to tell the age. If age is less than 18, then it will not 
#   sell alcoholic drink to the user, otherwise it will.
# @ if user will be asked to order something else, and the user will answer as : no, no thanks, thanks the program will be terminated.
# @ There is no limit to give order. However it leads a bug of code. It will be fixed in future:
# ===>> If there is some drinks are in menu if some of them not, then it forgets to say we do not sell it there.
#  
# Designed by Mahammad Namazov
# 24.02.2020

from default_settings import Settings
from natural_language_settings import NLP
import speech_recognition as sr

# Defining recognizer and microphone 
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Setting the language of the menu and speech
language = "en"

# Defining the settings class for calling
settings = Settings(microphone, recognizer, language)

# Menu
hot_drinks = ["black tea", "green tea", "jasmine", "coffee", "cappuccino", "latte", "americano", "espresso" ]
cold_drinks = ["ice tea", "lemon juice","orange juice", "cola", "fanta", "apple juice", "pineapple juice", "sprite", "vodka", "whiskey", "jager", "rom", "brandy"]
# Tea is used for preventing confusion if tea is not specified by ordering. Alcohol is used to ask the age.
tea = ["black tea", "jasmine", "green tea"]
alcohol = ["vodka", "whiskey", "jager", "rom", "brandy"]

# Default sentences are needed to be asked.
ask_another_order = "Do you want to get something else?"
repeat_to_say = "I could not understand. Could you please repeat it?"
goodbye_message = "It was nice to have you. See you later!"
rejection = ["no thanks", "no", "nothing", "thanks"]

# Defining the natural language settings class
NLP = NLP(settings, tea, hot_drinks, cold_drinks, alcohol, rejection)

# Defining nlp which tokenizes the sentences
nlp = NLP.nlp
# introduction() is used to give introduction about menu and for making greetings the user.
NLP.introduction()

# The main loop which makes process start
while True:
    order_customer = settings.get_the_message()
    print(order_customer) # For being sure what is the order, we are printing the order. If you do not want to see it, you can comment it.
    while not order_customer:
        settings.speech_generator(repeat_to_say) # If nothing has been ordered, then user will be asked to repeat to give an order
        order_customer = settings.get_the_message()
        print(order_customer) # For being sure what is the order, we are printing the order. If you do not want to see it, you can comment it.
    order_customer = order_customer.lower()
    
    order_doc = nlp(order_customer) # Then we tokenize the order
    
    check_point = NLP.check_order(order_doc)
    
    while not check_point:
        settings.speech_generator(repeat_to_say) # If nothing has been ordered, then user will be asked to repeat to give an order
        order_customer = settings.get_the_message()
        while not order_customer:
            settings.speech_generator(repeat_to_say) # If nothing has been ordered, then user will be asked to repeat to give an order
            order_customer = settings.get_the_message()
        
        order_customer = order_customer.lower()
        order_doc = nlp(order_customer)
        print(order_customer) 
        check_point = NLP.check_order(order_doc)
        
    [NLP.to_nltk_tree(sent.root).pretty_print() for sent in order_doc.sents] # Printing the tree of the sentence
    flag_rejection = NLP.answer_of_the_bot(order_doc) # answer of the bot is called by this. Additionally this function, is used for rejection.
    if flag_rejection == 1:
        settings.speech_generator(goodbye_message)
        break
    settings.speech_generator(ask_another_order) # in this step, user is asked about to have another order or not. If yes flag_rejection = 0, else it is 1. If not, then program is going to be terminated.