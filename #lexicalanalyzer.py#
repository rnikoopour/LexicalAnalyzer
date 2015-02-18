from dfsm import IdentifierDFSM
from transition import Transition
import string

def main():
    states = [1, 2, 3]
    input_symbols = string.lowercase + string.uppercase + string.digits + '_'
    transitions = [Transition(1, 'l', 2), Transition(2, 'l', 2), Transition(2, 'd', 2), Transition(2, '_', 3), Transition(3, 'l', 2), Transition(3, 'd', 2), Transition(3, '_', 3)]
    start_state = states[0]
    accept_states = [states[1]]
    d = IdentifierDFSM(states, input_symbols, transitions, start_state, accept_states)
    print(d.Accepts('a_123'))
    print(d.Accepts('aa'))

if __name__ == '__main__':
    main()
