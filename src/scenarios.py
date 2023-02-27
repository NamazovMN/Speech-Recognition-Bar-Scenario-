from src.nlp import ProcessOrder
from src.get_message import Listen


class ProcessScenario:
    """
    Class is used to collect and perform all possible scenarios
    """
    def __init__(self):
        """
        Method is an initializer of the class
        """
        self.mic = Listen()
        self.menu, self.hots, self.colds_non, self.cold_alc = self.define_menu()
        self.process_scenarios()

    @staticmethod
    def define_menu() -> tuple:
        """
        Method is utilized to define menu and list of each drinks for checking them.
        :return: tuple which contains string which informs user about the menu, list of hot drinks, non-alcoholic cold
        drinks and alcoholic cold drinks
        """
        hot_drinks = ['filter coffee', 'cappuccino', 'black tea', 'jasmine tea', 'green tea', 'espresso']
        non_alcoholic_cold = ['apple juice', 'orange juice', 'mango juice', 'pineapple juice', 'cola', 'fanta',
                              'water', 'sparkling water', 'sprite', 'lemonade']
        alcoholic_cold = ['whiskey', 'tequila', 'vodka', 'beer', 'prosecco']
        menu = f'Hello! Welcome to the MagaBar! As hot drinks we have {", ".join(hot_drinks)}, as cold ' \
               f'alcoholic drinks we have {", ".join(alcoholic_cold)} and as non-alcoholic cold drinks we ' \
               f'have {", ".join(non_alcoholic_cold)}'
        return menu, hot_drinks, non_alcoholic_cold, alcoholic_cold

    def process_age(self) -> bool:
        """
        Method is utilized to check the user's age: True if it is higher than 18, False otherwise. Note: it is asked
        when user orders alcoholic drinks
        :return: boolean variable specifies whether user old enough for alcoholic beverages or not
        """
        age_sentence = self.mic.get_the_order('You ordered alcoholic beverages. Could you please tell me your age?')

        age_process = ProcessOrder(age_sentence)
        result = age_process.get_single_pos('CD')
        while len(result) != 1:
            self.mic.speak('It is not understandable. Please just say your age!')
            result = input('It is not understandable. Please just say your age!')
            age_process = ProcessOrder(result)
            result = age_process.get_single_pos('CD')
        if int(result[0]) >= 18:
            return True
        else:
            self.mic.speak('Unfortunately, we are not allowed to serve alcoholic beverages to you, because of you age!')
            return False

    @staticmethod
    def process_order(order: str) -> list:
        """
        Method is utilized to process user's order. So that it checks nouns and noun phrases in order to determine
        user's order
        :param order: text which was provided by user
        :return: list of possible beverages that user's order includes
        """
        process_order = ProcessOrder(order)
        possible_combinations = [['NOUN', 'NOUN'], ['ADJ', 'NOUN'], ['PROPN', 'PROPN'], ['PROPN', 'NOUN']]
        result_list = list()
        for each_combination in possible_combinations:
            result_list.extend(process_order.collect_double_combinations(each_combination))
        single_items = process_order.get_single_pos('NN')
        result_list.extend(single_items)
        return result_list

    def check_drink(self, possible_drinks: list) -> tuple:
        """
        Method is utilized to check user's drinks. All drinks are filtered here, so that age control is also applied
        :param possible_drinks: list of all possible drinks
        :return: tuple of allowed drinks and alcohol refuse, which is boolean flag states whether age is under 18 (True)
                or not (False)
        """
        unique_list = set(possible_drinks)
        alc_drinks = list()
        non_alc_drinks = list()
        alcohol_refuse = False
        for each_drink in unique_list:
            if each_drink in self.hots or each_drink in self.colds_non:
                non_alc_drinks.append(each_drink)
            elif each_drink in self.cold_alc:
                alc_drinks.append(each_drink)
            else:
                pass
        if len(alc_drinks):
            if self.process_age():
                drinks = non_alc_drinks + alc_drinks

            else:
                alcohol_refuse = True
                drinks = non_alc_drinks
        else:
            drinks = non_alc_drinks

        return drinks, alcohol_refuse

    def serve_drinks(self, drinks: list, alcohol_refuse: bool) -> None:
        """
        Method is utilized to perform serving scene of the scenario
        :param drinks: list of servable drinks
        :param alcohol_refuse: boolean flag specifies whether user's age is under 18 (True) or not (False). Answer is
                dependent on this parameter
        :return: None
        """
        print(drinks)
        if len(drinks):
            servable = ', '.join(drinks)
            sentence = f'Here is your beverages: {servable}. Do you want anything else?'
        else:

            sentence = 'Do you want anything else?' if alcohol_refuse else \
                f'Unfortunately we cannot serve you anything since we dont have. Do you want anything else?'

        self.process_scenarios(sentence)

    def check_refusal(self, order: str) -> bool:
        """
        Method is utilized to decide about terminating the process or not. If answer contains one of the elements of
        the provided list, process will be terminated automatically
        :param order: answer of the user, that will be checked for termination
        :return: boolean variable to terminate (True) the process or not (False)
        """
        set_flag = 0
        refusal_quotes = ['no thanks', 'no', 'thanks']
        for each in refusal_quotes:
            if each in order:
                self.mic.speak('That was nice to have you! Come again please!')
                set_flag = 1
                break
        return True if set_flag else False

    def process_scenarios(self, message: str = None) -> None:
        """
        Method performs as a main function of this class and the project, so that all scenarios are controlled over
        this method.
        :param message: string object for the message to the user. If it is none then it is initial message, so that
                menu will be introduced to the user.
        :return: None
        """
        if message is None:
            self.mic.speak(self.menu)
            self.mic.init_mic()

        init_message = "What would you like to drink?" if message is None else message
        initial_order = self.mic.get_the_order(init_message).lower()
        if self.check_refusal(initial_order):
            exit()
        else:
            possible_drinks = self.process_order(initial_order)
            drinks, alcohol_refuse = self.check_drink(possible_drinks)
            self.serve_drinks(drinks, alcohol_refuse)
