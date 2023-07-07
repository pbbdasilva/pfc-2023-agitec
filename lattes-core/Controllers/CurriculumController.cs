using System.Text;
using Microsoft.AspNetCore.Mvc;

namespace lattes_core.Controllers;

[ApiController]
[Route("cv")]
public class CurriculumController : Controller
{
    private readonly WSCurriculo.WSCurriculoClient _lattesClient;
    public CurriculumController(WSCurriculo.WSCurriculoClient lattesClient)
    {
        _lattesClient = lattesClient;
    }

    [HttpGet]
    public async Task<IActionResult> Test()
    {
        string cnpq_id = "9591256136167135";
        var zippedCv = await _lattesClient.getCurriculoCompactadoAsync(cnpq_id);
        var s = System.Text.Encoding.UTF8.GetString(zippedCv);
        // var interpreter = new CVInterpreter();
        Console.WriteLine("ae");
        return Ok(zippedCv);
    }
}