1. What is the fundamental syntax for selecting an HTML element and applying an action in jQuery?

A. element.action()

B. $(selector).action()

C. jQuery(action).selector()

D. select(element).do(action)

Đáp án: B

2. How would you access a query string parameter named sort in a controller action?

A. [HttpGet] public IActionResult Get([FromRoute] string sort) { /*...*/}

B. [HttpGet] public IActionResult Get([FromBody] string sort) { /*...*/}

C. [HttpGet] public IActionResult Get([FromHeader] string sort) { /*...*/}

D. [HttpGet] public IActionResult Get([FromQuery] string sort) { /*...*/}

Đáp án: D

3. gRPC's support for long-lived streaming is made possible primarily by which HTTP/2 feature?

A. Server Push

B. Header Compression

C. Binary Framing

D. Bi-directional streams

Đáp án: D

4. How do you create a gRPC client in a .NET 8 console application?

A. var client = new HttpClient();

B. var channel = GrpcChannel. ForAddress("https://localhost:5001"); var client = new Greeter. GreeterClient(channel);

C. var client = new Greeter. GreeterStub("https://localhost:5001");

D. var client = GrpcClient.Create<GreeterClient>("https://localhost:5001");

Đáp án: B

5. Which of the following questions does "Authentication" answer?

A. "What can you do?"

B. "Who are you?"

C. "How long can you stay?"

D. "Where are you from?"

Đáp án: B

6. Consider this simple CoreWCF service contract for a .NET 9 application: [ServiceContract] public interface IGreeterService { [OperationContract] string Greet(string name); } Which part defines what the service does?

A. [Service Contract]

B. public interface IGreeterService

C. [OperationContract]

D. string Greet(string name);

Đáp án: D

7. What is the fundamental concept of "Code-First" development in Entity Framework Core?

A. You design the database schema first, and then EF Core generates the C# model classes.

B. You write the API endpoints first, which then dictates the model and database structure.

C. You define your data models as C# classes, and EF Core creates or updates the database schema to match them.

D. You write raw SQL scripts first for all data operations.

Đáp án: C

8. Which system query option is used to filter a collection of resources in an OData request?

A. $select

B. $orderby

C. $filter

D. $top

Đáp án: C

9. What is the purpose of the $expand query option?

A. To retrieve the next page of results in a paged collection.

B. To include related entities in the same response.

C. To get a count of all entities in a collection.

D. To expand all properties of an entity instead of a subset.

Đáp án: B

10. What does the "asynchronous" in AJAX mean?

A. The code is guaranteed to execute in a specific, synchronous order.

B. The web browser can continue to be responsive to the user while waiting for the server to send back a response.

C. The server must respond to the request immediately.

D. The data must be in XML format.

Đáp án: B

11. What is "binding source parameter inference" in controllers marked with [ApiController]?

A. The process of guessing the data types of action parameters.

B. A feature where ASP.NET Core automatically applies binding source attributes ([FromRoute], [FromBody], etc.) based on conventions, reducing boilerplate code.

C. The ability to infer validation rules from property names.

D. A mechanism for the client to tell the server where to find data.

Đáp án: B

12. If a client sends an Accept header with application/json; q=0.9, application/xml; q=1.0, what is it indicating?

A. It can only accept JSON.

B. It prefers XML (q=1.0) over JSON (q=0.9).

C. It can only accept XML.

D. It wants the response to be split between JSON and XML.

Đáp án: B

13. What is Content Negotiation in ASP.NET Core Web API?

A. The process where the client and server agree on which controller action to invoke.

B. The process where the server selects the best representation (e.g., JSON or XML) for a response based on the client's Accept header.

C. The process of negotiating security credentials.

D. The process where the client specifies which data it wants to post using the Content-Type header.

Đáp án: B

14. Which communication protocol is often chosen for high-performance, internal, service-to-service communication due to its use of HTTP/2 and binary serialization?

A. SOAP

B. REST over HTTP/1.1 with JSON

C. gRPC

D. FTP

Đáp án: C

15. To allow access to users who are in either the "Manager" role or the "Supervisor" role, what is the correct syntax?

A. [Authorize(Roles = "Manager", "Supervisor")]

B. [Authorize(Roles = "Manager")] [Authorize (Roles = "Supervisor")]

C. [Authorize(Roles = "Manager or Supervisor")]

D. [Authorize(Roles = "Manager, Supervisor")]

Đáp án: D

16. What is the primary purpose of the HTTP protocol?

A. To securely encrypt data transmissions.

B. To transfer hypertext documents across the internet.

C. To manage and query databases.

D. To define the structure of a web page.

Đáp án: B

17. Why is it critical to always use HTTPS for RESTful APIs?

A. It makes the API faster by compressing the data.

B. It ensures that the data (including credentials and sensitive information) transferred between the client and server is encrypted and protected from eavesdropping.

C. It is the only protocol that supports the GET and POST verbs.

D. It automatically handles user authorization.

Đáp án: B

18. Which data types are supported in JSON?

A. String, Number, Boolean, Array, Object, null

B. String, Integer, Float, Date, Array, Hashtable

C. Text, Decimal, Bit, List, Dictionary, null

D. Varchar, Number, Boolean, Collection, Object, undefined

Đáp án: A

19. Which of the following is a simple representation of a Model class in C# for an ASP.NET Core application?

A. A static class with methods for rendering HTML.

B. An interface defining controller actions.

C. A class with properties representing data, often called a POCO (Plain Old CLR Object).

D. An attribute used for routing.

Đáp án: C

20. Which selector targets the first paragraph element (<p>) on the page?

A. $("p:first-child")

B. $("p:first")

C. $("p:first-of-type")

D. All of the above could potentially work depending on the HTML structure.

Đáp án: D

21. The following C# code in a.NET creates an endpoint. What does it do? app.MapGet("/products/{id}", (int id=> { // Logic to find a product by id return Results. Ok($"Product {id}"); });

A. It defines an endpoint that creates a new product.

B. It defines an endpoint that retrieves a product by its ID using a POST request.

C. It defines an endpoint that retrieves a product by its ID using a GET request.

D. It defines an endpoint that deletes a product by its ID.

Đáp án: C

22. What is the opposite of a microservices architecture?

A. A serverless architecture

B. A monolithic architecture

C. A service-oriented architecture (SOA)

D. A distributed architecture

Đáp án: B

23. The following.NET 8 code is in Program.cs. What is its purpose? var app = builder.Build(); // app.UseAuthentication(); app.UseAuthorization(); // app.Run();

A. It registers the authentication services.

B. It adds the authentication and authorization middleware components to the request pipeline.

C. It configures the default authentication scheme.

D. It is redundant and has no effect.

Đáp án: B

24. What is a "channel" in gRPC?

A. The service implementation on the server.

B. The generated client-side code.

C. A long-lived connection to a gRPC service, which can be reused for multiple calls.

D. A specific type of streaming method.

Đáp án: C

25. In a .NET 8 Web API, what is the recommended way to handle model validation errors automatically and return a 400 Bad Request response?

A. Manually checking ModelState.IsValid in every action.

B. The [ApiController] attribute automatically handles it.

C. Using a custom middleware to inspect every request.

D. Relying on the database to throw an exception.

Đáp án: B

26. In an OData service with Categories and Products, how would you request all products belonging to the category with an ID of 5?

A. GET /Products?$filter=Categoryld eq 5

B. GET /Categories(5)/Products

C. GET/Products/Category(5)

D. Both A and B are typically valid ways to query.

Đáp án: D

27. To retrieve a single Category entity and all of its related Product entities in one request, which query would you use?

A. GET /Categories(1)?$select=Products

B. GET /Categories(1)?$expand=Products

C. GET /Categories(1),/Products

D. GET /Categories(1)/Products?$fetch=all

Đáp án: B

28. What is ASP.NET Core Identity?

A. A simple interface for generating unique IDs.

B. A membership system that provides services for user authentication and authorization, including user management, password hashing, and role management.

C. A client-side library for managing user profiles.

D. The default authentication scheme for Windows Authentication.

Đáp án: B

29. Which of the following is NOT a core principle of REST?

A. Statelessness

B. Client-Server architecture

C. Stateful connections

D. Uniform Interface

Đáp án: C

30. What is the primary advantage of using attribute routing over conventional routing?

A. It is the only way to define routes in minimal APIs.

B. It keeps the route definition next to the action method that it maps to, improving locality and discoverability.

C. It offers significantly better performance than conventional routing.

D. It is required for enabling Swagger/OpenAPI documentation.

Đáp án: B

31. The metadata of an OData service, which describes its data model, is typically exposed via which endpoint?

A. /$metadata

B. /$help

C. /$schema

D. /$info

Đáp án: A

32. Which formatter is configured by default in a new ASP.NET Core 8 Web API project?

A. An XML-based formatter (XmlSerializerInputFormatter/XmlSerializer OutputFormatter).

B. A JSON-based formatter using System.Text.Json.

C. A plain text formatter (TextInputFormatter/TextOutputFormatter).

D. A custom binary formatter.

Đáp án: B

33. What is a "load balancer" in the context of scaling a web service?

A. A tool that validates the data load of a JSON request.

B. A server or service that distributes incoming network traffic across multiple backend servers.

C. A database feature that balances data across multiple tables.

D. A client-side library for managing application load times.

Đáp án: B

34. In an ASP.NET Core Web API, which attribute is used to decorate an action method that should respond to HTTP POST requests?

A. [HttpGet]

B. [HttpPost]

C. [HttpPut]

D. [HttpDelete]

Đáp án: B

35. Which query correctly finds all products where the Name property ends with the string 'Edition'?

A. GET /Products?$filter-endswith(Name, 'Edition')

B. GET /Products?$filter=Name.endsWith('Edition')

C. GET /Products?$filter=last(Name) eq 'Edition'

D. GET /Products?$filter=Name like '%Edition'

Đáp án: A

36. Which of the following is a correctly formatted Media Type for JSON?

A. text/json

B. application/json

C. data/json

D. json/application

Đáp án: B

37. How do you enable OData query options on a specific controller action?

A. By adding the [EnableQuery] attribute to the action method.

B. By naming the action method GetWithOData.

C. By inheriting from ODataController.

D. It is enabled automatically on all actions once OData is configured.

Đáp án: A

38. The following code uses ODataModelBuilder to construct an EDM. What does it do? var builder = new ODataConventionModelBuilder(); builder.EntitySet<Product>("Products"); builder.EntitySet<Category>("Categories"); return builder.GetEdmModel();

A. It creates two entity sets, Products and Categories, and infers their properties and relationships by convention from the C# classes.

B. It defines two complex types that cannot be queried directly.

C. It creates an empty model and waits for the database to provide the schema.

D. It registers two controllers named Products and Categories.

Đáp án: A

39. What is an "Entity Set"?

A. The set of properties that make up an entity's key.

B. A named collection of entities of a specific Entity Type, like Products being a collection of Product entities.

C. The schema version of the data model.

D. A set of validation rules for an entity.

Đáp án: B

40. In a bidirectional streaming call, when does the server wait for the client to send all its messages before sending its own?

A. Always.

B. Never; the client and server can read and write in any order, their streams operate independently.

C. Only if the client explicitly signals it has finished writing.

D. This is configured by the wait_for_client option in the proto file.

Đáp án: B

41. A JWT consists of three parts separated by dots (.). What are they in the correct order?

A. Header, Payload, Signature

B. Payload, Header, Signature

C. Signature, Header, Payload

D. Header, Signature, Body

Đáp án: A

42. What is a "claim" in the context of a JWT?

A. A statement about a subject, such as a user's name, ID, or role.

B. A request from the client to access a protected resource.

C. An error message indicating invalid credentials.

D. The algorithm used to sign the token.

Đáp án: A

43. What is CoreWCF?

A. A complete rewrite of WCF with a different architecture and programming model.

B. A port of WCF to .NET (Core) and .NET 5+ that allows existing WCF services to be migrated to modern, cross-platform environments.

C. A client-only library for consuming legacy WCF services.

D. A graphical tool for managing WCF services.

Đáp án: B

44. To add support for XML serialization in a .NET 8 Web API, what service configuration is typically used in Program.cs?

A. builder. Services.AddControllers().AddXml();

B. builder. Services.AddMvc().AddXmlSerializerFormatters();

C. builder. Services.AddControllers().AddXmlSerializer Formatters();

D. builder. Services.AddXmlFormatting();

Đáp án: C

45. Which attribute forces a primitive type parameter to be bound exclusively from the query string?

A. [FromRoute]

B. [FromQuery]

C. [FromBody]

D. [FromHeader]

Đáp án: B

46. If a request is made to /products?id=abc for an action defined as public IActionResult GetProduct(int id), what will be the state of ModelState?

A. ModelState.IsValid will be true, and id will be 0.

B. An InvalidCastException will be thrown.

C. ModelState.IsValid will be false because "abc" cannot be converted to an integer.

D. id will be null.

Đáp án: C

47. What is the primary reason for using Data Transfer Objects (DTOs) in an API?

A. To replace the need for a database.

B. To shape data specifically for the client, preventing over-posting and under-posting, and decoupling the API from the database schema.

C. To increase the performance of database queries.

D. To enforce business logic and validation.

Đáp án: B

48. To create a new entity in an OData service, which HTTP method should be used?

A. GET

B. PUT

C. POST

D. MERGE

Đáp án: C

49. Which of the following bindings is designed for high performance, .NET-to-.NET communication on the same machine or across an intranet?

A. BasicHttpBinding

B. WSHttpBinding

C. NetTcpBinding

D. WebHttpBinding

Đáp án: C

50. In a controller decorated with [ApiController], what happens automatically if ModelState.IsValid is false?

A. The action method still executes as normal.

B. An HTTP 500 Internal Server Error is returned.

C. The request is automatically rejected with an HTTP 400 Bad Request response containing details of the validation errors.

D. The application logs the error and returns an HTTP 200 OK.

Đáp án: C
