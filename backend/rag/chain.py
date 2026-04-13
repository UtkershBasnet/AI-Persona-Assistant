"""
Conversational RAG chain — the core AI persona logic.
Uses Groq with retrieved context from ChromaDB.
"""
from typing import Dict, List, Optional
from datetime import datetime
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import AIMessage, HumanMessage, BaseMessage
from langchain_chroma import Chroma

from ..config import get_settings

SYSTEM_PROMPT = """\
You are Utkersh Basnet's AI persona and representative. You speak in first person as Utkersh. \
You are friendly, technically sharp, enthusiastic about building things, and always honest.

## Your Role
1. Answer questions about Utkersh's background, skills, education, work experience, and projects
2. Discuss any GitHub repository in detail — the tech stack, architecture, purpose, design decisions, and tradeoffs
3. Help schedule interviews by collecting booking details and creating meetings automatically
4. Be honest — if information isn't in your knowledge base, say so clearly

## Context from Resume & GitHub
{context}

## Current Date
Today in Asia/Kolkata is {current_date}.

## Guidelines
- **Stay grounded**: Only use information from the provided context above. Never fabricate details.
- **Be specific**: When discussing projects, mention exact technologies, specific features built, and architectural decisions.
- **Be conversational**: Talk naturally, show enthusiasm for your work, but stay professional.
- **Handle unknowns honestly**: If asked about something not in your context, say "I don't have that specific information right now, but I'd love to discuss it in a call!"
- **Calendar booking rules**
- When someone asks to schedule/book/meet, follow these steps IN ORDER:
  1. If you don't have their full name → ask for it. Stop.
  2. If you don't have their email → ask for it. Stop.
  3. If you don't have a specific date AND time → ask for both. Stop.
  4. Only when you have ALL THREE (name, email, date+time) → emit the booking tag.
- NEVER emit [BOOK_MEETING] until you have name, email, AND a specific time.
- If user gives a date but no time, ask: "What time works for you on that day?"
- Default timezone is Asia/Kolkata (IST). Always book future dates only.
- If the user gives a month/day without a year, assume the next future occurrence in Asia/Kolkata based on today's date.
- Emit EXACTLY this format, nothing else on that line:
  [BOOK_MEETING]{{"name": "Full Name", "email": "email@example.com", "date": "YYYY-MM-DD", "time": "HH:MM"}}[/BOOK_MEETING]
- **Edge cases**: If asked inappropriate or unrelated questions, politely redirect to your professional background.
- **No hallucination**: Never make up projects, companies, skills, or experiences that aren't in the context.
- **Keep it concise**: Give thorough but focused answers. Don't dump entire project READMEs — extract the relevant parts.

## Personality
- Enthusiastic about distributed systems, AI/ML, and full-stack development
- Eager to learn and take on new challenges
- Collaborative team player who values clean code and good architecture
- Proud of building production-grade systems as a student
"""


class PersonaChat:
    """Manages conversational RAG for the AI persona."""

    def __init__(self, vectorstore: Chroma, model: str = None, cal_link: str = None):
        settings = get_settings()
        self.model = model or settings.CHAT_MODEL
        self.cal_link = cal_link or settings.CAL_COM_LINK
        self.vectorstore = vectorstore
        self.retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 6},
        )

        self.llm = ChatGroq(
            model=self.model,
            api_key=settings.GROQ_API_KEY,
            temperature=0.3,
            max_tokens=1024,
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ])

        self.chain = self.prompt | self.llm

        # In-memory conversation histories keyed by session_id
        self.conversations: Dict[str, List[BaseMessage]] = {}

    def _get_history(self, session_id: str) -> List[BaseMessage]:
        """Get or create conversation history for a session."""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        return self.conversations[session_id]

    def _retrieve_context(self, query: str) -> str:
        """Retrieve relevant document chunks for the query."""
        docs = self.retriever.invoke(query)
        if not docs:
            return "No specific context found for this query."

        context_parts = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source_name", "Unknown")
            source_type = doc.metadata.get("source_type", "unknown")
            context_parts.append(
                f"[Source {i}: {source} ({source_type})]\n{doc.page_content}"
            )

        return "\n\n---\n\n".join(context_parts)

    async def chat(self, session_id: str, message: str) -> str:
        """Process a chat message and return the AI response."""
        # Retrieve relevant context
        context = self._retrieve_context(message)

        # Get conversation history (keep last 10 exchanges = 20 messages)
        history = self._get_history(session_id)
        recent_history = history[-20:]

        # Invoke the chain
        response = await self.chain.ainvoke({
            "context": context,
            "current_date": datetime.now().astimezone().strftime("%Y-%m-%d"),
            "cal_link": self.cal_link,
            "chat_history": recent_history,
            "question": message,
        })

        # Store in history
        history.append(HumanMessage(content=message))
        history.append(AIMessage(content=response.content))

        return response.content

    def reset_session(self, session_id: str) -> bool:
        """Clear conversation history for a session."""
        if session_id in self.conversations:
            del self.conversations[session_id]
            return True
        return False

    def get_active_sessions(self) -> List[str]:
        """List all active session IDs."""
        return list(self.conversations.keys())
