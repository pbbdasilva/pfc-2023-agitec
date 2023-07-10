using lattes_core.Domain;
using MongoDB.Driver;

namespace lattes_core.Services;

public interface ICVRepository
{
    void Save(CurriculumVitae cv);
}

public class CVRepository : ICVRepository
{
    private readonly MongoConnector _mongoConnector;

    public CVRepository(MongoConnector mongoConnector)
    {
        _mongoConnector = mongoConnector;
    }
    
    public void Save(CurriculumVitae cv)
    {
        var collection = _mongoConnector.GetCollection<CurriculumVitae>("lattes", "resumes");
        var query = Builders<CurriculumVitae>.Filter.Eq(x => x.Id, cv.Id);
        var update = Builders<CurriculumVitae>.Update.Set(x => x, cv);
        collection.UpdateOne(query, update, new UpdateOptions{ IsUpsert = true });
    }
}