using System.ComponentModel.DataAnnotations;
using DataBaseModels;
using Domain.Entities;

namespace Test.Application.UnitTests.Domain;

public class SubmittedAnswerTests
{
    [Fact]
    public void SubmittedAnswer_ShouldHaveOneToOneRelationshipWithQuizItem()
    {
        // Arrange
        var item = new QuizItem { Id = 50, QuestionText = "Define CI/CD" };
        var answer = new SubmittedAnswer 
        { 
            QuizItemId = 50, 
            AnswerText = "Continuous Integration and Deployment",
            QuizItem = item 
        };

        // Act
        item.SubmittedAnswer = answer;

        // Assert
        answer.QuizItem.Id.Should().Be(50);
        item.SubmittedAnswer.AnswerText.Should().Be(answer.AnswerText);
    }

    [Fact]
    public void SubmittedAnswer_EmptyText_Fails()
    {
        var answer = new SubmittedAnswer { AnswerText = null! };
        var ctx = new ValidationContext(answer);
        var results = new List<ValidationResult>();

        Validator.TryValidateObject(answer, ctx, results, true);

        results.Should().Contain(r => r.MemberNames.Contains("AnswerText"));
    }
}