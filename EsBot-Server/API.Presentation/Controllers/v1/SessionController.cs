using Core.Data.DTOs.Responses;
using Core.Exceptions;
using Core.Interfaces.Services;
using Microsoft.AspNetCore.Mvc;

namespace API.Presentation.Controllers.v1;


[ApiController]
[Route("v1/[controller]")]
public class SessionController : ControllerBase
{
    
    private readonly ISessionManagementService _sessionManagementService;
    
    public SessionController(ISessionManagementService  sessionManagementService)
    {
        _sessionManagementService = sessionManagementService;
    }

    
    [HttpGet]
    public async Task<ActionResult<IEnumerable<MessageResponse>>> OldSession([FromQuery] Guid sessionId)
    {
        IEnumerable<MessageResponse> result = null;
        try
        {
            result = await _sessionManagementService.GetSession(sessionId);
            return Ok(result);
        }
        catch (NotFoundException e)
        {
            return StatusCode(404, "did not find your session");
        }
        
    }
}