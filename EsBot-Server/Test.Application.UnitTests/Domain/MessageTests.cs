using Domain.Entities;
using Test.Application.UnitTests.Domain;

namespace Test.Application.UnitTests;

public class MessageTests
{

    [Fact]
    public void CreateMessage_WithValidData_SetsProperties()
    {
        var message = new Message { Content = "Explain AI", Role = true };

        message.Content.Should().Be("Explain AI");
        message.Role.Should().Be(true);
        message.Timestamp.Should().BeBefore(DateTime.UtcNow.AddSeconds(1));
    }

    [Fact]
    public void Message_ContentExceedsReasonableLimits_CheckIfRequired()
    {
        var message = new Message { Content = null!, Role = false };
        var errors = ValidationHelper.ValidateModel(message);
        errors.Should().Contain(e => e.MemberNames.Contains("Content"));
    }
}