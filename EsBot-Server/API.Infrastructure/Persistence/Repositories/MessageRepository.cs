using Domain.Entities;
using Domain.Interfaces;
using Microsoft.EntityFrameworkCore;
using API.Infrastructure.Persistence.Context;

namespace API.Infrastructure.Persistence.Repositories;

public class MessageRepository : IMessageRepository
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
    
    public async Task<Message?> GetByIdAsync(Guid id)
    {
        return await _context.Messages.FindAsync(id);
    }

    public async Task<IEnumerable<Message>> GetAll()
    {
        // Use ToListAsync to execute the query and bring results into memory
        return await _context.Messages.ToListAsync();
    }
}