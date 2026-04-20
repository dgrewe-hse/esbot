using System.Text.Json;
using Core.Data.DTOs.Responses;
using Reqnroll;
using Test.Presentation.FunctionalTests.Context;

namespace Test.Presentation.FunctionalTests.Steps;

[Binding]
public class ResumeSession
{
    private readonly HttpClient _client;
    private readonly TestContext _context;

    public ResumeSession(HttpClient client, TestContext context)
    {
        _client = client;
        _context = context;
    }

    [When(@"the student requests an old session with session-id")]
    public async Task WhenTheStudentRequestsAnOldSessionWithSessionId()
    {
        var userSessionId = Guid.NewGuid();
        var response = await _client.GetAsync($"API/v1/Session?id={userSessionId}");
        
        _context.Response = response;
        _context.ResponseContent = await response.Content.ReadAsStringAsync();
        _context.SessionId = userSessionId;
    }

    [Then(@"the response should contain all messages with that session-id")]
    public void ThenTheResponseShouldContainAllMessagesWithThatSessionId()
    {
        var message = JsonSerializer.Deserialize<IEnumerable<MessageResponse>>(
            _context.ResponseContent,
            new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
    }
    
    [When(@"the student request an session with a unknown session-id")]
    public async Task WhenTheStudentRequestAnSessionWithAUnknownSessionId()
    {
        
    }

    [Then(@"the response should contain ""did not find your session""")]
    public void ThenTheResponseShouldContainDidNotFindYourSession()
    {
        
    }
}