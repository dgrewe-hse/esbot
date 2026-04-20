using Core.Data.DTOs.Requests;
using Core.Data.DTOs.Responses;

namespace Core.Interfaces.Services;

public interface IQuestionManagementService
{
    Task<MessageResponse> AskQuestion(QuestionRequest question);
}