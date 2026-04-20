using AutoMapper;
using Core.Data.DTOs.Responses;
using Core.Exceptions;
using Core.Interfaces.Repositories;
using Core.Interfaces.Services;

namespace Core.Services;

public class SessionManagementService(
    IMapper mapper,
    IMessageRepository messageRepository) :  ISessionManagementService
{
    public async Task<IEnumerable<MessageResponse>> GetSession(Guid sessionId)
    {
        var messages = await messageRepository.GetBySessionIdAsync(sessionId);
        if (messages == null || !messages.Any())
        {
            throw new NotFoundException("Session not found");
        }
        var messagesResponse = mapper.Map<IEnumerable<MessageResponse>>(messages);
        return messagesResponse;
    }
    
}