"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations


from langgraph.graph import START, END
from langgraph.graph import StateGraph

from src.states import State
from src.nodes import len_str, add_one, add_two

def __add_nodes(simple_graph:StateGraph):
  simple_graph.add_node(
      "len_str", len_str
  )

  simple_graph.add_node(
      "add_one", add_one
  )

  simple_graph.add_node(
      "add_two", add_two
  )

def __is_stop_fnc(state: State) -> str:
    is_stop = state["is_stop"]
    if is_stop:
        return "go_stop"
    else:
        return "go_to_add_two_fnc"

def __add_edge(simple_graph:StateGraph):
  simple_graph.add_edge(
      START ,      # 시작 노드
      "len_str"    # 끝 노드
  )

  simple_graph.add_edge(
      "len_str",  # 시작 노드
      "add_one"   # 끝 노드
  )

  simple_graph.add_edge(
      "add_two",    # 시작 노드
      "add_one"     # 끝 노드
  )

  simple_graph.add_conditional_edges(
      "add_one",  # 시작 노드
      __is_stop_fnc,    # 어떤 노드로 전달할지 정의된 함수
      # 끝 노드
      {
          "go_to_add_two_fnc":"add_two",
          "go_stop":END
      }
  )


def main():
  simple_graph = StateGraph(State)

  __add_nodes(simple_graph)
  __add_edge(simple_graph)

  return simple_graph.compile()

graph = main()

