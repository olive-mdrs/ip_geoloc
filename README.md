# Cliente TCP de Geolocalização e Análise de IPs

Este projeto é uma aplicação Cliente com Interface de Terminal (TUI) desenvolvida para a disciplina de Redes de Computadores (Bacharelado em Tecnologia da Informação/UFRN). O software atua em duas frentes principais de reconhecimento de rede utilizando sockets: consome a API pública do ipinfo.io para rastrear dados geográficos e de infraestrutura, e integra-se à API do Shodan InternetDB via sockets seguros (TLS) para mapeamento de portas e identificação de vulnerabilidades (CVEs).

## Arquitetura do Projeto

```text
geolocalizador/
    ├── main.py                 # Ponto de entrada (Inicializa a TUI)
    ├── core/
    │   ├── ipinfo.py           # Lógica principal via sockets para ipinfo.io
    │   ├── orchestrator.py     # Coordenação das fases do projeto
    │   ├── scanner.py          # Scanner de portas TCP local
    │   └── shodan.py           # Comunicação com a API do Shodan via socket TLS
    ├── ui/
    │   └── interface.py        # Telas e tratamento de eventos (Textual)
    ├── test_network.py         # Testes unitários do protocolo HTTP
    ├── requirements.txt        # Dependências do projeto
    └── README.md               # Documentação
```

## Como Executar

Recomenda-se a criacao de um ambiente virtual Python isolado para a instalacao das dependencias.

1. Clone o repositorio ou baixe a pasta do projeto.

2. Abra o terminal na raiz do projeto e crie o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   
3. Instale as dependencias da interface grafica:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute a aplicação:
   ```bash
   python main.py
   ```

## Como Usar

* Digite um IP válido (ex: 8.8.8.8) ou um domínio (ex: google.com) na barra superior.
* Preencha as portas alvo separadas por vírgula (ex: 22,80,443).
* Aperte Enter ou clique com o mouse no botão "Analisar".
* Os dados de Localização, Infraestrutura (ISP, Organizacao) e Alertas de Seguranca (Deteccao de VPN, Proxy ou Datacenter) aparecerão no painel principal.
* O painel também exibirá as portas abertas detectadas e as vulnerabilidades cruzadas com o banco de dados do Shodan.
* Use a tecla 'ctrl + L' para limpar a tela e 'q' para encerrar o programa.

## Testes Unitários

O projeto possui um arquivo de testes focada em validar o comportamento da Camada de Aplicação, especificamente o algoritmo responsável pelo parsing (separação) de cabeçalhos HTTP crus e a extração segura do corpo JSON retornado pelos sockets.

Para rodar os testes localmente, certifique-se de estar na raiz do projeto e execute:

```bash
python -m unittest test_network.py
```
