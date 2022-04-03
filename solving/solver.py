from typing import Dict, List
from .node import MarkovNode


class MarkovSolver:
    """
    A generic MDP solver.
    """
    node_dict: Dict[str, MarkovNode]
    discount: float
    min: bool
    tolerance: float
    iteration: int

    def __init__(self, node_dict: Dict[str, MarkovNode], discount: float = 1.0, min: bool = False, tolerance: float = 0.01, iteration: int = 100):
        self.node_dict = node_dict
        self.discount = discount
        self.min = min
        self.tolerance = tolerance
        self.iteration = iteration

    def compute_value(self, node: MarkovNode) -> float:
        """
        Compute the new value of the node.
        """
        if node['edges'] is None:
            return node['reward']
        edge_value_sum = 0.0
        if node['policy'] is None:
            for edge in node['edges']:
                edge_value_sum += node['prob_dict'][edge] * \
                    self.node_dict[edge]['value']
        else:
            policy_node_name, policy_prob = node['policy']
            edge_len = len(node['edges'])
            for edge in node['edges']:
                if edge == policy_node_name:
                    edge_value_sum += policy_prob * \
                        self.node_dict[edge]['value']
                else:
                    edge_value_sum += ((1 - policy_prob) / (edge_len - 1)) * \
                        self.node_dict[edge]['value']
        return node['reward'] + self.discount * edge_value_sum

    def value_iteration_step(self) -> float:
        """
        Compute new values for all nodes and replace. Returns the maximum change.
        """
        new_node_dict: Dict[str, MarkovNode] = {}

        max_delta = 0.0

        for node in self.node_dict.values():
            new_node = node.copy()
            new_node['value'] = self.compute_value(node)
            new_node_dict[node['name']] = new_node
            delta = abs(new_node['value'] - node['value'])
            if delta > max_delta:
                max_delta = delta

        self.node_dict = new_node_dict

        return max_delta

    def value_iteration(self) -> None:
        """
        Perform value iteration.
        """
        for _ in range(self.iteration):
            delta = self.value_iteration_step()
            if delta <= self.tolerance:
                break

    def update_node_greedy_policy(self, node: MarkovNode) -> bool:
        """
        Update the greedy policy of the node.
        Returns True if the policy is changed.
        """
        edge_candidate = node['policy'][0]
        edge_candidate_value = self.node_dict[edge_candidate]['value']
        for edge in node['edges']:
            if edge == edge_candidate:
                continue
            edge_value = self.node_dict[edge]['value']
            if (self.min and edge_value < edge_candidate_value) or (not self.min and edge_value > edge_candidate_value):
                edge_candidate = edge
                edge_candidate_value = edge_value
        if edge_candidate != node['policy'][0]:
            node['policy'] = (edge_candidate, node['policy'][1])
            return True
        return False

    def greedy_policy_computation(self) -> bool:
        """
        Update the policy of all nodes.
        """
        policy_change = False
        for node in self.node_dict.values():
            if node['policy'] is None:
                continue
            policy_change |= self.update_node_greedy_policy(node)

        return policy_change

    def solve(self) -> None:
        """
        Solve the MDP.
        """
        while True:
            self.value_iteration()
            if not self.greedy_policy_computation():
                break

    def print_policy(self) -> None:
        """
        Print the current policy of all nodes.
        """
        nodes = sorted(self.node_dict.values(), key=lambda x: x['name'])
        for node in nodes:
            if node['policy'] is None:
                continue
            print(f"{node['name']} -> {node['policy'][0]}")

    def print_value(self) -> None:
        """
        Print the current value of all nodes.
        """
        eqs: List[str] = []
        nodes = sorted(self.node_dict.values(), key=lambda x: x['name'])
        for node in nodes:
            eqs.append(f"{node['name']}={node['value']:.3f}")
        print(f"{' '.join(eqs)}")

    def print(self) -> None:
        """
        Print the current policy and value of all nodes.
        """
        self.print_policy()
        print("")
        self.print_value()
