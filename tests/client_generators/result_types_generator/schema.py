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
  interfaceQuery: InterfaceI!
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
  unionField: UnionType!
  _: String!
  schema: String!
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
  field3: CustomType1
}

enum CustomEnum {
    VAL1
    VAL2
}

union UnionType = CustomType1 | CustomType2

scalar SCALARA

interface InterfaceI {
  id: ID!
}

type TypeA implements InterfaceI {
  id: ID!
  fieldA: String!
}

type TypeB implements InterfaceI {
  id: ID!
  fieldB: Float!
}

type TypeC implements InterfaceI {
  id: ID!
  fieldC: Int!
}
"""
