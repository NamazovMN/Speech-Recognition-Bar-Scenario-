from typing import Any

import spacy
from spacy.matcher import Matcher
from nltk import Tree
from spacy.tokens.token import Token


class ProcessOrder:
    """
    Class is utilized to configure NLP related tasks of the project
    """

    def __init__(self, order: str):
        """
        Method is utilized as an initializer for the class
        :param order: string which specifies the script of the user's order
        """
        self.nlp = spacy.load('en_core_web_sm')
        self.matcher = Matcher(self.nlp.vocab)
        self.order = self.tokenize_order(order)
        self.get_tree()

    def tokenize_order(self, order: str):
        """
        Method is utilized to generate nlp document from the provided order sentence
        :param order: scripts of the user's order
        :return: nlp doc of the user's order
        """
        return self.nlp(order)

    def collect_double_combinations(self, combination: list) -> list:
        """
        Method is utilized to match provided pos tag combinations in the user's order (e.g., orange juice)
        :param combination: list of two pos tag combinations
        :return: list of extracted matches from the provided order
        """
        pattern = [[{'POS': combination[0]}, {'POS': combination[1]}]]
        self.matcher.add("None", patterns=pattern)
        matches = self.matcher(self.order)
        request = [self.order[start: end].text for _, start, end in matches]
        return request

    def get_single_pos(self, pos_name: str) -> list:
        """
        Method is utilized to extract token which carries the provided pos tag
        :param pos_name: Part of Speech that is requested to extract
        :return: list of tokens that carry the provided pos
        """
        result = [each.text for each in self.order if each.tag_ == pos_name]
        return result

    @staticmethod
    def token_format(node: Token) -> str:
        """
        Method is utilized to combine token and its pos tag for the tree representation
        :param node: node which is token in the nlp doc format
        :return: string in which token and its pos tag are attached
        """
        return "_".join([node.orth_, node.tag_])

    def get_token_tree(self, node: Token) -> Any:
        """
        Method is utilized to generate token tree according to the provided node, recursively.
        :param node: node that is used as a source for tree generation
        :return: it either returns tree object or the last node of the tree to be analyzed
        """
        if node.n_lefts + node.n_rights > 0:
            return Tree(self.token_format(node), [self.get_token_tree(child) for child in node.children])
        else:
            return self.token_format(node)

    def get_tree(self):
        """
        Method is utilized to build generic tree of the order, in case it includes more than one sentence.
        :return:
        """
        for sentence in self.order.sents:
            node = sentence.root
            tree = self.get_token_tree(node)
            if type(tree) == Tree:
                tree.pretty_print()
