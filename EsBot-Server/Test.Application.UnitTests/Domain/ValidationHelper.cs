using System.ComponentModel.DataAnnotations;

namespace Test.Application.UnitTests.Domain;

public static class ValidationHelper
{
    public static IList<ValidationResult> ValidateModel(object model)
    {
        var validationResults = new List<ValidationResult>();
        var ctx = new ValidationContext(model, null, null);
        Validator.TryValidateObject(model, ctx, validationResults, true);
        return validationResults;
    }
}