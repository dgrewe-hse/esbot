using Domain.Entities;

namespace Domain.Interfaces;

public interface IMessageRepository
{
    Task AddMessage(Message person);
    Task<Message?> GetByIdAsync(Guid id);
    Task<IEnumerable<Message>>  GetAll();
}