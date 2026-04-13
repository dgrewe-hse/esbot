using System.ComponentModel.DataAnnotations;
using Domain.Entities;

namespace Test.Application.UnitTests.Domain;

public class QuizItemTests
{
    [Fact]
    public void QuizItem_ShouldLinkToQuizRequest()
    {
        var request = new QuizRequest { Id = 1, Topic = "Unit Testing" };
        var item = new QuizItem 
        { 
            Id = 10, 
            QuestionText = "What is a Mock?", 
            QuizRequest = request 
        };

        request.QuizItems.Add(item);

        item.QuizRequest.Should().Be(request);
        request.QuizItems.Should().Contain(item);
    }

    [Fact]
    public void QuizItem_MissingQuestionText_Fails()
    {
        var item = new QuizItem { QuestionText = string.Empty };
        var ctx = new ValidationContext(item);
        var results = new List<ValidationResult>();
        
        Validator.TryValidateObject(item, ctx, results, true);
        
        results.Should().Contain(r => r.MemberNames.Contains("QuestionText"));
    }
}