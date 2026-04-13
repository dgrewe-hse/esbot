using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using DataBaseModels;

namespace Domain.Entities;

public record EvaluationResult
{
    [Key]
    [ForeignKey("SubmittedAnswer")]
    public int SubmittedAnswerId { get; set; }

    [Required]
    public bool IsCorrect { get; set; }

    [Required]
    public string Feedback { get; set; }

    [Required]
    public DateTime EvaluatedAt { get; set; } = DateTime.UtcNow;

    // Navigation Property
    public SubmittedAnswer SubmittedAnswer { get; set; } = null!;
}