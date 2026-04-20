using Core.Data.Entities;
using Core.Interfaces.Repositories;
using Infrastructure.Persistence.Context;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Persistence.Repositories;

public class MessageRepository: IMessageRepository
{
    private readonly ApplicationDbContext _context;

    public MessageRepository(ApplicationDbContext context)
    {
        _context = context;
    }
    
    public async Task AddMessage(Message message)
    {
        await _context.Messages.AddAsync(message);
        await _context.SaveChangesAsync();
    }

    public async Task<IEnumerable<Message>> GetBySessionIdAsync(Guid id)
    {
        return await _context.Messages.Where(m => m.UserSessionId == id).ToListAsync();
    }
}