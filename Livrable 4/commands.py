import sources
import submiter
import sink
import receiver

variables = {
    "sampling_frequency": 44100,
    "data_frequency": 10,
    "output_range": (500, 1000),
    "arity": 8,
    "sync_call_duration": 10,
    "sync_transition_duration": 5
}

class Status:
    SUCCESS = 0
    FAILURE = 1
    INVALID_ARGS = 2
    EXIT = 3

def quit_cmd(args):
    return Status.EXIT

def submit_cmd(args):
    if len(args) == 0:
        print("You must select a submit source type !")
        return Status.INVALID_ARGS

    type_arg = args[0]

    sourceTypes = {
        "message": sources.Message
        # "file": sources.file
    }

    if not type_arg in sourceTypes:
        print(f"\"{type_arg}\" is not a valid source type : must be {[t for t in sourceTypes]}")
        return Status.INVALID_ARGS
    

    source = sourceTypes[type_arg](' '.join(args[1:]) if len(args) > 1 else [])
    
    s = submiter.Submiter(source, variables)
        
    return Status.SUCCESS

def set_cmd(args):
    # assert(len(args)>1)
    if len(args) < 2:
        print("Invalid number of arguments for \"set\"")
        return Status.INVALID_ARGS

    # Aquire the values
    variable = args[0]
    values = args[1:]
    
    # Checks if the variable is valid
    if not variable in variables:
        print(f"The variable \"{variable}\" doesn't exist")
        return Status.INVALID_ARGS
    
    # If the variable is a tuple
    if isinstance(variables[variable], tuple):

        # Checks if the lenghts of the tuples are the same
        if len(values) != len(variables[variable]):
            print(f"Expected {len(variables[variable])} values for \"{variable}\"")
            return Status.INVALID_ARGS
        try:
            values = tuple(type(variables[variable][0])(v) for v in values)
        except ValueError:
            print(f"Cannot convert {values} to the type of {variable}")
            return Status.FAILURE
        
    # If it as anything else
    else:
        # Try to convert it
        try:
            values = type(variables[variable])(values[0])
        except ValueError:
            print(f"Cannot convert {values[0]} to the type of {variable}")
            return Status.FAILURE

    variables[variable] = values
    return Status.SUCCESS

def help_cmd(arg):
    print("List of possible commands : ")
    for c in cmds:
        print(f"\t- {c}")

    return Status.SUCCESS

def receive_cmd(args):
    s = sink.Terminal()
    r = receiver.Receiver(s)
    
    return Status.SUCCESS

def test_cmd(args):
    submit_cmd(["message", "bonjour"])

cmds = {
    "quit": quit_cmd,
    "exit": quit_cmd,
    "submit": submit_cmd,
    "set": set_cmd,
    "help": help_cmd,
    "receive": receive_cmd,
    "test": test_cmd
}