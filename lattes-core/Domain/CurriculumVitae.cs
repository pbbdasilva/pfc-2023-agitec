using lattes_core.DTO;
using CurriculumVitaeDTO = lattes_core.DTO.CURRICULOVITAE;

namespace lattes_core.Domain;

public class CurriculumVitae
{
	public string? Author { get; set; }
	public string? Id { get; set; }
	public string? Summary { get; set; }
	public List<Idiom>? Idioms {  get; set; }
	public Undergrad Undergrad { get; set; }
	
	public PosGrad PosGrad { get; set; }
	public Masters Masters { get; set; }
	public Doctorate Doctorate { get; set; }

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

		
		if (cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO.GRADUACAO is not null)
			Undergrad = new Undergrad
			{
				Institution = cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO
					.GRADUACAO[0].NOMEINSTITUICAO,
				Course = cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO
					.GRADUACAO[0].NOMECURSO,
				ThesisTitle = cv.DADOSGERAIS.FORMACAOACADEMICATITULACAO
					.GRADUACAO[0].TITULODOTRABALHODECONCLUSAODECURSO,
			};

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