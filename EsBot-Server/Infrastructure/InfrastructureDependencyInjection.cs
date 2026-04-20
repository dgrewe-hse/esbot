using Core.Exceptions;
using Core.Interfaces.Repositories;
using Core.Interfaces.Services;
using Infrastructure.Persistence.Context;
using Infrastructure.Persistence.Repositories;
using Infrastructure.Services.External;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
namespace Infrastructure;

public static class InfrastructureDependencyInjection
{

    extension(IServiceCollection services)
    {
        public IServiceCollection AddInfrastructureServices()
        {
            services.AddScoped<IMessageRepository, MessageRepository>();
            services.AddScoped<ILlmInterface, LlmInterface>();
            services.AddScoped<IQuizRepository, QuizRepository>();
            return services;
        }

        public IServiceCollection AddDataBase(IConfiguration configuration, ILogger logger)
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