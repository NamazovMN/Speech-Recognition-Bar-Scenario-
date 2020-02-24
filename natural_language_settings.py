# This file of the program is holding main functions for proceeding the code properly, which are
# about the principles of the natural language.

# Designed by Mahammad Namazov
# 24.02.2020



from nltk import Tree
from spacy import displacy
import spacy
from spacy.symbols import NOUN, NUM, ADJ, PROPN
from spacy.matcher import Matcher
from speech_recognition_definitions import get_the_message,text_to_speech
import speech_recognition as sr



class NLP(object):

    def __init__(self, settings, tea, hot_drinks, cold_drinks, alcohol, rejection):
        self.hot_drinks = hot_drinks
        self.cold_drinks = cold_drinks
        self.tea = tea
        self.alcohol = alcohol
        self.rejection = rejection
        self.nlp = spacy.load("en_core_web_sm")
        self.settings = settings 
        self.matcher = Matcher(self.nlp.vocab)

    def tok_format(self, tok):
        return "_".join([tok.orth_, tok.tag_])

    def to_nltk_tree(self, node):
        if node.n_lefts + node.n_rights > 0:
            return (Tree(self.tok_format(node), [self.to_nltk_tree(child) for child in node.children]))
        else:
            return self.tok_format(node)

    # Concatanating menu elements while giving the information. It is used because of preventing pauses while speaking.
    def concatanate_menu(self, list_of_drinks):
        drink_sentence = list_of_drinks[0]
        for element in range(1, len(list_of_drinks)-1):
            drink_sentence = drink_sentence + ', ' + list_of_drinks[element] + '.'
        drink_sentence = drink_sentence + ' and ' + list_of_drinks[len(list_of_drinks)-1] + '.'
        return drink_sentence

    # The following method is used for introduction to menu and greetings part of the code.
    def introduction(self):
        cold_sentence = self.concatanate_menu(self.cold_drinks)
        hot_sentence = self.concatanate_menu(self.hot_drinks)
        introduction_sentence = "Welcome to the bar. We can serve you hot and cold drinks as you wish! "
        intro_hot = "As a hot drink we have " + hot_sentence + ". "
        intro_cold = "If you want cold drink we can serve you " + cold_sentence + ". "
        introduction_sentence = introduction_sentence + intro_hot + intro_cold + "What would you like to have?"
        self.settings.speech_generator(introduction_sentence)

    # Extracting patterns which are double nouns. E.g., apple juice
    def extract_double_nouns(self, order_doc):
        resulted_compounds = []
        pattern = [{'POS': 'NOUN'}, {'POS': 'NOUN'}]
        self.matcher.add("Double_Noun", None, pattern)
        matches = self.matcher(order_doc)
        for _, start, end in matches:
            span = order_doc[start:end]
            resulted_compounds.append(span.text)    
        return resulted_compounds
    
    # Extracting patterns which are adjective and noun. E.g., black tea
    def extract_adjective_noun(self, order_doc):
        resulted_compounds = []
        pattern = [{'POS': 'ADJ'}, {'POS': 'NOUN'}]
        self.matcher.add("Adjective_Noun", None, pattern)
        matches = self.matcher(order_doc)
        for _, start, end in matches:
            span = order_doc[start:end]
            resulted_compounds.append(span.text)    
        return resulted_compounds

    # Extracting patterns which are double pronouns. If double nouns or adjective and noun pattern are used
    # in non-completed sentence, they can be understood by code, because of this method.
    def extract_double_pronouns(self, order_doc):
        resulted_compounds = []
        pattern = [{'POS': 'PPN'}, {'POS': 'PPN'}]
        self.matcher.add('Double_Pronouns', None, pattern)
        matches = self.matcher(order_doc)
        for _, start, end in matches:
            span = order_doc[start:end]
            resulted_compounds.append(span.text)    
        return resulted_compounds

       
    # Collecting all nouns from the tokenized sentence
    def collect_nouns(self, order_doc):
        nouns = []
        for possible_subject in order_doc:
            if possible_subject.pos == NOUN:
                nouns.append(possible_subject)
        print(nouns)
        return nouns
    def collect_NNP(self, order_doc):
        pronouns = []
        for possible_subject in order_doc:
            if possible_subject.pos == PROPN:
                pronouns.append(possible_subject)
        print(pronouns)
        return pronouns

    # collecting all patterns from the tokenized sentence
    def collect_compounds(self, order_doc):
        compounds_dn = []
        compounds_an = []
        compounds_dpn = []
        compounds = []
        if self.extract_double_nouns(order_doc):
            compounds_dn = self.extract_double_nouns(order_doc)
        
        if self.extract_adjective_noun(order_doc):
            compounds_an = self.extract_adjective_noun(order_doc)
        
        if self.extract_double_pronouns(order_doc):
            compounds_dpn = self.extract_double_pronouns(order_doc)
        
        compounds = compounds_an
        
        for each in compounds_dn:
            if each not in compounds:
                compounds.append(each)
        
        for each in compounds_dpn:
            if each not in compounds:
                compounds.append(each)
        print(compounds)
        return compounds

    # By using the following function, we are checking wheter all collected probable drinks (nouns and compounds)
    # are in the menu or not.
    def check_if_drink_available(self, possible_drink):
        print("Possible DRINK : {}".format(possible_drink))
        drink = []
        if possible_drink:
            for each in possible_drink:
                for each_cold_drink in self.cold_drinks:
                    if str(each) == each_cold_drink:
                        drink.append(each_cold_drink)
                for each_hot_drink in self.hot_drinks:
                    if str(each) == each_hot_drink:
                        drink.append(each_hot_drink)
        return drink
        
    # The following method is very important for answering the customer. Because, all information that can be given 
    # according to the order is done by this function.

    def answer_to_the_order(self, drink_list, availability = True, case = 0):
        # case = 0 : there is not an alcoholic drink in order.
        # case = 1 : age is over 18, and all drinks are alcoholic.
        # case = 2 : age is under 18, and all drinks are alcoholic.
        # case = 3 : age is over 18, and there are alcoholic and other drinks.
        # case = 4 : age is under 18, and there are alcoholic and other drinks.
        
        if case == 0:
            if availability:
                if len(drink_list) == 1:
                    sentence = "Your " + drink_list[0] + " is coming right now!"
                elif len(drink_list) == 2:
                    sentence = "You want to get "+ drink_list[0] + " and " + drink_list[1] +". They are coming right now!"
                else:
                    sentence_2 = ""
                    for each in range(len(drink_list)-1):
                        sentence_2 = sentence_2 + ", " + drink_list[each]
                    sentence_2 = sentence_2 + " and " + drink_list[len(drink_list)-1]
                    sentence = "You have ordered " + sentence_2 + ". They are coming right now!"
            else:
                sentence = "I am sorry, we are not selling it here!"
        
        elif case == 1:
            if len(drink_list) == 1:
                sentence = "Your " + drink_list[0] + " is coming right now!"
            elif len(drink_list) == 2:
                sentence = "You want to get "+ drink_list[0] + " and " + drink_list[1] +". They are coming right now!"
            else:
                sentence_2 = ""
                for each in range(len(drink_list)-1):
                    sentence_2 = sentence_2 + ", " + drink_list[each]
                sentence_2 = sentence_2 + " and " + drink_list[len(drink_list)-1]
                sentence = "You have ordered " + sentence_2 + ". They are coming right now!"
        
        elif case == 2:
            if(len(drink_list)==1):
                sentence = "The drink that you have ordered is alcoholic and because of your age we cannot sell it to you!"                 
            else:
                sentence = "Drinks that you have ordered are alcoholic and because of your age we cannot sell them to you!"
        
        elif case == 3:
            if len(drink_list) == 2:
                sentence = "You want to get "+ drink_list[0] + " and " + drink_list[1] +". They are coming right now!"
            else:
                sentence_2 = ""
                for each in range(len(drink_list)-1):
                    sentence_2 = sentence_2 + ", " + drink_list[each]
                sentence_2 = sentence_2 + " and " + drink_list[len(drink_list)-1]
                sentence = "You have ordered " + sentence_2 + ". They are coming right now!"
        
        elif case == 4:
            sentence_core = "We cannot sell to you alcoholic drinks you have ordered, because of your age. However, "
            if len(drink_list) == 1:
                sentence = sentence_core + " you have also ordered " + drink_list[0] + ". It is coming right now!"
            elif len(drink_list) == 2:
                sentence = sentence_core + " you have also ordered " + drink_list[0] + " and " + drink_list[1] + ". They are coming right now!"
            else : 
                sentence_2 = ""
                for each in range(len(drink_list)-1):
                    sentence_2 = sentence_2 + ", " + drink_list[each]
                sentence_2 = sentence_2 + " and " + drink_list[len(drink_list)-1]
                sentence = sentence_core + " you have also ordered " + sentence_2 + ". They are coming right now!"

        return sentence

    # By using this method we are preventing from the confusion that if tea is ordered but not specified.
    def check_general_drinks(self, list_drink):
        list_drink_new = []
        for each in list_drink:
            list_drink_new.append(str(each))
        flag = 0
        thereistea = 0
        if "tea" in list_drink_new:
            thereistea = 1
        else:
            thereistea = 0
        if thereistea==0:
            flag = 1
            return list_drink_new
        else:
            for each in self.tea:
                if each in list_drink_new:
                    flag = 1
        
        if flag == 0:
            ask_specially = "Which kind of tea would you have? We are selling black tea, jasmine and green tea."
            self.settings.speech_generator(ask_specially)
            answer_special = self.settings.get_the_message()
            answer_special = answer_special.lower()
            print(20*"*")
            print(answer_special)
            print(20*"*")
            
            answer_doc = self.nlp(answer_special)
            possible_pronouns = self.collect_NNP(answer_doc)
            possible_nouns = self.collect_nouns(answer_doc)
            possible_compounds = self.collect_compounds(answer_doc)
            possible_drinks = possible_nouns + possible_compounds+ possible_pronouns
            
            for each in list_drink_new:
                if each != "tea":
                    possible_drinks.append(each)
            return possible_drinks
        else:
            return list_drink_new
    
    # We are checking whether the list of the drink contains alcohol or not and returns number of alcoholic drinks,
    # indexes of alcoholic drinks in the list of the drinks and the list of the alcoholic drinks.
    def check_alcohol(self, list_drink_doc):
        list_drink = []
        for each in list_drink_doc:
            list_drink.append(str(each))
        
        print(list_drink)
        count = 0
        alcohol_drinks = []
        alcohol_indexes = []
        for each in self.alcohol:
            if each in list_drink:
                count = count + 1
                alcohol_drinks.append(each)
                alcohol_indexes.append(list_drink.index(each))
        return alcohol_drinks, alcohol_indexes, count
    
    # if age of user is less than 18, then alcoholic drinks will be deleted from the list of drinks.
    def delete_alcohols(self, list_drink, alcohol_indexes):
        list_drink_temp = list_drink
        if alcohol_indexes:
            for each in range(len(alcohol_indexes)-1,-1,-1):
                del list_drink_temp[alcohol_indexes[each]]
        return list_drink_temp
    
    def check_order(self, order_doc):
        
        flag_rejection = 0
        order_tokens = self.get_all_tokens_as_list(order_doc)

        for each in order_tokens:
            if each in self.rejection:
                flag_rejection = 1
        
        if flag_rejection == 0:
            drinks = []
            poss_compounds = self.collect_compounds(order_doc)
            poss_nouns = self.collect_nouns(order_doc)
            poss_pronouns = self.collect_NNP(order_doc)
            drinks = poss_compounds + poss_nouns + poss_pronouns    
            if drinks:
                return True
            else:
                return False
        else:
            return True




    # asking the age of the user in order to check that the alcoholic drinks are eligible to sell to that user or not.
    def ask_customer_age(self, list_drink):
        list_drink_temp = list_drink
        case = 0

        alcohol_drinks, alcohol_indexes, count = self.check_alcohol(list_drink)
        print(alcohol_drinks)
        if count == 0:
            case = 0
            return list_drink, case
        else:
            drinks_alc = alcohol_drinks[0]
            if len(alcohol_drinks)==1:
                sentence = "You have ordered " + drinks_alc + ", which is alcoholic drink. Could you please tell me your age?"
            else:
                if len(alcohol_drinks)==2:
                    sentence = "You have ordered " + alcohol_drinks[0] + " and " + alcohol_drinks[1] + ", which are alcoholic drinks. Could you please tell me your age?"
                else:
                    for each_alc in range(1, len(alcohol_drinks)-1):
                        drinks_alc = drinks_alc + ", " + alcohol_drinks[each_alc]
                    sentence = "You have ordered " + drinks_alc + " and " + alcohol_drinks[len(alcohol_drinks)-1] + ", which are alcoholic drinks. Could you please tell me your age?" 
            
            repeat_age_asking = "Sorry, I could not understand. Could you please tell me how old are you ?"
            ans_age = ""
            self.settings.speech_generator(sentence)
            answer_age = self.settings.get_the_message()
            ans_age_doc = self.nlp(answer_age)
            for each in ans_age_doc:
                if each.pos == NUM:
                    ans_age = int(str(each))
            while not ans_age:
                self.settings.speech_generator(repeat_age_asking)
                answer_age = self.settings.get_the_message()
            ans_age_doc = self.nlp(answer_age)
                
            for each in ans_age_doc:
                if each.pos == NUM:
                    ans_age = int(str(each))

            if len(list_drink) == count:
                if ans_age>=18:
                    list_for_over = list_drink
                    case = 1
                    return list_for_over, case
                else:    
                    case = 2
                    list_for_under = self.delete_alcohols(list_drink_temp, alcohol_indexes)
                    return list_for_under, case
            else:
                if ans_age>=18:
                    list_for_over = list_drink
                    case = 3
                    return list_for_over, case 
                else:
                    list_for_under = self.delete_alcohols(list_drink_temp, alcohol_indexes)
                    case = 4
                    return list_for_under, case 
                # case 3 and 4 if all orders are not alcoholic. 
                # case 1 and 2 if all orders are alcoholic.


    # By using this following method we are getting all tokens of the sentence as a list of strings
    def get_all_tokens_as_list(self, doc):
        token_list = []
        tokens = [token.text for token in doc]
        for each in tokens:
            token_list.append(str(each))
        return token_list

    # This function does all main checkings, and according to the results answers to the customers.
    def answer_of_the_bot(self, order_doc):
        drink = []
        flag_rejection = 0
        order_tokens = self.get_all_tokens_as_list(order_doc)
        
        for each in order_tokens:
            if each in self.rejection:
                flag_rejection = 1

        if flag_rejection == 1:
            return flag_rejection
        else:
            possible_pronouns = self.collect_NNP(order_doc)
            possible_nouns = self.collect_nouns(order_doc)
            possible_compounds = self.collect_compounds(order_doc)
            possible_drinks = possible_compounds + possible_nouns + possible_pronouns
            drink = self.check_general_drinks(possible_drinks)
            print(drink)
            if self.check_if_drink_available(drink):
                drink = self.check_if_drink_available(drink)    
                drink, case = self.ask_customer_age(drink)
                sentence = self.answer_to_the_order(drink, case = case)
            else:
                drink, case = self.ask_customer_age(drink)
                sentence = self.answer_to_the_order(drink, availability = False, case = case)
            
            self.settings.speech_generator(sentence)
            print(flag_rejection)
            return flag_rejection