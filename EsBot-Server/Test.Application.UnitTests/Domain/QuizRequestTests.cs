using Domain.Entities;

namespace Test.Application.UnitTests.Domain;

public class QuizRequestTests
{

    [Fact]
    public void QuizRequest_ValidTopic_Passes()
    {
        var request = new QuizRequest { Topic = "Software Testing", UserSessionId = Guid.NewGuid() };
        var errors = ValidationHelper.ValidateModel(request);
        errors.Should().BeEmpty();
    }

    [Fact]
    public void QuizRequest_TopicTooLong_Fails()
    {
        var request = new QuizRequest { Topic = new string('x', 201) };
        var errors = ValidationHelper.ValidateModel(request);
        errors.Should().Contain(e => e.MemberNames.Contains("Topic"));
    }
}