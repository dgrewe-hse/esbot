using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace DataBaseModels;

public record EvaluationResult
{
    [Key]
    [ForeignKey("SubmittedAnswer")]
    public int SubmittedAnswerId { get; set; }

    public bool IsCorrect { get; set; }

    [Required]
    public string Feedback { get; set; } = string.Empty;

    public DateTime EvaluatedAt { get; set; } = DateTime.UtcNow;

    // Navigation Property
    public SubmittedAnswer SubmittedAnswer { get; set; } = null!;
}