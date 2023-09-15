using ICSharpCode.SharpZipLib.Zip;
using lattes_core.Domain;
using CurriculumVitaeDTO = lattes_core.DTO.CURRICULOVITAE;
namespace lattes_core.Services;

public enum DecoderStatus
{
    Success,
    NotFound
}

public class CVDecoder
{
    public DecoderStatus DecodeResponse(byte[] compressedResponse, string id, string rank)
    {
        try
        {
            var fileName = CurriculumVitae.GenerateFileName(id, rank);
            var zipStream = new ZipInputStream(new MemoryStream(compressedResponse));
            zipStream.GetNextEntry();
            var xml = GetXml(fileName);
            zipStream.CopyTo(xml);
            xml.Close();
            return DecoderStatus.Success;
        }
        catch (Exception e)
        {
            Console.WriteLine(e.Message);
            return DecoderStatus.NotFound;
        }
    }

    private FileStream GetXml(string fileName)
    {
        if (File.Exists(fileName))
            File.Delete(fileName);
        FileStream xml = new FileStream(fileName, FileMode.CreateNew);
        
        return xml;
    }
}