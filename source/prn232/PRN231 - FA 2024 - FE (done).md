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
