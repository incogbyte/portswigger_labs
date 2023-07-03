----

- GraphQL vulnerabilities generally arise due to implementation and design flaws.


## Finding GraphQL endpoints

- Before you can test a GraphQL API, you first need to find its endpoint. **As GraphQL APIs use the same endpoint for all requests**, this is a valuable piece of information.

### Universal queries

If you send `query{__typename}` to any GraphQL endpoint, it will include the string `{"data": {"__typename": "query"}}` somewhere in its response. This is known as a universal query, and is a useful tool in probing whether a URL corresponds to a GraphQL service.

The query works because every GraphQL endpoint has a reserved field called `__typename` that returns the queried object's type as a string.

### Common endpoint names

GraphQL services often use similar endpoint suffixes. When testing for GraphQL endpoints, you should look to send universal queries to the following locations:

- `/graphql`
- `/api`
- `/api/graphql`
- `/graphql/api`
- `/graphql/graphql`

If these common endpoints don't return a GraphQL response, you could also try appending `/v1` to the path.

### Request methods

The next step in trying to find GraphQL endpoints is to test using different request methods.

**It is best practice for production GraphQL endpoints to only accept POST requests that have a content-type of `application/json`, as this helps to protect against CSRF vulnerabilities**. However, some endpoints may accept alternative methods, such as GET requests or POST requests that use a content-type of `x-www-form-urlencoded`.

If you can't find the GraphQL endpoint by sending POST requests to common endpoints, try resending the universal query using alternative HTTP methods.

### Initial testing

Once you have discovered the endpoint, you can send some test requests to understand a little more about how it works. If the endpoint is powering a website, try exploring the web interface in Burp's browser and use the HTTP history to examine the queries that are sent.

## Exploiting unsanitized arguments

At this point, you can start to look for vulnerabilities. Testing query arguments is a good place to start.

If the API uses arguments to access objects directly, it may be vulnerable to [access control](https://portswigger.net/web-security/access-control) vulnerabilities. A user could potentially access information they should not have simply by supplying an argument that corresponds to that information. This is sometimes known as an insecure direct object reference (IDOR).

## Discovering schema information

The next step in testing the API is to piece together information about the underlying schema.

The best way to do this is to use introspection queries. Introspection is a built-in GraphQL function that enables you to query a server for information about the schema.

Introspection helps you to understand how you can interact with a GraphQL API. It can also disclose potentially sensitive data, such as description fields.


### Using introspection

To use introspection to discover schema information, query the `__schema` field. This field is available on the root type of all queries.

Like regular queries, you can specify the fields and structure of the response you want to be returned when running an introspection query. For example, you might want the response to contain only the names of available mutations.


### Probing for introspection

It is best practice for introspection to be disabled in production environments, but this advice is not always followed.

You can probe for introspection using the following simple query. If introspection is enabled, the response returns the names of all available queries.

`#Introspection probe request { "query": "{__schema{queryType{name}}}" }`

### Running a full introspection query

The next step is to run a full introspection query against the endpoint so that you can get as much information on the underlying schema as possible.

The example query below returns full details on all queries, mutations, subscriptions, types, and fragments.

`#Full introspection query query IntrospectionQuery { __schema { queryType { name } mutationType { name } subscriptionType { name } types { ...FullType } directives { name description args { ...InputValue } onOperation #Often needs to be deleted to run query onFragment #Often needs to be deleted to run query onField #Often needs to be deleted to run query } } } fragment FullType on __Type { kind name description fields(includeDeprecated: true) { name description args { ...InputValue } type { ...TypeRef } isDeprecated deprecationReason } inputFields { ...InputValue } interfaces { ...TypeRef } enumValues(includeDeprecated: true) { name description isDeprecated deprecationReason } possibleTypes { ...TypeRef } } fragment InputValue on __InputValue { name description type { ...TypeRef } defaultValue } fragment TypeRef on __Type { kind name ofType { kind name ofType { kind name ofType { kind name } } } }`


### Visualizing introspection results

Responses to introspection queries can be full of information, but are often very long and hard to process.

You can view relationships between schema entities more easily using a [GraphQL visualizer](http://nathanrandal.com/graphql-visualizer/). This is an online tool that takes the results of an introspection query and produces a visual representation of the returned data, including the relationships between operations and types.

### Using InQL

As an alternative to running an introspection query manually and visualizing the results, you can use Burp Suite's InQL extension.

InQL is a Burp Suite extension that helps you to audit GraphQL APIs securely. When you pass a URL to it (either by providing a live endpoint link or by uploading a JSON file), it issues an introspection query requesting all queries and mutations, and presents a structured view to make it easy to explore the results.

### Suggestions

Even if introspection is entirely disabled, you can sometimes use suggestions to glean information on an API's structure.

Suggestions are a feature of the Apollo GraphQL platform in which the server can suggest query amendments in error messages. These are generally used where a query is slightly incorrect but still recognizable (for example, `There is no entry for 'productInfo'. Did you mean 'productInformation' instead?`).

You can potentially glean useful information from this, as the response is effectively giving away valid parts of the schema.

[Clairvoyance](https://github.com/nikitastupin/clairvoyance) is a tool that uses suggestions to automatically recover all or part of a GraphQL schema, even when introspection is disabled. This makes it significantly less time consuming to piece together information from suggestion responses.

You cannot disable suggestions directly in Apollo. See [this GitHub thread](https://github.com/apollographql/apollo-server/issues/3919#issuecomment-836503305) for a workaround.