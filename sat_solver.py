import numpy as np
from variable import reset_calls, increment_calls, value_calls
from FORM import FORM, PROP


def naive_solve(formula):
    props = list(formula.get_prop_set())#list of labels for props
    assignment = {}
    for i in range(2 ** len(props)):
        assignment_array = sat_solver.num_to_vec_bitstring(i,len(props))
        for ii in range(len(props)):
            assignment[props[ii]] = (assignment_array[ii] == True)
        if formula.evaluate(assignment):
            return assignment
    return 'UNSAT'

def tree_solve_random(formula):
    props = list(formula.get_prop_set())
    for bool in [True, False]:
        assignment = {props[0]:bool}
        set_result = formula.set(assignment)
        #base case
        if set_result == True:
            return assignment
        elif set_result == False:
            continue
        #recursive case
        else: #isinstance(set_result, FORM):
            result = tree_solve_random(set_result)
            if isinstance(result, dict):
                result.update({props[0]:bool})
                result.update({key: False for key in list(set(props).difference(set(result.keys())))})
                return result
    return 'UNSAT'



def tree_solve(formula, unit_preference = False, two_clause = False, polarity = False):
    increment_calls()
    if isinstance(formula, PROP):
        return {formula.label: formula.operator != 'NOT'}
    prop, booleans = formula.heuristic_assignment(unit_preference,two_clause,polarity)
    for bool in booleans:
        assignment = {prop:bool}
        set_result = formula.set(assignment)
        #base case
        if set_result == True:
            return assignment
        elif set_result == False:
            continue
        #recursive case
        else: #isinstance(set_result, FORM):
            result = tree_solve(set_result, unit_preference, two_clause, polarity)
            if isinstance(result, dict):
                result.update({prop:bool})
                return result
    return 'UNSAT'








class sat_solver():
    def __init__(self) -> None:
        pass

    def num_to_vec_bitstring(number, width):
        return np.array([int(i) for i in (list(np.binary_repr(number,width=width)))])
    
    def find_unit(formula):#and formula of cnf form
        if isinstance(formula,PROP):
            return formula
        for clause in formula.sub_formulas:
            if clause.sub_formulas != None and len(clause.sub_formulas) == 1:
                return clause.sub_formulas[0]
        return None
    
    def unit_assignment(formula):
        if formula.operator == 'OR':
            return False
        unit = sat_solver.find_unit(formula)
        if unit != None:
            return {unit.label: unit.operator != 'NOT'}
        return False
    
    def find_contradiction(formula):
        units = []
        for clause in formula.sub_formulas:
            if isinstance(clause, PROP):
                label = clause.label if clause.operator != 'NOT' else -clause.label
                if -label in units:
                    return True
                units.append(label)
        return False