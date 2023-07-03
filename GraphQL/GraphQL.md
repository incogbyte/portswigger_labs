
----

- GraphQL is an API query language that is designed to facilitate efficient communication between clients and servers. It enables the user to specify exactly what data they want in the response, helping to avoid the large response objects and multiple calls that can sometimes be seen with REST APIs. GraphQL services define a contract through which a client can communicate with a server. The client doesn't need to know where the data resides. Instead, clients send queries to a GraphQL server, which fetches data from the relevant places. As GraphQL is platform-agnostic, it can be implemented with a wide range of programming languages and can be used to communicate with virtually any data store.

- How it works
	- GraphQL schemas define the structure of the service's data, listing the available objects (known as types), fields, and relationships.
	- **All GraphQL operations use the same endpoint**, and are generally sent as a POST request. This is significantly different to REST APIs, which use operation-specific endpoints across a range of HTTP methods. With GraphQL, the type and name of the operation define how the query is handled, rather than the endpoint it is sent to or the HTTP method used.

## What is a GraphQL schema?

In GraphQL, the schema represents a contract between the frontend and backend of the service. It defines the data available as a series of types, using a human-readable schema definition language. These types can then be implemented by a service.

Most of the types defined are object types. which define the objects available and the fields and arguments they have. Each field has its own type, which can either be another object or a scalar, enum, union, interface, or custom type.

The example below shows a simple schema definition for a Product type. The `!` operator indicates that the field is non-nullable when called (that is, mandatory).

`#Example schema definition type Product { id: ID! name: String! description: String! price: Int }`

Schemas must also include at least one available query. Usually, they also contain details of available mutations.

## What are GraphQL queries?

GraphQL queries retrieve data from the data store. They are roughly equivalent to GET requests in a REST API.

Queries usually have the following key components:

- A `query` operation type. This is technically optional but encouraged, as it explicitly tells the server that the incoming request is a query.
- A query name. This can be anything you want. The query name is optional, but encouraged as it can help with debugging.
- A data structure. This is the data that the query should return.
- Optionally, one or more arguments. These are used to create queries that return details of a specific object (for example "give me the name and description of the product that has the ID 123").

The example below shows a query called `myGetProductQuery` that requests the name, and description fields of a product with the `id` of `123`.

`#Example query query myGetProductQuery { getProduct(id: 123) { name description } }`

Note that the product type may contain more fields in the schema than those requested here. The ability to request only the data you need is a significant part of the flexibility of GraphQL.
