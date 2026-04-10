using DataBaseModels;

namespace Services;

public interface iExampleService
{
    Task<string> GetExplanationAsync(string userQuery);
}

public class ExampleService: iExampleService
{
    private readonly AppDbContext _context;

    public ExampleService(AppDbContext context)
    {
        _context = context; // The DB is injected into the Service
    }

    public async Task<string> GetExplanationAsync(string userQuery)
    {
        // Business logic: Structure the prompt, call AI (mocked or real), save to DB
        return $"Explanation for: {userQuery}";
    }
}