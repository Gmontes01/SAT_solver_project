class FORM():
    # All formulas will be in CNF form as specified below
    # https://www.cs.rice.edu/~vardi/comp409/satformat.pdf

    def __init__(self, sub_formulas, operator):
        self.label = None
        self.operator = operator
        self.sub_formulas = sub_formulas  # List of smaller formulas

    def write_cnf_form(self, file_name):
        # This method writes the formula in CNF format to a file.

        # Open the file for writing
        with open(file_name, "w") as f:
            # Write the problem line in the DIMACS format
            f.write(f"p cnf {len(self.get_prop_set())} {len(self.sub_formulas)}\n")

            # Iterate through each sub-formula
            for formula in self.sub_formulas:
                # Iterate through each literal in the sub-formula and write them
                for labels in list(formula.get_prop_set(signed=True)):
                    f.write(f"{labels} ")
                # Write '0' to indicate the end of the clause
                f.write("0 \n")


    def __repr__(self) -> str:
        if self.operator == 'AND':
            return f"({' ^ '.join(map(str, self.sub_formulas))})"
        elif self.operator == 'OR':
            return f"({' v '.join(map(str, self.sub_formulas))})"
        else:
            return Exception("operators not acceptable('NOT','AND','OR')")
        
    def condense(self):#one layer deep(i.e only works for cnf)
        sub_form_list = []
        for clause in self.sub_formulas:
            if isinstance(clause, PROP):
                sub_form_list.append(clause)
            elif len(clause.sub_formulas) == 1:
                sub_form_list.append(PROP(clause.sub_formulas[0].label, clause.sub_formulas[0].operator))
            elif clause.operator == self.operator:
                sub_form_list = sub_form_list + clause.sub_formulas
            else:
                sub_form_list.append(clause)
        sub_form_list = list(set(sub_form_list))
        return FORM(sub_form_list, self.operator)
        

    def heuristic_assignment(self,unit_preference = False, two_clause = False, polarity = False):
        #take in formula and heuristic parameters and return tuple (label, [assignments])
        #label is unsigned label of proposition
        if isinstance(self, PROP): #return assignment that satisfies formula
            return (self.label, [self.operator != 'NOT'])
        if not(unit_preference) and not(two_clause) and not(polarity):
            if isinstance(self.sub_formulas[0], PROP):
                return (self.sub_formulas[0].label, [True, False])
            else:
                return (self.sub_formulas[0].sub_formulas[0].label, [True, False])
        two_clause_counter = {}
        polarity_tracker = {}
        non_polar = set([])
        for clause in self.sub_formulas:
            if unit_preference and isinstance(clause, PROP):
                return (clause.label, [clause.operator != 'NOT'])
            if two_clause and not(isinstance(clause, PROP)) and len(clause.sub_formulas) == 2:
                for i in range(2):
                    prop = clause.sub_formulas[i].unsign()
                    if prop not in two_clause_counter.keys():
                        two_clause_counter[prop] = 1
                    else:
                        two_clause_counter[prop] = two_clause_counter[prop] + 1
            if polarity:
                if isinstance(clause, PROP):
                    un_prop = clause.unsign()
                    if not(un_prop in non_polar):
                        if un_prop in polarity_tracker.keys():
                            if polarity_tracker[un_prop] != (clause.operator != 'NOT'):
                                del polarity_tracker[un_prop]
                                non_polar.add(un_prop)
                        elif not(un_prop in non_polar):
                            polarity_tracker[un_prop] = (clause.operator != 'NOT')
                    continue
                for prop in clause.sub_formulas:
                    un_prop = prop.unsign()
                    if not(un_prop in non_polar):
                        if un_prop in polarity_tracker.keys():
                            if polarity_tracker[un_prop] != (prop.operator != 'NOT'):
                                del polarity_tracker[un_prop]
                                non_polar.add(un_prop)
                        elif not(un_prop in non_polar):
                            polarity_tracker[un_prop] = (prop.operator != 'NOT')
        if len(polarity_tracker) > 0:
            polar_prop = list(polarity_tracker.keys())[0]
            return (polar_prop.label, [polar_prop.operator != 'NOT'])
        if two_clause and len(two_clause_counter) > 0:
            max_prop = None
            max_count = None
            for prop, count in two_clause_counter.items():
                if max_prop is None or count > max_count:
                    max_prop = prop
                    max_count = count
            return (max_prop.label, [True, False])
        if isinstance(self.sub_formulas[0], PROP):
            return (self.sub_formulas[0].label, [True, False])
        else:
            return (self.sub_formulas[0].sub_formulas[0].label, [True, False])

    def evaluate(self, assignment):
        #recursively call sub-formulas and operator
        if self.operator == 'AND':
            #assuming all is optomized to break when a single false is given
            return all(formula.evaluate(assignment) for formula in self.sub_formulas)
        elif self.operator == 'OR':
            #assuming any is optimized to break when a single true is given
            return any(formula.evaluate(assignment) for formula in self.sub_formulas)
        elif self.operator == 'NOT':#implies only 1 sub-formula
            return self.sub_formulas[0].evaluate(assignment) != True
        else:
            return Exception("operators not acceptable('NOT','AND','OR')")
        
    def count_props(self, signed = False):#return dictionary with counts of {label:prop}
        prop_dict = {}
        for formula in self.sub_formulas:
            for prop in list(formula.count_props(signed).keys()):
                if prop in prop_dict.keys():
                    prop_dict[prop] = prop_dict[prop] + formula.count_props(signed)[prop]
                else:
                    prop_dict[prop] = formula.count_props(signed)[prop]
        return prop_dict

    def get_prop_set(self, signed = False):
        prop_set = set([])
        return prop_set.union(*[formula.get_prop_set(signed) for formula in self.sub_formulas])

    def set(self, assignment):
        form_set = set([formula.set(assignment) for formula in self.sub_formulas])
        form_list = list(form_set.difference(set([True,False])))
        if form_set.issubset(set([True,False])):
            return (not(False in form_set)) if self.operator == 'AND' else (True in form_set)
        if (self.operator == 'AND') and (False in form_set):
            return False
        elif (self.operator == 'OR') and (True in form_set):
            return True
        elif len(form_list) == 1:
            return form_list[0]
        else:
            return FORM(form_list, self.operator)





class PROP(FORM):
    def __init__(self, label, operator=None):
        self.label = label if label > 0 else -label #label is non-zero integer
        self.operator = operator if label > 0 else 'NOT'
        self.sub_formulas = None

    def get_prop_set(self, signed = False):
        if signed:
            return {(-1) * self.label} if self.operator == 'NOT' else {self.label}
        else:
            return {self.label}
        
    def count_props(self, signed = False):
        if signed:
            return {(-1) * self.label: 1} if self.operator == 'NOT' else {self.label: 1}
        else:
            return {self.label: 1}
        
    def unsign(self):
        return self.negate() if self.operator == 'NOT' else self
    
    def negate(self):
        if self.operator == None:
            return PROP(self.label, operator='NOT')
        else:
            return PROP(self.label)
        
    def evaluate(self, assignment):
        if assignment == 'UNSAT':
            return False
        if not(self.label in assignment.keys()):
            return False != (self.operator == 'NOT')
        #assignment is dict from proposition labels(int) -> T/F val
        return assignment[self.label] != (self.operator == 'NOT')#'!=' operator is same as xor
    
    def set(self, assignment):
        if self.label in assignment.keys():
            return assignment[self.label] != (self.operator == 'NOT')#'!=' operator is same as xor
        else:
            return self
        
    def __repr__(self) -> str:
        if self.operator == 'NOT':
            return f"(-x_{self.label})"
        return f"x_{self.label}"

    def __eq__(self, other):
        if not isinstance(other, PROP):
            return False
        return self.label == other.label and self.operator == other.operator
    
    def __hash__(self):
        return hash(self.label) * 10 + hash(self.operator)