using API.Infrastructure;
using Domain.Exceptions;
using Scalar.AspNetCore;


const string devCorsPolicy = "DevCorsPolicy";
const string prodCorsPolicy = "ProdCorsPolicy";

using var loggerFactory = LoggerFactory.Create(builder => builder.AddConsole());
var logger = loggerFactory.CreateLogger("Program");
try
{
    var builder = WebApplication.CreateBuilder(args);
    builder.Logging.ClearProviders();
    builder.Logging.AddConsole();
    // builder.Logging.AddFile("logs/app-{Date}.txt");
    
    builder.Services.AddOpenApi();

    builder.Services.AddCors(options =>
    {
        options.AddPolicy(devCorsPolicy, policy =>
        {
            policy.AllowAnyOrigin()
                .AllowAnyMethod()
                .AllowAnyHeader();
        });
    
        options.AddPolicy(prodCorsPolicy, policy =>
        {
            var origins = builder.Configuration.GetSection("AllowedOrigins").Get<string[]>();
            if (origins != null)
            {
                policy.WithOrigins(origins)
                    .AllowAnyMethod()
                    .AllowAnyHeader();
            }
            else
            {
                logger.LogCritical("No origins configured");
                Environment.Exit(1);
            }
        });
    });

    // Add other layers
    if (!builder.Environment.IsEnvironment("Testing"))
    {
        builder.Services.AddDataBase(builder.Configuration, logger); ;
    }
    else
    {
        logger.LogInformation($"Skipping database connection Test in Environment {builder.Environment}");
    }
    
    builder.Services.AddServices();
    builder.Services.AddMapper();

    builder.Services.AddControllers();

    var app = builder.Build();

    if (!app.Environment.IsEnvironment("Testing"))
    {
        app.Services.TestDatabaseConnection(logger);
    }
    else
    {
        logger.LogInformation($"Skipping database connection Test in Environment {app.Environment}");
    }

    if (app.Environment.IsDevelopment())
    {
        app.UseCors(devCorsPolicy);
        app.MapOpenApi();
        app.MapScalarApiReference();
    }
    else
    {
        app.UseCors(prodCorsPolicy);
    }
    app.UsePathBase("/api");
    app.UseHttpsRedirection();
    app.UseAuthentication();
    app.UseAuthorization();
    app.MapControllers();

    app.Run();
}
catch (RequirementException ex)
{
    logger.LogCritical("Startup failed: {Message}", ex.Message);
    Environment.Exit(1); 
}
catch (Exception ex)
{
    // Catch-all for any other unexpected disaster
    logger.LogCritical(ex, "An unhandled exception occurred during startup.");
    Environment.Exit(1);
}

public partial class Program { }