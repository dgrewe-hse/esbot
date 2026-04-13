using API.Application.DTOs.Requests;
using API.Application.DTOs.Responses;
using AutoMapper;
using Domain.Entities;

namespace API.Application.Mappings;

public class EvaluationResultMappingProfile : Profile
{
    public EvaluationResultMappingProfile()
    {
        CreateMap<EvaluationResult, EvaluationResult>();
        CreateMap<CreateMessageRequest, EvaluationResult>()
            .ForMember(dest => dest.EvaluatedAt, opt => opt.MapFrom(src =>DateTime.UtcNow));
    }
}