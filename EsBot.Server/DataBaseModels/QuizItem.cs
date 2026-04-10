using System.ComponentModel.DataAnnotations;

namespace DataBaseModels;

public record QuizItem
{
    [Key]
    public int Id { get; set; }

    public int QuizRequestId { get; set; }

    [Required]
    public string QuestionText { get; set; } = string.Empty;

    // Stores expected answer structure (e.g., JSON or Keywords)
    public string ExpectedAnswerCriteria { get; set; } = string.Empty;

    // Navigation Properties
    public QuizRequest QuizRequest { get; set; } = null!;
    public SubmittedAnswer? SubmittedAnswer { get; set; }
}