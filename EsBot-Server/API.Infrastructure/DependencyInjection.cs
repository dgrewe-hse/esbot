using API.Application;
using API.Application.Interfaces;
using API.Application.Services;
using API.Infrastructure.Persistence.Context;
using API.Infrastructure.Persistence.Repositories;
using API.Infrastructure.Services.External;
using Domain.Exceptions;
using Domain.Interfaces;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
namespace API.Infrastructure;

public static class DependencyInjection
{

    public static IServiceCollection AddServices(this IServiceCollection services) {
        services.AddScoped<IMessageRepository, MessageRepository>();
        services.AddScoped<IMessageManagementService, MessageManagementService>();
        services.AddScoped<IExternalUseLibExample, ExternalUseLibExample>();
        return services;
    }
    
    public static IServiceCollection AddMapper(this IServiceCollection services) {
        services.AddAutoMapper(cfg => {},typeof(IApplicationAssemblyMarker).Assembly); // Pick any Profile finds all then
        return services;
    }
    public static IServiceCollection AddDataBase(this IServiceCollection services, IConfiguration configuration, ILogger logger)
    {
        
        var connectionString = configuration.GetConnectionString("DefaultConnection");
        
        if (string.IsNullOrWhiteSpace(connectionString))
        {
            logger.LogCritical("DATABASE STARTUP ERROR: 'DefaultConnection' string is missing.");
            
            throw new RequirementException("Database connection string is required for startup.");
        }
        
        services.AddDbContext<ApplicationDbContext>(options =>
            options.UseNpgsql(connectionString,
                b => b.MigrationsAssembly(typeof(ApplicationDbContext).Assembly.FullName)));

        return services;
    }
    public static void TestDatabaseConnection(this IServiceProvider services, ILogger logger)
    {
        using var scope = services.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();

        try
        {
            if (!context.Database.CanConnect())
            {
                throw new RequirementException("Database is reachable but connection was refused.");
            }
        
            logger.LogInformation("Database connection verified successfully.");
        }
        catch (Exception ex)
        {
            logger.LogCritical(ex, "DATABASE CONNECTION FAILED: Could not establish a link to PostgreSQL.");
            throw new RequirementException($"Database connection failed: {ex.Message}");
        }
    }
}