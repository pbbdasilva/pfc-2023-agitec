using System.Xml.Linq;
using System.Xml.Serialization;
using lattes_core.Domain;
using CurriculumVitaeDTO = lattes_core.DTO.CURRICULOVITAE;

public class CVParser {
    private XmlSerializer _serializer = new(typeof(CurriculumVitaeDTO));
    private XElement? LoadXml(string filename) {
        XElement cv;
        string path = Environment.GetEnvironmentVariable("CVPath") + filename + ".xml";
        
        try {
            cv = XElement.Load(path);
        } catch (Exception e) {
            Console.WriteLine(e.Message);
            return null;
        }
        
        return cv;
    }
    
    public CurriculumVitae ParseCV(string filename) {
        var xml = LoadXml(filename);
        
        if (xml is null)
            return new CurriculumVitae();
        
        TextReader reader = new StringReader(xml.ToString());
        
        return new CurriculumVitae((CurriculumVitaeDTO) _serializer.Deserialize(reader));
    }

}
