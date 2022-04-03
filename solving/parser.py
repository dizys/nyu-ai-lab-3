from typing import Set, Dict, Union, Tuple, List
import re

from .node import MarkovNode


class ParseError(Exception):
    """
    Parse error.
    """
    pass


def parse_reward_value(value: str) -> float:
    value = value.strip()
    return float(value)


def parse_edge_list_value(value: str) -> List[str]:
    value = value.strip()
    if len(value) <= 2 or value[0] != "[" or value[-1] != "]":
        raise ParseError(f"Invalid edge list \"{value}\"")
    edge_list = [x.strip() for x in value[1:-1].split(",")]
    return edge_list


def parse_prob_list_value(value: str) -> List[float]:
    value = value.strip()
    value = re.sub('\s+', ' ', value)
    prob_list = [float(x) for x in value.split(" ")]
    if len(prob_list) == 0:
        raise ParseError(f"Probability list is empty")
    elif len(prob_list) > 1:
        # Check if the sum of probabilities is 1.0
        prob_sum = sum(prob_list)
        if abs(prob_sum - 1.0) > 1e-2:
            raise ParseError(f"Probability list does not sum to 1.0")
    return prob_list


class MarkovNodeInputParser:
    """
    A text parser to parse a text file into a Markov node dictionary.
    """

    reward_dict: Dict[str, float] = {}
    prob_list_dict: Dict[str, List[float]] = {}
    edge_dict: Dict[str, List[str]] = {}

    def reset(self):
        """
        Resets the parser states.
        """
        self.reward_dict = {}
        self.prob_list_dict = {}
        self.edge_dict = {}

    def parse_text_into_states(self, text: str) -> None:
        """
        Parses the text into class states, prepare for further parsing.
        """
        for i, line in enumerate(text.splitlines()):
            try:
                line = line.strip()
                if line.startswith("#") or len(line) == 0:
                    continue
                if line.find("=") != -1:
                    name, value = line.split("=")
                    name = name.strip()
                    self.reward_dict[name] = parse_reward_value(value)
                elif line.find(":") != -1:
                    name, value = line.split(":")
                    name = name.strip()
                    self.edge_dict[name] = parse_edge_list_value(value)
                elif line.find("%") != -1:
                    name, value = line.split("%")
                    name = name.strip()
                    self.prob_list_dict[name] = parse_prob_list_value(value)
                else:
                    raise ParseError(f"Invalid line \"{line}\"")
            except ParseError as e:
                raise ParseError(f"Error parsing input line {i + 1}: {e}")

    def build_node(self, name: str) -> MarkovNode:
        """
        Builds a Markov node with the given name from the class states.
        """
        reward = self.reward_dict[name] if name in self.reward_dict else 0.0
        edges: Union[List[str], None] = None
        prob_dict: Union[Dict[str, float], None] = None
        policy: Union[Tuple[str, float], None] = None

        if name not in self.edge_dict or len(self.edge_dict[name]) == 0:
            # Terminal node with no edges
            if name in self.prob_list_dict:
                raise ParseError(
                    f"Node \"{name}\" has a probability list but no edges")
        else:
            edges = self.edge_dict[name]

            if name not in self.prob_list_dict:
                if len(edges) == 1:
                    # Chance node with single edge
                    prob_dict = {edges[0]: 1.0}
                else:
                    # Decision node with no probability list
                    policy = (edges[0], 1.0)
            else:
                prob_list = self.prob_list_dict[name]
                if len(prob_list) == 1:
                    # Decision node with a single probability
                    policy = (edges[0], prob_list[0])
                else:
                    # Chance node with a probability list
                    if len(prob_list) != len(edges):
                        raise ParseError(
                            f"Probability list length does not match edge list length for node \"{name}\"")
                    prob_dict = dict(zip(edges, prob_list))

        return MarkovNode(
            name=name, reward=reward, edges=edges, prob_dict=prob_dict, policy=policy, value=reward)

    def build_node_dict(self) -> Dict[str, MarkovNode]:
        """
        Builds a Markov node dictionary containing all nodes from the class states.
        """
        node_dict: Dict[str, MarkovNode] = {}

        node_name_set: Set[str] = set(
            [*self.edge_dict.keys(), *self.reward_dict.keys()])

        for name in node_name_set:
            node_dict[name] = self.build_node(name)

        return node_dict

    def parse(self, text: str) -> Dict[str, MarkovNode]:
        """
        Parses the text into a Markov node dictionary.
        """
        self.reset()
        self.parse_text_into_states(text)
        return self.build_node_dict()
