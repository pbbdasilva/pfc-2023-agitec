using lattes_core.Domain;
using lattes_core.Services;

namespace lattes_core;

public static class Startup
{
    public static void ConfigureServices(this WebApplicationBuilder builder)
    {
        builder.Services.AddSingleton<WSCurriculo.WSCurriculoClient>();
        builder.Services.AddScoped<MongoConnector>();
        builder.Services.AddScoped<ICVRepository, CVRepository>();
        builder.Services.AddSingleton<CVParser>();
        builder.Services.AddSingleton<CVDecoder>();
        builder.Services.AddScoped<CurriculumService>();
        builder.Services.AddControllers();
    }
}