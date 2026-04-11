using System.ComponentModel.DataAnnotations;

namespace Domain.Entities;

public record UserSession
{
    [Key] public Guid Id { get; set; }
    
    [Required] [MaxLength(100)] public string ExternalUserId { get; set; }

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime LastInteractionAt { get; set; } = DateTime.UtcNow;
    public ICollection<Message> Messages { get; set; } = new List<Message>();
    public ICollection<QuizRequest> QuizRequests { get; set; } = new List<QuizRequest>();
}