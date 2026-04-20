using Core.Data.Entities;

namespace Core.Interfaces.Repositories;

public interface IMessageRepository
{
    public Task AddMessage(Message message);

    public Task<IEnumerable<Message>> GetBySessionIdAsync(Guid id);
}