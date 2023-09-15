using lattes_core.Domain;
using Microsoft.AspNetCore.Mvc;

namespace lattes_core.Controllers;

[ApiController]
[Route("cv")]
public class CurriculumController : Controller
{
    private readonly CurriculumService _service;
    public CurriculumController(CurriculumService service)
    {
        _service = service;
    }

    [HttpGet("{rank}/{id}")]
    public async Task<IActionResult> ProcessCurriculumByCnpqId([FromRoute] string rank, [FromRoute] string id)
    {
        var cv = await _service.ProcessCurriculumByCnpqId(id, rank);
        if (cv is null)
            return NotFound();

        return Ok(cv);
    }
    
}