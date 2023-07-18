using lattes_core.DTO;
using CurriculumVitaeDTO = lattes_core.DTO.CURRICULOVITAE;

namespace lattes_core.Domain;

public class CurriculumVitae
{
	public CurriculumVitae(){}
	public CurriculumVitae(CurriculumVitaeDTO? cv)
	{
		if (cv is null)
			return;
		
		Author = cv.DADOSGERAIS.NOMECOMPLETO;
		Summary = cv.DADOSGERAIS.RESUMOCV.TEXTORESUMOCVRH;
		Id = cv.NUMEROIDENTIFICADOR;
		// Idioms = cv.DADOSGERAIS.IDIOMAS.Select(idiom => new Idiom {
		// 	Name = idiom.,
		// 	Reading = idiom.LEITURA,
		// 	Speaking = idiom.FALA,
		// 	Writing = idiom.ESCRITA,
		// 	Comprehension = idiom.COMPREENSAO
		// }).ToList();
		// ActingAreas = cv.ATUACOESPROFISSIONAIS.Select(area => area.ATUACAOPROFISSIONAL).ToList();
		// AdditionalInfoList = cv.DADOSCOMPLEMENTARES.Select(info => info.DADOSCOMPLEMENTARES).ToList();
	}

	public string? Author { get; set; }
    public string? Id { get; set; }
    public string? Summary { get; set; }
    public List<Idiom>? Idioms {  get; set; }
    public List<string>? ActingAreas { get; set; }
    public List<string>? AdditionalInfoList { get; set; }

    public static string GenerateFileName(string id)
    {
	    return $"cv_{id}.xml";
    }
}

/*
 * dados-complementares
	
	formacao complementar
		outros
		cursos de curta duracao
		formacao complementar de extensao universitaria
		mba
			nome do curso
			nome instituicao
dados gerais
	formacao academica titulacao
		tudo menos ensino medio
	atuacoes profissionais
		tudo menos vinculos
	atividades de servico tecnico especializado
	atividades de estagio
	atividades de direcao e administracao
	atividades de participacao em projeto
		nome�do�projeto
*/