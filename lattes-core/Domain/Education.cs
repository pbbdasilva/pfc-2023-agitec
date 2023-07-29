using lattes_core.DTO;

namespace lattes_core.Domain;
using CurriculumVitaeDTO = CURRICULOVITAE;

public class Education
{
    public string Institution { get; set; }
    public string Course { get; set; }
    public string ThesisTitle { get; set; }
    public List<string> Areas { get; set; }
    public List<string> Keywords { get; set; }
}

public class Doctorate : Education
{
	public static List<string> ParseKnowledgeAreas(CurriculumVitaeDTO cv)
	{
		var list = new List<string>();
		if (cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO1 is not null &&
			!string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO1.NOMEDAESPECIALIDADE))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO1.NOMEDAESPECIALIDADE);
		
		if (cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO2 is not null &&
		    !string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO2.NOMEDAESPECIALIDADE))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO2.NOMEDAESPECIALIDADE);
		
		if (cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO3 is not null &&
		    !string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO1.NOMEDAESPECIALIDADE))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO3.NOMEDAESPECIALIDADE);

		return list;
	}

	public static List<string> ParseKeywords(CurriculumVitaeDTO cv)
	{
		var list = new List<string>();
		if (cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].PALAVRASCHAVE is null)
			return list;
		
		if (!string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].PALAVRASCHAVE.PALAVRACHAVE1))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].PALAVRASCHAVE.PALAVRACHAVE1);
		if (!string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].PALAVRASCHAVE.PALAVRACHAVE2))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].PALAVRASCHAVE.PALAVRACHAVE2);
		if (!string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].PALAVRASCHAVE.PALAVRACHAVE3))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].PALAVRASCHAVE.PALAVRACHAVE3);
		if (!string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].PALAVRASCHAVE.PALAVRACHAVE4))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].PALAVRASCHAVE.PALAVRACHAVE4);
		if (!string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].PALAVRASCHAVE.PALAVRACHAVE5))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].PALAVRASCHAVE.PALAVRACHAVE5);
		if (!string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].PALAVRASCHAVE.PALAVRACHAVE6))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO[0].PALAVRASCHAVE.PALAVRACHAVE6);

		return list;
	}
}
public class Masters : Education
{
	public static List<string> ParseKnowledgeAreas(CurriculumVitaeDTO cv)
	{
		var list = new List<string>();
		if (cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO1 is not null && 
		    !string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO1.NOMEDAESPECIALIDADE))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO1.NOMEDAESPECIALIDADE);
		
		if (cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO2 is not null && 
		    !string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO2.NOMEDAESPECIALIDADE))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO2.NOMEDAESPECIALIDADE);
		
		if (cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO3 is not null && 
		    !string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO3.NOMEDAESPECIALIDADE))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].AREASDOCONHECIMENTO.AREADOCONHECIMENTO3.NOMEDAESPECIALIDADE);

		return list;
	}

	public static List<string> ParseKeywords(CURRICULOVITAE cv)
	{
		var list = new List<string>();
		if (cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].PALAVRASCHAVE is null)
			return list;
		
		if (!string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].PALAVRASCHAVE.PALAVRACHAVE1))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].PALAVRASCHAVE.PALAVRACHAVE1);
		if (!string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].PALAVRASCHAVE.PALAVRACHAVE2))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].PALAVRASCHAVE.PALAVRACHAVE2);
		if (!string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].PALAVRASCHAVE.PALAVRACHAVE3))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].PALAVRASCHAVE.PALAVRACHAVE3);
		if (!string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].PALAVRASCHAVE.PALAVRACHAVE4))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].PALAVRASCHAVE.PALAVRACHAVE4);
		if (!string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].PALAVRASCHAVE.PALAVRACHAVE5))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].PALAVRASCHAVE.PALAVRACHAVE5);
		if (!string.IsNullOrEmpty(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].PALAVRASCHAVE.PALAVRACHAVE6))
			list.Add(cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO[0].PALAVRASCHAVE.PALAVRACHAVE6);

		return list;
	}
}

public class PosGrad : Education
{
}

public class Undergrad : Education
{
}