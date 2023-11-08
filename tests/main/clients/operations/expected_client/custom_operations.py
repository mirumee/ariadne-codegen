__all__ = [
    "cMutation_GQL",
    "cQuery_GQL",
    "cSubscription_GQL",
    "getAWithFragment_GQL",
    "getA_GQL",
    "getXYZ_GQL",
]
cQuery_GQL = """
query cQuery {
  constQuery
}
"""
cMutation_GQL = """
mutation cMutation {
  constMutation
}
"""
cSubscription_GQL = """
subscription cSubscription {
  constSubscription
}
"""
getA_GQL = """
query getA {
  a {
    value
    valueB {
      value
    }
  }
}
"""
getAWithFragment_GQL = """
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
getXYZ_GQL = """
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
