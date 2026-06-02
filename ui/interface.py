from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, RichLog
from textual.containers import Horizontal, Vertical
from textual import work

from core.network import buscar_dados_ip

class GeolocApp(App):
    """Uma aplicação para Geolocalização de IPs."""

    CSS = """
    Input {
        width: 3fr;
    }
    Button {
        width: 1fr;
    }
    #caixa-busca {
        height: auto;
        margin: 1;
    }
    RichLog {
        margin: 1;
        border: solid #00FF00;
        height: 1fr;
    }
    """

    BINDINGS = [
        ("q", "quit", "Sair"),
        ("c", "clear_log", "Limpar Tela")
    ]

    def compose(self) -> ComposeResult:
        """Monta os componentes na tela."""
        yield Header(show_clock=True)
        
        # Caixa para colocar o Input e o Botão lado a lado
        with Horizontal(id="caixa-busca"):
            yield Input(placeholder="Digite um IP ou Domínio (ex: 8.8.8.8)", id="input_ip")
            yield Button("Buscar", variant="success", id="btn_buscar")
            
        # Uma tela de log para mostrar os resultados
        yield RichLog(id="tela_resultados", highlight=True, markup=True)
        yield Footer()

    def action_clear_log(self) -> None:
        """Ação disparada ao apertar a tecla 'c'."""
        tela = self.query_one("#tela_resultados", RichLog)
        tela.clear()

    # --- Tratamento de Eventos ---

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Disparado quando o botão é clicado."""
        if event.button.id == "btn_buscar":
            self.iniciar_busca()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Disparado quando o usuário aperta ENTER no Input."""
        if event.input.id == "input_ip":
            self.iniciar_busca()

    def iniciar_busca(self) -> None:
        """Captura o texto e inicia o processo de rede."""
        input_widget = self.query_one("#input_ip", Input)
        alvo = input_widget.value.strip()
        
        if not alvo:
            return

        tela = self.query_one("#tela_resultados", RichLog)
        tela.write(f"[bold yellow]Resolvendo e buscando dados para:[/bold yellow] {alvo}...")
        
        # Chama a função que faz o trabalho pesado de rede
        self.executar_requisicao_rede(alvo)
        
        input_widget.value = "" # Limpa a caixa de texto
    # ---- Roda a requisição em uma segunda thread ----
    @work(thread=True)
    def executar_requisicao_rede(self, alvo: str) -> None:
        """
        A anotação @work(thread=True) é o segredo de ouro aqui!
        As requisições de socket demoram (bloqueiam a execução). Se fizéssemos
        isso na thread principal, a interface "congelaria". Essa anotação 
        joga a busca para outra thread, mantendo o visual fluido.
        """
        sucesso, resultado = buscar_dados_ip(alvo)
        
        # Como estamos em outra thread, usamos call_from_thread para atualizar o visual
        self.call_from_thread(self.mostrar_resultado, sucesso, resultado)

    def mostrar_resultado(self, sucesso: bool, dados: dict) -> None:
        """Atualiza a tela de log com a resposta da API."""
        tela = self.query_one("#tela_resultados", RichLog)
        
        if not sucesso:
            tela.write(f"[bold red]{dados}[/bold red]\n")
            return

        # Se teve sucesso, formatamos os dados de forma bonita (usando markup do Textual/Rich)
        ip = dados.get('ip', 'N/A')
        cidade = dados.get('city', 'N/A')
        pais = dados.get('country', 'N/A')
        org = dados.get('org', 'N/A')

        texto_saida = (
            f"[bold green]Resultado para {ip}:[/bold green]\n"
            f"  - Cidade/País: {cidade}, {pais}\n"
            f"  - Organização: {org}\n"
        )

        if 'privacy' in dados:
            priv = dados['privacy']
            if priv.get('vpn') or priv.get('proxy') or priv.get('hosting'):
                texto_saida += "  - [bold red blink]ALERTA:[/bold red blink] Proxy/VPN/Datacenter detectado!\n"

        tela.write(texto_saida)
        tela.write("-" * 40)
