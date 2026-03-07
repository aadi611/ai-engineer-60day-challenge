"""
Production RAG System - Interactive Chatbot
A chatbot interface for the RAG pipeline
"""

import argparse
from pathlib import Path
from typing import Dict, Optional
from loguru import logger
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.pipeline import RAGPipeline


class RAGChatbot:
    """
    Interactive chatbot interface for RAG system
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize chatbot
        
        Args:
            config_path: Path to configuration file
        """
        self.console = Console()
        self.pipeline = RAGPipeline(config_path)
        self.conversation_history = []
        
        logger.info("RAGChatbot initialized")
    
    def welcome_message(self):
        """Display welcome message"""
        welcome = """
# Market Intelligence & Geopolitical Analyst

Powered by a RAG pipeline with 22 embedded analytical frameworks across macro, markets, strategy, and competitive intelligence.

## Embedded Frameworks:
**Markets:** Global Macro · Liquidity Cycle · Business Cycle · Supply-Demand · Sector Rotation · Factor Investing · Quant/StatArb

**Strategy:** PESTLE · SWOT · Porter's Five Forces · TAM-SAM-SOM · Value Chain · Segmentation · Blue Ocean · BCG Matrix · Ansoff · GE-McKinsey · JTBD · Customer Journey · 4Ps · Competitive Positioning · Demand-Supply Gap

## Commands:
- `/ingest <path>` - Ingest documents from file or directory
- `/fetch <topic>` - Pull live data (news, Wikipedia, markets) on any topic
- `/fetch market <ticker>` - Fetch live company/stock data (e.g. `/fetch market AAPL`)
- `/stats` - Show system statistics
- `/reset` - Reset the system (clear all documents)
- `/help` - Show this help message
- `/quit` or `/exit` - Exit

## Example queries:
- *"Analyze Apple's competitive position using Porter's Five Forces"*
- *"What does the current macro environment mean for tech stocks?"*
- *"Break down the geopolitical risk to semiconductor supply chains"*
- *"Apply the BCG matrix to the EV market landscape"*

---
"""
        self.console.print(Markdown(welcome))
    
    def show_stats(self):
        """Display system statistics"""
        stats = self.pipeline.get_stats()
        
        stats_text = f"""
## System Statistics

- **Total Chunks:** {stats['total_chunks']}
- **Collections:** {', '.join(stats['collections'])}
- **Chunking Strategy:** {stats['chunking_strategy']}
- **Retrieval Strategy:** {stats['retrieval_strategy']}
- **Reranking Enabled:** {stats['reranking_enabled']}
"""
        self.console.print(Markdown(stats_text))
    
    def ingest_documents(self, path: str):
        """
        Ingest documents from file or directory
        
        Args:
            path: Path to file or directory
        """
        path_obj = Path(path)
        
        if not path_obj.exists():
            self.console.print(f"[red]Error: Path not found: {path}[/red]")
            return
        
        self.console.print(f"[yellow]Ingesting documents from: {path}[/yellow]")
        
        try:
            if path_obj.is_file():
                count = self.pipeline.ingest_documents(file_paths=[str(path_obj)])
            elif path_obj.is_dir():
                count = self.pipeline.ingest_documents(directory_path=str(path_obj))
            else:
                self.console.print(f"[red]Error: Invalid path type[/red]")
                return
            
            self.console.print(f"[green]✓ Successfully ingested {count} documents![/green]")
            self.show_stats()
            
        except Exception as e:
            self.console.print(f"[red]Error ingesting documents: {e}[/red]")
            logger.error(f"Ingestion error: {e}")
    
    def process_query(self, query: str):
        """
        Process user query
        
        Args:
            query: User question
        """
        # Check if system has documents
        if self.pipeline.vector_store.count() == 0:
            self.console.print(
                "[yellow]⚠ No documents ingested yet! "
                "Use '/ingest <path>' to add documents first.[/yellow]"
            )
            return
        
        self.console.print("[yellow]Searching and generating response...[/yellow]")
        
        try:
            # Query the pipeline
            result = self.pipeline.query(query, include_citations=True)
            
            # Display response
            self._display_response(query, result)
            
            # Add to conversation history
            self.conversation_history.append({
                "query": query,
                "response": result["response"],
                "num_sources": result.get("num_sources", 0)
            })
            
        except Exception as e:
            self.console.print(f"[red]Error processing query: {e}[/red]")
            logger.error(f"Query error: {e}")
    
    def _display_response(self, query: str, result: Dict):
        """
        Display query response in a formatted way
        
        Args:
            query: User query
            result: Response from pipeline
        """
        # Display answer
        self.console.print("\n")
        self.console.print(Panel(
            Markdown(result["response"]),
            title="[bold green]Answer[/bold green]",
            border_style="green"
        ))
        
        # Display sources
        if result.get("sources"):
            sources_text = "\n## 📚 Sources:\n\n"
            for source in result["sources"]:
                metadata = source.get("metadata", {})
                source_name = metadata.get("file_name", metadata.get("source", "Unknown"))
                score = source.get("score", 0.0)
                sources_text += f"- **[{source['source_number']}]** {source_name} (relevance: {score:.3f})\n"
            
            self.console.print(Markdown(sources_text))
        
        self.console.print("\n")
    
    def reset_system(self):
        """Reset the RAG system"""
        confirm = Prompt.ask(
            "[yellow]Are you sure you want to reset the system? This will delete all documents.[/yellow]",
            choices=["yes", "no"],
            default="no"
        )
        
        if confirm == "yes":
            self.pipeline.reset()
            self.conversation_history = []
            self.console.print("[green]✓ System reset successfully[/green]")
        else:
            self.console.print("[yellow]Reset cancelled[/yellow]")
    
    def fetch_live_data(self, args: str):
        """
        Pull live data and ingest into the pipeline.
        Usage: /fetch <topic>  or  /fetch market <TICKER>
        """
        import subprocess, sys
        script = str(Path(__file__).parent / "ingest_live_data.py")

        parts = args.strip().split(maxsplit=1)
        if parts[0].lower() == "market":
            ticker = parts[1] if len(parts) > 1 else ""
            if not ticker:
                self.console.print("[red]Usage: /fetch market <TICKER> (e.g. /fetch market AAPL)[/red]")
                return
            self.console.print(f"[yellow]Fetching live market data for {ticker.upper()}...[/yellow]")
            cmd = [sys.executable, script, "--source", "market", "--topic", ticker.upper()]
        else:
            topic = args.strip()
            self.console.print(f"[yellow]Fetching live data for: '{topic}'...[/yellow]")
            cmd = [sys.executable, script, "--source", "all", "--topic", topic, "--limit", "10"]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                self.console.print(f"[green]{result.stdout.strip()}[/green]")
            else:
                self.console.print(f"[red]Fetch error:\n{result.stderr[-800:]}[/red]")
        except subprocess.TimeoutExpired:
            self.console.print("[red]Fetch timed out after 120s[/red]")
        except Exception as e:
            self.console.print(f"[red]Fetch failed: {e}[/red]")

    def run(self):
        """Run the interactive chatbot"""
        self.welcome_message()
        
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith("/"):
                    command_parts = user_input.split(maxsplit=1)
                    command = command_parts[0].lower()
                    args = command_parts[1] if len(command_parts) > 1 else ""
                    
                    if command in ["/quit", "/exit"]:
                        self.console.print("[yellow]Goodbye![/yellow]")
                        break
                    elif command == "/help":
                        self.welcome_message()
                    elif command == "/stats":
                        self.show_stats()
                    elif command == "/reset":
                        self.reset_system()
                    elif command == "/ingest":
                        if args:
                            self.ingest_documents(args)
                        else:
                            self.console.print("[red]Usage: /ingest <path>[/red]")
                    elif command == "/fetch":
                        if args:
                            self.fetch_live_data(args)
                        else:
                            self.console.print("[red]Usage: /fetch <topic>  or  /fetch market <TICKER>[/red]")
                    else:
                        self.console.print(f"[red]Unknown command: {command}[/red]")
                        self.console.print("[yellow]Type '/help' for available commands[/yellow]")
                else:
                    # Process as query
                    self.process_query(user_input)
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Use '/quit' to exit[/yellow]")
            except EOFError:
                break
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
                logger.error(f"Chatbot error: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Production RAG System - Interactive Chatbot"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file",
        default="config/config.yaml"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logger.remove()
    logger.add(
        sys.stderr,
        level=args.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"
    )
    logger.add(
        "logs/chatbot.log",
        rotation="10 MB",
        retention="1 week",
        level="DEBUG"
    )
    
    # Check if config exists
    config_path = args.config if Path(args.config).exists() else None
    if not config_path:
        logger.warning(f"Config file not found: {args.config}, using defaults")
    
    # Run chatbot
    chatbot = RAGChatbot(config_path=config_path)
    chatbot.run()


if __name__ == "__main__":
    main()
