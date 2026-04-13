namespace API.Application.DTOs.Responses;

public record AllMessagesResponse
{
    public required MessageResponse[] AllMessages { get; set; }
}