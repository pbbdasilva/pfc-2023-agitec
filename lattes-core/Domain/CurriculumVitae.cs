using lattes_core.DTO;
using MongoDB.Bson.Serialization.Attributes;
using CurriculumVitaeDTO = lattes_core.DTO.CURRICULOVITAE;

namespace lattes_core.Domain;

public class CurriculumVitae
{
	[BsonElement("author")]
	public string? Author { get; }
	[BsonElement("_id")]
	public string? Id { get; }
	[BsonElement("summary")]
	public string? Summary { get; }
	[BsonElement("idioms")]
	public List<Idiom>? Idioms {  get; }
	[BsonElement("undergrad")]
	public List<Undergrad> UndergradList { get; }
	[BsonElement("posgrad")]
	public PosGrad PosGrad { get; }
	[BsonElement("masters")]
	public Masters Masters { get; }
	[BsonElement("doctorate")]
	public Doctorate Doctorate { get; }
	[BsonElement("workexp")]
	public List<WorkExperience> WorkExperiences { get; }
	[BsonElement("rank")]
	public string Rank { get; set; }

	[BsonElement("areas")] 
	public List<ActingAreas> AreasList;

	[BsonElement("articles")] 
	public List<string> Articles;
	public static string GenerateFileName(string id, string rank)
	{
		return $"cv_{rank}_{id}.xml";
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
		if (cv.DADOSGERAIS.IDIOMAS is not null)
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

		if (cv.DADOSGERAIS.ATUACOESPROFISSIONAIS is not null)
		{
			WorkExperiences = new List<WorkExperience>();
			var len = cv.DADOSGERAIS.ATUACOESPROFISSIONAIS.Length;
			for (int i = 0; i < len; i++)
			{
				WorkExperiences.Add(new WorkExperience
				{
					Institution = cv.DADOSGERAIS.ATUACOESPROFISSIONAIS[i].NOMEINSTITUICAO
				});
			}
		}


		if (cv.DADOSGERAIS.AREASDEATUACAO is not null)
		{
			AreasList = new List<ActingAreas>();
			for (int i = 0; i < cv.DADOSGERAIS.AREASDEATUACAO.Length; i++)
			{
				AreasList.Add(new ActingAreas
				{
					KnowledgeArea = cv.DADOSGERAIS.AREASDEATUACAO[i].NOMEDAAREADOCONHECIMENTO,
					Specialty = cv.DADOSGERAIS.AREASDEATUACAO[i].NOMEDAESPECIALIDADE,
				});
			}
		}

		if (cv.PRODUCAOBIBLIOGRAFICA is not null && cv.PRODUCAOBIBLIOGRAFICA.ARTIGOSPUBLICADOS is not null)
		{
			Articles = new List<string>();
			for (int i = 0; i < cv.PRODUCAOBIBLIOGRAFICA.ARTIGOSPUBLICADOS.Length; i++)
			{
				Articles.Add(cv.PRODUCAOBIBLIOGRAFICA.ARTIGOSPUBLICADOS[i].DADOSBASICOSDOARTIGO.TITULODOARTIGO);
			}
		}
	}
}