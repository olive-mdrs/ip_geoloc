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
        #TODO
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        #TODO
    def iniciar_busca(self) -> None:
        #TODO

    @work(thread=True)
    def executar_requisicao_rede(self, alvo: str) -> None:
        #TODO
    def mostrar_resultado(self, sucesso: bool, dados: dict) -> None:
        #TODO
