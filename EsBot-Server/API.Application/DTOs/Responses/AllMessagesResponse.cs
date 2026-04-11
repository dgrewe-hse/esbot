namespace API.Application.DTOs.Responses;

public record AllMessagesResponse
{
    public required string[] AllMessages { get; set; }
}