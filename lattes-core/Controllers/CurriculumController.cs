using lattes_core.Services;
using Microsoft.AspNetCore.Mvc;

namespace lattes_core.Controllers;

[ApiController]
[Route("cv")]
public class CurriculumController : Controller
{
    private readonly CVParser _cvParser;
    private readonly ICVRepository _cvRepository;
    public CurriculumController(ICVRepository cvRepository, CVParser cvParser)
    {
        _cvRepository = cvRepository;
        _cvParser = cvParser;
    }

    [HttpGet]
    public async Task<IActionResult> Test()
    {
        // string cnpq_id = "9591256136167135";
        // var zippedCv = await _lattesClient.getCurriculoCompactadoAsync(cnpq_id);
        // var s = System.Text.Encoding.UTF8.GetString(zippedCv);
        // var parser = new CVParser();
        // var cvDoXML = parser.ParseCV("duarte_cv");
        var cv = _cvParser.ParseCV("duarte_cv");
        _cvRepository.Save(cv);
        return Ok(cv);
    }
    
}