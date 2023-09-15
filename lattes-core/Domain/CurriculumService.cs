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

    public async Task<CurriculumVitae?> ProcessCurriculumByCnpqId(string id, string rank)
    {
        if (!TryGetLocalCopyCurriculum(id, rank, out var curriculum))
        {
            var compressedCurriculum = await _lattesClient.getCurriculoCompactadoAsync(id);
            var response = _decoder.DecodeResponse(compressedCurriculum, id, rank);
            if (response == DecoderStatus.NotFound)
                return null;
            curriculum = _parser.ParseFromFileName(CurriculumVitae.GenerateFileName(id, rank));
        }
        
        if (curriculum.Id is null)
            return null;

        curriculum.Rank = rank;
        _repository.Save(curriculum);
        return curriculum;
    }

    private bool TryGetLocalCopyCurriculum(string id, string rank, out CurriculumVitae curriculum)
    {
        curriculum = _parser.ParseFromFileName(CurriculumVitae.GenerateFileName(id, rank));
        return curriculum.Id is not null;
    }
}