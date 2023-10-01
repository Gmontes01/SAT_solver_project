README interim report

Author: Gabriel Montes
GT email: gmontes7@gatech.edu
GTID: 903558369

I have adhered to the honor code and only used my own code

Interrim Report:
    Files in this report should include cnf_io.py, einstein_problem.cnf, FORM.py, sat_solver.py,
        and puzzle.ipynb.
        
    The file puzzle.ipynb gives most of the information about my handling of the einstein problem. 
        It describes how I define my propositions based on their given integer values. There are 
        Three sections in puzzle.ipynb: Defining Propositions, Encoding Einstins's Problem, and Solution.
        
        The section 'Defining Propositions' describes the meaning of every proposition given that
        some distinct meaning needs to be given to every propositions and therefore its label number.
        
        The section 'Encoding Einstein's Problem' details all the constraints in the problem and their 
        SAT and CNF encoding. The section describes every constraint, both general and specified, and 
        how they are encoded in SAT. The section also describes how many constraints are converted from 
        SAT to CNF. The CNF encodings are also all checked so that they have the correct
        meaning and they are functionally equivalent to their non-CNF original formula description. 

        The final section 'Solution' works with finding and interpretting the solution to the already set up 
        einstein problem. The submitted form of the notebook can either read 'einstein_problem.cnf' using the cnf_io.py
        file's functoin or build the formula from the work done in the previous section. With unit preference enabled,
        my computer found a solution in less than 7 seconds regardless of polarity and two clause heuristic enabling. 
        The notebook also has a built in function that describes the meaning of every proposition, so once the solution
        is found the script will read the meaning of the solution.
        
        
    The file einstein_problem.cnf is the cnf file encoding of my einstein problem. My encoding of 
        the einstein problem involves 125 propositions and 1568 clauses. The exact method used to 
        encode every restriction of the problem is described in puzzle.ipynb.
        The clauses are reordered from my original ordering so all of the restraints of the system are
        not clearly seperable. 
        
    The file FORM.py holds the class FORM and PROP. Both names are short for formula and proposition
        and both classes encode seperately formulas and propositions. A formula of type FORM is defined
        by a list of sub_formulas and an operator. Operators can be 'AND', 'OR', or 'NOT' and evaluation
        of a given formula depends on the evaluation of the sub_formulas. The structure of FORM is recursive
        since a formula depends on sub_formulas and the base case of a formula is a proposition in class
        PROP. A proposition in PROP is characterized by its label, a number which distinguishes the proposition
        from other propositions, and its operator, either None or Not. Commets on all the functions on FORM and 
        PROP are commented and explain what they do. 
    
    The file cnf_io.py is a file designed to hold the function read_cnf_file(). This function does 
        exactly what its name suggests. It reads a .cnf file and returns a formula of the class FORM.

