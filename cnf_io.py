from FORM import FORM,PROP
import os
import re

# def read_cnf_file(file_name):
#     building = False
#     str = ""
#     form_list = []
#     with open(file_name, "r") as file:
#         for line in file:
#             if building:
#                 str = str + line
#             if line[0] == 'p':
#                 building = True
#         for clause_str in str.replace('\n',' ').split(" 0 "):
#             form_list.append(FORM([PROP(int(str)) for str in (clause_str.split())],'OR'))
#     return FORM(form_list, 'AND').condense()

def read_cnf_file(file_location):
  """Reads a CNF file from the given location.

  Args:
    file_location: The location of the CNF file.

  Returns:
    A FORM object representing the CNF file.
  """

  building = False
  form_list = []
  with open(file_location, "r") as file:
    for line in file:
      # Remove comments
      line = re.sub(r'//.*', '', line)

      if building:
        form_list.append(FORM([PROP(int(str)) for str in (line.split()[:-1])],'OR'))
      if line[0] == 'p':
        building = True
  return FORM(form_list,'AND')



    