# TỔNG HỢP CÂU HỎI MÔN PRN232 

1. Choose correct information about ASP.NET Core HTTP verbs

A. PUT - This verb is used to update the existing resource. DELETE - This verb is used to delete the existing resource. GET - This verb is used to retrieve the data or information. It does not have any other effect except getting data. POST - This verb is used to generate or create the resource.

B. PUT - This verb is used to generate or create the resource. DELETE - This verb is used to delete the existing resource. GET - This verb is used to retrieve the data or information. It does not have any other effect except getting data. POST - This verb is used to update the existing resource.

C. PUT - This verb is used to retrieve the data or information. It does not have any other effect except getting data. DELETE - This verb is used to delete the existing resource. GET - This verb is used to update the existing resource. POST - This verb is used to generate or create the resource.

D. PUT - This verb is used to delete the existing resource. DELETE - This verb is used to update the existing resource. GET - This verb is used to retrieve the data or information. It does not have any other effect except getting data. POST - This verb is used to generate or create the resource.

Đáp án: A

2. What is REST API?

A. A REST API (RESTful API) is an application programming interface that conforms to the constraints of REST architectural style and allows for interaction with RESTful web services.

B. A REST API (RESTful API) is an application programming that allows for interaction with RESTful web services without constraints.

C. A REST API (RESTful API) is an application programming interface that conforms to the constraints of REST architectural style and does not allow for interaction with RESTful web services.

D. A REST API (RESTful API) is an application programming that conforms to the constraints of REST architectural style and does not allow for interaction with RESTful web services.

Đáp án: A

3. Choose the option that is not one of characteristics of a REST based network.

A. Client-Server

B. Stateful

C. Uniform interface

D. Cache

Đáp án: B

4. Choose the correct information.

A. REST web services communicate over the HTTP specification, using HTTP vocabulary

B. REST is an architectural pattern for developing web services as opposed to a specification

C. REST stands for Representational State Transfer

D. All of the others.

Đáp án: D

5. What does REST stand for?

A. Remote Encoding and State Transfer

B. Representational State Transfer

C. Resource Extraction and State Transportation

D. Rapid and Efficient Service Transfer

Đáp án: B

6. What is microservice?

A. Microservice is an architectural style that structures an application as a collection of services.

B. Microservice is a software architectural design that structures an application as a collection of services.

C. Microservice is a hardware design that structures a hardware of an application as a collection of services.

D. None of the others.

Đáp án: A

7. What is the Startup class in ASP.NET Core Web API?

A. Startup class is the entry point of the ASP.NET Core application or Web API.

B. It is not necessary that class name must be Startup, it can be anything, just need to configure startup class in Program class.

C. Both the answers are corect

D. Both the answers are incorrect

Đáp án: C

8. To test your mappings with AutoMapper, you need to create a test that does the thing(s). Call your bootstrapper class to create all the mappings and call MapperConfiguration.AssertConfigurationlsValid

A. var config = AutoMapperConfiguration.Configure(); config.AssertConfigurationIsValid();

B. var config = AutoMapperConfiguration.Configure(); config.AssertConfigurationIsNotValid();

C. var config = AutoMapperConfiguration. Configure(); config.AssertAllConfigurationlsValid();

D. var config = AutoMapperConfiguration.Configure(); config.AssertConfigurationlsValid(true);

Đáp án: A

9. What is a microservice?

A. A monolithic application

B. A self-contained, independent service

C. A programming language

D. A database management system

Đáp án: B

10. What is the purpose of using an AJAX JavaScript client with an ASP.NET Core Web API?

A. To handle server-side logic

B. To improve the performance of the web application

C. To integrate third-party APIs

D. To make asynchronous HTTP requests to the Web API

Đáp án: D

11. Choose the correct information about using CORS.

A. public void ConfigureServices (IServiceCollection services) { services.AddCors (o => o.AddPolicy("AllowOrigins", builder => { builder.WithOrigins("http://localhost:5500") .AllowAnyMethod() .AllowAnyHeader(); })); // ... } { public void Configure(IApplicationBuilder app, IWebHostEnvironment env) app.UseRouting(); app.UseCors("AllowOrigins"); app. UseAuthorization(); // ... }

B. public void Configure (IServiceCollection services) { services.AddCors(o => o.AddPolicy("AllowOrigins", builder => { builder.WithOrigins("http://localhost:5500") .AllowAnyMethod() .AllowAnyHeader(); })); // ... } public void ConfigureServices (IApplicationBuilder app, IWebHostEnvironment env) { app.UseRouting(); app.UseCors("AllowOrigins"); app.UseAuthorization(); }

Đáp án: A

12. JavaScript is a powerful programming language for calling ASP.NET Core Web API. Which object is used to call the Web API from JavaScript object?

A. XMLHttpRequest (XHR) object

B. XMLHttpResponse (XHR) object

C. XMLHttpRequestObject (XHR)

D. XMLHttpResponseObject (XHR) object

Đáp án: A

13. To call the ASP.NET Core Web API with JavaScript, configure the app to serve static files and enable default file mapping. Which code is needed in the method of Startup.cs?

A. public void Configure(IApplicationBuilder app, IWebHostEnvironment env) { // app.UseDefaultFiles(); app.UseStaticFiles(); // }

B. public void ConfigureServices (IApplication Builder app, IWebHostEnvironment env) { // app.UseDefaultFiles(); app.UseStaticFiles(); // }

C. public void ConfigureServices (IServiceCollection app) { // app.UseDefaultFiles(); app.UseStaticFiles(); // }

D. public void Configure(IServiceCollection app) { // app.UseDefaultFiles(); app. UseStaticFiles(); // }

Đáp án: A

14. What is content negotiation?

A. Content negotiation is a mechanism that can be used to serve different representations of the same resource at a given URI, providing ability to their clients to decide the best suited representations.

B. Content negotiation is a collection of API that can be used to serve different representations of the same resource at a given URI, providing ability to their clients to decide the best suited representations.

C. Content negotiation is an application that can be used to serve different representations of the same resource at a given URI, providing ability to their clients to decide the best suited representations.

Đáp án: A

15. If an HTTP request does not include an "Accept" header, and the server supports both XML and JSON, what will be the server's default response format?

A. XML

B. JSON

C. HTML

D. Server error

Đáp án: B

16. What does "Accept: application/json; q=0.8, application/xml;q=0.9" mean in the "Accept" header of an HTTP Request Message?

A. The server should respond with JSON data only.

B. The server should respond with XML data only.

C. The server should respond with either JSON or XML data, but XML is preferred over JSON.

D. The server should respond with either JSON or XML data, but JSON is preferred over XML.

Đáp án: C

17. How can you return an XML response from an action method in ASP.NET Core Web API?

A. By using the [XmlResult] attribute on the action method.

B. By manually serializing the data to XML format using an XmlSerializer.

C. By returning an ObjectResult with the desired data and specifying the response format as XML.

D. By configuring the media types in the Startup class.

Đáp án: D

18. Which attribute can be used to indicate the expected media type for a request or response in Web API?

A. [HttpGet]

B. [HttpPost]

C. [Produces]

D. [Consumes]

Đáp án: C

19. What is the main purpose of the WCF architecture?

A. To provide a platform for building distributed systems

B. To simplify the development of web applications

C. To manage database connectivity

D. To enhance the user interface design

Đáp án: A

20. What is the main advantage of using Windows Communication Foundation (WCF) for building RESTful services?

A. Improved performance

B. Cross-platform compatibility

C. Scalability and flexibility

D. Security enhancements

Đáp án: C

21. MessageContract can be applied to .....

A. Interface

B. Class

C. Method

D. Service

Đáp án: B

22. You need to implement which interface for global exception handling in WCF?

A. IWCFException

B. IErrorHandler

C. IExceptionHandler

D. IArgumentHandler

Đáp án: B

23. Choose the correct information about security with RESTful Web Services.

A. Validation - Validate all inputs on the server. Protect your server against SQL or NoSQL injection attacks.

B. Session Based Authentication - Use session based authentication to authenticate a user whenever a request is made to a Web Service method.

C. No Sensitive Data in the URL - Never use username, password or session token in a URL, these values should be passed to Web Service via the POST method.

D. All of the others.

E. None of the others.

Đáp án: D

24. Which part of the JWT contains information needed to verify the signature?

A. Header

B. Payload

C. Signature

D. Body

Đáp án: A

25. Which of the following is typically used for user authentication in a RESTful Web Service?

A. API keys

B. JSON Web Tokens (JWT)

C. OAuth2

D. SSL/TLS certificates

Đáp án: B

26. Which of the following is a security issue with web services?

A. Confidentiality

B. Authentication

C. Network Security

D. Cyber Security

E. All of the others.

F. None of the others.

Đáp án: E

27. How Authentication and Authorization works? Choose the correct order of steps.

A. Step 1. The Request reaches the Authentication Middleware. Step 2. The Authentication Middleware checks to see if a proper credential present in the request. It will use the default authentication handler to do that. It could be a Cookies handler or JWT handler. Since it does not find any credential, it will set the User Property to an anonymous user. Step 3. Authorization Middleware (UseAuthorization()) checks to see if the destination page needs Authorization. If No then the user is allowed to visit the Page If Yes it invokes the ChallengeAsync() on the Authentication Handler. It redirects the user to Login Page.

B. Step 1. The Authentication Middleware checks to see if a proper credential present in the request. It will use the default authentication handler to do that. It could be a Cookies handler or JWT handler. Since it does not find any credential, it will set the User Property to an anonymous user. Step 2. The Request reaches the Authentication Middleware. Step 3. Authorization Middleware (UseAuthorization()) checks to see if the destination page needs Authorization. If No then the user is allowed to visit the Page If Yes it invokes the ChallengeAsync() on the Authentication Handler. It redirects the user to Login Page.

C. Step 1. The Request reaches the Authentication Middleware. Step 2. Authorization Middleware (UseAuthorization()) checks to see if the destination page needs Authorization. If No then the user is allowed to visit the Page If Yes it invokes the ChallengeAsync() on the Authentication Handler. It redirects the user to Login Page. Step 3. The Authentication Middleware checks to see if a proper credential present in the request. It will use the default authentication handler to do that. It could be a Cookies handler or JWT handler. Since it does not find any credential, it will set the User Property to an anonymous user.

D. None of the others.

Đáp án: A

28. What is the role of Protocol Buffers in gRPC with C#?

A. Protocol Buffers is used for data serialization and communication between client and server.

B. Protocol Buffers is used for Ul rendering in C# applications.

C. Protocol Buffers is used for database management in C# applications.

D. Protocol Buffers is used for logging and monitoring in C# applications.

Đáp án: A

29. gRPC services couldn't hosted by which ASP.NET Core servers?

A. Kestrel

B. TestServer

C. IIS

D. HTTP.sys

E. All of the others

Đáp án: B

30. Choose the correct information about Protocol buffers.

A. Protocol buffers, also known as Protobuf, is a protocol that Google developed internally to enable serialization and deserialization of structured data between different services.

B. Parsing Protocol Buffers (binary format) is less CPU intensive because it's closer to how a machine represents data.

C. All of the others.

D. None of the others.

Đáp án: C

31. Which of the following statements about streaming in gRPC is true?

A. gRPC only supports client-side streaming

B. gRPC only supports server-side streaming

C. gRPC supports both client-side and server-side streaming

D. gRPC does not support streaming

Đáp án: C

32. What does the following OData query retrieve: /Orders?$filter=Orderltems/all(item: item/Quantity ge 10)

A. Orders with all items having a quantity greater than or equal to 10.

B. Orders with any item having a quantity greater than or equal to 10.

C. Orders with all items having a quantity less than 10.

D. Orders with any item having a quantity less than 10.

Đáp án: A

33. What is the purpose of the Sexpand query option in OData?

A. It allows filtering the data based on specified conditions.

B. It enables including related entities in the query results.

C. It limits the number of results returned by the query.

D. It performs aggregations on the queried data.

Đáp án: B

34. What is the purpose of an OData controller in ASP.NET Core Web API?

A. To handle routing and URL mapping.

B. To provide authentication and authorization functionalities.

C. To serialize and deserialize data in OData format.

D. To expose OData endpoints and handle OData-specific queries.

Đáp án: D

35. Which class is responsible for registering the Entity Data Model and enabling OData endpoints in ASP.NET Core Web API?

A. DbContext

B. Startup

C. ApiController

D. ODataController

Đáp án: B

36. What does the $top operator do in OData?

A. It retrieves only a specified number of records from the data.

B. It selects specific properties from the data.

C. It performs pagination by skipping a specified number of records.

D. It groups the data based on specific properties.

Đáp án: A

37. What is the purpose of the app. UseAuthorization() middleware in ASP.NET Core Web API?

A. It authenticates and logs incoming requests.

B. It checks whether the request is authorized based on the user's claims or roles.

C. It processes the request body and maps it to the appropriate model.

D. It logs the response status codes and exceptions.

Đáp án: B

38. Which of the following statements is true about Middleware in ASP.NET Core Web API?

A. Middleware can only be added once in an application.

B. Middleware runs only before the request processing pipeline.

C. Middleware runs only after the response processing pipeline.

D. Multiple middleware components can be added and ordered to form a pipeline.

Đáp án: D

39. What is the default data format used by Web API for communication?

A. JSON

B. XML

C. CSV

D. Plain text

Đáp án: A

40. Choose the correct information in asynchronous programming with ASP.NET Web API about the return type.

A. Task<TResult>, for an async method that returns a value.

B. Task, for an async method that does not return a value.

C. void, which we can use for an event handler.

D. All of the others.

E. None of the others.

Đáp án: D

41. Choose the incorrect information about Async programming with ASP.NET Web API.

A. Async programming is a parallel programming technique that allows the working process to run separately from the main application thread.

B. Async programming cannot informs the main thread about the result whether it was successful or not.

C. Using async programming, we can enhance the responsiveness of our application.

D. Using async programming, we can avoid performance bottlenecks.

Đáp án: B

42. Can you have multiple [Route] attributes on a single action method in ASP.NET Core Web API?

A. Yes, but only for different HTTP methods

B. No, it is not supported in Attribute Routing

C. Yes, it allows you to define multiple routes for the same action method

D. Yes, but only for different controller classes

Đáp án: C

43. How do you add query strings to a URL in ASP.NET Core Web API?

A. By appending the parameters directly to the route template

B. By using the [QueryString] attribute in the action method's parameters

C. By using the [FromQuery] attribute in the action method's parameters

D. By adding them as headers in the request

Đáp án: C

44. What happens if model validation fails in ASP.NET Core Web API?

A. The API endpoint returns a 500 Internal Server Error response

B. The API endpoint returns a 404 Not Found response

C. The ASP.NET Core Web API automatically handles and returns a 400 Bad Request response

D. The ASP.NET Core Web API throws an exception and crashes

Đáp án: C

45. Where should you typically add the UseRouting middleware in the startup.cs file?

A. Inside the ConfigureServices method

B. Before the UseEndpoints middleware

C. After the UseAuthentication middleware

D. Inside the Configure method

Đáp án: B

46. What is the purpose of the UseEndPoints middleware in ASP.NET Core Web API?

A. To handle HTTP requests and responses

B. To map incoming requests to appropriate endpoint handlers

C. To enable routing for static files in the web application

D. To provide authentication and authorization features

Đáp án: B

47. Choose the correct information for validation the properties on the model

A. In ASP.NET Core Web API, developer can use attributes from the System.ComponentModel.DataAnnotations namespace to set validation rules for properties on the model

B. In ASP.NET Core Web API, developer can use attributes from the System.DataManagementModel.DataAnnotations namespace to set validation rules for properties on the model.

C. Both the answers are corect

D. Both the answers are incorrect

Đáp án: A

48. What are Data Transfer Objects (DTOs)?

A. Data Transfer Objects (DTOs) are classes that define a Model with sometimes predefined validation in place for HTTP responses and requests.

B. The DTOs can be known as ViewModels in MVC where you only want to expose relevant data to the View.

C. Both the answers are incorrect

D. Both the answers are correct

Đáp án: D

49. Consider with model binding in ASP.NET Core, choose one is not the role of the model binding system.

A. Converts string data to .NET types.

B. Provides the data to view using method parameters and public properties.

C. Updates properties of complex types.

D. Retrieves data from various sources such as route data, form fields, and query strings.

Đáp án: B

50. Which of the following statements is true about DTOS (Data Transfer Objects)?

A. DTOs are typically mutable objects

B. DTOs should contain complex business logic and validation rules

C. DTOs should closely resemble the structure of database tables

D. DTOs are lightweight objects used for data transfer and do not contain behavior

Đáp án: D

51. Which statement accurately describes the OData Versioning Feature in ASP.NET Core Web API?

A. It offers versioning of the OData protocol itself.

B. It enables versioning of individual controllers and actions within the Web API project.

C. It allows for versioning of the entire Web API project.

D. It provides automatic versioning of response data based on the client's request.

Đáp án: B

52. What is the main advantage of using Windows Communication Foundation (WCF) for building RESTful services?

A. Cross-platform compatibility

B. Scalability and flexibility

C. Improved performance

D. Security enhancements

Đáp án: B

53. Choose the correct information about "multiple receivers" communication type in microservices.

A. None of the others.

B. Each request can be processed by zero to multiple receivers.

C. Each request must be processed by exactly one receiver or service

D. All of the others.

Đáp án: B

54. WCF endpoint includes which components?

A. Address

B. All of the others

C. Binding

D. Contract

Đáp án: B

55. Choose the incorrect information about Async programming with ASP.NET Web API.

A. Using async programming, we can enhance the responsiveness of our application.

B. Using async programming, we can avoid performance bottlenecks.

C. Async programming cannot informs the main thread about the result whether it was successful or not.

D. Async programming is a parallel programming technique that allows the working process to run separately from the main application thread.

Đáp án: C

56. Choose the suitable reasons for choosing.NET for Web Services.

A. Targeting microservices.

B. Cross-platform.

C. Side-by-side.NET versions per application.

D. All of the others.

Đáp án: D

57. Which of the following is typically used for user authentication in a RESTful Web Service?

A. JSON Web Tokens (JWT)

B. API keys

C. SSL/TLS certificates

D. OAuth2

Đáp án: A

58. Which status code is typically returned when a resource is successfully created in a RESTful service?

A. 201 (Created)

B. 200 (OK)

C. 400 (Bad Request)

D. 204 (No Content)

Đáp án: A

59. A binding source attribute defines the location at which an action parameter's value is found. Choose the incorrect information about binding source attribute.

A. [FromBody] - Gets values from the response body.

B. [FromForm] - Gets values from posted form fields.

C. [FromQuery] - Gets values from the query string.

D. [FromRoute] - Gets values from route data.

E. [FromHeader] - Gets values from HTTP headers.

Đáp án: A

60. What is the purpose of a Data Transfer Object (DTO) in .NET?

A. To manage user input validation in forms

B. To define the structure and behavior of database tables

C. To transfer data between different layers or components of an application

D. To encapsulate business logic within a separate class

Đáp án: C

61. Which command is used to create a new ASP.NET Core Web API project using the.NET CLI?

A. dotnet new mvc

B. dotnet new api

C. dotnet new console

D. dotnet new web

Đáp án: B

62. Which protocol does gRPC primarily use for communication?

A. HTTP/2

B. WebSocket

C. FTP

D. HTTP/1.1

Đáp án: A

63. Choose the correct information about Azure Service Fabric microservice platform of Microsoft.

A. Azure Service Fabric is a distributed systems platform that makes it easy to package, deploy, and manage scalable and reliable microservices and containers.

B. None of the others.

C. Azure Service Fabric is a centralization systems platform that makes it easy to package, deploy, and manage scalable and reliable microservices and containers.

D. Azure Service Fabric is a localization systems platform that makes it easy to package, deploy, and manage scalable and reliable microservices and containers.

Đáp án: A

64. Which component in ASP.NET Core Web API is responsible for handling Content Negotiation?

A. MediaTypeFormatter

B. ApiController

C. HttpRequestMessage

D. HttpClient

Đáp án: A

65. Choose the incorrect information about validation built-in attributes. The attributes can get from the System.ComponentModel.DataAnnotations namespace.

A. [EmailAddress]: Validates that the property has an email format.

B. [Compare]: Validates that two properties in a model match.

C. [Required]: Validates that the field is not null.

D. [RegularExpression]: Validates that the property value matches a specified range.

Đáp án: D

66. What is AutoMapper?

A. All of the others.

B. AutoMapper is an object-object mapper of EntityFramework Core with ASP.NET Core Web APΡΙ.

C. Object-object mapping works by transforming an input collection of one type into an output object of a different type.

D. AutoMapper is an object-object mapper. Object-object mapping works by transforming an input object of one type into an output object of a different type.

Đáp án: D

67. What is complex model binder?

A. In the case the request is complex, pass data in request body as an entity with the desired content-type, then such kind of request is mapped by complex model binder.

B. None of the others.

C. If the request is simple, input parameter are of type int, string, Boolean, GUID, decimal, etc. and is available in the URL, then such kind of request is mapped to complex model binder.

D. In the case the response is complex, pass data in response body as an entity with the desired content-type, then such kind of response is mapped by complex model binder.

Đáp án: A

68. What is the purpose of the OData Content Types feature in ASP.NET Core Web API?

A. It allows clients to perform both read and write operations on OData-enabled endpoints.

B. It enables batch processing of multiple OData requests.

C. It provides support for querying and filtering data using the OData query syntax.

D. It allows clients to request data in different formats such as JSON or XML.

Đáp án: D

69. Which part of the JWT contains information needed to verify the signature?

A. Body

B. Header

C. Payload

D. Signature

Đáp án: B

70. What is the purpose of the $expand query option in OData?

A. It allows filtering the data based on specified conditions.

B. It performs aggregations on the queried data.

C. It limits the number of results returned by the query.

D. It enables including related entities in the query results.

Đáp án: D

71. How Authentication and Authorization works? Choose the correct order of steps.

A. Step 1. The Request reaches the Authentication Middleware. Step 2. Authorization Middleware (UseAuthorization()) checks to see if the destination page needs Authorization. If No then the user is allowed to visit the Page If Yes it invokes the ChallengeAsync() on the Authentication Handler. It redirects the user to Login Page. Step 3. The Authentication Middleware checks to see if a proper credential present in the request. It will use the default authentication handler to do that. It could be a Cookies handler or JWT handler. Since it does not find any credential, it will set the User Property to an anonymous user.

B. None of the others.

C. Step 1. The Request reaches the Authentication Middleware. Step 2. The Authentication Middleware checks to see if a proper credential present in the request. It will use the default authentication handler to do that. It could be a Cookies handler or JWT handler. Since it does not find any credential, it will set the User Property to an anonymous user. Step 3. Authorization Middleware (UseAuthorization()) checks to see if the destination page needs Authorization. If No then the user is allowed to visit the Page If Yes it invokes the ChallengeAsync() on the Authentication Handler. It redirects the user to Login Page.

D. Step 1. The Authentication Middleware checks to see if a proper credential present in the request. It will use the default authentication handler to do that. It could be a Cookies handler or JWT handler. Since it does not find any credential, it will set the User Property to an anonymous user. Step 2. The Request reaches the Authentication Middleware. Step 3. Authorization Middleware (UseAuthorization()) checks to see if the destination page needs Authorization. If No then the user is allowed to visit the Page If Yes it invokes the ChallengeAsync() on the Authentication Handler. It redirects the user to Login Page.

Đáp án: C

72. You need to configure which type of behaviour to return exception detail from WCF service?

A. OperationBehavior

B. EndpointBehavior

C. MessageBehavior

D. ServiceBehavior

Đáp án: D

73. What is the role of Web API controllers?

A. Handling HTTP requests and producing HTTP responses

B. Rendering views and templates

C. Handling user authentication

D. Managing database operations

Đáp án: A

74. What is the $filter query option used for in OData?

A. To specify the requested data fields in the response.

B. To filter the results based on specified criteria.

C. To include related entities in the response.

D. To order the results based on specified criteria.

Đáp án: B

75. What is the default media type used by the JsonMediaTypeFormatter in Web API?

A. application/xml

B. application/json

C. application/x-www-form-urlencoded

D. text/xml

Đáp án: B

76. What is CORS in ASP.NET Core Web API?

A. An attribute used to enable cross-origin requests

B. A middleware that handles Cross-Origin Resource Sharing

C. A policy used to configure cross-origin requests

D. A feature used for caching responses from different origins

Đáp án: B

77. What is the role of URI (Uniform Resource Identifier) in RESTful APIs?

A. URIs define the security and authentication settings for the API

B. URIs determine the allowed set of HTTP methods for each resource

C. URIs define the structure of the API's data models

D. URIs represent the unique identifiers for each resource in the API

Đáp án: D

78. How can you enable CORS using a named policy in ASP.NET Core Web API?

A. By configuring the policy in the ConfigureServices method of the Startup.cs file

B. By setting the allowed origins in the Authorization header of the request

C. By adding the policy configuration in the appsettings.json file

D. By applying the [EnableCors] attribute with the policy name

Đáp án: A

79. gRPC services couldn't hosted by which ASP.NET Core servers?

A. Kestrel

B. HTTP.sys

C. TestServer

D. IIS

E. None of the others

Đáp án: C

80. What is the purpose of the [Produces ResponseType] attribute in ASP.NET Core Web API?

A. It specifies the HTTP status codes that the action method can return.

B. It enables caching of the response data.

C. It defines the response type and format for the action method.

D. It allows anonymous access to the action method.

Đáp án: A

81. How can you specify the returned data properties in OData?

A. By using the $order query option.

B. By using the $select query option.

C. By using the $expand query option.

D. By using the $filter query option.

Đáp án: B

82. Which one is not a benefit of gRPC?

A. Modern, high-performance, lightweight RPC framework.

B. Supports client, server, but does not allow bi-directional streaming calls.

C. Contract-first API development, using Protocol Buffers by default, allowing for language agnostic implementations.

D. Tooling available for many languages to generate strongly-typed servers and clients.

Đáp án: B

83. Which file is the application configuration file in ASP.NET Core Web Application or Web API used to store the configuration settings (database connections strings, any application scope global variables)?

A. Startup.cs

B. Program.cs

C. appsettings.Development.json

D. appsettings.json

Đáp án: D

84. Which type of hosting is suitable for WCF services that require high scalability and availability?

A. Self-Hosting

B. Windows Service Hosting

C. WAS Hosting

D. IIS Hosting

Đáp án: C

85. To test your mappings with AutoMapper, you need to create a test that does the thing(s). Call your bootstrapper class to create all the mappings and call MapperConfiguration.AssertConfigurationlsValid

A. var config = AutoMapperConfiguration.Configure(); config.AssertAllConfigurationIsValid();

B. var config = AutoMapperConfiguration.Configure(); config.AssertConfigurationlsNotValid();

C. var config = AutoMapperConfiguration.Configure(); config.AssertConfigurationIsValid();

D. var config = AutoMapperConfiguration.Configure(); config.AssertConfigurationlsValid(true).

Đáp án: C

86. How can you enable CORS using endpoint routing in ASP.NET Core Web API?

A. By using the app. UseCors() method in the Configure method of the startup.cs file

B. By configuring the CORS options in the appsettings.json file

C. By setting the allowed origins in the Authorization header of the request

D. By adding the [EnableCors] attribute to the Startup.cs file

Đáp án: A

87. To force clients to set a value, make the property nullable and set the Required attribute

A. [RequireAttribute(0, 999)] public decimal? Price { get; set; }

B. [RequiredNotNull] public decimal? Price {get; set; }

C. [RequiredRange(0, 999)] public decimal? Price { get; set; }

D. [Required] public decimal? Price {get; set; }

Đáp án: D

88. Choose the incorrect HTTP response components.

A. Each Response must have a unique URL.

B. Response Headers.

C. HTTP Status Code.

D. Data Response can have data return to the client.

Đáp án: A

89. Choose the correct information about scaling RESTful web services.

A. None of the others.

B. RESTful web services support only support vertical scaling in communication.

C. RESTful web services support both vertical and horizontal scaling.

D. RESTful web services depend on the IP address and port number of the system to get a response.

Đáp án: C

90. What is ASP.NET Core Identity?

A. A framework for managing user authentication and authorization

B. A library for handling database operations in ASP.NET Core

C. A middleware used for routing in ASP.NET Core

D. A feature for generating HTML views in ASP.NET Core

Đáp án: A

91. What is a microservice?

A. A self-contained, independent service

B. A database management system

C. A monolithic application

D. A programming language

Đáp án: A

92. What does "Accept: application/json; q=0.8, application/xml;q=0.9" mean in the "Accept" header of an HTTP Request Message?

A. The server should respond with either JSON or XML data, but XML is preferred over JSON.

B. The server should respond with XML data only.

C. The server should respond with either JSON or XML data, but JSON is preferred over XML.

D. The server should respond with JSON data only.

Đáp án: A

93. What is the role of Model in ASP.NET Core MVC?

A. The Models in ASP.NET Core MVC contains a set of classes that are used to represent the domain data or business data as well as it also contains logic to manage the domain/business data.

B. Models are responsible for the data and these data are used on Controllers.

C. Both A and B

D. Neither A nor B

Đáp án: A

94. Choose the correct information about HTTP Request Pipeline

A. The Request Pipeline in ASP.NET Core Web API Application can have multiple middlewares

B. All of the others.

C. Once the pipeline is completed, then only it navigates the request to the corresponding controller action method.

D. Before hitting the controller action method, the request has to pass through a pipeline.

Đáp án: B

95. What is a key difference between gRPC and REST in terms of payload serialization?

A. gRPC uses Protocol Buffers, REST uses XML

B. gRPC uses XML, REST uses JSON

C. gRPC uses JSON, REST uses XML

D. gRPC uses JSON, REST uses Protocol Buffers

Đáp án: A

96. What is the purpose of the NegotiateContent method in IContentNegotiator?

A. It negotiates and selects the appropriate response format based on the client's preferences.

B. It checks for authentication and authorization.

C. It handles routing and URL mapping.

D. It handles serialization and deserialization of data.

Đáp án: A

97. What is the purpose of the UseEndPoints middleware in ASP.NET Core Web API?

A. To map incoming requests to appropriate endpoint handlers

B. To provide authentication and authorization features

C. To enable routing for static files in the web application

D. To handle HTTP requests and responses

Đáp án: A

98. Which WCF binding is commonly used for building RESTful services?

A. BasicHttpBinding

B. WSHttpBinding

C. NetTcpBinding

D. WebHttpBinding

Đáp án: D

99. What is the purpose of the authentication middleware in ASP.NET Core Web API?

A. To enable authentication for the web application

B. To map incoming requests to appropriate endpoint handlers

C. To handle incoming HTTP requests and responses

D. To provide role-based authorization

Đáp án: A

100. Choose the correct information about scaling RESTful web services.

A. RESTful web services support both vertical and horizontal scaling.

B. RESTful web services depend on the IP address and port number of the system to get a response.

C. None of the others.

D. RESTful web services support only support vertical scaling in communication.

Đáp án: A

101. How can you enable CORS using a named policy in ASP.NET Core Web API?

A. By setting the allowed origins in the Authorization header of the request

B. By applying the [EnableCors] attribute with the policy name

C. By adding the policy configuration in the appsettings.json file

D. By configuring the policy in the ConfigureServices method of the Startup.cs file

Đáp án: D

102. Which of the message exchange patterns is not supported in WCF?

A. Multi-way

B. One-way

C. Request-reply

D. Duplex

Đáp án: A

103. Choose the correct information about Azure Service Fabric microservice platform of Microsoft.

A. None of the others.

B. Azure Service Fabric is a distributed systems platform that makes it easy to package, deploy. and manage scalable and reliable microservices and containers.

C. Azure Service Fabric is a localization systems platform that makes it easy to package, deploy, and manage scalable and reliable microservices and containers.

D. Azure Service Fabric is a centralization systems platform that makes it easy to package, deploy, and manage scalable and reliable microservices and containers.

Đáp án: B

104. What happens if model validation fails in ASP.NET Core Web API?

A. The ASP.NET Core Web API throws an exception and crashes

B. The ASP.NET Core Web API automatically handles and returns a 400 Bad Request response

C. The API endpoint returns a 404 Not Found response

D. The API endpoint returns a 500 Internal Server Error response

Đáp án: B

105. Which command is used to create a new ASP.NET Core Web API project using the.NET CLI?

A. dotnet new web

B. dotnet new console

C. dotnet new mvc

D. dotnet new api

Đáp án: D

106. Which of the following is a benefit of using OData in ASP.NET Core Web API?

A. Increased performance for API requests.

B. Simplified data access and query capabilities.

C. Enhanced support for file uploads and downloads.

D. Improved security for API endpoints.

Đáp án: D

107. To force clients to set a value, make the property nullable and set the Required attribute

A. [RequiredNotNull] public decimal? Price { get; set; }

B. [RequiredRange(0, 999)] public decimal? Price { get; set; }

C. [Required] public decimal? Price { get; set; }

D. [RequireAttribute(0, 999)] public decimal? Price {get; set; }

Đáp án: C

108. Which package in ASP.NET Core is commonly used for implementing JWT authentication?

A. Microsoft. EntityFramework Core

B. Microsoft.AspNetCore.Http

C. Microsoft.AspNetCore.Mvc

D. Microsoft.AspNetCore.Authentication.JwtBearer

Đáp án: D

109. Which is not an attribute that can be used to configure the behavior of web API controllers and action methods?

A. [Binding]

B. [Route]

C. [HttpGet]

D. [Produces]

Đáp án: A

110. A binding source attribute defines the location at which an action parameter's value is found. Which one is not a binding source attribute?

A. [FromQuery]

B. [FromRouting]

C. [FromHeader]

D. [FromServices]

Đáp án: B

111. What is the role of IContentNegotiator in ASP.NET Core Web API?

A. It handles serialization and deserialization of data.

B. It checks for authentication and authorization.

C. It handles routing and URL mapping.

D. It negotiates and selects the appropriate response format based on the client's preferences.

Đáp án: D

112. What is the purpose of using media types (MIME types) in RESTful services?

A. To define the URL structure for resource endpoints

B. To enforce security protocols in the communication

C. To change a resource in a RESTful service

D. To specify the format of the data being sent or received

Đáp án: D

113. What is the role of URI (Uniform Resource Identifier) in RESTful APIs?

A. URIs represent the unique identifiers for each resource in the API

B. URIs define the security and authentication settings for the API

C. URIs define the structure of the API's data models

D. URIs determine the allowed set of HTTP methods for each resource

Đáp án: A

114. How can you pass multiple dynamic values in the route template of an ASP.NET Core Web API endpoint?

A. By using the [MultipleValues] attribute on the route parameter

B. By passing the values as query string parameters

C. By separating the values using commas (.)

D. By using multiple route parameters in the route template

Đáp án: D

115. What is the role of the "Accept" header in Content Negotiation?

A. It specifies the encoding format for the request body.

B. It specifies the client's preferred media types for the response.

C. It specifies the content type that the server should return.

D. It specifies the authentication credentials for the request.

Đáp án: B

116. Choose the incorrect information about ASP.NET Core Web API.

A. ASP.NET Core Web API is an application can interact with a resource by knowing the resource only.

B. Calls to a Web API service are based on the core HTTP verbs (Get. Put. Post, Delete) through a uniform resource identifier (URI).

C. ASP.NET Core Web API. from the beginning, was designed to be a service-based framework for building REpresentational State Transfer (RESTful) services.

D. It is based on the MVC framework minus the V (view), with optimizations for creating headless services.

Đáp án: A

117. What is the purpose of the Service Metadata Feature in OData?

A. To provide information about the available OData endpoints and entities in the Web API.

B. To allow automatic retrieval of remote OData services.

C. To enable configuration of dynamic service routes for OData endpoints.

D. To enable automatic generation of sample data for OData response.

Đáp án: A

118. JavaScript is a powerful programming language for calling ASP.NET Core Web API. Which object is used to call the Web API from JavaScript object?

A. XMLHttpResponse (XHR) object

B. XMLHttpRequest (XHR) object

C. XMLHttpResponseObject (XHR) object

D. XMLHttpRequestObject (XHR)

Đáp án: B

119. What is the default media type used by the JsonMediaTypeFormatter in Web API?

A. application/x-www-form-urlencoded

B. text/xml

C. application/json

D. application/xml

Đáp án: C

120. Which of the following statements is true about the routing middleware in ASP.NET Core Web API?

A. Routing is only applicable for POST requests

B. Routing is not supported in ASP.NET Core Web API

C. Routing is applicable for all types of HTTP requests

D. Routing is only applicable for GET requests

Đáp án: C

121. By passing parameters in the URL of the HTTP request

A. By using query string parameters in the URL

B. By adding data to the header of the HTTP request

C. By adding data to the body of the HTTP request

D. By passing parameters in the URL of the HTTP request

Đáp án: A

122. To test your mappings with AutoMapper, you need to create a test that does the thing(s). Call your bootstrapper class to create all the mappings and call MapperConfiguration.AssertConfigurationlsValid

A. var config AutoMapperConfiguration.Configure(): config.AssertConfigurationlsNotValid():

B. var config AutoMapperConfiguration.Configure(); config.AssertAllConfigurationis Valid():

C. var config AutoMapperConfiguration.Configure(): config.AssertConfigurationlsValid(true):

D. var config AutoMapperConfiguration.Configure(): config.AssertConfigurationIsValid():

Đáp án: D

123. What types of variables can be used in a route template in ASP.NET Core Web API?

A. Any type of data

B. Only integers

C. Only predefined types like DateTime or Guid

D. Only strings

Đáp án: C

124. Which of the following open-source libraries is used by WEB API for JSON serialization?

A. Json.NET

B. System.Data.Json.NET

C. System.Text.Json

D. Microsoft.Extensions.Json.NET

Đáp án: A

125. How do gRPC and REST differ in terms of communication protocol?

A. gRPC uses TCP, REST uses UDP

B. gRPC uses HTTP/1.1. REST uses HTTP/2

C. gRPC uses WebSocket, REST uses MQTT

D. gRPC uses HTTP/2, REST uses HTTP/1.1

Đáp án: D

126. How to add gRPC services to an ASP.NET Core application (in Startup.cs)?

A. public void ConfigureServices (IServiceCollection services) { services.AddGrpc(); }

B. public void ConfigureServices (IApplication Builer services) { services.AddGrpc(): }

C. public void Configure(IServiceCollection services) { services.AddGrpc(): }

D. public void Configure(IApplication Builder services) { services.AddGrpc(): }

Đáp án: A

127. What is the purpose of the NegotiateContent method in IContent Negotiator?

A. It negotiates and selects the appropriate response format based on the client's preferences.

B. It checks for authentication and authorization.

C. It handles routing and URL mapping.

D. It handles serialization and deserialization of data.

Đáp án: A

128. What are Data Transfer Objects (DTOs)?

A. None of the others.

B. Data Transfer Objects (DTOs) are classes that define a Model with sometimes predefined validation in place for HTTP responses and requests.

C. All of the others.

D. The DTOs can be known as ViewModels in MVC where you only want to expose relevant data to the View.

Đáp án: C

129. Which of the following statements about streaming in gRPC is true?

A. gRPC only supports client-side streaming

B. gRPC only supports server-side streaming

C. gRPC does not support streaming

D. gRPC supports both client-side and server-side streaming

Đáp án: D

130. What is ASP.NET Core Identity?

A. A library for handling database operations in ASP.NET Core

B. A framework for managing user authentication and authorization

C. A feature for generating HTML views in ASP.NET Core

D. A middleware used for routing in ASP.NET Core

Đáp án: B

131. In Web API, how can you bind the incoming data to a model automatically?

A. By using the [FromRoute] attribute on the API method parameter

B. By using the [FromBody] attribute on the model class

C. By using the [FromQuery] attribute on the API method parameter

D. By using the [FromBody] attribute on the API method parameter

Đáp án: D

132. Which namespace needs to be imported to use the "ControllerBase" class?

A. System.Net

B. Microsoft.AspNetCore.Mvc

C. System.Web.Mvc

D. System.Web

Đáp án: B

133. How is a one-to-many relationship represented in OData?

A. By linking the parent entity to the related entities using navigation properties.

B. By including the related entity IDs as an array within the parent entity.

C. By embedding the related entities' data within the parent entity.

D. By creating separate tables for each relationship type.

Đáp án: A

134. Which OData operator is used to perform paging of data?

A. $expand

B. $skip

C. $top

D. $filter

Đáp án: B

135. Use the EF Core Migrations feature to create the database. Choose the correct information.

A. The Migrations is a set of tools that create and update a database to match the data model.

B. The Update Database of Migration is a set of tools that create and update a database to match the data model.

C. The Migrations is a set of Web API component that create and update a database to match the data model.

D. None of the others.

Đáp án: A

136. MessageContract can be applied to

A. Interface

B. Method

C. Class

D. Service

Đáp án: C

137. What is the purpose of HTTP headers in RESTful APIs?

A. HTTP headers contain metadata about the request or response

B. HTTP headers store the actual data being transferred in the API

C. HTTP headers enforce security and authentication in the API

D. HTTP headers define the structure of the API's data models

Đáp án: A

138. What is the purpose of the "route parameters" in a RESTful service?

A. They control the behavior of caching in RESTful services

B. They are used to define the response format (e.g.. JSON or XML)

C. They allow for passing data as part of the URL to identify specific resources

D. They are used to specify the type of HTTP verb to be used

Đáp án: C

139. What is the purpose of using the [ServiceContract] attribute in WCF?

A. To specify the XML namespace for the service

B. To define a service operation

C. To mark a class as a service implementation

D. To mark a class as a data contract

Đáp án: C

140. What is a key difference between gRPC and REST in terms of payload serialization?

A. gRPC uses JSON, REST uses XML

B. gRPC uses Protocol Buffers, REST uses XML

C. gRPC uses XML, REST uses JSON

D. gRPC uses JSON, REST uses Protocol Buffers

Đáp án: B

141. What is the significance of resources in RESTful APIs?

A. Resources represent the data entities exposed by the API

B. Resources are the network endpoints of the API

C. Resources refer to the methods and operations provided by the API

D. Resources are the protocols used to communicate with the API

Đáp án: A

142. Which HTTP verb is used to create a new resource in a RESTful service?

A. GET

B. POST

C. PUT

D. DELETE

Đáp án: B

143. What is.NET for Docker containers?

A. A containerization platform developed by Microsoft

B. A programming language specifically designed for Docker containers

C. A runtime environment for executing.NET applications in Docker containers

D. A container orchestration tool for managing Docker containers

Đáp án: C

144. Choose the correct information about Azure Service Fabric - microservice platform of Microsoft.

A. Azure Service Fabric is a distributed systems platform that makes it easy to package, deploy, and manage scalable and reliable microservices and containers.

B. Azure Service Fabric is a centralization systems platform that makes it easy to package, deploy, and manage scalable and reliable microservices and containers.

C. Azure Service Fabric is a localization systems platform that makes it easy to package, deploy, and manage scalable and reliable microservices and containers.

D. None of the others.

Đáp án: A

145. Which one is not communication in microservices?

A. Synchronous messaging

B. Asynchronous messaging

C. Concurrency messaging

D. None of the others.

Đáp án: C

146. To test your mappings with AutoMapper, you need to create a test that does the thing(s). Call your bootstrapper class to create all the mappings and call MapperConfiguration.AssertConfigurationIsValid

A. var config = AutoMapperConfiguration.Configure(); config.AssertConfigurationIsValid();

B. var config = AutoMapperConfiguration.Configure(); config.AssertConfigurationIsNotValid();

C. var config = AutoMapperConfiguration.Configure(); config.AssertAllConfigurationIsValid();

D. var config = AutoMapperConfiguration.Configure(); config.AssertConfigurationIsValid(true);

Đáp án: A

147. What is the default CORS policy behavior in ASP.NET Core Web API if no policy is explicitly configured?

A. All cross-origin requests are allowed

B. Only same-origin requests are allowed

C. All cross-origin requests are blocked

D. An exception is thrown for all cross-origin requests

Đáp án: B

148. By passing parameters in the URL of the HTTP request

A. By adding data to the body of the HTTP request

B. By using query string parameters in the URL

C. By adding data to the header of the HTTP request

D. By passing parameters in the URL of the HTTP request

Đáp án: B

149. What are static files in ASP.NET Core API Project?

A. Images

B. Html files

C. CSS files

D. JavaScript files

E. All of the others

Đáp án: E

150. What is Content Negotiation in ASP.NET Core Web API?

A. The process of negotiating content prices between client and server.

B. The process of selecting the appropriate response format based on the request's Accept header.

C. The process of caching response content on the server.

D. The process of securing content transmission between client and server.

Đáp án: B

151. Which HTTP header is used to specify the preferred media types in the request?

A. Accept

B. Content-Type

C. Authorization

D. Cache-Control

Đáp án: A

152. What is the default media type used by the JsonMediaTypeFormatter in Web API?

A. application/json

B. text/xml

C. application/xml

D. application/x-www-form-urlencoded

Đáp án: A

153. What media type formatters in ASP.NET Core Web API?

A. Media type formatters are classes that are responsible for serialization data.

B. The Web API cannot understand request data format in serializing request/response data and send data in a format that the client expects.

C. XmlMediaTypeFormatter class handles HTML form URL-encoded data.

D. JsonMediaTypeFormatter class handles both XML format and JSON format.

Đáp án: A

154. What is the main difference between [DataContract] and [MessageContract] in WCF?

A. [DataContract] is used for defining data structures, while [MessageContract] is used for defining message formats.

B. [DataContract] is used for defining message headers, while [MessageContract] is used for defining message bodies.

C. [DataContract] is used for request messages, while [MessageContract] is used for response messages.

D. [DataContract] is used for contract-first development, while [MessageContract] is used for code-first development.

Đáp án: A

155. WCF endpoint includes which components?

A. Address

B. Binding

C. Contract

D. All of the others

Đáp án: D

156. Which WCF binding is commonly used for building RESTful services?

A. BasicHttpBinding

B. NetTcpBinding

C. WebHttpBinding

D. WSHttpBinding

Đáp án: C

157. Authorization is the process of:

A. Verifying the identity of a user or a client

B. Granting access to specific resources or actions

C. Encrypting sensitive data during transmission

D. Logging user activities for auditing purposes

Đáp án: B

158. Which authentication middleware is commonly used with ASP.NET Core Identity?

A. UseAuthentication

B. UseAuthorization

C. UseRouting

D. UseEndpoints

Đáp án: A

159. Choose the correct information to configure autoscaling for an Azure solution.

A. Azure App Service has built-in autoscaling. Autoscale settings apply to all of the apps within an App Service.

B. Azure App Service has built-in autoscaling only at the role level.

C. The connection is slow in autoscaling option with Azure App Sercive.

D. All of the others.

Đáp án: A

160. What is the purpose of the [AllowAnonymous] attribute in ASP.NET Core authentication?

A. To allow anonymous access to an action method, overriding authentication rules

B. To specify multiple authentication schemes for an action method

C. To skip model validation for a specific action method

D. To allow anonymous access to a specific controller, overriding authentication rules

Đáp án: A

161. What is the purpose of the [Authorize] attribute in ASP.NET Core Web API?

A. It is used to create and manage user accounts

B. It is used to enable authentication for a specific action method or controller

C. It is used to define custom authorization policies

D. It is used to handle exceptions during the authorization process

Đáp án: B

162. Can Protocol Buffers be used for bidirectional streaming in gRPC with C#?

A. Yes, Protocol Buffers support bidirectional streaming in gRPC with C#.

B. No, Protocol Buffers only support unidirectional streaming in gRPC with C#.

C. Bidirectional streaming is not supported by gRPC with C#.

D. Protocol Buffers cannot be used for streaming in gRPC with C#.

Đáp án: A

163. Which one is not a benefit of gRPC?

A. Supports client, server, but does not allow bi-directional streaming calls.

B. Tooling available for many languages to generate strongly-typed servers and clients.

C. Contract-first API development, using Protocol Buffers by default, allowing for language agnostic implementations.

D. Modern, high-performance, lightweight RPC framework.

Đáp án: A

164. How do gRPC and REST differ in terms of communication protocol?

A. gRPC uses HTTP/1.1, REST uses HTTP/2

B. gRPC uses HTTP/2, REST uses HTTP/1.1

C. gRPC uses TCP, REST uses UDP

D. gRPC uses WebSocket, REST uses MQTT

Đáp án: B

165. Which the OData query option that determine all attributes or properties to include in the fetched result?

A. $select

B. $top

C. Şinlinecount

D. $selectall

Đáp án: A

166. What is the purpose of the $filter query option in OData?

A. It allows clients to request a specific subset of entity properties.

B. It enables clients to perform complex filtering operations on entity collections.

C. It allows clients to update or modify existing entities.

D. It provides a way to sort the returned entities based on a specified property.

Đáp án: B

167. How can you specify the returned data properties in OData?

A. By using the $select query option.

B. By using the $filter query option.

C. By using the $order query option.

D. By using the $expand query option.

Đáp án: A

168. How does OData enable clients to query and filter data?

A. By using custom SQL queries.

B. By sending raw JSON data in the request payload.

C. By using a standardized query syntax in the URL.

D. By encoding data using a secure encryption algorithm.

Đáp án: C

169. What is the role of Web API controllers?

A. Handling user authentication

B. Managing database operations

C. Handling HTTP requests and producing HTTP responses

D. Rendering views and templates

Đáp án: C

170. Which namespace needs to be imported to use the "ControllerBase" class?

A. System.Net

B. System.Web

C. Microsoft.AspNetCore.Mvc

D. System.Web.Mvc

Đáp án: C

171. In ASP.NET Core Web API, which file is used to configure the application and its services?

A. Program.cs

B. Startup.cs

C. appsettings.json

D. appsettings.Development.json

Đáp án: A

172. Which middleware is used to serve static files like HTML, CSS, and JavaScript in ASP.NET Core Web API?

A. app.UseExceptionHandler()

B. app.UseStaticFiles()

C. app.UseHttpsRedirection()

D. app.UseCors()

Đáp án: B

173. How can you include route parameters in Attribute Routing?

A. By adding curly braces {} around the parameter name in the route template

B. By adding square brackets around the parameter name in the route template

C. By using the [RouteParam] attribute before the parameter name in the action method

D. By adding the parameter name directly in the route template

Đáp án: A

174. What is complex type binding?

A. HTTP Methods like POST and PUT where you have to send the send model/entity data to the server, uses complex type binding, by default.

B. POST and PUT can also use combination of primitive and complex type. In the case you want to update data, you can pass the Id in query string and the data to be updated in response body.

C. Both the answers are corect

D. Both the answers are incorrect

Đáp án: C

175. Which annotation attribute can be used to specify validation rules in ASP.NET Core Web API?

A. [Validate]

B. [Required]

C. [Rule]

D. [Validation]

Đáp án: B

176. To force clients to set a value, make the property nullable and set the Required attribute

A. [Required] public decimal? Price { get; set; }

B. [RequireAttribute(0, 999)] public decimal? Price { get; set; }

C. [RequiredRange(0, 999)] public decimal? Price { get; set; }

D. [RequiredNotNull] public decimal? Price { get; set; }

Đáp án: A

177. Which pattern can be used alongside DTOs (Data Transfer Objects) to simplify and automate the mapping between objects?

A. Singleton Pattern

B. Observer Pattern

C. Factory Pattern

D. Mapper Pattern

Đáp án: D

178. Web API does not automatically return an error to the client when validation fails. It is up to the controller action to check the model state and respond appropriately. Which property is using in this case?

A. ModelState.IsValid

B. ModelState.IsCorrect

C. ModelState.IsVerify

D. ModelState.Is True

Đáp án: A

179. Which HTTP response code represents a successful request in REST?

A. 200 (OK)

B. 300 (Multiple Choices)

C. 400 (Bad Request)

D. 500 (Internal Server Error)

Đáp án: A

180. What is the purpose of the HTTP POST method in a RESTful API?

A. To retrieve or fetch a resource from the server

B. To update an existing resource on the server

C. To delete a resource from the server

D. To create a new resource on the server

Đáp án: D

181. Which Docker command is used to run a .NET container image?

A. docker build

B. docker run

C. docker stop

D. docker push

Đáp án: B

182. What is the role of IContentNegotiator in ASP.NET Core Web API?

A. It handles routing and URL mapping.

B. It checks for authentication and authorization.

C. It negotiates and selects the appropriate response format based on the client's preferences.

D. It handles serialization and deserialization of data.

Đáp án: C

183. What is JSON?

A. JSON (JavaScript Object Notation): It is similar to HTML but is more flexible than HTML because it allows users to create their own custom tags.

B. JSON (JavaScript Object Notation): It is especially designed to store and transport data.

C. JSON (JavaScript Object Notation): It is used for representing structured information such as documents, data, configuration, etc.

D. JSON (JavaScript Object Notation): It is a lightweight format designed to store and transport data.

Đáp án: B, D

184. Which attribute can be used to override the default media type for a specific action or controller in ASP.NET Core Web API?

A. \[HttpPost]

B. \[AllowAnonymous]

C. \[Produces]

D. \[Route]

Đáp án: C

185. What is the purpose of using the \[ServiceContract] attribute in WCF?

A. To define a service operation

B. To mark a class as a data contract

C. To specify the XML namespace for the service

D. To mark a class as a service implementation

Đáp án: D

186. Which type of hosting is suitable for WCF services that require high scalability and availability?

A. IIS Hosting

B. Self-Hosting

C. Windows Service Hosting

D. WAS Hosting

Đáp án: D

187. Which type of contract is applicable to interface in WCF?

A. Operation contract

B. Message contract

C. Service contract

D. Data contract

Đáp án: C

188. What is the purpose of the authentication middleware in ASP.NET Core Web API?

A. To handle incoming HTTP requests and responses

B. To enable authentication for the web application

C. To map incoming requests to appropriate endpoint handlers

D. To provide role-based authorization

Đáp án: B

189. Which parts of the JWT are typically Base64Url encoded?

A. Header and payload

B. Payload and signature

C. Header and signature

D. All parts of the JWT are Base64Url encoded

Đáp án: A

190. Protocol Buffers is used to define the Messages (data, Request and Response) and Service (Service name and RPC endpoints). Choose the correct syntax.

A. syntax = "proto3"; service Greeter { rpc SayHello (HelloRequest) returns (HelloReply); } message HelloRequest ( string name = 1; } message HelloReply { string message = 1; }

B. syntax = "proto3"; message Greeter { rpc SayHello (HelloRequest) replies (HelloReply); } service HelloRequest { string name = 1; } service HelloReply { string message = 1; }

Đáp án: A

191. How are gRPC services registered and configured in ASP.NET Core?

A. In the ConfigureServices method of the Startup class

B. By adding a configuration file named appSettings.json

C. By modifying the Global.asax file

D. In the ConfigureServices method of the Controller class

Đáp án: A

192. Which protocol does gRPC primarily use for communication?

A. HTTP/1.1

B. HTTP/2

C. WebSocket

D. FTP

Đáp án: B

193. Choose the correct information about EnableQueryAttribute class ([EnableQuery] attribute)

A. This class defines an attribute that can be applied to an action to enable querying using the OData query syntax.

B. This class defines both attribute and method that can be applied to an action to enable querying using the OData query syntax.

C. This class defines a method that can be applied to an action to enable querying using the OData query syntax.

D. None of the others.

Đáp án: A

194. Choose the correct information about pagging OData.

A. To enable paging, just mention the page count at the [Queryable] [EnableQuery(PageSize =5)] public IActionResult GetData() => Ok(objService.GetObjects());

B. To enable paging, just mention the page count at the [Queryable] [EnableQuery(PageIndex =5)] public IActionResult GetData() => Ok(objService.GetObjects());

C. To enable paging, just mention the page count at the [AllowQueryable] [AllowEnableQuery(PageSize =5)] public IActionResult GetData() => Ok(objService.GetObjects());

Đáp án: A

195. A binding source attribute defines the location at which an action parameter's value is found. Which one is not a binding source attribute?

A. [FromServices]

B. [FromHeader]

C. [FromQuery]

D. [FromRouting]

Đáp án: D

196. ASP.NET Core supports creating web APIs using controllers or using minimal APIs. Controllers in a Web API are classes that derive from which of the following class?

A. ControllerBase

B. Controller

C. ControllerAttribute

D. ControllerContext

Đáp án: A

197. Which information is true about ASP.NET Core Web API Architecture?

A. The ASP.NET Web API framework has been designed using the task-based asynchronous programming model from the top to the bottom.

B. Ability to host both in IIS (or development server) and in any nonweb server process (called self-hosted).

C. All of the others.

D. Can customize many elements of ASP.NET Core Web API by supplying custom implementation.

Đáp án: C

198. What is the purpose of the Primitive Model Binder in ASP.NET Core Web API?

A. It is used for binding complex models with nested properties

B. It is used for binding primitive types like strings and integers

C. It is used for validating model properties

D. It is used for handling query string parameters

Đáp án: B

199. Which of the following is true about the [HttpGet] attribute in ASP.NET Core Web API?

A. It specifies that the route should only handle GET requests

B. It is used to map the route to a specific HTTP method

C. It is not supported in Attribute Routing

D. It is used to define the route template for the action method

Đáp án: A

200. What is the purpose of the UseRouting middleware in ASP.NET Core Web API?

A. To handle HTTP requests and responses

B. To map incoming requests to appropriate endpoint handlers

C. To enable routing for static files in the web application

D. To provide authentication and authorization features

Đáp án: B

201. What is model validation in ASP.NET Core Web API?

A. A process to check the authenticity of the model data

B. A way to validate that the model conforms to specified rules

C. A technique to validate the authentication of the API user

D. A feature to validate the structure of the model schema

Đáp án: B

202. What is the purpose of a Data Transfer Object (DTO) in .NET?

A. To transfer data between different layers or components of an application

B. To define the structure and behavior of database tables

C. To encapsulate business logic within a separate class

D. To manage user input validation in forms

Đáp án: A

203. What is AutoMapper?

A. AutoMapper is an object-object mapper. Object-object mapping works by transforming an input object of one type into an output object of a different type.

B. AutoMapper is an object-object mapper of EntityFramework Core with ASP.NET Core Web API.

C. Object-object mapping works by transforming an input collection of one type into an output object of a different type.

D. All of the others.

Đáp án: A

204. Choose the incorrect information about ASP.NET Core Web AΡΙ.

A. ASP.NET Core Web API, from the beginning, was designed to be a service-based framework for building REpresentational State Transfer (RESTful) services.

B. It is based on the MVC framework minus the V (view), with optimizations for creating headless services.

C. ASP.NET Core Web API is an application can interact with a resource by knowing the resource only.

D. Calls to a Web API service are based on the core HTTP verbs (Get, Put, Post, Delete) through a uniform resource identifier (URI).

Đáp án: C

205. What is a key difference between gRPC and REST in terms of payload serialization?

A. gRPC uses XML, REST uses JSON

B. gRPC uses JSON, REST uses Protocol Buffers

C. gRPC uses Protocol Buffers, REST uses XML

D. gRPC uses JSON, REST uses XML

Đáp án: C

206. What is the role of URI (Uniform Resource Identifier) in RESTful APIs?

A. URIs define the structure of the API's data models

B. URIs represent the unique identifiers for each resource in the API

C. URIs determine the allowed set of HTTP methods for each resource

D. URIs define the security and authentication settings for the API

Đáp án: B

207. Which status code is typically returned when a resource is successfully created in a RESTful service?

A. 200 (OK)

B. 201 (Created)

C. 204 (No Content)

D. 400 (Bad Request)

Đáp án: B

208. What is not a microservice attribute?

A. Independent deployment

B. Technology adoption

C. Consistency and resiliency

D. Combined functionality

Đáp án: D

209. Which of the following is executed on each request in RESTful with ASP.NET Core Web API?

A. Startup

B. Middlewares

C. Main method

D. All of the others.

Đáp án: B

210. Which of the following is correct?

A. jQuery is a JavaScript library for calling ASP.NET Core Web API

B. jQuery is a JavaScript simple template for calling ASP.NET Core Web API

C. jQuery is a JSON library for calling ASP.NET Core Web API

D. jQuery is a JSON template for calling ASP.NET Core Web API

Đáp án: A

211. What is not the purpose of a Media Formatter in web development?

A. To format data into a specific media type for HTTP responses

B. To format data into a specific media type for HTTP requests

C. To serialize and deserialize objects for communication between client and server

D. To define the data type for attribute routing

Đáp án: D

212. How to configure JSON Serialization in ASP.NET Core?

A. public void ConfigureServices (IServiceCollection services) { services.AddControllers With Views().AddJsonOptions(options => options.JsonSerializerOptions. PropertyNamingPolicy = null); }

B. public void Configure (IServiceCollection services) { services.AddControllers With Views().AddJsonOptions(options => options.JsonSerializerOptions.PropertyNamingPolicy = null); }

C. public void ConfigureServices (IApplication Builder services) { services.AddControllersWith Views().AddJsonOptions(options => options.JsonSerializerOptions.PropertyNamingPolicy = null); }

D. public void ConfigureServices (IEnvironmentBuilder services) { services.AddControllers With Views().AddJsonOptions(options => options.JsonSerializerOptions. PropertyNamingPolicy = null); }

Đáp án: A

213. Which attribute can be used to specify the media type for a specific action method in ASP.NET Core Web API?

A. [HttpPost]

B. [AllowAnonymous]

C. [Produces]

D. [Route]

Đáp án: C

214. WCF stands for what?

A. Windows Communication Framework

B. Windows Communication Foundation

C. Windows Connection Framework

D. Windows Com Framework

Đáp án: B

215. Which utility can be used to create WSDL from WCF service?

A. Wcf.exe

B. Svc.exe

C. ILDASM.exe

D. SvcUtil.exe

Đáp án: D

216. MessageContract can be applied to

A. Interface

B. Class

C. Method

D. Service

Đáp án: B

217. Which contract in WCF maps data contracts to SOAP envelopes?

A. MessageContract

B. DataContract

C. OperationContract

D. ServiceContract

Đáp án: A

218. Authentication is the process of:

A. Verifying the identity of a user or a client

B. Granting access to specific resources or actions

C. Encrypting sensitive data during transmission

D. Logging user activities for auditing purposes

Đáp án: A

219. What are Identity Claims in ASP.NET Core Identity?

A. Additional information associated with a user, like role membership or email

B. Secret tokens used for user authentication

C. Encrypted data stored in the user cookie

D. User credentials used for password-based authentication

Đáp án: A

220. What is the purpose of an authentication handler in ASP.NET Core?

A. To validate user credentials and issue authentication tickets

B. To handle encryption and decryption of data

C. To handle user session management

D. To enforce authorization rules on the application

Đáp án: A

221. What is the serialization format used by gRPC?

A. JSON

B. XML

C. Protocol Buffers

D. YAML

Đáp án: C

222. Which one is not correct about OData protocol?

A. The OData protocol is the same with other REST-based web service approaches.

B. The OData protocol is an application-level protocol for interacting with data via RESTful interfaces.

C. The OData protocol improves semantic interoperability between systems and allows an ecosystem to emerge.

D. None of the others.

Đáp án: A

223. How can you enable OData routing in ASP.NET Core Web API?

A. By adding the [ODataRoute] attribute to the controller or action method.

B. By configuring the routing in the Startup class.

C. By installing a third-party OData middleware.

D. By using the [ApiController] attribute on the controller.

Đáp án: B

224. Which OData query example filters a collection of products to retrieve those with any related orders?

A. /Products?$filter=Any(Orders)

B. /Products?$filter=All(Orders)

C. /Products?$filter=Any(Orders eq true)

D. /Products?$filter=All(Orders eq true)

Đáp án: A

225. Which command is used to create a new ASP.NET Core Web API project using the .NET CLI?

A. dotnet new console

B. dotnet new mvc

C. dotnet new api

D. dotnet new web

Đáp án: C

226. What is the primary role of ASP.NET Web API?

A. Serving dynamic web pages

B. Handling and responding to HTTP requests and building RESTful APIs

C. Server-side form validation

D. Managing database connections

Đáp án: B

227. Which class does "ControllerBase" inherit from?

A. System.Web.Mvc.Controller

B. System.Net.Http.HttpController

C. System.Web.Http.ApiController

D. System.Object

E. Microsoft.AspNetCore.MVC

Đáp án: D, E

228. In the case the request is simple, input parameter are of type int, string, boolean, GUID, decimal, etc. and is available in the URL, then such kind of request is mapped to what model binding?

A. primitive model binding

B. complex model binder

C. combination model binding

D. extraction model binder

Đáp án: A

229. In Web API, how can you bind the incoming data to a model automatically?

A. By using the [FromBody] attribute on the API method parameter

B. By using the [FromQuery] attribute on the API method parameter

C. By using the [FromBody] attribute on the model class

D. By using the [FromRoute] attribute on the API method parameter

Đáp án: A

230. What is a Model in ASP.NET Core Web API?

A. A model is a class with.cs (for C#) as an extension having both properties and methods.

B. Models are used only to set the data.

C. Both the answers are corect

D. Both the answers are incorrect

Đáp án: A

231. What is the fundamental syntax for selecting an HTML element and applying an action in jQuery?

A. element.action()

B. $(selector).action()

C. jQuery(action).selector()

D. select(element).do(action)

Đáp án: B

232. How would you access a query string parameter named sort in a controller action?

A. [HttpGet] public IActionResult Get([FromRoute] string sort) { /*...*/}

B. [HttpGet] public IActionResult Get([FromBody] string sort) { /*...*/}

C. [HttpGet] public IActionResult Get([FromHeader] string sort) { /*...*/}

D. [HttpGet] public IActionResult Get([FromQuery] string sort) { /*...*/}

Đáp án: D

233. gRPC's support for long-lived streaming is made possible primarily by which HTTP/2 feature?

A. Server Push

B. Header Compression

C. Binary Framing

D. Bi-directional streams

Đáp án: D

234. How do you create a gRPC client in a .NET 8 console application?

A. var client = new HttpClient();

B. var channel = GrpcChannel. ForAddress("https://localhost:5001"); var client = new Greeter. GreeterClient(channel);

C. var client = new Greeter. GreeterStub("https://localhost:5001");

D. var client = GrpcClient.Create<GreeterClient>("https://localhost:5001");

Đáp án: B

235. Which of the following questions does "Authentication" answer?

A. "What can you do?"

B. "Who are you?"

C. "How long can you stay?"

D. "Where are you from?"

Đáp án: B

236. Consider this simple CoreWCF service contract for a .NET 9 application: [ServiceContract] public interface IGreeterService { [OperationContract] string Greet(string name); } Which part defines what the service does?

A. [Service Contract]

B. public interface IGreeterService

C. [OperationContract]

D. string Greet(string name);

Đáp án: D

237. What is the fundamental concept of "Code-First" development in Entity Framework Core?

A. You design the database schema first, and then EF Core generates the C# model classes.

B. You write the API endpoints first, which then dictates the model and database structure.

C. You define your data models as C# classes, and EF Core creates or updates the database schema to match them.

D. You write raw SQL scripts first for all data operations.

Đáp án: C

238. Which system query option is used to filter a collection of resources in an OData request?

A. $select

B. $orderby

C. $filter

D. $top

Đáp án: C

239. What is the purpose of the $expand query option?

A. To retrieve the next page of results in a paged collection.

B. To include related entities in the same response.

C. To get a count of all entities in a collection.

D. To expand all properties of an entity instead of a subset.

Đáp án: B

240. What does the "asynchronous" in AJAX mean?

A. The code is guaranteed to execute in a specific, synchronous order.

B. The web browser can continue to be responsive to the user while waiting for the server to send back a response.

C. The server must respond to the request immediately.

D. The data must be in XML format.

Đáp án: B

241. What is "binding source parameter inference" in controllers marked with [ApiController]?

A. The process of guessing the data types of action parameters.

B. A feature where ASP.NET Core automatically applies binding source attributes ([FromRoute], [FromBody], etc.) based on conventions, reducing boilerplate code.

C. The ability to infer validation rules from property names.

D. A mechanism for the client to tell the server where to find data.

Đáp án: B

242. If a client sends an Accept header with application/json; q=0.9, application/xml; q=1.0, what is it indicating?

A. It can only accept JSON.

B. It prefers XML (q=1.0) over JSON (q=0.9).

C. It can only accept XML.

D. It wants the response to be split between JSON and XML.

Đáp án: B

243. Which communication protocol is often chosen for high-performance, internal, service-to-service communication due to its use of HTTP/2 and binary serialization?

A. SOAP

B. REST over HTTP/1.1 with JSON

C. gRPC

D. FTP

Đáp án: C

244. To allow access to users who are in either the "Manager" role or the "Supervisor" role, what is the correct syntax?

A. [Authorize(Roles = "Manager", "Supervisor")]

B. [Authorize(Roles = "Manager")] [Authorize (Roles = "Supervisor")]

C. [Authorize(Roles = "Manager or Supervisor")]

D. [Authorize(Roles = "Manager, Supervisor")]

Đáp án: D

245. What is the primary purpose of the HTTP protocol?

A. To securely encrypt data transmissions.

B. To transfer hypertext documents across the internet.

C. To manage and query databases.

D. To define the structure of a web page.

Đáp án: B

246. Why is it critical to always use HTTPS for RESTful APIs?

A. It makes the API faster by compressing the data.

B. It ensures that the data (including credentials and sensitive information) transferred between the client and server is encrypted and protected from eavesdropping.

C. It is the only protocol that supports the GET and POST verbs.

D. It automatically handles user authorization.

Đáp án: B

247. Which data types are supported in JSON?

A. String, Number, Boolean, Array, Object, null

B. String, Integer, Float, Date, Array, Hashtable

C. Text, Decimal, Bit, List, Dictionary, null

D. Varchar, Number, Boolean, Collection, Object, undefined

Đáp án: A

248. Which of the following is a simple representation of a Model class in C# for an ASP.NET Core application?

A. A static class with methods for rendering HTML.

B. An interface defining controller actions.

C. A class with properties representing data, often called a POCO (Plain Old CLR Object).

D. An attribute used for routing.

Đáp án: C

249. Which selector targets the first paragraph element (<p>) on the page?

A. $("p:first-child")

B. $("p:first")

C. $("p:first-of-type")

D. All of the above could potentially work depending on the HTML structure.

Đáp án: D

250. The following C# code in a.NET creates an endpoint. What does it do? app.MapGet("/products/{id}", (int id=> { // Logic to find a product by id return Results. Ok($"Product {id}"); });

A. It defines an endpoint that creates a new product.

B. It defines an endpoint that retrieves a product by its ID using a POST request.

C. It defines an endpoint that retrieves a product by its ID using a GET request.

D. It defines an endpoint that deletes a product by its ID.

Đáp án: C

251. What is the opposite of a microservices architecture?

A. A serverless architecture

B. A monolithic architecture

C. A service-oriented architecture (SOA)

D. A distributed architecture

Đáp án: B

252. The following.NET 8 code is in Program.cs. What is its purpose? var app = builder.Build(); // app.UseAuthentication(); app.UseAuthorization(); // app.Run();

A. It registers the authentication services.

B. It adds the authentication and authorization middleware components to the request pipeline.

C. It configures the default authentication scheme.

D. It is redundant and has no effect.

Đáp án: B

253. What is a "channel" in gRPC?

A. The service implementation on the server.

B. The generated client-side code.

C. A long-lived connection to a gRPC service, which can be reused for multiple calls.

D. A specific type of streaming method.

Đáp án: C

254. In a .NET 8 Web API, what is the recommended way to handle model validation errors automatically and return a 400 Bad Request response?

A. Manually checking ModelState.IsValid in every action.

B. The [ApiController] attribute automatically handles it.

C. Using a custom middleware to inspect every request.

D. Relying on the database to throw an exception.

Đáp án: B

255. In an OData service with Categories and Products, how would you request all products belonging to the category with an ID of 5?

A. GET /Products?$filter=Categoryld eq 5

B. GET /Categories(5)/Products

C. GET/Products/Category(5)

D. Both A and B are typically valid ways to query.

Đáp án: D

256. To retrieve a single Category entity and all of its related Product entities in one request, which query would you use?

A. GET /Categories(1)?$select=Products

B. GET /Categories(1)?$expand=Products

C. GET /Categories(1),/Products

D. GET /Categories(1)/Products?$fetch=all

Đáp án: B

257. Which of the following is NOT a core principle of REST?

A. Statelessness

B. Client-Server architecture

C. Stateful connections

D. Uniform Interface

Đáp án: C

258. What is the primary advantage of using attribute routing over conventional routing?

A. It is the only way to define routes in minimal APIs.

B. It keeps the route definition next to the action method that it maps to, improving locality and discoverability.

C. It offers significantly better performance than conventional routing.

D. It is required for enabling Swagger/OpenAPI documentation.

Đáp án: B

259. The metadata of an OData service, which describes its data model, is typically exposed via which endpoint?

A. /$metadata

B. /$help

C. /$schema

D. /$info

Đáp án: A

260. Which formatter is configured by default in a new ASP.NET Core 8 Web API project?

A. An XML-based formatter (XmlSerializerInputFormatter/XmlSerializer OutputFormatter).

B. A JSON-based formatter using System.Text.Json.

C. A plain text formatter (TextInputFormatter/TextOutputFormatter).

D. A custom binary formatter.

Đáp án: B

261. What is a "load balancer" in the context of scaling a web service?

A. A tool that validates the data load of a JSON request.

B. A server or service that distributes incoming network traffic across multiple backend servers.

C. A database feature that balances data across multiple tables.

D. A client-side library for managing application load times.

Đáp án: B

262. In an ASP.NET Core Web API, which attribute is used to decorate an action method that should respond to HTTP POST requests?

A. [HttpGet]

B. [HttpPost]

C. [HttpPut]

D. [HttpDelete]

Đáp án: B

263. Which query correctly finds all products where the Name property ends with the string 'Edition'?

A. GET /Products?$filter-endswith(Name, 'Edition')

B. GET /Products?$filter=Name.endsWith('Edition')

C. GET /Products?$filter=last(Name) eq 'Edition'

D. GET /Products?$filter=Name like '%Edition'

Đáp án: A

264. Which of the following is a correctly formatted Media Type for JSON?

A. text/json

B. application/json

C. data/json

D. json/application

Đáp án: B

265. How do you enable OData query options on a specific controller action?

A. By adding the [EnableQuery] attribute to the action method.

B. By naming the action method GetWithOData.

C. By inheriting from ODataController.

D. It is enabled automatically on all actions once OData is configured.

Đáp án: A

266. The following code uses ODataModelBuilder to construct an EDM. What does it do? var builder = new ODataConventionModelBuilder(); builder.EntitySet<Product>("Products"); builder.EntitySet<Category>("Categories"); return builder.GetEdmModel();

A. It creates two entity sets, Products and Categories, and infers their properties and relationships by convention from the C# classes.

B. It defines two complex types that cannot be queried directly.

C. It creates an empty model and waits for the database to provide the schema.

D. It registers two controllers named Products and Categories.

Đáp án: A

267. What is an "Entity Set"?

A. The set of properties that make up an entity's key.

B. A named collection of entities of a specific Entity Type, like Products being a collection of Product entities.

C. The schema version of the data model.

D. A set of validation rules for an entity.

Đáp án: B

268. In a bidirectional streaming call, when does the server wait for the client to send all its messages before sending its own?

A. Always.

B. Never; the client and server can read and write in any order, their streams operate independently.

C. Only if the client explicitly signals it has finished writing.

D. This is configured by the wait_for_client option in the proto file.

Đáp án: B

269. A JWT consists of three parts separated by dots (.). What are they in the correct order?

A. Header, Payload, Signature

B. Payload, Header, Signature

C. Signature, Header, Payload

D. Header, Signature, Body

Đáp án: A

270. What is a "claim" in the context of a JWT?

A. A statement about a subject, such as a user's name, ID, or role.

B. A request from the client to access a protected resource.

C. An error message indicating invalid credentials.

D. The algorithm used to sign the token.

Đáp án: A

271. What is CoreWCF?

A. A complete rewrite of WCF with a different architecture and programming model.

B. A port of WCF to .NET (Core) and .NET 5+ that allows existing WCF services to be migrated to modern, cross-platform environments.

C. A client-only library for consuming legacy WCF services.

D. A graphical tool for managing WCF services.

Đáp án: B

272. To add support for XML serialization in a .NET 8 Web API, what service configuration is typically used in Program.cs?

A. builder. Services.AddControllers().AddXml();

B. builder. Services.AddMvc().AddXmlSerializerFormatters();

C. builder. Services.AddControllers().AddXmlSerializer Formatters();

D. builder. Services.AddXmlFormatting();

Đáp án: C

273. Which attribute forces a primitive type parameter to be bound exclusively from the query string?

A. [FromRoute]

B. [FromQuery]

C. [FromBody]

D. [FromHeader]

Đáp án: B

274. If a request is made to /products?id=abc for an action defined as public IActionResult GetProduct(int id), what will be the state of ModelState?

A. ModelState.IsValid will be true, and id will be 0.

B. An InvalidCastException will be thrown.

C. ModelState.IsValid will be false because "abc" cannot be converted to an integer.

D. id will be null.

Đáp án: C

275. What is the primary reason for using Data Transfer Objects (DTOs) in an API?

A. To replace the need for a database.

B. To shape data specifically for the client, preventing over-posting and under-posting, and decoupling the API from the database schema.

C. To increase the performance of database queries.

D. To enforce business logic and validation.

Đáp án: B

276. To create a new entity in an OData service, which HTTP method should be used?

A. GET

B. PUT

C. POST

D. MERGE

Đáp án: C

277. Which of the following bindings is designed for high performance, .NET-to-.NET communication on the same machine or across an intranet?

A. BasicHttpBinding

B. WSHttpBinding

C. NetTcpBinding

D. WebHttpBinding

Đáp án: C

278. In a controller decorated with [ApiController], what happens automatically if ModelState.IsValid is false?

A. The action method still executes as normal.

B. An HTTP 500 Internal Server Error is returned.

C. The request is automatically rejected with an HTTP 400 Bad Request response containing details of the validation errors.

D. The application logs the error and returns an HTTP 200 OK.

Đáp án: C

