using System.Net;
using FluentAssertions;
using Test.Presentation.FunctionalTests.Helper;
using Xunit;

namespace Test.Presentation.FunctionalTests;

public class IsItEvenStartingTests: IClassFixture<ApiFactory>
{
    private readonly ApiFactory _factory;
    private readonly HttpClient _client;

    public IsItEvenStartingTests(ApiFactory factory)
    {
        _factory = factory;
        _client = factory.CreateClient();
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