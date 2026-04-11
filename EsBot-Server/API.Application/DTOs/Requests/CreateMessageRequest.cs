using System.ComponentModel.DataAnnotations;

namespace API.Application.DTOs.Requests;

public record CreateMessageRequest
{
    [Required]
    public string Content { get; init; }
}