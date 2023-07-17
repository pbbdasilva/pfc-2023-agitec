using lattes_core.Services;
using lattes_core.WSCurriculo;
namespace lattes_core.Domain;

public class CurriculumService
{
    private readonly WSCurriculoClient _lattesClient;
    private readonly CVDecoder _decoder;
    private readonly ICVRepository _repository;
    private readonly CVParser _parser;

    public CurriculumService(WSCurriculoClient lattesClient, CVDecoder decoder, ICVRepository repository, CVParser parser)
    {
        _lattesClient = lattesClient;
        _decoder = decoder;
        _repository = repository;
        _parser = parser;
    }

    public async Task<CurriculumVitae?> ProcessCurriculumByCnpqId(string id)
    {
        if (!TryGetLocalCopyCurriculum(id, out var curriculum))
        {
            var response = _decoder.DecodeResponse(await _lattesClient.getCurriculoCompactadoAsync(id), id);
            if (response == DecoderStatus.NotFound)
                return null;
            curriculum = _parser.ParseFromFileName(CurriculumVitae.GenerateFileName(id));
        }
        
        if (curriculum.Id is null)
            return null;
        
        _repository.Save(curriculum);
        return curriculum;
    }

    private bool TryGetLocalCopyCurriculum(string id, out CurriculumVitae curriculum)
    {
        curriculum = _parser.ParseFromFileName(CurriculumVitae.GenerateFileName(id));
        return curriculum.Id is not null;
    }
}