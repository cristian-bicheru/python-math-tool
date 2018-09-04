import roots
import cfunctions

def execCode(code):
    try:
        global output
        exec(f"global output\noutput = None\n{code}")
        if output == None:
            output = "output variable was not specified or is None"
        return output
    except Exception as e:
        return f"ERROR: {e}"
