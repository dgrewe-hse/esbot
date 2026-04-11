using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Domain.Entities;

namespace DataBaseModels;

public record SubmittedAnswer
{
    [Key]
    [ForeignKey("QuizItem")]
    public int QuizItemId { get; set; }

    [Required]
    public string AnswerText { get; set; } = string.Empty;

    public DateTime SubmittedAt { get; set; } = DateTime.UtcNow;

    // One-to-one relationship with Evaluation
    public EvaluationResult? Evaluation { get; set; }

    // Navigation Property
    public QuizItem QuizItem { get; set; } = null!;
}