using DataBaseModels;
using Domain.Entities;

namespace Test.Application.UnitTests.Domain;

public class EvaluationResultTests
{

    [Fact]
    public void CreateEvaluation_WithValidData_SetsPropertiesCorrectly()
    {
        // Arrange
        var evaluation = new EvaluationResult
        {
            SubmittedAnswerId = 101,
            IsCorrect = true,
            Feedback = "Excellent explanation of the concept.",
            EvaluatedAt = DateTime.UtcNow
        };

        // Assert
        evaluation.SubmittedAnswerId.Should().Be(101);
        evaluation.IsCorrect.Should().BeTrue();
        evaluation.Feedback.Should().Be("Excellent explanation of the concept.");
    }

    [Fact]
    public void Evaluation_MissingFeedback_ShouldFailValidation()
    {
        // Arrange
        var evaluation = new EvaluationResult
        {
            SubmittedAnswerId = 1,
            Feedback = string.Empty // [Required] constraint
        };

        // Act
        var errors = ValidationHelper.ValidateModel(evaluation);

        // Assert
        errors.Should().Contain(e => e.MemberNames.Contains("Feedback"));
    }

    [Fact]
    public void Relationship_EvaluationToAnswer_ShouldBeConsistent()
    {
        // Arrange
        var answer = new SubmittedAnswer 
        { 
            QuizItemId = 5, 
            AnswerText = "Polymorphism is many shapes." 
        };
        
        var evaluation = new EvaluationResult
        {
            SubmittedAnswerId = 5,
            IsCorrect = true,
            Feedback = "Correct.",
            SubmittedAnswer = answer
        };

        // Act
        answer.Evaluation = evaluation;

        // Assert
        // Verify bidirectional link
        answer.Evaluation.Should().Be(evaluation);
        evaluation.SubmittedAnswer.Should().Be(answer);
        
        // Verify shared key integrity (1:1 relationship)
        evaluation.SubmittedAnswerId.Should().Be(answer.QuizItemId);
    }

    [Fact]
    public void Evaluation_Defaults_ShouldSetTimestamp()
    {
        // Arrange & Act
        var evaluation = new EvaluationResult();

        // Assert
        evaluation.EvaluatedAt.Should().BeCloseTo(DateTime.UtcNow, TimeSpan.FromSeconds(5));
    }
}