using lattes_core;

var builder = WebApplication.CreateBuilder(args);
builder.ConfigureServices();
var app = builder.Build();
app.MapControllers();
app.Run();