#!/usr/bin/env python3

#######################################################################
#
# Author: Martha Maria Del Toro Carballo
# Copyright 2023
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

"""
Summary:
Algorithm to provide users with explanations for understanding planner decisions 
when eliminating redundant actions from plans to enhance quality.

The algorithm compares an original plan with its perfectly justified 
counterpart, extracting and analyzing causal links. If no differences are found, 
no explanation is generated, indicating the original plan is already perfectly
justified.

However, if differences are detected, the algorithm follows these steps:
(1) Identifying and presenting irrelevant objects for the plan: 
Objects present in the initial state, not in objectives, and unused in relevant 
actions. 
(2) Finding and explaining unjustified chains of actions: 
Sequences in the unjustified plan producing an event for a relevant action in 
the perfectly justified plan, considered unnecessary. 
(3) Explaining reasons for action redundancy in the unjustified plan, leading to 
elimination and resulting in the perfectly justified plan. 
(4) Providing explanations for relevant actions in the perfectly justified plan, 
highlighting dependencies and illustrating execution in the unjustified plan.
"""


import argparse
import sys

from copy import deepcopy
from collections import defaultdict
from plan_parser import parse_plan
from sas_parser import parse_task


def show_redundant_objects(list_actions_plan, list_pos_redundant_actions):
    """
    Display redundant objects based on the provided list of actions in a plan
    and the positions of redundant actions in the plan.

    Args:
    - list_actions_plan (list): A list representing the actions in the plan.
    - list_pos_redundant_actions (list): Positions of redundant actions in the
    plan.

    Returns:
    None
    """
    while True:
        show_irrelevant_objects = input(
            "\nWould you like to obtain redundant objects? (Yes/No): "
        ).lower()
        if show_irrelevant_objects == "no":
            print("Obtaining redundant objects finished.")
            break
        elif show_irrelevant_objects == "yes":
            list_irrelevant_objects = identifying_redundant_objects(
                list_actions_plan, list_pos_redundant_actions
            )
            # Printing irrelevant objects, in case they exist (those not found
            # in relevant actions)
            if len(list_irrelevant_objects) == 0:
                print("There are no irrelevant objects.")
            elif len(list_irrelevant_objects) > 1:
                objects_str = (
                    ", ".join(list_irrelevant_objects[:-1])
                    + " and "
                    + list_irrelevant_objects[-1]
                )
                print(
                    f"--> Objects {objects_str} are irrelevant because they are"
                    f" not used in any Relevant Action."
                )
            else:
                objects_str = list_irrelevant_objects[0]
                print(
                    f"--> Object {objects_str} is irrelevant because "
                    f"it is not used in any Relevant Action."
                )
            break
        else:
            print("You have entered an invalid option.")


def identifying_redundant_objects(list_actions_plan, list_pos_redundant_actions):
    """
    Identify and return the objects considered redundant in a plan.

    Args:
    - list_actions_plan (list): A list representing the actions in the plan.
    - list_pos_redundant_actions (list): Positions of redundant actions in the plan.

    Returns:
    list: A list of objects considered redundant in the plan.
    """
    list_all_objects = []
    list_relevant_objects = []
    # Objects present in relevant actions are considered relevant, regardless
    # of their presence in the goal state; otherwise, they are not considered
    # relevant.
    for i, action in enumerate(list_actions_plan):
        objects = action[action.find(" ") + 1 : -1].split()
        list_all_objects = list(set(list_all_objects) | set(objects))
        if (i + 1) not in list_pos_redundant_actions:
            list_relevant_objects = list(set(list_relevant_objects) | set(objects))

    list_irrelevant_objects = list(set(list_all_objects) - set(list_relevant_objects))
    return list_irrelevant_objects


def get_operators_from_plan(operators, plan, operator_name_to_index, ordered):
    """
    Select and return the operators from the task planning domain (SAS+) that
    are present in the given plan.

    Args:
    - operators (list): A list of all operators in the task planning domain (SAS+).
    - plan (list): A list representing the actions in the plan.
    - operator_name_to_index (dict): A dictionary mapping operator names to their
    indices.
    - ordered (bool): A boolean indicating whether the tasks in the plan are
    ordered or unordered.

    Returns:
    list: A list of selected operators from the planning domain based on their
    presence in the plan.
    """
    plan_operators = []
    added = set()

    for op in plan:
        if "skip-action" in op:
            plan_operators += [None]
        else:
            if ordered:
                # Ordered tasks create a different operator for each operator in the plan
                plan_operators += [deepcopy(operators[operator_name_to_index[op]])]
            else:
                # Unordered tasks create a different operator for each unique operator in the plan
                # added.add(op) is only used for its' side effects.
                # set.add(x) always returns None so it doesn't affect the condition
                if not op in added or added.add(op):
                    plan_operators += [operators[operator_name_to_index[op]]]
    return plan_operators


def is_perfectly_justified(plan):
    """
    Determine if a given plan is perfectly justified.

    Args:
    - plan (list): A list representing the actions in the plan.

    Returns:
    bool: True if the plan is perfectly justified, False otherwise.
    """
    for action in plan:
        if "skip-action" in action:
            return False
    return True


def get_var_pre_post_list(operators):
    """
    Generates a combined list of variable preconditions, prevail conditions, and effects
    for a given list of operators.

    Args:
    - operators (list): A list of operators representing actions of the plan.

    Returns:
    tuple: A tuple containing two lists:
        - A list of tuples, where each tuple contains two sublists:
            - Combined variable preconditions and prevail conditions for an operator.
            - A list of variable effects for the corresponding operator.
        - A list of prevail conditions for each operator.
    """
    op_precond_list = []
    op_prevail_list = []
    op_eff_list = []

    for op in operators:
        op_precond = []
        op_prevail = []
        op_eff = []

        if not op is None:
            for prevail_val in op.prevail:
                op_prevail += [(prevail_val[0], prevail_val[1])]
            for var, precond_val, eff_val, _ in op.pre_post:
                op_precond += [(var, precond_val)]
                op_eff += [(var, eff_val)]

        op_precond_list += [op_precond]
        op_prevail_list += [op_prevail]
        op_eff_list += [op_eff]

    precond_prevail_list = []
    for precond_sublist, prevail_sublist in zip(op_precond_list, op_prevail_list):
        if not prevail_sublist:
            precond_prevail_list.append(precond_sublist)
        else:
            precond_prevail_combined = precond_sublist + prevail_sublist
            precond_prevail_list.append(precond_prevail_combined)

    return list(zip(precond_prevail_list, op_eff_list)), op_prevail_list


def get_prevail_link(prevail_link):
    """
    Extracts and processes information from a prevail link.

    Args:
    - prevail_link (tuple): A tuple representing a prevail link with the following elements:
        - producers_list (list): A list of producer indices.
        - fact (tuple): A tuple representing a fact with two values.
        - consumer (int): The index of the consumer.

    Returns:
    tuple: A tuple containing the processed prevail link information:
        - The index of the last producer for the consumer.
        - The fact tuple.
        - The index of the consumer.
    """
    producers_list, fact, consumer = prevail_link
    producers_list.sort()

    last_producer_for_consumer = max(filter(lambda x: x < consumer, producers_list))

    return (last_producer_for_consumer, fact, consumer)


def initialize_causal_links(task):
    """
    Initializes the list of causal links based on the initial state of the SAS+ planning task.

    Args:
    - task (SASTask): The SAS+ planning task.

    Returns:
    - list: List of initial causal links in the form [[[0], (var, val), []], ...],
    where var and val represent the variable and its value in the initial state.
    """
    # Obtain the values of the initial state of the form (var,val)
    return [
        [[0], (var, task.init.values[var]), []] for var in range(len(task.init.values))
    ]


def finalize_causal_links(list_causal_links, task):
    """
    Finalizes the list of causal links by formatting them into a more readable form.

    Args:
    - list_causal_links (list): List of causal links in the form [[producers, fact, consumers], ...].
    - task (SASPlusTask): The SAS+ planning task.

    Returns:
    - list: List of finalized causal links in the form [(producer, fact, consumer), ...],
    where producer, fact, and consumer are indices, variable-value pairs, and indices, respectively.
    """
    list_causal_links_final = []
    for i in range(len(list_causal_links)):
        causal_link_temp = list_causal_links[i]
        fact = task.variables.value_names[causal_link_temp[1][0]][
            causal_link_temp[1][1]
        ]
        producers = causal_link_temp[0]
        consumers = causal_link_temp[2]
        if "NegatedAtom" not in fact:
            for j in range(len(producers)):
                if j < len(consumers):
                    list_causal_links_final.append(
                        (producers[j], causal_link_temp[1], consumers[j])
                    )
                else:
                    list_causal_links_final.append(
                        (producers[j], causal_link_temp[1], -1)
                    )

    return list_causal_links_final


def finalize_prevail_links(list_causal_links_prevail, task):
    """
    Finalizes the list of prevail links by formatting them into a more readable form.

    Args:
    - list_causal_links_prevail (list): List of prevail links in the form [prevail_link, ...].
    - task (SASTask): The SAS+ planning task.

    Returns:
    - list: List of finalized prevail links in the form [(producer, fact, consumer), ...],
    where producer, fact, and consumer are indices, variable-value pairs, and indices, respectively.
    """
    list_prevail_links_final = []
    for producer, (var, val), consumer in list_causal_links_prevail:
        if "NegatedAtom" not in task.variables.value_names[var][val]:
            list_prevail_links_final.append((producer, (var, val), consumer))

    return list_prevail_links_final


def update_causal_links(list_causal_links, list_var_pre_post, op_prevail_list):
    """
    Updates the list of causal links based on variable preconditions, effects, and prevail conditions.

    Args:
    - list_causal_links (list): List of causal links in the form [[producers, fact, consumers], ...].
    - list_var_pre_post (list): List of variable preconditions and effects for each operator.
    - op_prevail_list (list): List of prevail conditions for each operator.

    Returns:
    - list: List of finalized prevail links in the form [(producer, fact, consumer), ...],
    where producer, fact, and consumer are indices, variable-value pairs, and indices, respectively.
    """
    list_causal_links_prevail = []

    for i in range(len(list_var_pre_post)):
        list_precond = list_var_pre_post[i][0]
        list_effects = list_var_pre_post[i][1]
        for j in range(len(list_precond)):
            fact = list_precond[j]
            for k in range(len(list_causal_links)):
                causal_link_temp = list_causal_links[k]
                if causal_link_temp[1] == fact or (
                    causal_link_temp[1][1] == -fact[1]
                    and causal_link_temp[1][0] == fact[0]
                ):
                    if fact not in op_prevail_list[i]:
                        list_causal_links[k][2].append(i + 1)
                    else:
                        causal_link_prevail = (
                            list_causal_links[k][0],
                            fact,
                            i + 1,
                        )
                        list_causal_links_prevail.append(causal_link_prevail)

        for l in range(len(list_effects)):
            fact = list_effects[l]
            exist = False
            for k in range(len(list_causal_links)):
                causal_link_temp = list_causal_links[k]
                if causal_link_temp[1] == fact:
                    exist = True
                    list_causal_links[k][0].append(i + 1)
                    break
            if not exist:
                list_causal_links.append([[i + 1], fact, []])

    return [
        get_prevail_link(prevail_link) for prevail_link in list_causal_links_prevail
    ]


def extract_causal_prevail_links(task, plan_operators):
    """
    Extracts causal links and prevail conditions from a SAS+ planning task.

    Args:
    - task (SASTask): The SAS+ planning task.
    - plan_operators (list): List of operators of the plan.

    Returns:
    - tuple: A tuple containing two lists:
        - list_causal_links_final: List of causal links in the form (producer, fact, consumer).
        - list_prevail_links_final: List of prevail conditions in the form (producer, fact, consumer).
    """
    list_causal_links = initialize_causal_links(task)

    list_var_pre_post, op_prevail_list = get_var_pre_post_list(plan_operators)

    list_causal_links_prevail = update_causal_links(
        list_causal_links, list_var_pre_post, op_prevail_list
    )

    list_causal_links_final = finalize_causal_links(list_causal_links, task)
    list_prevail_links_final = finalize_prevail_links(list_causal_links_prevail, task)

    return list_causal_links_final, list_prevail_links_final


def pretty_print_causal_links(list_cl, plan_op, task):
    """
    Prints the causal links with their corresponding operators and variable values.

    Args:
    - list_cl (list): List of causal links in the form [(producer, (var, value), consumer), ...].
    - plan_op (list): List of operators representing the plan.
    - task (SASTask): The SAS+ planning task.
    """
    for prod, (var, value), cons in list_cl:
        prod_name = plan_op[prod - 1].name if prod > 0 else "Init"
        cons_name = plan_op[cons - 1].name if cons > 0 else "None"
        print(
            f"{prod_name :<25} -> {task.variables.value_names[var][value] :<25} -> {cons_name}"
        )


def list_cl_to_dict(list_cl, is_key_producer=True):
    """
    Converts a list of causal links into a dictionary where the keys can be the
    producers or the consumers depending on is_key_producer and the values
    lists of the remaining elements:
    producer: (consumer, var_value)
    consumer: (producer, var_value)

    Args:
    - list_cl (list): List of causal links in the form [(producer, (var, value), consumer), ...].
    - is_key_producer (bool): If True, uses producers as keys; if False, uses consumers as keys.

    Returns:
    - dict: Dictionary where keys are either producers or consumers based on the is_key_producer parameter,
      and values are lists of tuples containing the corresponding (other_element, var_value).
    """
    dict_cl = defaultdict(list)

    for producer, var_value, consumer in list_cl:
        dict_cl[producer if is_key_producer else consumer].append(
            (consumer if is_key_producer else producer, var_value)
        )

    return dict_cl


def exist_in_sas_plan(causal_link_temp_renamed, task, list_causal_links_sas_plan):
    """
    Check if a specific causal link belonging to the perfectly justified plan also exists in the unjustified plan.

    Args:
    - causal_link_temp_renamed (tuple): Renamed causal link in the form (producer, instanced_fact, consumer).
    - task (SASTask): The SAS+ planning task.
    - list_causal_links_sas_plan (list): List of causal links of the plan.

    Returns:
    - bool: True if the causal link exists in the unjustified plan, False otherwise.
    """
    for causal_link_temp in list_causal_links_sas_plan:
        fact_sas_plan = (
            causal_link_temp[0],
            task.variables.value_names[causal_link_temp[1][0]][causal_link_temp[1][1]],
            causal_link_temp[2],
        )
        if fact_sas_plan == causal_link_temp_renamed:
            return True
    return False

# TODO: FIX EVERYTHING BELOW
def causal_chain(elements, ordered_dict, element, list_temp):
    for val in elements:
        if val not in list_temp:
            list_temp.append(val)
            list_temp2 = ordered_dict.get(val, [])
            elements2 = list(set([valor[0] for valor in list_temp2]))
            causal_chain(elements2, ordered_dict, element, list_temp)
    return list_temp


def causal_chains(list_cl_plan_ae, task, list_cl_plan, ordered_dict):
    causal_chain_list = []
    for causal_link_temp in list_cl_plan_ae:
        causal_link_temp_renamed = (
            causal_link_temp[0],
            task.variables.value_names[causal_link_temp[1][0]][causal_link_temp[1][1]],
            causal_link_temp[2],
        )
        is_in_sas_plan = exist_in_sas_plan(causal_link_temp_renamed, task, list_cl_plan)
        # Identify the causal links of the justified plan that are not in the unjustified plan to find the casual chains
        if is_in_sas_plan == False and causal_link_temp[2] != -1:
            for causal_link_dict in ordered_dict[causal_link_temp[2]]:
                fact_renamed = task.variables.value_names[causal_link_dict[1][0]][
                    causal_link_dict[1][1]
                ]
                if fact_renamed == causal_link_temp_renamed[1]:
                    list_temp = ordered_dict.get(causal_link_dict[0], [])
                    elements = list(set([value[0] for value in list_temp]))
                    causal_chain_temp = [causal_link_dict[0]]
                    causal_chain_temp.extend(
                        causal_chain(
                            elements, ordered_dict, causal_link_temp_renamed[0], []
                        )
                    )
                    causal_chain_list.append(
                        (causal_link_temp, sorted(causal_chain_temp))
                    )
    return causal_chain_list


def pos_redundant_actions(sas_plan_ae):
    """
    Identify and return the positions of redundant actions (label "skip-action")
    in the perfectly justified plan.

    Args:
    - sas_plan_ae (list): List of actions in the perfectly justified plan.

    Returns:
    - list: List of positions (indices) of redundant actions found in the plan.
    """
    list_pos_redundant_actions = []
    for action in sas_plan_ae:
        if "skip-action" in action:
            pos = "".join(filter(str.isdigit, action))
            list_pos_redundant_actions.append(int(pos) + 1)
    return list_pos_redundant_actions


def convert_to_dict_producer_fact(list_action_fact):
    dict_final = {}
    for tuple in list_action_fact:
        key = tuple[0]
        value = tuple[1]

        if key in dict_final:
            dict_final[key].append(value)
        else:
            dict_final[key] = [value]
    return dict_final


def show_plan_ae(plan, plan_ae_cost, list_pos_redundant_actions):
    print(
        "\nPerfectly justified plan (the redundant actions contained in the unjustified plan are shown)"
    )
    for i in range(len(plan)):
        if (i + 1) in list_pos_redundant_actions:
            print(f"{i+1} (redundant action) --> {plan[i]}")
        else:
            print(f"{i+1} {plan[i]}")
    print(f"; cost = {plan_ae_cost} (general cost)")


def get_redundant_producer(action_number, fact, task, causal_chain_list):
    for causal_link_and_chain in causal_chain_list:
        if (
            causal_link_and_chain[0][2] == action_number
            and fact
            == task.variables.value_names[causal_link_and_chain[0][1][0]][
                causal_link_and_chain[0][1][1]
            ]
        ):
            return causal_link_and_chain[1][-1]


def get_relevant_causal_links(
    plan, relevant_action_causal_links, list_prevail_links, task
):
    list_explanations = []
    list_fact_produced_initial_state = []

    for causal_link_temp in relevant_action_causal_links:
        fact_index = causal_link_temp[1]
        fact = task.variables.value_names[fact_index[0]][fact_index[1]]
        producer = causal_link_temp[0]

        if producer == 0:
            list_fact_produced_initial_state.append(fact)
        else:
            str = f"{fact} as a precondition which is obtained through the effects produced by the Relevant Action {producer} {plan[producer-1]}"
            list_explanations.append(str)

    if len(list_fact_produced_initial_state) > 0:
        if len(list_fact_produced_initial_state) > 1:
            facts_str = (
                ", ".join(list_fact_produced_initial_state[:-1])
                + " and "
                + list_fact_produced_initial_state[-1]
                + " as preconditions which are obtained from the initial state"
            )
        else:
            facts_str = (
                list_fact_produced_initial_state[0]
                + " as a precondition which is obtained from the initial state"
            )
        list_explanations.append(facts_str)

    if len(list_prevail_links) > 0:
        list_explanations += get_justif_prevail_conditions(
            plan, list_prevail_links, task
        )

    return list_explanations


def get_justif_prevail_conditions(plan, list_prevail_links, task):
    list_explanations = []
    list_fact_produced_initial_state = []

    for prevail_link_temp in list_prevail_links:
        fact_var_val = prevail_link_temp[1]
        fact = task.variables.value_names[fact_var_val[0]][fact_var_val[1]]
        producer = prevail_link_temp[0]

        if producer == 0:
            list_fact_produced_initial_state.append(fact)
        else:
            str = f"{fact} as a prevail-condition which is obtained through the effects produced by the Relevant Action {producer} {plan[producer-1]}"
            list_explanations.append(str)

    if len(list_fact_produced_initial_state) > 0:
        if len(list_fact_produced_initial_state) > 1:
            facts_str = (
                ", ".join(list_fact_produced_initial_state[:-1])
                + " and "
                + list_fact_produced_initial_state[-1]
                + " as prevail-conditions which are obtained from the initial state."
            )
        else:
            facts_str = (
                list_fact_produced_initial_state[0]
                + " as a prevail-condition which is obtained from the initial state."
            )
        list_explanations.append(facts_str)

    return list_explanations


def generating_explanations(
    plan,
    list_pos_redundant_actions,
    list_causal_links_sas_plan,
    list_causal_links_ae_sas_plan,
    task,
    causal_chain_list,
    list_links_prevail_ae_plan,
):
    explanations_dict = {}

    while True:
        explain = input("\nWould you like to generate explanations? (Yes/No): ").lower()
        if explain == "no":
            print("Explanation generation execution is finished.")
            break
        elif explain == "yes":
            action_number_input = input("Enter the number of the action: ")
            if not action_number_input.isdigit():
                print("You have entered an invalid action number.")
            else:
                action_number = int(action_number_input)
                if 0 < action_number <= len(plan):
                    if action_number in explanations_dict:
                        print(explanations_dict[action_number])
                    else:
                        explanation_str = ""
                        explanation_str += (
                            f"\nAction #{action_number}: {plan[action_number-1]}\n"
                        )

                        relevant_action_causal_links_dict = list_cl_to_dict(
                            [tuple[0] for tuple in causal_chain_list], False
                        )
                        if (
                            len(relevant_action_causal_links_dict) == 0
                            or action_number not in relevant_action_causal_links_dict
                        ):
                            relevant_action_causal_links_dict = list_cl_to_dict(
                                list_causal_links_ae_sas_plan, False
                            )
                        redundant_action_causal_links_dict = list_cl_to_dict(
                            list_causal_links_sas_plan, True
                        )

                        prevail_links_dict = list_cl_to_dict(
                            list_links_prevail_ae_plan, False
                        )

                        if action_number in list_pos_redundant_actions:
                            consumers_list = redundant_action_causal_links_dict.get(
                                action_number, []
                            )
                            dict_temp = convert_to_dict_producer_fact(consumers_list)
                            explanation_str += "This Action is Redundant in the plan because it produces:"
                            for consumer, fact_list in dict_temp.items():
                                fact_list_renamed = [
                                    task.variables.value_names[fact[0]][fact[1]]
                                    for fact in fact_list
                                ]
                                facts_str = ""
                                if len(fact_list) == 1:
                                    facts_str = fact_list_renamed[0]
                                else:
                                    facts_str = (
                                        ", ".join(fact_list_renamed[:-1])
                                        + " and "
                                        + fact_list_renamed[-1]
                                    )
                                if consumer == -1:
                                    explanation_str += f"\n--> {facts_str} that is not consumed by any other action."
                                elif consumer in list_pos_redundant_actions:
                                    explanation_str += f"\n--> {facts_str} which is consumed by the Action {consumer} {plan[consumer-1]} also Redundant."
                                else:
                                    if consumer in prevail_links_dict:
                                        relevant_causal_links = (
                                            get_relevant_causal_links(
                                                plan,
                                                relevant_action_causal_links_dict[
                                                    consumer
                                                ],
                                                prevail_links_dict[consumer],
                                                task,
                                            )
                                        )
                                    else:
                                        relevant_causal_links = (
                                            get_relevant_causal_links(
                                                plan,
                                                relevant_action_causal_links_dict[
                                                    consumer
                                                ],
                                                [],
                                                task,
                                            )
                                        )
                                    rel_expl_str = ""
                                    if len(relevant_causal_links) == 1:
                                        rel_expl_str = relevant_causal_links[0]
                                    else:
                                        rel_expl_str = (
                                            "; ".join(relevant_causal_links[:-1])
                                            + " and "
                                            + relevant_causal_links[-1]
                                        )
                                    explanation_str += f"\n--> {facts_str} which is consumed by the Action {consumer} {plan[consumer-1]} that is Relevant. Action {consumer} in the justified plan needs {rel_expl_str}."

                        else:
                            producers_list = relevant_action_causal_links_dict.get(
                                action_number, []
                            )
                            explanation_str += "In the justified plan, in order for this Relevant Action to be executed, it requires the fact:"
                            list_fact_produced_initial_state = []
                            for element in producers_list:
                                producer, (var_index, val_index) = element
                                fact = task.variables.value_names[var_index][val_index]
                                if producer == 0:
                                    list_fact_produced_initial_state.append(fact)
                                else:
                                    redundant_action = get_redundant_producer(
                                        action_number, fact, task, causal_chain_list
                                    )
                                    if redundant_action is None:
                                        explanation_str += f"\n--> {fact} as a precondition which is obtained through the effects produced by the Relevant Action {producer} {plan[producer-1]}."
                                    else:
                                        explanation_str += f"\n--> {fact} as a precondition which is obtained through the effects produced by the Relevant Action {producer} {plan[producer-1]}. This fact, in the unjustified plan, Action {action_number} {plan[action_number-1]} obtained it through the Redundant Action {redundant_action} {plan[redundant_action-1]}."

                            facts_str = ""
                            if len(list_fact_produced_initial_state) > 1:
                                facts_str = (
                                    ", ".join(list_fact_produced_initial_state[:-1])
                                    + " and "
                                    + list_fact_produced_initial_state[-1]
                                    + " as preconditions which are obtained from the initial state."
                                )
                            if len(list_fact_produced_initial_state) == 1:
                                facts_str = (
                                    list_fact_produced_initial_state[0]
                                    + " as a precondition which is obtained from the initial state."
                                )

                            if len(facts_str) > 0:
                                explanation_str += f"\n--> {facts_str}"

                            if action_number in prevail_links_dict:
                                list_prevail_justif = get_justif_prevail_conditions(
                                    plan, prevail_links_dict[action_number], task
                                )
                                if len(list_prevail_justif) > 0:
                                    for prevail_justif in list_prevail_justif:
                                        explanation_str += f"\n--> {prevail_justif}"

                        explanations_dict[action_number] = explanation_str
                        print(explanation_str)
                else:
                    print("You have entered an invalid action number.")
        else:
            print("You have entered an invalid option.")


def showing_causal_chains(plan, causal_chain_list, task):
    while True:
        show_causal_chains = input(
            "\nWould you like to obtain the causal chains present in the unjustified plan? (Yes/No): "
        ).lower()
        if show_causal_chains == "no":
            print("Obtaining causal chains finished.")
            break
        elif show_causal_chains == "yes":
            if len(causal_chain_list) > 0:
                for causal_link_chain in causal_chain_list:
                    explanation_str = ""
                    causal_link = causal_link_chain[0]
                    causal_chain = causal_link_chain[1]
                    fact_instantiated = task.variables.value_names[causal_link[1][0]][
                        causal_link[1][1]
                    ]
                    explanation_str = (
                        f"--> Fact {fact_instantiated} is produced by the "
                    )
                    if causal_link[0] == 0:
                        explanation_str += "initial state"
                    else:
                        explanation_str += (
                            f"Action {causal_link[0]} {plan[causal_link[0]-1]} "
                        )
                    explanation_str += f" and is consumed by Action {causal_link[2]} {plan[causal_link[2]-1]} in the perfectly justified plan. In the unjustified plan, this fact would be obtained through the following causal chain of actions:"
                    producer = causal_link[0]

                    causal_chain_str = ""
                    found = False
                    for action in causal_chain:
                        if action == producer:
                            found = True
                        if found and action != 0:
                            temp = f" {plan[action-1]}"
                            causal_chain_str += " " + str(action) + temp + ","
                    explanation_str += causal_chain_str.rstrip(",")
                    print(explanation_str)

            else:
                print(
                    "There are no unnecessary or non-justified causal chains of actions because the Relevant Actions of the justified plan do not consume facts produced by Redundant Actions in the unjustified plan."
                )
            break
        else:
            print("You have entered an invalid option.")


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    required_named = parser.add_argument_group("required named arguments")
    required_named.add_argument(
        "-t",
        "--task",
        help="Path to task file in SAS+ format.",
        type=str,
        required=True,
    )
    required_named.add_argument(
        "-p", "--plan", help="Path to original plan file.", type=str, required=True
    )
    required_named.add_argument(
        "-s", "--splan", help="Path to skip plan file.", type=str, required=True
    )
    parser.add_argument(
        "--subsequence",
        help="Compiled task must guarantee maintaining order of original actions",
        action="store_true",
        default=False,
    )
    options = parser.parse_args()

    # Check files required as parameters
    if options.task == None or options.plan == None or options.splan == None:
        parser.print_help()
        sys.exit(2)

    print("\nParsing AE plan")
    ae_plan, plan_ae_cost = parse_plan(options.splan)
    print(ae_plan)

    if is_perfectly_justified(ae_plan):
        print("\nThe original plan is perfectly justified.")
    else:
        print("\nThe original plan is not perfectly justified.")

        # Extract causal links from the input plan
        # print(f"\nParsing original task")
        task, operator_name_to_index_map = parse_task(options.task)
        # print(operator_name_to_index_map)
        # task.dump()

        print("\nParsing original plan")
        plan, plan_cost = parse_plan(options.plan)
        print(plan)

        print("\nExtracting causal links from original plan")
        plan_operators = get_operators_from_plan(
            task.operators, plan, operator_name_to_index_map, options.subsequence
        )
        list_cl_plan, list_cl_prevail_plan = extract_causal_prevail_links(
            task, plan_operators
        )
        print(list_cl_plan)
        # print(list_cl_prevail_plan)
        # pretty_print_causal_links (list_cl_plan, plan_operators, task)

        print(
            "\nExtracting causal links from the justified plan (with skip actions) using original task"
        )
        # print(f"\nOp name index orig task")
        # print(operator_name_to_index_map)
        # print(f"\nOp name index ae task")
        # print(operator_name_to_index_map_ae)
        ae_plan_operators = get_operators_from_plan(
            task.operators, ae_plan, operator_name_to_index_map, options.subsequence
        )
        list_cl_ae_plan, list_cl_prevail_ae_plan = extract_causal_prevail_links(
            task, ae_plan_operators
        )
        print(list_cl_ae_plan)
        # print(list_cl_prevail_ae_plan)
        # pretty_print_causal_links (list_cl_ae_plan, ae_plan_operators, task)

        # Convert causal links of original plan into a dictionary where the keys represent the consumers and the values are lists of (producers, fact)
        # to simplify the search for causal chains
        dict_cl_plan_consumer_ordered = list_cl_to_dict(list_cl_plan, False)
        # print("\nOrdered dictionary (consumer key) causal links original plan\n", dict_cl_plan_consumer_ordered)

        # Obtain the causal chains
        # The causal chains is formed by a list containing tuples, which are formed by the causal link of the justified plan and its causal chain
        # of the unjustified plan
        print("\nExtracting causal chains")
        causal_chain_list = causal_chains(
            list_cl_ae_plan, task, list_cl_plan, dict_cl_plan_consumer_ordered
        )
        print(causal_chain_list)

        list_pos_redundant_actions = pos_redundant_actions(ae_plan)
        print(
            f"\nPositions of the redundant actions in the plan: {list_pos_redundant_actions}"
        )

        # Print plan with action elimination
        show_plan_ae(plan, plan_ae_cost, list_pos_redundant_actions)

        # Show irrelevant/redundant objects, which are those that are not needed in the perfectly justified plan
        show_redundant_objects(plan, list_pos_redundant_actions)

        # Show causal chains
        showing_causal_chains(plan, causal_chain_list, task)

        # Generating explanations for actions
        generating_explanations(
            plan,
            list_pos_redundant_actions,
            list_cl_plan,
            list_cl_ae_plan,
            task,
            causal_chain_list,
            list_cl_prevail_ae_plan,
        )


if __name__ == "__main__":
    main()
