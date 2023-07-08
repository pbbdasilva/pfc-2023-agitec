using lattes_core.Domain;

namespace lattes_core.Services;

public interface ICVRepository
{
    void Save(string filename);
}

public class CVRepository : ICVRepository
{
    private readonly MongoConnector _mongoConnector;
    private readonly CVParser _cvParser;

    public CVRepository(CVParser cvParser, MongoConnector mongoConnector)
    {
        _cvParser = cvParser;
        _mongoConnector = mongoConnector;
    }
    
    public void Save(string filename)
    {
        var cv = _cvParser.ParseCV(filename);
        var collection = _mongoConnector.GetCollection<CurriculumVitae>("lattes", "resumes");
        collection.InsertOne(cv);
    }
}