using System.Net;
using System.Net.Http.Json;
using DataBaseModels;
using FluentAssertions;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;

namespace Test.Integration.API;

public class ApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public ApiTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.WithWebHostBuilder(builder =>
        {
            builder.UseEnvironment("Testing");
        }).CreateClient();
    }
    
    [Fact]
    public async Task Swagger_Doc_IsAccessible_SmokeTest()
    {
        // Act: Check if OpenAPI/Swagger is actually serving metadata
        var response = await _client.GetAsync("/openapi/v1.json"); // Or /swagger/v1/swagger.json depending on config

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
    }
}