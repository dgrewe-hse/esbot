using System.ComponentModel.DataAnnotations;

namespace DataBaseModels;

public record Message
{
    [Key]
    public int Id { get; set; }

    public Guid UserSessionId { get; set; }

    [Required]
    public bool Role { get; set; } // If True User if False AI

    [Required]
    public string Content { get; set; } = string.Empty;

    public DateTime Timestamp { get; set; } = DateTime.UtcNow;

    // Navigation Property
    public UserSession UserSession { get; set; } = null!;
};