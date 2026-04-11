using API.Application.DTOs.Requests;
using API.Application.DTOs.Responses;
using API.Application.Interfaces;
using AutoMapper;
using Domain.Entities;
using Domain.Interfaces;

namespace API.Application.Services;

public class MessageManagementService : IMessageManagementService
{
    private readonly IMapper _mapper;
    private readonly IMessageRepository _messageRepository;

    public MessageManagementService( IMapper mapper, IMessageRepository messageRepository)
    {
        _mapper = mapper;
        _messageRepository = messageRepository;

    }

    public async Task<MessageResponse> CreatePersonAsync(CreateMessageRequest request)
    {
        var message = _mapper.Map<Message>(request);
        await _messageRepository.AddMessage(message);
        return _mapper.Map<MessageResponse>(message);
    }

    public async Task<MessageResponse> GetByIdAsync(Guid id)
    {
        var message = await _messageRepository.GetByIdAsync(id);
        return _mapper.Map<MessageResponse>(message);
    }

    public async Task<AllMessagesResponse> GetAllAsync()
    {
        var message = await _messageRepository.GetAll();
        return _mapper.Map<AllMessagesResponse>(message);
    }
}