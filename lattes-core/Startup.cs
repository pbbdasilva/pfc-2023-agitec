namespace lattes_core;

public static class Startup
{
    public static void ConfigureServices(this WebApplicationBuilder builder)
    {
        builder.Services.AddSingleton<WSCurriculo.WSCurriculoClient>();
        //builder.Services.AddSingleton<WSCurriculo.WSCurriculoChannel>();
        //builder.Services.AddSingleton<WSCurriculo.WSCurriculo>();
        builder.Services.AddControllers();
    }
}