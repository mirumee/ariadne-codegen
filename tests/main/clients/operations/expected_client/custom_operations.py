__all__ = [
    "C_MUTATION_GQL",
    "C_QUERY_GQL",
    "C_SUBSCRIPTION_GQL",
    "GET_A_GQL",
    "GET_A_WITH_FRAGMENT_GQL",
    "GET_XYZ_GQL",
]

C_QUERY_GQL = """
query cQuery {
  constQuery
}
"""

C_MUTATION_GQL = """
mutation cMutation {
  constMutation
}
"""

C_SUBSCRIPTION_GQL = """
subscription cSubscription {
  constSubscription
}
"""

GET_A_GQL = """
query getA {
  a {
    value
    valueB {
      value
    }
  }
}
"""

GET_A_WITH_FRAGMENT_GQL = """
query getAWithFragment {
  a {
    value
    valueB {
      ...fragmentB
    }
  }
}

fragment fragmentB on TypeB {
  value
}
"""

GET_XYZ_GQL = """
query getXYZ {
  xyz {
    __typename
    ... on TypeX {
      valueX
    }
    ... on TypeY {
      ...fragmentY
    }
  }
}

fragment fragmentY on TypeY {
  valueY
}
"""
