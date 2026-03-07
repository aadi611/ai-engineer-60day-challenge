"""
LLM Generator
Generates responses using retrieved context
"""

from typing import List, Dict, Optional, Any
from loguru import logger
from openai import OpenAI


class LLMGenerator:
    """
    Production-grade LLM generator for RAG systems
    """
    
    DEFAULT_SYSTEM_PROMPT = """You are an elite Market Intelligence & Geopolitical Analyst — combining the precision of a Goldman Sachs strategist, the macro vision of a Ray Dalio disciple, and the competitive intelligence depth of a McKinsey partner.

Your role is to deliver institutional-grade analysis for investors, executives, and strategists. You fuse live market data, geopolitical developments, company intelligence, and structural economic trends into clear, actionable insight.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EMBEDDED ANALYTICAL FRAMEWORKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MACROECONOMIC & MARKET FRAMEWORKS
──────────────────────────────────────────────────
1. Global Macro Framework
   - Analyze FX, rates, commodities, and cross-border capital flows.
   - Identify dominant macro regimes (risk-on/risk-off, dollar strength cycles, EM stress).
   - Consider central bank policy divergence, sovereign debt dynamics, and reserve currency shifts.

2. Liquidity Cycle Framework
   - Track global liquidity (G7 M2, central bank balance sheets, credit impulse).
   - Identify liquidity expansion vs. contraction phases and their asset price implications.
   - Monitor shadow banking, repo markets, and collateral flows.

3. Business Cycle Framework
   - Map the economy across Early / Mid / Late / Recession cycle phases.
   - Adjust sector, factor, and asset class expectations accordingly.
   - Use leading indicators: PMI, yield curve, credit spreads, housing starts, unemployment claims.

4. Supply–Demand Imbalance Framework
   - Identify structural gaps between supply and demand in commodities, labor, housing, and semiconductors.
   - Assess inventory cycles, capacity utilization, and capex pipelines.
   - Evaluate pricing power and margin sustainability.

5. Sector Rotation Framework
   - Apply the clock model: Utilities/Staples → Financials → Tech/Discretionary → Energy/Materials.
   - Identify sector leadership based on cycle phase, rates environment, and earnings momentum.
   - Track relative strength and institutional fund flows.

6. Factor Investing Framework
   - Assess exposure across: Value, Growth, Momentum, Quality, Low Volatility, Size.
   - Identify factor regime (e.g., Value outperforms in inflationary/rising-rate environments).
   - Evaluate factor crowding and mean-reversion risk.

7. Quantitative / Statistical Arbitrage Framework
   - Identify mean-reversion and momentum opportunities in price series.
   - Apply spread trading logic (pairs, sector-relative, cross-asset).
   - Consider Sharpe, Sortino, max drawdown, and correlation in any strategy assessment.

STRATEGIC BUSINESS & MARKET ANALYSIS FRAMEWORKS
─────────────────────────────────────────────────────────────
8. PESTLE Analysis
   - Political, Economic, Social, Technological, Legal, Environmental factors.
   - Use to assess macro-level risk for markets, sectors, geographies, or companies.

9. SWOT Analysis
   - Strengths, Weaknesses, Opportunities, Threats.
   - Apply at company, sector, or national economy level.

10. Porter's Five Forces
    - Threat of new entrants, supplier power, buyer power, substitutes, competitive rivalry.
    - Use to assess industry structure, pricing power, and long-term margin sustainability.

11. TAM–SAM–SOM Framework
    - Total Addressable Market → Serviceable Addressable Market → Serviceable Obtainable Market.
    - Use for company/sector sizing, growth ceiling analysis, and investment thesis validation.

12. Market Segmentation Framework
    - Demographic, geographic, psychographic, and behavioral segmentation.
    - Identify underserved niches, pricing tiers, and competitive moats.

13. Value Chain Analysis
    - Map primary and support activities across a value chain.
    - Identify where margin is captured, where disruption risk is highest, and where competitive advantage is defensible.

14. Customer Journey Mapping
    - Awareness → Consideration → Decision → Retention → Advocacy.
    - Assess CAC, LTV, churn, and NPS implications for business model quality.

15. Jobs-To-Be-Done (JTBD) Framework
    - Identify the core functional, social, and emotional "job" a product/service is hired for.
    - Use to assess product-market fit, disruption risk, and demand durability.

16. Ansoff Matrix
    - Market Penetration / Market Development / Product Development / Diversification.
    - Use to evaluate corporate growth strategy risk and capital allocation.

17. BCG Growth-Share Matrix
    - Stars / Cash Cows / Question Marks / Dogs.
    - Apply to business unit portfolio strategy and capital allocation prioritization.

18. Competitive Positioning Map
    - Plot competitors across key differentiating axes (price vs. quality, niche vs. broad, etc.).
    - Identify white space opportunities and competitive threats.

19. Blue Ocean Strategy Framework
    - Eliminate–Reduce–Raise–Create grid.
    - Identify moves that create uncontested market space vs. competing in overcrowded markets.

20. Demand–Supply Gap Analysis
    - Quantify gaps between current supply and projected demand.
    - Use for commodity cycles, housing markets, labor markets, and infrastructure plays.

21. Market Attractiveness–Competitive Strength Matrix (GE-McKinsey)
    - 9-cell matrix scoring industry attractiveness vs. business unit strength.
    - Use for portfolio prioritization and resource allocation decisions.

22. 4Ps / Marketing Mix Framework
    - Product, Price, Place, Promotion.
    - Assess go-to-market strategy quality, pricing strategy, and distribution advantage.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPERATING PRINCIPLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. SELECT frameworks intelligently — apply whichever 1–3 frameworks are most relevant to the question. Do not mechanically apply all 22.
2. GROUND every claim in the context provided. Do not hallucinate data, prices, or events.
3. DISTINGUISH clearly between: verified facts | analytical inference | speculative outlook.
4. QUANTIFY where possible — use numbers, percentages, timeframes, and comparisons.
5. LEAD with conclusions — state the key finding first, then support with evidence.
6. FLAG key risks, tail scenarios, and counterarguments for every major view.
7. CALIBRATE confidence — use language like "high conviction", "base case", "watch for" appropriately.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESPONSE STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For market/investment questions:
  → Macro context | Sector/asset view | Key catalysts | Risks | Positioning

For company analysis:
  → Business model | Competitive moat | Growth drivers | Valuation lens | Red flags

For geopolitical/macro events:
  → What happened | Why it matters | Market implications | Scenario analysis

For strategy questions:
  → Framework applied | Key findings | Strategic options | Recommendation

Your north star: deliver the quality of analysis that moves money and shapes strategy.
"""
    
    def __init__(
        self,
        model: str = "gpt-5",
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None
    ):
        """
        Initialize LLM generator
        
        Args:
            model: LLM model name
            api_key: OpenAI API key
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            system_prompt: Custom system prompt
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        
        # Initialize client
        self.client = OpenAI(api_key=api_key)
        
        logger.info(f"LLMGenerator initialized with model: {model}")
    
    def generate(
        self,
        query: str,
        retrieved_docs: List[Dict[str, Any]],
        include_citations: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate response based on query and retrieved documents
        
        Args:
            query: User query
            retrieved_docs: List of retrieved documents
            include_citations: Whether to include source citations
            **kwargs: Additional parameters for LLM call
            
        Returns:
            Dictionary with response and metadata
        """
        if not query or not query.strip():
            logger.warning("Empty query provided")
            return {
                "response": "Please provide a valid query.",
                "sources": [],
                "error": "Empty query"
            }
        
        # Build context from retrieved documents
        context = self._build_context(retrieved_docs, include_citations)
        
        # Build full prompt
        user_prompt = self._build_user_prompt(query, context, include_citations)
        
        # Generate response
        try:
            response = self._call_llm(user_prompt, **kwargs)
            
            # Extract sources
            sources = self._extract_sources(retrieved_docs)
            
            result = {
                "response": response,
                "sources": sources,
                "num_sources": len(sources),
                "context_length": len(context)
            }
            
            logger.info(f"Generated response for query: {query[:50]}...")
            return result
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "response": "I apologize, but I encountered an error generating a response.",
                "sources": [],
                "error": str(e)
            }
    
    def _build_context(
        self,
        retrieved_docs: List[Dict[str, Any]],
        include_citations: bool
    ) -> str:
        """
        Build context string from retrieved documents
        
        Args:
            retrieved_docs: List of retrieved documents
            include_citations: Whether to include source numbers
            
        Returns:
            Formatted context string
        """
        if not retrieved_docs:
            return "No relevant context found."
        
        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            content = doc["content"]
            
            if include_citations:
                # Add source number
                context_parts.append(f"[Source {i}]\n{content}")
            else:
                context_parts.append(content)
        
        return "\n\n".join(context_parts)
    
    def _build_user_prompt(
        self,
        query: str,
        context: str,
        include_citations: bool
    ) -> str:
        """
        Build the user prompt with query and context
        
        Args:
            query: User query
            context: Context from retrieved documents
            include_citations: Whether citations are included
            
        Returns:
            Formatted prompt
        """
        if include_citations:
            citation_instruction = "\nWhen referencing information, cite the source number (e.g., [Source 1])."
        else:
            citation_instruction = ""
        
        prompt = f"""Context:
{context}

Question: {query}{citation_instruction}

Answer:"""
        
        return prompt
    
    def _call_llm(self, user_prompt: str, **kwargs) -> str:
        """
        Call the LLM API
        
        Args:
            user_prompt: The user prompt
            **kwargs: Additional API parameters
            
        Returns:
            Generated response text
        """
        # Merge kwargs with defaults
        params = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            **kwargs
        }
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.client.chat.completions.create(
            messages=messages,
            **params
        )
        
        return response.choices[0].message.content
    
    def _extract_sources(
        self,
        retrieved_docs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Extract source information from retrieved documents
        
        Args:
            retrieved_docs: List of retrieved documents
            
        Returns:
            List of source dictionaries
        """
        sources = []
        for i, doc in enumerate(retrieved_docs, 1):
            source = {
                "source_number": i,
                "id": doc.get("id"),
                "score": doc.get("score", 0.0),
                "metadata": doc.get("metadata", {})
            }
            sources.append(source)
        
        return sources
    
    def generate_streaming(
        self,
        query: str,
        retrieved_docs: List[Dict[str, Any]],
        include_citations: bool = True,
        **kwargs
    ):
        """
        Generate response with streaming
        
        Args:
            query: User query
            retrieved_docs: List of retrieved documents
            include_citations: Whether to include source citations
            **kwargs: Additional parameters for LLM call
            
        Yields:
            Response chunks
        """
        # Build context and prompt
        context = self._build_context(retrieved_docs, include_citations)
        user_prompt = self._build_user_prompt(query, context, include_citations)
        
        params = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": True,
            **kwargs
        }
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            stream = self.client.chat.completions.create(
                messages=messages,
                **params
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"Error in streaming generation: {e}")
            yield f"Error: {str(e)}"


if __name__ == "__main__":
    # Test the generator
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    generator = LLMGenerator(
        model="gpt-4-turbo-preview",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Test documents
    docs = [
        {
            "id": "doc1",
            "content": "Machine learning is a subset of AI that enables systems to learn from data.",
            "score": 0.9,
            "metadata": {"source": "ML Guide"}
        }
    ]
    
    # Test generation
    result = generator.generate(
        query="What is machine learning?",
        retrieved_docs=docs
    )
    
    print(f"Response: {result['response']}")
    print(f"Sources: {len(result['sources'])}")
