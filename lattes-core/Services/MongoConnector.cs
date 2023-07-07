using MongoDB.Driver;

namespace lattes_core.Services;

public class MongoConnector
{
    private readonly string _connectionUsername = "admin";
    private readonly string _connectionPassword = "sYJ4KLacrTQ5vYd";

    private string GetConnectionUrl 
        => $"mongodb+srv://{_connectionUsername}:{_connectionPassword}.8zno4lk.mongodb.net/?retryWrites=true&w=majority&connect=replicaSet";
    private MongoClient GetConnection
    {
        get
        {
            var connectionUrl = GetConnectionUrl;
            var settings = MongoClientSettings.FromConnectionString(connectionUrl);
            settings.ServerApi = new ServerApi(ServerApiVersion.V1);
            var client = new MongoClient(connectionUrl);
            return client;
        }
    }

    public IMongoCollection<T> GetCollection<T>(string dbName, string collectionName) 
        => GetConnection.GetDatabase(dbName).GetCollection<T>(collectionName);
}

