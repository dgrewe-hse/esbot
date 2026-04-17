using System.Net;
using System.Net.Http.Json;
using Core.Data.DTOs.Requests;
using Reqnroll;
using Test.Presentation.FunctionalTests.Helper;

namespace Test.Presentation.FunctionalTests.Steps;

[Binding]
public class MessageSteps
{
    private readonly HttpClient _client;
    private HttpResponseMessage _response;
    
    public MessageSteps(ApiFactory factory)
    {
        _client = factory.CreateClient();
    }

    [Given(@"the API is running")]
    public async Task GivenTheApiIsRunning()
    {
        var response  = await _client.GetAsync("/openapi/v1.json");
        var content = await response.Content.ReadAsStringAsync();
        response.StatusCode.Should().Be(HttpStatusCode.OK, because: $"API failed with: {content}");
    }
    
    [When(@"I send a POST request to ""(.*)"" with valid data")]
    public async Task WhenISendPostRequest(string url)
    {
        var payload = new CreateMessageRequest
        {
            Content = "John Doe"
        };

        _response = await _client.PostAsJsonAsync(url, payload);
    }
    
    [Then(@"the response status should be (.*)")]
    public void ThenStatusShouldBe(int statusCode)
    {
        ((int)_response.StatusCode).Should().Be(statusCode);
    }
}