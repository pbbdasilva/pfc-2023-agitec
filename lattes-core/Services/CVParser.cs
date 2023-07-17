using System.Text;
using System.Xml;
using System.Xml.Serialization;
using lattes_core.Domain;
using CurriculumVitaeDTO = lattes_core.DTO.CURRICULOVITAE;

public class CVParser
{
    private string ERROR_MESSAGE = "<ERRO>";
    private XmlSerializer _serializer = new(typeof(CurriculumVitaeDTO));

    public XmlDocument LoadXmlEncoded(string fileName)
    {
        string path = fileName;
        Encoding encoding = Encoding.GetEncoding("ISO-8859-1");
        using XmlReader reader = XmlReader.Create(new StreamReader(path, encoding));
        XmlDocument xml = new XmlDocument();
        xml.Load(reader);
        return xml;
    }
    
    public CurriculumVitae ParseFromFileName(string filename) {
        var xml = LoadXmlEncoded(filename);
        var xmlContent = xml.OuterXml;
        if (xmlContent.Contains(ERROR_MESSAGE))
            return new CurriculumVitae();
        
        TextReader reader = new StringReader(xmlContent);
        return new CurriculumVitae((CurriculumVitaeDTO) _serializer.Deserialize(reader));
    }
}
