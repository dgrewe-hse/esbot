using API.Application.DTOs.Requests;
using API.Application.DTOs.Responses;
using AutoMapper;
using Domain.Entities;

namespace API.Application.Mappings;

public class MessagesMappingProfile : Profile
{
    public MessagesMappingProfile()
    {
        CreateMap<Message, MessageResponse>();
        CreateMap<CreateMessageRequest, Message>()
            .ForMember(dest => dest.Id, opt => opt.MapFrom(src => Guid.NewGuid()))
            .ForMember(dest => dest.Timestamp, opt => opt.MapFrom(src =>DateTime.UtcNow));
        CreateMap<IEnumerable<Message>, AllMessagesResponse>()
            .ForMember(dest => dest.AllMessages, 
                opt => opt.MapFrom(src => src));
        
    }
}