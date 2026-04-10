using DataBaseModels;

namespace Services;

public interface IDataLoaderService
{
    Task LoadDbAppData();
}

public class DataLoaderService : IDataLoaderService
{
    private readonly AppDbContext _context;

    public DataLoaderService(AppDbContext context)
    {
        _context = context;
    }

    public async Task LoadDbAppData()
    {
        // Ensure database is created (especially useful for In-Memory)
        await _context.Database.EnsureCreatedAsync();
        
        if (!_context.UserSessions.Any())
        {
            var initialSession = new UserSession 
            { 
                ExternalUserId = "system-init",
                CreatedAt = DateTime.UtcNow 
            };
            
            _context.UserSessions.Add(initialSession);
            await _context.SaveChangesAsync();
        }
    }
}