using API.Application.DTOs.Requests;
using API.Application.DTOs.Responses;

namespace API.Application.Interfaces;

public interface IMessageManagementService
{
    Task<MessageResponse> CreatePersonAsync(CreateMessageRequest message);
    Task<MessageResponse> GetByIdAsync(Guid id);
    Task<AllMessagesResponse> GetAllAsync();
}