using System;
using System.Xml.Linq;
using System.Xml.Serialization;

public class CVInterpreter {
    public List<XElement> CVList { get; private set;}
    private XmlSerializer serializer = new XmlSerializer(typeof(lattes_core.DTO.CURRICULOVITAE));

    public CVInterpreter (){
        CVList = new List<XElement>();
    }
    private XElement LoadXml(string path) {
        XElement cv;
        try {
            cv = XElement.Load(path);
        } catch (Exception e) {
            Console.WriteLine(e.Message);
            return null;
        }
        return cv;
    }
    public void SaveXML(string path) {
        CVList.Add(LoadXml(path));
    }
    public lattes_core.DTO.CURRICULOVITAE rawCV(string filename) {
        string path = Environment.GetEnvironmentVariable("CVPath") + filename + ".xml";
        var tree = LoadXml(path);
        TextReader reader = new StringReader(tree.ToString());
        return (lattes_core.DTO.CURRICULOVITAE) serializer.Deserialize(reader);
        
    }

}
