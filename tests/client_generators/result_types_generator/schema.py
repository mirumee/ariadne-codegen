SCHEMA_STR = """
schema {
  query: Query
  mutation: Mutation
  subscription: Subscription
}

type Query {
  query1(
    id: ID!
  ): CustomType
  query2: [CustomType!]
  query3: CustomType3!
  query4: UnionType!
  camelCaseQuery: CustomType!
}

type Mutation {
    mutation1(num: Int!): CustomType!
}

type Subscription {
  subscription1(num: Int!): CustomType!
}

type CustomType {
    id: ID!
    field1: CustomType1!
    field2: CustomType2
    field3: CustomEnum!
    _field4: String!
    _Field5: String!
    scalarField: SCALARA
}

type CustomType1 {
    fielda: Int!
}

type CustomType2 {
    fieldb: Int
}

type CustomType3 {
    field1: CustomType1!
    field2: CustomType1!
}

enum CustomEnum {
    VAL1
    VAL2
}

union UnionType = CustomType1 | CustomType2

scalar SCALARA
"""
