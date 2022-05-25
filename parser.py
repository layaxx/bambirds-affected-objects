import pyparsing as pp
# relationship will refer to 'track' in all of your examples
relationship = pp.Word(pp.alphas).setResultsName('relationship')

number = pp.Word(pp.nums + '.')
variable = pp.Word(pp.alphas + pp.nums)
complex = pp.Word(pp.nums + ",.[]")
# an argument to a relationship can be either a number or a variable
argument = number | variable | complex

# arguments are a delimited list of 'argument' surrounded by parenthesis
arguments = (pp.Suppress('(') + pp.delimitedList(argument) +
             pp.Suppress(')')).setResultsName('arguments')

# a fact is composed of a relationship and it's arguments
# (I'm aware it's actually more complicated than this
# it's just a simplifying assumption)
fact = (relationship + arguments).setResultsName('fact', listAllMatches=True)

# a sentence is a fact plus a period
sentence = fact + pp.Suppress('.')

# self explanatory
parser = pp.OneOrMore(sentence)
