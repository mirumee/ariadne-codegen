from graphql import print_ast

from .graphql_client.custom_fields import (
    AdminFields,
    GuestFields,
    PersonInterfaceInterface,
    PostFields,
    UserFields,
)
from .graphql_client.custom_mutations import Mutation
from .graphql_client.custom_queries import Query
from .graphql_client.enums import Role
from .graphql_client.input_types import AddUserInput, UpdateUserInput


def test_simple_hello():
    built_query = print_ast(Query.hello().to_ast(0))
    expected_query = "hello"
    assert built_query == expected_query


def test_greeting_with_name():
    query = Query.greeting(name="Alice")
    expected_query = "greeting(name: $name_0)"

    built_query = print_ast(query.to_ast(0))

    assert built_query == expected_query
    assert query.get_formatted_variables() == {
        "name_0": {"name": "name", "type": "String", "value": "Alice"}
    }


def test_user_by_id():
    query = Query.user(user_id="1").fields(
        UserFields.id,
        UserFields.name,
        UserFields.age,
        UserFields.email,
    )
    expected_query = "user(user_id: $user_id_0) {\n  id\n  name\n  age\n  email\n}"

    built_query = print_ast(query.to_ast(0))

    assert built_query == expected_query
    assert query.get_formatted_variables() == {
        "user_id_0": {"name": "user_id", "type": "ID!", "value": "1"}
    }


def test_all_users():
    query = Query.users().fields(
        UserFields.id,
        UserFields.name,
        UserFields.age,
        UserFields.email,
    )
    expected_query = "users {\n  id\n  name\n  age\n  email\n}"

    built_query = print_ast(query.to_ast(0))

    assert built_query == expected_query
    assert not query.get_formatted_variables()


def test_user_with_friends():
    query = Query.user(user_id="1").fields(
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
    expected_query = (
        "user(user_id: $user_id_0) {\n"
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

    built_query = print_ast(query.to_ast(0))

    assert built_query == expected_query
    assert query.get_formatted_variables() == {
        "user_id_0": {"name": "user_id", "type": "ID!", "value": "1"}
    }


def test_search_example():
    query = (
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
    )
    expected_query = (
        "search(text: $text_0) {\n"
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

    built_query = print_ast(query.to_ast(0))

    assert built_query == expected_query
    assert query.get_formatted_variables() == {
        "text_0": {"name": "text", "type": "String!", "value": "example"}
    }


def test_posts_with_authors():
    query = Query.posts().fields(
        PostFields.id,
        PostFields.title,
        PostFields.content,
        PostFields.author().fields(
            PersonInterfaceInterface.id,
            PersonInterfaceInterface.name,
            PersonInterfaceInterface.email,
        ),
        PostFields.published_at,
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

    built_query = print_ast(query.to_ast(0))

    assert built_query == expected_query
    assert not query.get_formatted_variables()


def test_get_person():
    query = (
        Query.person(person_id="1")
        .fields(
            PersonInterfaceInterface.id,
            PersonInterfaceInterface.name,
            PersonInterfaceInterface.email,
        )
        .on(
            "User",
            UserFields.age,
            UserFields.role,
            UserFields.metafield(key="meta"),
        )
        .on(
            "Admin",
            AdminFields.privileges,
            AdminFields.custom_field(),
            AdminFields.metafield(key="meta"),
        )
    )
    expected_query = (
        "person(person_id: $person_id_0) {\n"
        "  id\n"
        "  name\n"
        "  email\n"
        "  ... on User {\n"
        "    age\n"
        "    role\n"
        "    metafield(key: $key_0)\n"
        "  }\n"
        "  ... on Admin {\n"
        "    privileges\n"
        "    custom_field\n"
        "    metafield(key: $key_0_1)\n"
        "  }\n"
        "}"
    )

    built_query = print_ast(query.to_ast(0))

    assert built_query == expected_query
    assert query.get_formatted_variables() == {
        "person_id_0": {"name": "person_id", "type": "ID!", "value": "1"},
        "key_0": {"name": "key", "type": "String!", "value": "meta"},
        "key_0_1": {"name": "key", "type": "String!", "value": "meta"},
    }


def test_get_people():
    query = (
        Query.people()
        .fields(
            PersonInterfaceInterface.id,
            PersonInterfaceInterface.name,
            PersonInterfaceInterface.email,
        )
        .on("User", UserFields.age, UserFields.role)
        .on("Admin", AdminFields.privileges)
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

    built_query = print_ast(query.to_ast(0))

    assert built_query == expected_query
    assert not query.get_formatted_variables()


def test_add_user_mutation():
    user_input = AddUserInput(
        name="bob",
        age=30,
        email="bob@example.com",
        role=Role.ADMIN,
        createdAt="2024-06-07T00:00:00.000Z",
    )
    mutation = Mutation.add_user(user_input=user_input).fields(
        UserFields.id,
        UserFields.name,
        UserFields.age,
        UserFields.email,
        UserFields.role,
        UserFields.created_at,
    )
    expected_mutation = (
        "addUser("
        "user_input: $user_input_0"
        ") {\n"
        "  id\n"
        "  name\n"
        "  age\n"
        "  email\n"
        "  role\n"
        "  createdAt\n"
        "}"
    )

    built_mutation = print_ast(mutation.to_ast(0))

    assert built_mutation == expected_mutation
    assert mutation.get_formatted_variables() == {
        "user_input_0": {
            "name": "user_input",
            "type": "AddUserInput!",
            "value": user_input,
        }
    }


def test_update_user_mutation():
    user_input = UpdateUserInput(
        name="Alice Updated",
        age=25,
        email="alice.updated@example.com",
        role=Role.USER,
        createdAt="2024-06-07T00:00:00.000Z",
    )
    mutation = Mutation.update_user(
        user_id="1",
        user_input=user_input,
    ).fields(
        UserFields.id,
        UserFields.name,
        UserFields.age,
        UserFields.email,
        UserFields.role,
        UserFields.created_at,
    )
    expected_mutation = (
        "updateUser("
        "user_id: $user_id_0, "
        "user_input: $user_input_0"
        ") {\n"
        "  id\n"
        "  name\n"
        "  age\n"
        "  email\n"
        "  role\n"
        "  createdAt\n"
        "}"
    )

    built_mutation = print_ast(mutation.to_ast(0))

    assert built_mutation == expected_mutation
    assert mutation.get_formatted_variables() == {
        "user_id_0": {"name": "user_id", "type": "ID!", "value": "1"},
        "user_input_0": {
            "name": "user_input",
            "type": "UpdateUserInput!",
            "value": user_input,
        },
    }


def test_delete_user_mutation():
    mutation = Mutation.delete_user(user_id="1").fields(
        UserFields.id,
        UserFields.name,
    )
    expected_mutation = "deleteUser(user_id: $user_id_0) {\n  id\n  name\n}"

    built_mutation = print_ast(mutation.to_ast(0))

    assert built_mutation == expected_mutation
    assert mutation.get_formatted_variables() == {
        "user_id_0": {"name": "user_id", "type": "ID!", "value": "1"}
    }


def test_add_post_mutation():
    mutation = Mutation.add_post(
        title="New Post",
        content="This is the content",
        author_id="1",
        published_at="2024-06-07T00:00:00.000Z",
    ).fields(
        PostFields.id,
        PostFields.title,
        PostFields.content,
        PostFields.author().fields(
            PersonInterfaceInterface.id,
            PersonInterfaceInterface.name,
        ),
        PostFields.published_at,
    )
    expected_mutation = (
        "addPost(\n"
        "  title: $title_0\n"
        "  content: $content_0\n"
        "  authorId: $authorId_0\n"
        "  publishedAt: $publishedAt_0\n"
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

    built_mutation = print_ast(mutation.to_ast(0))

    assert built_mutation == expected_mutation
    assert mutation.get_formatted_variables() == {
        "title_0": {
            "name": "title",
            "type": "String!",
            "value": "New Post",
        },
        "content_0": {
            "name": "content",
            "type": "String!",
            "value": "This is the content",
        },
        "authorId_0": {
            "name": "authorId",
            "type": "ID!",
            "value": "1",
        },
        "publishedAt_0": {
            "name": "publishedAt",
            "type": "String!",
            "value": "2024-06-07T00:00:00.000Z",
        },
    }


def test_update_post_mutation():
    mutation = Mutation.update_post(
        post_id="1",
        title="Updated Title",
        content="Updated Content",
        published_at="2024-06-07T00:00:00.000Z",
    ).fields(
        PostFields.id,
        PostFields.title,
        PostFields.content,
        PostFields.published_at,
    )
    expected_mutation = (
        "updatePost(\n"
        "  post_id: $post_id_0\n"
        "  title: $title_0\n"
        "  content: $content_0\n"
        "  publishedAt: $publishedAt_0\n"
        ") {\n"
        "  id\n"
        "  title\n"
        "  content\n"
        "  publishedAt\n"
        "}"
    )

    built_mutation = print_ast(mutation.to_ast(0))

    assert built_mutation == expected_mutation
    assert mutation.get_formatted_variables() == {
        "post_id_0": {"name": "post_id", "type": "ID!", "value": "1"},
        "title_0": {"name": "title", "type": "String", "value": "Updated Title"},
        "content_0": {"name": "content", "type": "String", "value": "Updated Content"},
        "publishedAt_0": {
            "name": "publishedAt",
            "type": "String",
            "value": "2024-06-07T00:00:00.000Z",
        },
    }


def test_delete_post_mutation():
    mutation = Mutation.delete_post(post_id="1").fields(
        PostFields.id,
        PostFields.title,
    )
    expected_mutation = "deletePost(post_id: $post_id_0) {\n  id\n  title\n}"

    built_mutation = print_ast(mutation.to_ast(0))

    assert built_mutation == expected_mutation
    assert mutation.get_formatted_variables() == {
        "post_id_0": {"name": "post_id", "type": "ID!", "value": "1"}
    }


def test_user_specific_fields():
    query = Query.user(user_id="1").fields(UserFields.id, UserFields.name)
    expected_query = "user(user_id: $user_id_0) {\n  id\n  name\n}"

    built_query = print_ast(query.to_ast(0))

    assert built_query == expected_query
    assert query.get_formatted_variables() == {
        "user_id_0": {"name": "user_id", "type": "ID!", "value": "1"}
    }


def test_user_with_friends_specific_fields():
    query = Query.user(user_id="1").fields(
        UserFields.id,
        UserFields.name,
        UserFields.friends().fields(UserFields.id, UserFields.name),
        UserFields.created_at,
    )
    expected_query = (
        "user(user_id: $user_id_0) {\n"
        "  id\n"
        "  name\n"
        "  friends {\n"
        "    id\n"
        "    name\n"
        "  }\n"
        "  createdAt\n"
        "}"
    )

    built_query = print_ast(query.to_ast(0))

    assert built_query == expected_query
    assert query.get_formatted_variables() == {
        "user_id_0": {"name": "user_id", "type": "ID!", "value": "1"}
    }


def test_people_with_metadata():
    query = (
        Query.people()
        .fields(
            PersonInterfaceInterface.id,
            PersonInterfaceInterface.name,
            PersonInterfaceInterface.email,
            PersonInterfaceInterface.metafield(key="bio"),
            PersonInterfaceInterface.metafield(key="ots"),
        )
        .on("User", UserFields.age, UserFields.role)
    )
    expected_query = (
        "people {\n"
        "  id\n"
        "  name\n"
        "  email\n"
        "  metafield(key: $key_0)\n"
        "  metafield(key: $key_0_1)\n"
        "  ... on User {\n"
        "    age\n"
        "    role\n"
        "  }\n"
        "}"
    )

    built_query = print_ast(query.to_ast(0))

    assert built_query == expected_query
    assert query.get_formatted_variables() == {
        "key_0": {"name": "key", "type": "String!", "value": "bio"},
        "key_0_1": {"name": "key", "type": "String!", "value": "ots"},
    }
