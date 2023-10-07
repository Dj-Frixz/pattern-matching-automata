class pattern_matching_fsa:
    '''# pattern_matching_fsa
    ### A class to build pattern matching automata
    ---
    This class takes a pattern (string) with length greater than zero as a parameter.
    If the object is passed to print(), the TABLE associated to the FSA will be printed to console.
    Warning: the __dict parameter should be left as default (not assigned).'''

    ### SPECIAL METHODS

    def __init__(self, pattern:str, __dict = None) -> None:
        self.PATTERN = pattern
        self.M = len(pattern) # the length of the pattern
        # this dictionary will be the structure of the automation
        self.dict = __dict if __dict is not None else {0 : {-1 : 0}}
        self.__generate_dict()
        # private attribute, useful only for formatting output internally
        self.__digits = len(str(self.M))
    
    def __str__(self) -> str:
        '''A method to represent the FSA in the table format.'''
        table = '\n    '
        SIGMA = self.alphabet
        for ch in SIGMA:
            table += ' '*self.__digits + ch
        table += '\n     ' + ('-'*(self.__digits + 1)) * (len(SIGMA)-1) + '-'*self.__digits
        for state in self.dict:
            table += '\n {:{space}d} :'.format(state, space=self.__digits)
            for ch in SIGMA:
                if ch in self.dict[state]:
                    table += ' {:{space}d}'.format(self.dict[state][ch], space=self.__digits)
                else:
                    table += ' 0' # self.dict[state][-1] should be 0 for any state
        table += '\n'
        return table
    
    def __eq__(self, __value: object) -> bool:
        '''Two istances are comparated by their patterns, as two identical patterns should generate the same FSA'''
        return self.PATTERN == __value.PATTERN
    
    def __add__(self, __value:str|object) -> object:
        '''Using the <+> operator produces a new FSA without rebuilding the entire FSA structure from scratch'''
        if type(__value) == str:
            return pattern_matching_fsa(self.PATTERN + __value, self.dict)
        return pattern_matching_fsa(self.PATTERN + __value.PATTERN, self.dict)

    ### PRIVATE METHODS

    def __generate_dict(self):
        '''The table for the machine is generated in a dict, following the scheme:
        STATE : INPUT : OUTPUT (new_state).

        If the input (str type) is not found in the dict,
        the input searched defaults to -1 (int type, not str).'''

        start = max(self.dict) + 1

        if self.M < start:
            return # the dictionary is already completed
        
        self.dict[start-1][self.PATTERN[start-1]] = start

        for i in range(start, self.M+1):
            self.dict[i] = {}
            self.__find_pointers(self.PATTERN[0:i],i)
        

    def __find_pointers(self, substr:str, state:int) -> None:
        '''This method finds what every state should point to based on the possible inputs.'''
        k = len(substr)
        # if the first char of the pattern is found defaults to state 0
        # (this behaviour can be overwritten in the loop below)
        self.dict[state][substr[0]] = 1
        for i in range(1,k):
            if substr[0:i] == substr[k-i:k]:
                self.dict[state][substr[i]] = i+1
        # if the correct char is found, go to the next state (new_state = state+1)
        # this overwrites any behaviour set in the loop,
        # as the priority should be to look for a match
        if state!=self.M: # if it is self.M it's already in the final state
            self.dict[state][self.PATTERN[state]] = state+1
        # -1 (not '-1') is a special jolly input for the cases not considered
        # It represents the "default" case, where new_state is always 0
        self.dict[state][-1] = 0
    
    ### NON-PUBLIC METHODS

    def _f(self, state:int, input_) -> int:
        if input_ not in self.dict[state]:
            input_ = -1
        return self.dict[state][input_]
    
    ### USER METHODS

    def process(self, text:str, verbose:bool = False) -> int:
        '''# pattern_matching_fsa.process
        #### This method lets the built FSA process the string passed as a parameter
        ---
        parameters:
        - text (str): the string to process
        - verbose (bool): if True, every step of the FSA is printed to the console

        return:
        - count (int): the number of times the pattern has been found in text'''

        if len(text) < self.M:
            print('\n 0 matches have been found in text.')
            return 0
        
        count = 0 # number of matches found in text
        state = 0 # current state (starting state is always 0)

        if verbose: print('\n state: {:{space}d}   '.format(state, text[0], space=self.__digits), end='')

        for ch in text:
            state = self._f(state, ch)
            count += 1 if (state == self.M) else 0

            if verbose:
                print('{} ---> {:{space}d}   {}\n state: {:{space}d}   '.format(
                        ch, state, '+1' if state == self.M else '', state, ch, space=self.__digits
                    ), end='')
        
        if verbose:
            print('{} ---> {:{space}d}   {}'.format(text[-1], state, '+1' if state == self.M else '', space=self.__digits))
        
        print('\n {:d} matches have been found in text.\n'.format(count))
        return count

    @property
    def alphabet(self):
        return set(self.PATTERN)


if __name__ == '__main__':

    # Basic usage
    k = pattern_matching_fsa('TAT')
    print('Pattern:',k.PATTERN)
    print('Alphabet: ',k.alphabet)
    print('Table:')
    print(k)
    text = 'CCCGGCTGCTACAGTAATTATATAAGTATTATTATGCC'
    print('Text:',text)
    k.process(text, verbose=True)

    # Some more advanced examples
    a = pattern_matching_fsa('TAT')
    b = pattern_matching_fsa('ATA')
    print('Pattern a:',a.PATTERN)
    print('Pattern b:',b.PATTERN)
    print('k == a ?  ', k == a)
    print('a == b ?  ', a == b)
    c = a + b
    print('Pattern c = a + b:',c.PATTERN)
    c.process(text)
    j = k + a
    print('Table j (subset of table k):')
    print(j)
    j.process(text, verbose = True)