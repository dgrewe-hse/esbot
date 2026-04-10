using DataBaseModels;
using Microsoft.EntityFrameworkCore;
using Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddOpenApi();

var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");

builder.Services.AddScoped<IDataLoaderService, DataLoaderService>();

builder.Services.AddDbContext<AppDbContext>(options =>
{
    if (builder.Environment.IsEnvironment("Testing"))
    {
        options.UseInMemoryDatabase("TestDb");
    }
    else
    {
        options.UseNpgsql(connectionString);
    }
});

builder.Services.AddScoped<iExampleService, ExampleService>();

var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var services = scope.ServiceProvider;
    try
    {
        var dataLoader = services.GetRequiredService<IDataLoaderService>();
        await dataLoader.LoadDbAppData();
        Console.WriteLine(">>> Application Data Loaded Successfully.");
    }
    catch (Exception ex)
    {
        Console.WriteLine($">>> Error loading data: {ex.Message}");
    }
}

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();