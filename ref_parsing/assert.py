from typing import Dict, Union, Any
import json

# Default function name
def get_assert(output: str, context) -> Union[bool, float, Dict[str, Any]]:
    
    # return {
    #   'pass': False,
    #   'score': 0,
    #   'reason': str(context),
    # }

    expected = context["test"]["assert"][0]["expected"]
    try:
        output = json.loads(output)
    except:
        return {
            'pass': False,
            'score': 0.0,
            'reason': "Output is not valid JSON"
        }
    
    if output["refs"] != expected:
        return {
            'pass': False,
            'score': 0.0,
            'reason': "Output does not match expected: \n" + json.dumps(expected, ensure_ascii=False, indent=2)
        }

    return {
      'pass': True,
      'score': 1.0,
      'reason': "Output matches expected",
    }