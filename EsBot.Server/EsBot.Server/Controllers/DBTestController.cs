using DataBaseModels;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace EsBot.Server.Controllers;

[ApiController]
[Route("[controller]")]
public class DbTestController: ControllerBase
{

    private readonly ILogger<DbTestController> _logger;
    private readonly AppDbContext _dbContext;

    public DbTestController(ILogger<DbTestController> logger, AppDbContext dbContext)
    {
        _logger = logger;
        _dbContext =  dbContext;
    }

    [HttpGet]
    public async Task<IActionResult> GetAll()
    {
        var items = await _dbContext.UserSessions.ToListAsync();
        return Ok(items);
    }

    // POST: api/dbtest
    [HttpPost]
    public async Task<IActionResult> Create([FromBody] string botName)
    {
        var newBot = new UserSession { ExternalUserId = botName };
        
        _dbContext.UserSessions.Add(newBot);
        await _dbContext.SaveChangesAsync();

        return CreatedAtAction(nameof(GetAll), new { id = newBot.ExternalUserId }, newBot);
    }
}