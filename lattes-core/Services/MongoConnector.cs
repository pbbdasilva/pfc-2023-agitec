using MongoDB.Driver;

namespace lattes_core.Services;

public class MongoConnector
{
    private readonly string _connectionUsername = "pfc-admin";
    private readonly string _connectionPassword = "8VpzGHa63nQl7Ifh";

    private string GetConnectionUrl
        => $"mongodb+srv://{_connectionUsername}:{_connectionPassword}@lattes-pfc-2023.twn2hk2.mongodb.net/?retryWrites=true&w=majority";
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

