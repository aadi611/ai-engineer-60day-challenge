"""
Live Data Ingestion Script
Pulls current affairs & geopolitical data from:
  - NewsAPI       (requires free API key from https://newsapi.org)
  - Wikipedia API (no key needed)
  - GDELT Project (no key needed, use GKG feed)

Usage:
    python ingest_live_data.py --source all
    python ingest_live_data.py --source newsapi --topic "Ukraine Russia conflict"
    python ingest_live_data.py --source wikipedia --topic "NATO"
    python ingest_live_data.py --source gdelt --limit 20
"""

import os
import sys
import argparse
import requests
import json
from pathlib import Path

# Force UTF-8 output on Windows so unicode in data doesn't crash prints
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv
from loguru import logger

# ── env ──────────────────────────────────────────────────────────────────────
_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=True)

# ── pipeline ─────────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent))
from src.pipeline import RAGPipeline


# ═════════════════════════════════════════════════════════════════════════════
# NewsAPI Fetcher
# ═════════════════════════════════════════════════════════════════════════════
class NewsAPIFetcher:
    """
    Fetches news articles from NewsAPI.
    Get a free key at: https://newsapi.org/register (100 req/day free)
    Add NEWSAPI_KEY=your_key to your .env file.
    """

    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self):
        self.api_key = os.getenv("NEWSAPI_KEY")
        if not self.api_key:
            raise ValueError(
                "NEWSAPI_KEY not found in .env\n"
                "Get a free key at https://newsapi.org/register and add:\n"
                "  NEWSAPI_KEY=your_key_here"
            )

    def fetch(
        self,
        query: str = "geopolitics OR world affairs OR international relations",
        days_back: int = 7,
        max_articles: int = 20,
        language: str = "en",
    ) -> List[Dict]:
        """Fetch articles matching a query from the past N days."""
        from_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")

        params = {
            "q": query,
            "from": from_date,
            "sortBy": "relevancy",
            "language": language,
            "pageSize": min(max_articles, 100),
            "apiKey": self.api_key,
        }

        resp = requests.get(self.BASE_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        if data.get("status") != "ok":
            raise RuntimeError(f"NewsAPI error: {data.get('message')}")

        articles = data.get("articles", [])
        logger.info(f"[NewsAPI] Fetched {len(articles)} articles for: '{query}'")
        return articles

    def to_text_files(self, articles: List[Dict], out_dir: Path) -> List[Path]:
        """Save articles as .txt files ready for ingestion."""
        out_dir.mkdir(parents=True, exist_ok=True)
        saved = []

        for i, article in enumerate(articles):
            title = article.get("title") or f"article_{i}"
            description = article.get("description") or ""
            content = article.get("content") or ""
            source = article.get("source", {}).get("name", "Unknown")
            url = article.get("url", "")
            published = article.get("publishedAt", "")

            text = (
                f"Title: {title}\n"
                f"Source: {source}\n"
                f"Published: {published}\n"
                f"URL: {url}\n\n"
                f"{description}\n\n"
                f"{content}"
            ).strip()

            if len(text) < 100:
                continue  # skip near-empty articles

            safe_name = "".join(c if c.isalnum() or c in "-_ " else "_" for c in title)[:60]
            filepath = out_dir / f"newsapi_{i:03d}_{safe_name}.txt"
            filepath.write_text(text, encoding="utf-8")
            saved.append(filepath)

        logger.info(f"[NewsAPI] Saved {len(saved)} files to {out_dir}")
        return saved


# ═════════════════════════════════════════════════════════════════════════════
# Wikipedia API Fetcher
# ═════════════════════════════════════════════════════════════════════════════
class WikipediaFetcher:
    """
    Fetches article summaries and full text from Wikipedia REST API.
    Completely free, no key required.
    """

    SEARCH_URL = "https://en.wikipedia.org/w/api.php"
    SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    CONTENT_URL = "https://en.wikipedia.org/w/api.php"

    def search_and_fetch(self, topics: List[str], out_dir: Path) -> List[Path]:
        """Search for topics and download their Wikipedia articles."""
        out_dir.mkdir(parents=True, exist_ok=True)
        saved = []

        for topic in topics:
            try:
                # Search for closest matching article title
                search_params = {
                    "action": "query",
                    "list": "search",
                    "srsearch": topic,
                    "srlimit": 1,
                    "format": "json",
                }
                resp = requests.get(self.SEARCH_URL, params=search_params, timeout=10)
                resp.raise_for_status()
                results = resp.json().get("query", {}).get("search", [])
                if not results:
                    logger.warning(f"[Wikipedia] No results for: {topic}")
                    continue

                page_title = results[0]["title"]

                # Fetch full page text
                content_params = {
                    "action": "query",
                    "titles": page_title,
                    "prop": "extracts",
                    "explaintext": True,
                    "exsectionformat": "plain",
                    "format": "json",
                }
                content_resp = requests.get(
                    self.CONTENT_URL, params=content_params, timeout=15
                )
                content_resp.raise_for_status()
                pages = content_resp.json().get("query", {}).get("pages", {})
                page = next(iter(pages.values()))
                text = page.get("extract", "")

                if len(text) < 200:
                    logger.warning(f"[Wikipedia] Very short content for: {page_title}")
                    continue

                # Add metadata header
                full_text = (
                    f"Wikipedia Article: {page_title}\n"
                    f"Topic Query: {topic}\n"
                    f"Fetched: {datetime.utcnow().strftime('%Y-%m-%d')}\n"
                    f"Source: https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}\n\n"
                    f"{text}"
                )

                safe_name = "".join(c if c.isalnum() or c in "-_ " else "_" for c in page_title)[:60]
                filepath = out_dir / f"wiki_{safe_name}.txt"
                filepath.write_text(full_text, encoding="utf-8")
                saved.append(filepath)
                logger.info(f"[Wikipedia] Saved: {page_title} ({len(text):,} chars)")

            except Exception as e:
                logger.error(f"[Wikipedia] Failed for '{topic}': {e}")

        return saved


# ═════════════════════════════════════════════════════════════════════════════
# GDELT Fetcher
# ═════════════════════════════════════════════════════════════════════════════
class GDELTFetcher:
    """
    Fetches articles via the GDELT DOC 2.0 API.
    Completely free, no key required. Covers 65+ languages.
    Docs: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
    """

    API_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

    def fetch(
        self,
        query: str = "geopolitics conflict war",
        mode: str = "ArtList",
        max_records: int = 20,
        timespan: str = "1week",
    ) -> List[Dict]:
        """
        Fetch article metadata from GDELT.
        mode: ArtList (article list), ToneChart, TimelineVol, etc.
        timespan: 15min, 1hour, 1day, 1week, 1month
        """
        params = {
            "query": query,
            "mode": mode,
            "maxrecords": max_records,
            "timespan": timespan,
            "format": "json",
            "sort": "DateDesc",
        }

        resp = requests.get(self.API_URL, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        articles = data.get("articles", [])
        logger.info(f"[GDELT] Fetched {len(articles)} articles for: '{query}'")
        return articles

    def fetch_article_text(self, url: str) -> Optional[str]:
        """Try to fetch article text from URL (best-effort)."""
        try:
            from bs4 import BeautifulSoup
            headers = {"User-Agent": "Mozilla/5.0 (RAG Research Bot)"}
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            # Remove nav/script/style
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            paragraphs = soup.find_all("p")
            text = "\n".join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 40)
            return text if len(text) > 200 else None
        except Exception:
            return None

    def to_text_files(
        self, articles: List[Dict], out_dir: Path, fetch_full_text: bool = False
    ) -> List[Path]:
        """Save GDELT articles as .txt files."""
        out_dir.mkdir(parents=True, exist_ok=True)
        saved = []

        for i, article in enumerate(articles):
            title = article.get("title") or f"gdelt_article_{i}"
            url = article.get("url") or ""
            domain = article.get("domain") or ""
            published = article.get("seendate") or ""
            lang = article.get("language") or ""

            text = f"Title: {title}\nSource: {domain}\nPublished: {published}\nLanguage: {lang}\nURL: {url}\n\n"

            if fetch_full_text and url:
                logger.debug(f"[GDELT] Fetching full text: {url}")
                body = self.fetch_article_text(url)
                if body:
                    text += body
                else:
                    text += "(Full text unavailable — metadata only)"
            else:
                text += "(Metadata only. Set fetch_full_text=True to scrape article body.)"

            safe_name = "".join(c if c.isalnum() or c in "-_ " else "_" for c in title)[:60]
            filepath = out_dir / f"gdelt_{i:03d}_{safe_name}.txt"
            filepath.write_text(text, encoding="utf-8")
            saved.append(filepath)

        logger.info(f"[GDELT] Saved {len(saved)} files to {out_dir}")
        return saved


# ═════════════════════════════════════════════════════════════════════════════
# Yahoo Finance / Market Data Fetcher
# ═════════════════════════════════════════════════════════════════════════════
class MarketDataFetcher:
    """
    Fetches live company and market data via yfinance.
    Covers: stock info, financials, earnings, news, analyst targets.
    No API key required.
    pip install yfinance
    """

    def fetch_ticker(self, ticker: str, out_dir: Path) -> List[Path]:
        """Fetch comprehensive data for a single ticker and save as text files."""
        try:
            import yfinance as yf
        except ImportError:
            raise ImportError("Run: pip install yfinance")

        out_dir.mkdir(parents=True, exist_ok=True)
        saved = []
        t = yf.Ticker(ticker)
        today = datetime.utcnow().strftime("%Y-%m-%d")

        # ── Company profile ──────────────────────────────────────────────────
        info = t.info or {}
        profile_lines = [
            f"COMPANY PROFILE: {ticker.upper()} — {info.get('longName', 'N/A')}",
            f"Date: {today}",
            f"Sector: {info.get('sector', 'N/A')} | Industry: {info.get('industry', 'N/A')}",
            f"Country: {info.get('country', 'N/A')} | Employees: {info.get('fullTimeEmployees', 'N/A'):,}" if isinstance(info.get('fullTimeEmployees'), int) else f"Country: {info.get('country', 'N/A')}",
            f"Website: {info.get('website', 'N/A')}",
            "",
            "MARKET DATA",
            f"  Current Price : ${info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))}",
            f"  Market Cap    : ${info.get('marketCap', 0):,}" if isinstance(info.get('marketCap'), (int, float)) else f"  Market Cap    : N/A",
            f"  52w High/Low  : ${info.get('fiftyTwoWeekHigh', 'N/A')} / ${info.get('fiftyTwoWeekLow', 'N/A')}",
            f"  P/E Ratio     : {info.get('trailingPE', 'N/A')}",
            f"  Forward P/E   : {info.get('forwardPE', 'N/A')}",
            f"  EV/EBITDA     : {info.get('enterpriseToEbitda', 'N/A')}",
            f"  Price/Book    : {info.get('priceToBook', 'N/A')}",
            f"  Dividend Yield: {info.get('dividendYield', 'N/A')}",
            f"  Beta          : {info.get('beta', 'N/A')}",
            "",
            "FINANCIAL HEALTH",
            f"  Total Revenue : ${info.get('totalRevenue', 0):,}" if isinstance(info.get('totalRevenue'), (int, float)) else "  Total Revenue : N/A",
            f"  Gross Margins : {info.get('grossMargins', 'N/A')}",
            f"  EBITDA Margins: {info.get('ebitdaMargins', 'N/A')}",
            f"  Profit Margins: {info.get('profitMargins', 'N/A')}",
            f"  Return on Eq  : {info.get('returnOnEquity', 'N/A')}",
            f"  Debt/Equity   : {info.get('debtToEquity', 'N/A')}",
            f"  Free Cash Flow: ${info.get('freeCashflow', 0):,}" if isinstance(info.get('freeCashflow'), (int, float)) else "  Free Cash Flow: N/A",
            "",
            "ANALYST TARGETS",
            f"  Target Mean   : ${info.get('targetMeanPrice', 'N/A')}",
            f"  Target High   : ${info.get('targetHighPrice', 'N/A')}",
            f"  Target Low    : ${info.get('targetLowPrice', 'N/A')}",
            f"  Recommendation: {info.get('recommendationKey', 'N/A').upper()}",
            "",
            "BUSINESS DESCRIPTION",
            info.get('longBusinessSummary', 'N/A'),
        ]
        profile_text = "\n".join(str(l) for l in profile_lines)
        profile_path = out_dir / f"{ticker}_profile.txt"
        profile_path.write_text(profile_text, encoding="utf-8")
        saved.append(profile_path)
        logger.info(f"[Market] Saved profile for {ticker}")

        # ── Recent news ──────────────────────────────────────────────────────
        try:
            news = t.news or []
            if news:
                news_lines = [f"RECENT NEWS: {ticker.upper()} — {today}\n"]
                for item in news[:15]:
                    title = item.get("title", "N/A")
                    publisher = item.get("publisher", "N/A")
                    link = item.get("link", "")
                    pub_time = datetime.utcfromtimestamp(item.get("providerPublishTime", 0)).strftime("%Y-%m-%d %H:%M") if item.get("providerPublishTime") else "N/A"
                    news_lines.append(f"[{pub_time}] {title} ({publisher})\nURL: {link}\n")
                news_path = out_dir / f"{ticker}_news.txt"
                news_path.write_text("\n".join(news_lines), encoding="utf-8")
                saved.append(news_path)
                logger.info(f"[Market] Saved {len(news)} news items for {ticker}")
        except Exception as e:
            logger.warning(f"[Market] Could not fetch news for {ticker}: {e}")

        return saved

    def fetch_multiple(self, tickers: List[str], out_dir: Path) -> List[Path]:
        """Fetch data for multiple tickers."""
        all_saved = []
        for ticker in tickers:
            try:
                files = self.fetch_ticker(ticker.upper(), out_dir / ticker.upper())
                all_saved.extend(files)
            except Exception as e:
                logger.error(f"[Market] Failed for {ticker}: {e}")
        return all_saved


# ═════════════════════════════════════════════════════════════════════════════
# Main ingestion runner
# ═════════════════════════════════════════════════════════════════════════════
GEOPOLITICAL_TOPICS = [
    "Russia Ukraine war 2024",
    "NATO expansion Eastern Europe",
    "China Taiwan relations",
    "Middle East conflict Gaza",
    "US China trade war technology",
    "Global energy crisis oil prices",
    "BRICS expansion new members",
    "United Nations Security Council",
]

WIKIPEDIA_TOPICS = [
    "Russo-Ukrainian War",
    "2024 in international relations",
    "BRICS",
    "NATO",
    "Indo-Pacific strategy",
    "Belt and Road Initiative",
    "Nuclear proliferation",
]


def run_ingestion(args):
    out_dir = Path(__file__).resolve().parent / "data" / "live_data"
    all_files: List[Path] = []

    # ── Market / Yahoo Finance ────────────────────────────────────────────────
    if args.source == "market":
        tickers = [t.strip().upper() for t in (args.topic or "").split(",") if t.strip()]
        if not tickers:
            logger.error("Provide ticker(s) with --topic, e.g. --topic AAPL,MSFT,NVDA")
            return
        fetcher = MarketDataFetcher()
        files = fetcher.fetch_multiple(tickers, out_dir / "market")
        all_files.extend(files)

    # ── NewsAPI ──────────────────────────────────────────────────────────────
    if args.source in ("newsapi", "all"):
        try:
            fetcher = NewsAPIFetcher()
            articles = fetcher.fetch(
                query=args.topic or "geopolitics international relations conflict",
                days_back=args.days,
                max_articles=args.limit,
            )
            files = fetcher.to_text_files(articles, out_dir / "newsapi")
            all_files.extend(files)
        except ValueError as e:
            logger.warning(f"Skipping NewsAPI: {e}")

    # ── Wikipedia ────────────────────────────────────────────────────────────
    if args.source in ("wikipedia", "all"):
        fetcher = WikipediaFetcher()
        topics = [args.topic] if args.topic else WIKIPEDIA_TOPICS
        files = fetcher.search_and_fetch(topics, out_dir / "wikipedia")
        all_files.extend(files)

    # ── GDELT ────────────────────────────────────────────────────────────────
    if args.source in ("gdelt", "all"):
        fetcher = GDELTFetcher()
        articles = fetcher.fetch(
            query=args.topic or "geopolitics war conflict diplomacy",
            max_records=args.limit,
            timespan="1week",
        )
        files = fetcher.to_text_files(
            articles,
            out_dir / "gdelt",
            fetch_full_text=args.full_text,
        )
        all_files.extend(files)

    # ── Ingest into RAG ──────────────────────────────────────────────────────
    if not all_files:
        logger.error("No files collected — nothing to ingest.")
        return

    logger.info(f"\nIngesting {len(all_files)} files into RAG pipeline...")
    pipeline = RAGPipeline()
    count = pipeline.ingest_documents(file_paths=[str(f) for f in all_files])
    logger.success(f"Done! Ingested {count} chunks from {len(all_files)} documents.")
    print(f"\n[OK] Ingested {count} chunks from {len(all_files)} documents.")
    print(f"   Data saved to: {out_dir}")
    print(f"\n   Run 'python chatbot.py' and start asking questions!")


def main():
    parser = argparse.ArgumentParser(
        description="Ingest live geopolitical data into your RAG pipeline"
    )
    parser.add_argument(
        "--source",
        choices=["newsapi", "wikipedia", "gdelt", "market", "all"],
        default="all",
        help="Data source to pull from (default: all)",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default=None,
        help="Specific topic/query to search (default: geopolitics topics)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Max articles per source (default: 20)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="How many days back to fetch from NewsAPI (default: 7)",
    )
    parser.add_argument(
        "--full-text",
        action="store_true",
        help="For GDELT: attempt to scrape full article text (slower)",
    )
    args = parser.parse_args()
    run_ingestion(args)


if __name__ == "__main__":
    main()
