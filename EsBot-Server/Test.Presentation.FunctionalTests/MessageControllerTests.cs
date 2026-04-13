using System.Net;
using System.Net.Http.Json;
using API.Application.DTOs.Responses;
using API.Infrastructure.Persistence.Context;
using Domain.Entities;
using Microsoft.Extensions.DependencyInjection;
using Test.Presentation.FunctionalTests.Helper;
using Xunit;

namespace Test.Presentation.FunctionalTests;

public class MessageControllerTests : IClassFixture<ApiFactory>
{
    private readonly ApiFactory _factory;
    private readonly HttpClient _client;

    public MessageControllerTests(ApiFactory factory)
    {
        _factory = factory;
        _client = factory.CreateClient();
        SeedDatabase();
    }
    
    private void SeedDatabase()
    {
        using var scope = _factory.Services.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();

        // Ensure database is fresh
        context.Database.EnsureDeleted();
        context.Database.EnsureCreated();

        // Add fake data
        context.Messages.Add(new Message { Id = Guid.NewGuid(), Content = "John Doe" });
        context.SaveChanges();
    }

    [Fact]
    public async Task Get_Message_Returns_Success_And_CorrectContentType()
    {
        // Act
        var response = await _client.GetAsync("/api/v1/message");

        // Assert
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        Assert.Equal("application/json; charset=utf-8", 
            response.Content.Headers.ContentType?.ToString());
        var messages = await response.Content.ReadFromJsonAsync<AllMessagesResponse>();

        Assert.NotNull(messages);
        Assert.Contains(messages.AllMessages[0].Content,"John Doe");
    }
}