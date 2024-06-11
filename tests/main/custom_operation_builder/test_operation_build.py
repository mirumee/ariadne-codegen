from graphql import print_ast

from .graphql_client.custom_fields import (
    AdminFields,
    GuestFields,
    PersonInterface,
    PostFields,
    UserFields,
)
from .graphql_client.custom_mutations import Mutation
from .graphql_client.custom_queries import Query
from .graphql_client.enums import Role
from .graphql_client.input_types import AddUserInput, UpdateUserInput


def test_simple_hello():
    built_query = print_ast(Query.hello().to_ast())
    expected_query = "hello"
    assert built_query == expected_query


def test_greeting_with_name():
    built_query = print_ast(Query.greeting(name="Alice").to_ast())
    expected_query = 'greeting(name: "Alice")'
    assert built_query == expected_query


def test_user_by_id():
    built_query = print_ast(
        Query.user(user_id="1")
        .fields(
            UserFields.id,
            UserFields.name,
            UserFields.age,
            UserFields.email,
        )
        .to_ast()
    )
    expected_query = 'user(user_id: "1") {\n  id\n  name\n  age\n  email\n}'
    assert built_query == expected_query


def test_all_users():
    built_query = print_ast(
        Query.users()
        .fields(
            UserFields.id,
            UserFields.name,
            UserFields.age,
            UserFields.email,
        )
        .to_ast()
    )
    expected_query = "users {\n  id\n  name\n  age\n  email\n}"
    assert built_query == expected_query


def test_user_with_friends():
    built_query = print_ast(
        Query.user(user_id="1")
        .fields(
            UserFields.id,
            UserFields.name,
            UserFields.age,
            UserFields.email,
            UserFields.friends().fields(
                UserFields.id,
                UserFields.name,
            ),
            UserFields.created_at,
        )
        .to_ast()
    )
    expected_query = (
        'user(user_id: "1") {\n'
        "  id\n"
        "  name\n"
        "  age\n"
        "  email\n"
        "  friends {\n"
        "    id\n"
        "    name\n"
        "  }\n"
        "  createdAt\n"
        "}"
    )
    assert built_query == expected_query


def test_search_example():
    built_query = print_ast(
        Query.search(text="example")
        .on(
            "User",
            UserFields.id,
            UserFields.name,
            UserFields.email,
            UserFields.created_at,
        )
        .on(
            "Admin",
            AdminFields.id,
            AdminFields.name,
            AdminFields.privileges,
            AdminFields.created_at,
        )
        .on(
            "Guest",
            GuestFields.id,
            GuestFields.name,
            GuestFields.visit_count,
            GuestFields.created_at,
        )
        .to_ast()
    )
    expected_query = (
        'search(text: "example") {\n'
        "  ... on User {\n"
        "    id\n"
        "    name\n"
        "    email\n"
        "    createdAt\n"
        "  }\n"
        "  ... on Admin {\n"
        "    id\n"
        "    name\n"
        "    privileges\n"
        "    createdAt\n"
        "  }\n"
        "  ... on Guest {\n"
        "    id\n"
        "    name\n"
        "    visitCount\n"
        "    createdAt\n"
        "  }\n"
        "}"
    )
    assert built_query == expected_query


def test_posts_with_authors():
    built_query = print_ast(
        Query.posts()
        .fields(
            PostFields.id,
            PostFields.title,
            PostFields.content,
            PostFields.author().fields(
                PersonInterface.id, PersonInterface.name, PersonInterface.email
            ),
            PostFields.published_at,
        )
        .to_ast()
    )
    expected_query = (
        "posts {\n"
        "  id\n"
        "  title\n"
        "  content\n"
        "  author {\n"
        "    id\n"
        "    name\n"
        "    email\n"
        "  }\n"
        "  publishedAt\n"
        "}"
    )
    assert built_query == expected_query


def test_get_person():
    built_query = print_ast(
        Query.person(person_id="1")
        .fields(PersonInterface.id, PersonInterface.name, PersonInterface.email)
        .on("User", UserFields.age, UserFields.role)
        .on("Admin", AdminFields.privileges)
        .to_ast()
    )
    expected_query = (
        'person(person_id: "1") {\n'
        "  id\n"
        "  name\n"
        "  email\n"
        "  ... on User {\n"
        "    age\n"
        "    role\n"
        "  }\n"
        "  ... on Admin {\n"
        "    privileges\n"
        "  }\n"
        "}"
    )
    assert built_query == expected_query


def test_get_people():
    built_query = print_ast(
        Query.people()
        .fields(PersonInterface.id, PersonInterface.name, PersonInterface.email)
        .on("User", UserFields.age, UserFields.role)
        .on("Admin", AdminFields.privileges)
        .to_ast()
    )
    expected_query = (
        "people {\n"
        "  id\n"
        "  name\n"
        "  email\n"
        "  ... on User {\n"
        "    age\n"
        "    role\n"
        "  }\n"
        "  ... on Admin {\n"
        "    privileges\n"
        "  }\n"
        "}"
    )
    assert built_query == expected_query


def test_add_user_mutation():
    built_mutation = print_ast(
        Mutation.add_user(
            user_input=AddUserInput(
                name="bob",
                age=30,
                email="bob@example.com",
                role=Role.ADMIN,
                createdAt="2024-06-07T00:00:00.000Z",
            )
        )
        .fields(
            UserFields.id,
            UserFields.name,
            UserFields.age,
            UserFields.email,
            UserFields.role,
            UserFields.created_at,
        )
        .to_ast()
    )
    expected_mutation = (
        "addUser(\n"
        '  user_input: {name: "bob", age: 30, email: "bob@example.com", role: "ADMIN", '
        'created_at: "2024-06-07T00:00:00.000Z"}\n'
        ") {\n"
        "  id\n"
        "  name\n"
        "  age\n"
        "  email\n"
        "  role\n"
        "  createdAt\n"
        "}"
    )
    assert built_mutation == expected_mutation


def test_update_user_mutation():
    built_mutation = print_ast(
        Mutation.update_user(
            user_id="1",
            user_input=UpdateUserInput(
                name="Alice Updated",
                age=25,
                email="alice.updated@example.com",
                role=Role.USER,
                createdAt="2024-06-07T00:00:00.000Z",
            ),
        )
        .fields(
            UserFields.id,
            UserFields.name,
            UserFields.age,
            UserFields.email,
            UserFields.role,
            UserFields.created_at,
        )
        .to_ast()
    )
    expected_mutation = (
        "updateUser(\n"
        '  user_id: "1"\n'
        "  user_input: "
        '{name: "Alice Updated", age: 25, email: "alice.updated@example.com", '
        'role: "USER", created_at: "2024-06-07T00:00:00.000Z"}\n'
        ") {\n"
        "  id\n"
        "  name\n"
        "  age\n"
        "  email\n"
        "  role\n"
        "  createdAt\n"
        "}"
    )
    assert built_mutation == expected_mutation


def test_delete_user_mutation():
    built_mutation = print_ast(
        Mutation.delete_user(user_id="1")
        .fields(
            UserFields.id,
            UserFields.name,
        )
        .to_ast()
    )
    expected_mutation = 'deleteUser(user_id: "1") {\n  id\n  name\n}'
    assert built_mutation == expected_mutation


def test_add_post_mutation():
    built_mutation = print_ast(
        Mutation.add_post(
            title="New Post",
            content="This is the content",
            authorId="1",
            publishedAt="2024-06-07T00:00:00.000Z",
        )
        .fields(
            PostFields.id,
            PostFields.title,
            PostFields.content,
            PostFields.author().fields(PersonInterface.id, PersonInterface.name),
            PostFields.published_at,
        )
        .to_ast()
    )
    expected_mutation = (
        "addPost(\n"
        '  title: "New Post"\n'
        '  content: "This is the content"\n'
        '  authorId: "1"\n'
        '  publishedAt: "2024-06-07T00:00:00.000Z"\n'
        ") {\n"
        "  id\n"
        "  title\n"
        "  content\n"
        "  author {\n"
        "    id\n"
        "    name\n"
        "  }\n"
        "  publishedAt\n"
        "}"
    )
    assert built_mutation == expected_mutation


def test_update_post_mutation():
    built_mutation = print_ast(
        Mutation.update_post(
            post_id="1",
            title="Updated Title",
            content="Updated Content",
            publishedAt="2024-06-07T00:00:00.000Z",
        )
        .fields(
            PostFields.id,
            PostFields.title,
            PostFields.content,
            PostFields.published_at,
        )
        .to_ast()
    )
    expected_mutation = (
        "updatePost(\n"
        '  post_id: "1"\n'
        '  title: "Updated Title"\n'
        '  content: "Updated Content"\n'
        '  publishedAt: "2024-06-07T00:00:00.000Z"\n'
        ") {\n"
        "  id\n"
        "  title\n"
        "  content\n"
        "  publishedAt\n"
        "}"
    )
    assert built_mutation == expected_mutation


def test_delete_post_mutation():
    built_mutation = print_ast(
        Mutation.delete_post(post_id="1")
        .fields(
            PostFields.id,
            PostFields.title,
        )
        .to_ast()
    )
    expected_mutation = 'deletePost(post_id: "1") {\n  id\n  title\n}'
    assert built_mutation == expected_mutation


def test_user_specific_fields():
    built_query = print_ast(
        Query.user(user_id="1").fields(UserFields.id, UserFields.name).to_ast()
    )
    expected_query = 'user(user_id: "1") {\n  id\n  name\n}'
    assert built_query == expected_query


def test_user_with_friends_specific_fields():
    built_query = print_ast(
        Query.user(user_id="1")
        .fields(
            UserFields.id,
            UserFields.name,
            UserFields.friends().fields(UserFields.id, UserFields.name),
            UserFields.created_at,
        )
        .to_ast()
    )
    expected_query = (
        'user(user_id: "1") {\n'
        "  id\n"
        "  name\n"
        "  friends {\n"
        "    id\n"
        "    name\n"
        "  }\n"
        "  createdAt\n"
        "}"
    )
    assert built_query == expected_query


def test_people_with_metadata():
    built_query = print_ast(
        Query.people()
        .fields(
            PersonInterface.id,
            PersonInterface.name,
            PersonInterface.email,
            PersonInterface.metafield(key="bio"),
        )
        .on("User", UserFields.age, UserFields.role)
        .to_ast()
    )
    expected_query = (
        "people {\n"
        "  id\n"
        "  name\n"
        "  email\n"
        '  metafield(key: "bio")\n'
        "  ... on User {\n"
        "    age\n"
        "    role\n"
        "  }\n"
        "}"
    )
    assert built_query == expected_query
