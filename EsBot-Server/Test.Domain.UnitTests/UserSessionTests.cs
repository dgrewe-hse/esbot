using Domain.Entities;

namespace Test.Domain.UnitTests;

public class UserSessionTests
{
    [Fact]
    public void CreateSession_WithValidData_SetsPropertiesCorrectly()
    {
        // Arrange & Act
        var session = new UserSession { 
            ExternalUserId = "user-123", 
            Id = Guid.NewGuid() 
        };

        // Assert
        session.ExternalUserId.Should().Be("user-123");
        session.CreatedAt.Should().BeBefore(DateTime.UtcNow.AddSeconds(1));
    }

    [Fact]
    public void UserSession_MissingExternalUserId_ShouldFailValidation()
    {
        // Arrange
        var session = new UserSession { ExternalUserId = null! };

        // Act
        var errors = ValidationHelper.ValidateModel(session);

        // Assert
        errors.Should().Contain(e => e.MemberNames.Contains("ExternalUserId"));
    }

    [Fact]
    public void Relationship_MessageAndSession_ShouldBeBidirectional()
    {
        // Arrange
        var session = new UserSession { Id = Guid.NewGuid(), ExternalUserId = "test" };
        var message = new Message { 
            Content = "Hello", 
            Role = true, 
            UserSession = session 
        };

        // Act
        session.Messages.Add(message);

        // Assert
        session.Messages.Should().Contain(message);
        message.UserSession.Should().Be(session);
    }
    
}