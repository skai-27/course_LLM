from typing_extensions import TypedDict, Optional

class State(TypedDict):
  input: Optional[str]
  node_ouput: Optional[int]
  is_stop: Optional[bool]

