using lattes_core.DTO;
using CurriculumVitaeDTO = lattes_core.DTO.CURRICULOVITAE;

namespace lattes_core.Domain;

public class CurriculumVitae
{
	public string? Author { get; }
	public string? Id { get; }
	public string? Summary { get; }
	public List<Idiom>? Idioms {  get; }
	public List<Undergrad> UndergradList { get; }
	
	public PosGrad PosGrad { get; }
	public Masters Masters { get; }
	public Doctorate Doctorate { get; }

	public static string GenerateFileName(string id)
	{
		return $"cv_{id}.xml";
	}
	
	public CurriculumVitae(){}
	public CurriculumVitae(CurriculumVitaeDTO? cv)
	{
		if (cv is null)
			return;
		
		Author = cv.DADOSGERAIS.NOMECOMPLETO;
		
		if (cv.DADOSGERAIS.RESUMOCV is not null && cv.DADOSGERAIS.RESUMOCV.TEXTORESUMOCVRH is not null)
			Summary = cv.DADOSGERAIS.RESUMOCV.TEXTORESUMOCVRH;
		
		Id = cv.NUMEROIDENTIFICADOR;
		Idioms = cv.DADOSGERAIS.IDIOMAS.Select(idiom => new Idiom {
			Name = idiom.DESCRICAODOIDIOMA,
			Reading = idiom.PROFICIENCIADELEITURA.ToString(),
			Speaking = idiom.PROFICIENCIADEFALA.ToString(),
			Writing = idiom.PROFICIENCIADEESCRITA.ToString(),
			Comprehension = idiom.PROFICIENCIADECOMPREENSAO.ToString()
		}).ToList();

		UndergradList = new List<Undergrad>();
		if (cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.GRADUACAO is not null)
		{
			var len = cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.GRADUACAO.Length;
			for (int idx = 0; idx < len; idx++)
				UndergradList.Add(new Undergrad
				{
					Institution = cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO
						.GRADUACAO[idx].NOMEINSTITUICAO,
					Course = cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO
						.GRADUACAO[idx].NOMECURSO,
					ThesisTitle = cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO
						.GRADUACAO[idx].TITULODOTRABALHODECONCLUSAODECURSO,
				});
		}

		if (cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.APERFEICOAMENTO is not null)
			PosGrad = new PosGrad
			{
				Institution = cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.APERFEICOAMENTO[0].NOMEINSTITUICAO,
				Course = cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.APERFEICOAMENTO[0].NOMECURSO,
				ThesisTitle = cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.APERFEICOAMENTO[0].TITULODAMONOGRAFIA
			};
		
		if (cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.MESTRADO is not null)
			Masters = new Masters
			{
				Institution = cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO
					.MESTRADO[0].NOMEINSTITUICAO,
				Course = cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO
					.MESTRADO[0].NOMECURSO,
				ThesisTitle = cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO
					.MESTRADO[0].TITULODADISSERTACAOTESE,
				Areas = Masters.ParseKnowledgeAreas(cv),
				Keywords = Masters.ParseKeywords(cv)
			};

		if (cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.DOUTORADO is not null)
			Doctorate = new Doctorate
			{
				Institution = cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO
					.DOUTORADO[0].NOMEINSTITUICAO,
				Course = cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO
					.DOUTORADO[0].NOMECURSO,
				ThesisTitle = cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO
					.DOUTORADO[0].TITULODADISSERTACAOTESE,
				Areas = Doctorate.ParseKnowledgeAreas(cv),
				Keywords = Doctorate.ParseKeywords(cv)
			};
	}
}