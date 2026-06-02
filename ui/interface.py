from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, RichLog
from textual.containers import Horizontal
from textual import work

from core.orchestrator import executar_analise_completa

class GeolocApp(App):
    """Uma aplicação Textual para Análise de Redes e Segurança."""

    CSS = """
    Input { width: 2fr; }
    #input_portas { width: 1fr; }
    Button { width: 1fr; }
    #caixa-busca { height: auto; margin: 1; }
    RichLog { margin: 1; border: solid #00FF00; height: 1fr; }
    """

    BINDINGS = [
        ("q", "quit", "Sair"),
        ("ctrl+l", "clear_log", "Limpar Tela")
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Horizontal(id="caixa-busca"):
            yield Input(placeholder="Alvo (ex: scanme.nmap.org)", id="input_ip")
            yield Input(placeholder="Portas (ex: 22,80,443)", id="input_portas")
            yield Button("Analisar", variant="success", id="btn_buscar")
            
        yield RichLog(id="tela_resultados", highlight=True, markup=True)
        yield Footer()

    def action_clear_log(self) -> None:
        tela = self.query_one("#tela_resultados", RichLog)
        tela.clear()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_buscar":
            self.iniciar_busca()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.iniciar_busca()

    def iniciar_busca(self) -> None:
        input_widget = self.query_one("#input_ip", Input)
        input_portas_widget = self.query_one("#input_portas", Input)
        
        alvo = input_widget.value.strip()
        portas_str = input_portas_widget.value.strip()
        
        if not alvo:
            return

        tela = self.query_one("#tela_resultados", RichLog)
        tela.write(f"[bold yellow]Iniciando varredura completa para:[/bold yellow] {alvo}...")
        
        self.executar_requisicao_rede(alvo, portas_str)
        
    @work(thread=True)
    def executar_requisicao_rede(self, alvo: str, portas_str: str) -> None:
        sucesso, resultado = executar_analise_completa(alvo, portas_str)
        self.call_from_thread(self.mostrar_resultado, sucesso, resultado)

    def mostrar_resultado(self, sucesso: bool, dados: dict) -> None:
        tela = self.query_one("#tela_resultados", RichLog)
        
        if not sucesso:
            tela.write(f"[bold red]Erro: {dados}[/bold red]\n")
            return

        ip = dados.get("ip")
        texto_saida = f"\n[bold green]=== RELATÓRIO DO ALVO: {ip} ===[/bold green]\n"

        # 1. Dados Geográficos
        geo = dados.get("geo", {})
        if geo:
            texto_saida += "[bold blue][ IPINFO ][/bold blue]\n"
            texto_saida += f"  - Localização: {geo.get('city', 'N/A')}, {geo.get('country', 'N/A')}\n"
            texto_saida += f"  - Organização: {geo.get('org', 'N/A')}\n"

        # 2. Dados do Shodan
        shodan = dados.get("shodan", {})
        texto_saida += "\n[bold blue][ SHODAN INTERNETDB ][/bold blue]\n"
        if "info" in shodan:
            texto_saida += f"  - {shodan['info']}\n"
        else:
            hostnames = ", ".join(shodan.get('hostnames', []))
            tags = ", ".join(shodan.get('tags', []))
            cves = shodan.get('vulns', [])
            
            texto_saida += f"  - Hostnames: {hostnames or 'Nenhum'}\n"
            texto_saida += f"  - Tags: {tags or 'Nenhuma'}\n"
            
            if cves:
                texto_saida += f"  - [bold red]Vulnerabilidades Críticas (CVEs) Detectadas: {len(cves)}[/bold red]\n"
                texto_saida += f"    Exemplos: {', '.join(cves[:5])}...\n"
            else:
                texto_saida += "  - Vulnerabilidades (CVEs): Nenhuma detectada no banco do Shodan.\n"

        # 3. Scanner Local
        portas = dados.get("portas_abertas_local", [])
        texto_saida += "\n[bold blue][ SCANNER DE PORTAS LOCAL (TCP) ][/bold blue]\n"
        if portas:
            for p in portas:
                texto_saida += f"  - Porta [bold cyan]{p['porta']}[/bold cyan] ABERTA | Banner: {p['banner']}\n"
        else:
             texto_saida += "  - Nenhuma porta aberta encontrada no intervalo fornecido.\n"

        tela.write(texto_saida)
        tela.write("-" * 55)
