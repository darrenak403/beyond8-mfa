1. Choose correct information about ASP.NET Core HTTP verbs

A. PUT - This verb is used to update the existing resource. DELETE - This verb is used to delete the existing resource. GET - This verb is used to retrieve the data or information. It does not have any other effect except getting data. POST - This verb is used to generate or create the resource.

B. PUT - This verb is used to generate or create the resource. DELETE - This verb is used to delete the existing resource. GET - This verb is used to retrieve the data or information. It does not have any other effect except getting data. POST - This verb is used to update the existing resource.

C. PUT - This verb is used to retrieve the data or information. It does not have any other effect except getting data. DELETE - This verb is used to delete the existing resource. GET - This verb is used to update the existing resource. POST - This verb is used to generate or create the resource.

D. PUT - This verb is used to delete the existing resource. DELETE - This verb is used to update the existing resource. GET - This verb is used to retrieve the data or information. It does not have any other effect except getting data. POST - This verb is used to generate or create the resource.

Đáp án: A

2. Which HTTP response code represents a successful request in REST?

A. 200 (OK)

B. 300 (Multiple Choices)

C. 400 (Bad Request)

D. 500 (Internal Server Error)

Đáp án: A

3. What is the purpose of HTTP headers in RESTful APIs?

A. HTTP headers contain metadata about the request or response

B. HTTP headers define the structure of the API's data models

C. HTTP headers store the actual data being transferred in the API

D. HTTP headers enforce security and authentication in the API

Đáp án: A

4. What does REST stand for?

A. Remote Encoding and State Transfer

B. Representational State Transfer

C. Resource Extraction and State Transportation

D. Rapid and Efficient Service Transfer

Đáp án: B

5. What is the purpose of the HTTP POST method in a RESTful API?

A. To retrieve or fetch a resource from the server

B. To update an existing resource on the server

C. To delete a resource from the server

D. To create a new resource on the server

Đáp án: D

6. What is a microservice?

A. A monolithic application

B. A self-contained, independent service

C. A programming language

D. A database management system

Đáp án: B

7. Which Docker command is used to run a .NET container image?

A. docker build

B. docker run

C. docker stop

D. docker push

Đáp án: B

8. What is the Startup class in ASP.NET Core Web API?

A. Startup class is the entry point of the ASP.NET Core application or Web API.

B. It is not necessary that class name must be Startup, it can be anything, just need to configure startup class in Program class.

C. Both the answers are corect

D. Both the answers are incorrect

Đáp án: C

9. To call the ASP.NET Core Web API with JavaScript, configure the app to serve static files and enable default file mapping. Which code is needed in the method of Startup.cs?

A. public void Configure(IApplicationBuilder app, IWebHostEnvironment env) { // app. UseDefaultFiles(); app.UseStaticFiles(); // }

B. public void ConfigureServices (IApplication Builder app, IWebHostEnvironment env) { // app. UseDefaultFiles(); app.UseStaticFiles(); // }

C. public void ConfigureServices (IServiceCollection app) { // app.UseDefaultFiles(); app.UseStaticFiles(); // }

D. public void Configure(IServiceCollection app) { // app.UseDefaultFiles(); app.UseStaticFiles(); // }

Đáp án: A

10. What is Content Negotiation in ASP.NET Core Web API?

A. The process of negotiating content prices between client and server.

B. The process of selecting the appropriate response format based on the request's Accept header.

C. The process of caching response content on the server.

D. The process of securing content transmission between client and server.

Đáp án: B

11. What is the default media type used by the JsonMediaTypeFormatter in Web API?

A. application/json

B. text/xml

C. application/xml

D. application/x-www-form-urlencoded

Đáp án: A

12. What is the role of IContentNegotiator in ASP.NET Core Web API?

A. It handles routing and URL mapping.

B. It checks for authentication and authorization.

C. It negotiates and selects the appropriate response format based on the client's preferences.

D. It handles serialization and deserialization of data.

Đáp án: C

13. What is JSON?

A. JSON (JavaScript Object Notation): It is similar to HTML but is more flexible than HTML because it allows users to create their own custom tags.

B. JSON (JavaScript Object Notation): It is especially designed to store and transport data.

C. JSON (JavaScript Object Notation): It is used for representing structured information such as documents, data, configuration, etc.

D. JSON (JavaScript Object Notation): It is a lightweight format designed to store and transport data.

Đáp án: B, D

14. Which attribute can be used to override the default media type for a specific action or controller in ASP.NET Core Web API?

A. \[HttpPost]

B. \[AllowAnonymous]

C. \[Produces]

D. \[Route]

Đáp án: C

15. What is the purpose of using the \[ServiceContract] attribute in WCF?

A. To define a service operation

B. To mark a class as a data contract

C. To specify the XML namespace for the service

D. To mark a class as a service implementation

Đáp án: D

16. Which type of hosting is suitable for WCF services that require high scalability and availability?

A. IIS Hosting

B. Self-Hosting

C. Windows Service Hosting

D. WAS Hosting

Đáp án: D

17. Which type of contract is applicable to interface in WCF?

A. Operation contract

B. Message contract

C. Service contract

D. Data contract

Đáp án: C

18. WCF endpoint includes which components?

A. Address

B. Binding

C. Contract

D. All of the others

Đáp án: D

19. What is the purpose of the authentication middleware in ASP.NET Core Web API?

A. To handle incoming HTTP requests and responses

B. To enable authentication for the web application

C. To map incoming requests to appropriate endpoint handlers

D. To provide role-based authorization

Đáp án: B

20. Which of the following is typically used for user authentication in a RESTful Web Service?

A. API keys

B. JSON Web Tokens (JWT)

C. OAuth2

D. SSL/TLS certificates

Đáp án: B

21. Authorization is the process of:

A. Verifying the identity of a user or a client

B. Granting access to specific resources or actions

C. Encrypting sensitive data during transmission

D. Logging user activities for auditing purposes

Đáp án: B

22. Which parts of the JWT are typically Base64Url encoded?

A. Header and payload

B. Payload and signature

C. Header and signature

D. All parts of the JWT are Base64Url encoded

Đáp án: A

23. Choose the correct information to configure autoscaling for an Azure solution.

A. Azure App Service has built-in autoscaling. Autoscale settings apply to all of the apps within an App Service.

B. Azure App Service has built-in autoscaling only at the role level.

C. The connection is slow in autoscaling option with Azure App Sercive.

D. All of the others.

Đáp án: A

24. Protocol Buffers is used to define the Messages (data, Request and Response) and Service (Service name and RPC endpoints). Choose the correct syntax.

A. syntax = "proto3"; service Greeter { rpc SayHello (HelloRequest) returns (HelloReply); } message HelloRequest ( string name = 1; } message HelloReply { string message = 1; }

B. syntax = "proto3"; message Greeter { rpc SayHello (HelloRequest) replies (HelloReply); } service HelloRequest { string name = 1; } service HelloReply { string message = 1; }

Đáp án: A

25. How are gRPC services registered and configured in ASP.NET Core?

A. In the ConfigureServices method of the Startup class

B. By adding a configuration file named appSettings.json

C. By modifying the Global.asax file

D. In the ConfigureServices method of the Controller class

Đáp án: A

26. Can Protocol Buffers be used for bidirectional streaming in gRPC with C#?

A. Yes, Protocol Buffers support bidirectional streaming in gRPC with C#.

B. No, Protocol Buffers only support unidirectional streaming in gRPC with C#.

C. Bidirectional streaming is not supported by gRPC with C#.

D. Protocol Buffers cannot be used for streaming in gRPC with C#.

Đáp án: A

27. Which protocol does gRPC primarily use for communication?

A. HTTP/1.1

B. HTTP/2

C. WebSocket

D. FTP

Đáp án: B

28. How does OData enable clients to query and filter data?

A. By using custom SQL queries.

B. By sending raw JSON data in the request payload.

C. By using a standardized query syntax in the URL.

D. By encoding data using a secure encryption algorithm.

Đáp án: C

29. Choose the correct information about EnableQueryAttribute class ([EnableQuery] attribute)

A. This class defines an attribute that can be applied to an action to enable querying using the OData query syntax.

B. This class defines both attribute and method that can be applied to an action to enable querying using the OData query syntax.

C. This class defines a method that can be applied to an action to enable querying using the OData query syntax.

D. None of the others.

Đáp án: A

30. What is the purpose of the Service Metadata Feature in OData?

A. To provide information about the available OData endpoints and entities in the Web API.

B. To enable automatic generation of sample data for OData response.

C. To allow automatic retrieval of remote OData services.

D. To enable configuration of dynamic service routes for OData endpoints.

Đáp án: A

31. What is the purpose of the $filter query option in OData?

A. It allows clients to request a specific subset of entity properties.

B. It enables clients to perform complex filtering operations on entity collections.

C. It allows clients to update or modify existing entities.

D. It provides a way to sort the returned entities based on a specified property.

Đáp án: B

32. Choose the correct information about pagging OData.

A. To enable paging, just mention the page count at the [Queryable] [EnableQuery(PageSize =5)] public IActionResult GetData() => Ok(objService.GetObjects());

B. To enable paging, just mention the page count at the [Queryable] [EnableQuery(PageIndex =5)] public IActionResult GetData() => Ok(objService.GetObjects());

C. To enable paging, just mention the page count at the [AllowQueryable] [AllowEnableQuery(PageSize =5)] public IActionResult GetData() => Ok(objService.GetObjects());

Đáp án: A

33. Choose the incorrect information about Async programming with ASP.NET Web API.

A. Async programming is a parallel programming technique that allows the working process to run separately from the main application thread.

B. Async programming cannot informs the main thread about the result whether it was successful or not.

C. Using async programming, we can enhance the responsiveness of our application.

D. Using async programming, we can avoid performance bottlenecks.

Đáp án: B

34. A binding source attribute defines the location at which an action parameter's value is found. Which one is not a binding source attribute?

A. [FromServices]

B. [FromHeader]

C. [FromQuery]

D. [FromRouting]

Đáp án: D

35. ASP.NET Core supports creating web APIs using controllers or using minimal APIs. Controllers in a Web API are classes that derive from which of the following class?

A. ControllerBase

B. Controller

C. ControllerAttribute

D. ControllerContext

Đáp án: A

36. Which information is true about ASP.NET Core Web API Architecture?

A. The ASP.NET Web API framework has been designed using the task-based asynchronous programming model from the top to the bottom.

B. Ability to host both in IIS (or development server) and in any nonweb server process (called self-hosted).

C. All of the others.

D. Can customize many elements of ASP.NET Core Web API by supplying custom implementation.

Đáp án: C

37. What is the purpose of the Primitive Model Binder in ASP.NET Core Web API?

A. It is used for binding complex models with nested properties

B. It is used for binding primitive types like strings and integers

C. It is used for validating model properties

D. It is used for handling query string parameters

Đáp án: B

38. Which of the following is true about the [HttpGet] attribute in ASP.NET Core Web API?

A. It specifies that the route should only handle GET requests

B. It is used to map the route to a specific HTTP method

C. It is not supported in Attribute Routing

D. It is used to define the route template for the action method

Đáp án: A

39. Where should you typically add the UseRouting middleware in the startup.cs file?

A. Inside the ConfigureServices method

B. Before the UseEndpoints middleware

C. After the UseAuthentication middleware

D. Inside the Configure method

Đáp án: B

40. What is the purpose of the UseRouting middleware in ASP.NET Core Web API?

A. To handle HTTP requests and responses

B. To map incoming requests to appropriate endpoint handlers

C. To enable routing for static files in the web application

D. To provide authentication and authorization features

Đáp án: B

41. What is model validation in ASP.NET Core Web API?

A. A process to check the authenticity of the model data

B. A way to validate that the model conforms to specified rules

C. A technique to validate the authentication of the API user

D. A feature to validate the structure of the model schema

Đáp án: B

42. To force clients to set a value, make the property nullable and set the Required attribute

A. [Required] public decimal? Price { get; set; }

B. [RequireAttribute(0, 999)] public decimal? Price { get; set; }

C. [RequiredRange(0, 999)] public decimal? Price { get; set; }

D. [RequiredNotNull] public decimal? Price { get; set; }

Đáp án: A

43. What is the purpose of a Data Transfer Object (DTO) in .NET?

A. To transfer data between different layers or components of an application

B. To define the structure and behavior of database tables

C. To encapsulate business logic within a separate class

D. To manage user input validation in forms

Đáp án: A

44. What is AutoMapper?

A. AutoMapper is an object-object mapper. Object-object mapping works by transforming an input object of one type into an output object of a different type.

B. AutoMapper is an object-object mapper of EntityFramework Core with ASP.NET Core Web API.

C. Object-object mapping works by transforming an input collection of one type into an output object of a different type.

D. All of the others.

Đáp án: A

45. What are Data Transfer Objects (DTOs)?

A. Data Transfer Objects (DTOs) are classes that define a Model with sometimes predefined validation in place for HTTP responses and requests.

B. The DTOs can be known as ViewModels in MVC where you only want to expose relevant data to the View.

C. Both the answers are incorrect

D. Both the answers are correct

Đáp án: D

46. Choose the option that is not one of characteristics of a REST based network.

A. Client-Server

B. Stateful

C. Uniform interface

D. Cache

Đáp án: B

47. Choose the incorrect information about ASP.NET Core Web AΡΙ.

A. ASP.NET Core Web API, from the beginning, was designed to be a service-based framework for building REpresentational State Transfer (RESTful) services.

B. It is based on the MVC framework minus the V (view), with optimizations for creating headless services.

C. ASP.NET Core Web API is an application can interact with a resource by knowing the resource only.

D. Calls to a Web API service are based on the core HTTP verbs (Get, Put, Post, Delete) through a uniform resource identifier (URI).

Đáp án: C

48. How Authentication and Authorization works? Choose the correct order of steps.

A. Step 1. The Request reaches the Authentication Middleware. Step 2. The Authentication Middleware checks to see if a proper credential present in the request. It will use the default authentication handler to do that. It could be a Cookies handler or JWT handler. Since it does not find any credential, it will set the User Property to an anonymous user. Step 3. Authorization Middleware (UseAuthorization()) checks to see if the destination page needs Authorization. If No then the user is allowed to visit the Page If Yes it invokes the ChallengeAsync() on the Authentication Handler. It redirects the user to Login Page.

B. Step 1. The Authentication Middleware checks to see if a proper credential present in the request. It will use the default authentication handler to do that. It could be a Cookies handler or JWT handler. Since it does not find any credential, it will set the User Property to an anonymous user. Step 2. The Request reaches the Authentication Middleware. Step 3. Authorization Middleware (UseAuthorization()) checks to see if the destination page needs Authorization. If No then the user is allowed to visit the Page If Yes it invokes the ChallengeAsync() on the Authentication Handler. It redirects the user to Login Page.

C. Step 1. The Request reaches the Authentication Middleware. Step 2. Authorization Middleware (UseAuthorization()) checks to see if the destination page needs Authorization. If No then the user is allowed to visit the Page If Yes it invokes the ChallengeAsync() on the Authentication Handler. It redirects the user to Login Page. Step 3. The Authentication Middleware checks to see if a proper credential present in the request. It will use the default authentication handler to do that. It could be a Cookies handler or JWT handler. Since it does not find any credential, it will set the User Property to an anonymous user.

D. None of the others.

Đáp án: A

49. What is a key difference between gRPC and REST in terms of payload serialization?

A. gRPC uses XML, REST uses JSON

B. gRPC uses JSON, REST uses Protocol Buffers

C. gRPC uses Protocol Buffers, REST uses XML

D. gRPC uses JSON, REST uses XML

Đáp án: C
