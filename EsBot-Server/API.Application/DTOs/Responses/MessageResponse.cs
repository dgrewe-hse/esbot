namespace API.Application.DTOs.Responses;

public record MessageResponse
{
    public required Guid Id { get; init; }
    
    public required Guid UserSessionId { get; set; }
    
    public required bool Role { get; set; } // If True User if False AI
    
    public required string Content { get; set; } = string.Empty;
    
    public required DateTime Timestamp { get; init; }
}