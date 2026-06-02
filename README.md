# Cliente TCP de Geolocalização de IPs

Este projeto é uma aplicação Cliente com Interface de Terminal (TUI) desenvolvida para a disciplina de Redes de Computadores (Bacharelado em Tecnologia da Informação/UFRN). O software consome a API pública do ipinfo.io para rastrear dados geográficos, de infraestrutura e de segurança de endereços de rede.

## Arquitetura do Projeto

```text
geolocalizador/
├── main.py                 # Ponto de entrada (Inicializa a TUI)
├── core/
│   └── network.py          # Lógica principal da aplicação fazendo requisição à API utilizada
├── ui/
│   └── interface.py        # Telas e tratamento de eventos (Textual)
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação
```

## Como Executar

Recomenda-se a criacao de um ambiente virtual Python isolado para a instalacao das dependencias.

1. Instale as dependencias da interface grafica:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute a aplicação:
   ```bash
   python main.py
   ```

## Como Usar

* Digite um IP valido (ex: 8.8.8.8) ou um dominio (ex: google.com) na barra superior.
* Aperte Enter ou clique com o mouse no botao "Buscar".
* Os dados de Localizacao, Infraestrutura (ISP, Organizacao) e Alertas de Seguranca (Deteccao de VPN, Proxy ou Datacenter) aparecerao no painel principal.
* Use a tecla 'c' para limpar a tela e 'q' para encerrar o programa.
