using System.Text;
using System.Xml;
using System.Xml.Serialization;
using lattes_core.Domain;
using CurriculumVitaeDTO = lattes_core.DTO.CURRICULOVITAE;

public class CVParser
{
    private string ERROR_MESSAGE = "<ERRO>";
    private XmlSerializer _serializer = new(typeof(CurriculumVitaeDTO));
    private int MAX_NUMBER_OF_DAYS_WITHOUT_UPDATE = 90;

    public XmlDocument LoadXmlEncoded(string path)
    {
        Encoding encoding = Encoding.GetEncoding("ISO-8859-1");
        using XmlReader reader = XmlReader.Create(new StreamReader(path, encoding));
        XmlDocument xml = new XmlDocument();
        xml.Load(reader);
        return xml;
    }
    
    public CurriculumVitae ParseFromFileName(string filename)
    {
        var path = Environment.GetEnvironmentVariable("CVPath") + filename;
        var lastWriteTime = File.GetLastWriteTime(path);
        if (DateTime.Now.Subtract(lastWriteTime).TotalDays > MAX_NUMBER_OF_DAYS_WITHOUT_UPDATE)
            return new CurriculumVitae();
        
        var xml = LoadXmlEncoded(path);
        var xmlContent = xml.OuterXml;
        if (xmlContent.Contains(ERROR_MESSAGE))
            return new CurriculumVitae();
        
        TextReader reader = new StringReader(xmlContent);
        return new CurriculumVitae((CurriculumVitaeDTO) _serializer.Deserialize(reader));
    }
}
