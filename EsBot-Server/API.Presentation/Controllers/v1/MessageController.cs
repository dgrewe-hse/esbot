using API.Application.DTOs.Requests;
using API.Application.DTOs.Responses;
using API.Application.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace API.Presentation.Controllers.v1;
[ApiController]
[Route("v1/[controller]")]
public class MessageController : ControllerBase
{
    private readonly ILogger<MessageController> _logger;
    private readonly IMessageManagementService _messageManagementService;

    public MessageController(ILogger<MessageController> logger, IMessageManagementService  messageManagementService)
    {
        _logger = logger;
        _messageManagementService = messageManagementService;
    }
    [HttpPost]
    [ProducesResponseType(StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> Create(CreateMessageRequest request) {
        if (request == null) return BadRequest("Request body cannot be empty.");

        _logger.LogInformation($"Creating a new Person with title: {request.Content}");

        try 
        {
            // 2. Delegate work to the Application Layer
            var result = await _messageManagementService.CreatePersonAsync(request);

            // 3. Return a 201 Created status with the location of the new resource
            return CreatedAtAction(nameof(GetById), new { id = result.Id }, result);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error occurred while creating person.");
            return StatusCode(500, "An internal error occurred.");
        }
    }
    
    [HttpGet("{id}")]
    public async Task<ActionResult<MessageResponse>> GetById(Guid id)
    {
        var message = await _messageManagementService.GetByIdAsync(id);
        
        if (message == null) return NotFound();
        
        return Ok(message);
    }
    
    [HttpGet]
    public async Task<ActionResult<AllMessagesResponse>> GetAll()
    {
        var message = await _messageManagementService.GetAllAsync();
        
        if (message == null) return NotFound();
        
        return Ok(message);
    }
}