# Mowhive
This is a small mower swarm controller library, to setup and execute your fleet of land mowers.

It was written with the thought of exetension on different collition protocols, so it comes with 
support for 3 different default protocols that make some assumptions depending on the situations:
- `STOP_ON_COLLITION`: in case of collition, do not perform inhibited movement and try to perform the next
- `ABORT_ON_COLLITION`: in case of collition, raise an exception with information about the collition specifics
- `AWAIT_ON_COLLITION`: in case of collition, if it's another mower prohibiting the movement, requeue the inhibited mower
    for later attempts and continue with the next available mower. Requeuing will be done
    at most *max-number-of-mowers* times in a row.

All movement operation return details about the mowers execution to allow for further library extensibility and serve as an example

## Setups and Execution
Mowhive is written in `Python 3.9`, and `venv` setup is recomomended: run on your project folder

    python -m venv <myenv>

replacing `<myenv>` with your preferred virtualenv folder name. To activate your venv on linux run:

    source <myenv>/bin/activate

to activate it on Windows run

    .\<myenv>\Scripts\activate

**Note**: sometimes you have to use the `.ps1` or `.bat` extention on your Windows activate binary.

Install testingg deoendencies with:

    pip install -r requirements.txt

And that's the setup!


### Execution 
For executing the example, you can do

    python main.py < inputfile

where `inputfile` is the scenario description file with the format

    5 5
    1 2 N
    LMLMLMLMM
    3 3 E
    MMRMMRMRRM

You'll get an output of the final state of the form 
    
    1 3 N
    5 1 E

if you wish to try different protocols, you must edit the `main.py` and add the parameter `collition_protocol=<protocol_value>` 
to the `MowController` instantiation using `<protocol_value>` as one of

    CollitionProtocols.STOP_ON_COLLITIONS
    CollitionProtocols.ABORT_ON_COLLITIONS
    CollitionProtocols.AWAIT_ON_COLLITIONS

### Tests

If you wish to execute the tests, after installing all dependencies, execute

    pytest

and all the tests within the `test/` folder will be executed