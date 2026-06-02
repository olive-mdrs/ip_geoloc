# Cliente TCP de Geolocalização de IPs

Este projeto é uma aplicação Cliente com Interface de Terminal (TUI) desenvolvida para a disciplina de Redes de Computadores (Bacharelado em Tecnologia da Informação/UFRN). O software consome a API pública do ipinfo.io para rastrear dados geográficos, de infraestrutura e de segurança de endereços de rede.

## Arquitetura do Projeto

```text
geolocalizador/
├── main.py                 # Ponto de entrada (Inicializa a TUI)
├── core/
│   └── network.py          # Lógica de Sockets e parsing HTTP/JSON
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

TODO
