__all__ = [
    "GET_COMPLEX_SCALAR_GQL",
    "GET_QUERY_A_GQL",
    "GET_QUERY_A_WITH_FRAGMENT_GQL",
    "GET_QUERY_B_GQL",
    "GET_QUERY_I_GQL",
    "GET_QUERY_WITH_MIXINS_FRAGMENTS_GQL",
    "GET_SIMPLE_SCALAR_GQL",
    "SUBSCRIBE_TO_TYPE_A_GQL",
]

GET_QUERY_A_GQL = """
query getQueryA {
  queryA {
    fieldA
  }
}
"""

GET_QUERY_B_GQL = """
query getQueryB {
  queryB {
    fieldB
  }
}
"""

GET_QUERY_I_GQL = """
query getQueryI($dataI: InputI!) {
  queryI(dataI: $dataI) {
    fieldI
    date
  }
}
"""

GET_QUERY_A_WITH_FRAGMENT_GQL = """
query getQueryAWithFragment {
  ...getQueryAFragment
}

fragment getQueryAFragment on Query {
  queryA {
    fieldA
  }
}
"""

GET_QUERY_WITH_MIXINS_FRAGMENTS_GQL = """
query getQueryWithMixinsFragments {
  queryA {
    ...fragmentA
  }
  queryB {
    ...fragmentB
  }
}

fragment fragmentA on TypeA @mixin(from: ".mixins_a", import: "MixinA") {
  fieldA
}

fragment fragmentB on TypeB @mixin(from: ".mixins_b", import: "MixinB") {
  fieldB
}
"""

GET_SIMPLE_SCALAR_GQL = """
query GetSimpleScalar {
  justSimpleScalar
}
"""

GET_COMPLEX_SCALAR_GQL = """
query GetComplexScalar {
  justComplexScalar
}
"""

SUBSCRIBE_TO_TYPE_A_GQL = """
subscription SubscribeToTypeA {
  subscribeToTypeA {
    fieldA
  }
}
"""
