namespace lattes_core.Domain;
public enum NiveisIdioma {
    Pouco,
    Razoavelmente,
    Bem
}
public class Idioma {
    public string Nome { get; set; }
    public string Leitura { get; set; }
    public string Fala { get; set;}
    public string Escrita { get; set; }
    public string Compreenssao { get; set;}
}

public class CurriculumVitae
{
    public string Nome { get; set; }
    public string Id { get; set; }
    public string? ResumoCV { get; set; }
    public List<Idioma>? Idiomas {  get; set; }
    public List<string>? AreasDeAtuacao { get; set; }
    public List<string>? InformacoesAdicionais { get; set; }
	
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
		nome do projeto
*/