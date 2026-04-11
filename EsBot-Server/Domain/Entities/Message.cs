using System.ComponentModel.DataAnnotations;

namespace Domain.Entities;

public record Message
{
    [Key] public Guid Id { get; init; }
    
    [Required]
    public Guid UserSessionId { get; set; }

    [Required]
    public bool Role { get; set; } // If True User if False AI

    [Required]
    public string Content { get; set; } = string.Empty;

    [Required]
    public DateTime Timestamp { get; init; }

    // Navigation Property
    public UserSession UserSession { get; set; } = null!;
};