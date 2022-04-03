from typing import TypedDict, Dict, Union, Tuple, List


class MarkovNode(TypedDict):
    """
    A Markov node.
    - name (str): The name of the node.
    - reward (float): The reward value of the node.
    - edges (List[str]): The list of edges of the node.
    - prob_dict (Dict[str, float]): The transition probability dictionary from the node, none if not a chance node.
    - policy (Tuple[str, float]): The policy of the node ([policy_node_name, success_rate]), none if not a decision node.
    """
    name: str
    reward: float
    edges: Union[List[str], None]
    prob_dict: Union[Dict[str, float], None]
    policy: Union[Tuple[str, float], None]
    value: float
