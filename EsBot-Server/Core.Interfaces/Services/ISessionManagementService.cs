using Core.Data.DTOs.Responses;

namespace Core.Interfaces.Services;

public interface ISessionManagementService
{
    public Task<IEnumerable<MessageResponse>> GetSession(Guid sessionId);
}