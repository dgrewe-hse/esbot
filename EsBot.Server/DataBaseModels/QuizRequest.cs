using System.ComponentModel.DataAnnotations;

namespace DataBaseModels;

public record QuizRequest
{
    [Key]
    public int Id { get; set; }

    public Guid UserSessionId { get; set; }

    [Required]
    [MaxLength(200)]
    public string Topic { get; set; } = string.Empty;

    public DateTime RequestedAt { get; set; } = DateTime.UtcNow;

    // Navigation Properties
    public UserSession UserSession { get; set; } = null!;
    public ICollection<QuizItem> QuizItems { get; set; } = new List<QuizItem>();
}