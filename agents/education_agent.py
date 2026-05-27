"""
Education Agent
---------------
Determines what finance concept to teach today and prepares the lesson context.

This agent doesn't call Claude itself — it prepares the "lesson brief"
that gets included in the main orchestrator prompt.

Key concept: By separating "what to teach" from "how to write it",
we keep each agent focused on one job (Single Responsibility Principle).
"""

from memory.database import get_next_topic, get_recent_topics, get_newsletters_sent


# Difficulty level descriptions passed to Claude
DIFFICULTY_DESCRIPTIONS = {
    1: "beginner-friendly with simple language, real-world analogies, and no complex math",
    2: "intermediate with some formulas, technical terminology, and exam-style examples",
    3: "advanced with full derivations, professional-level analysis, and exam preparation",
}


def get_lesson_brief() -> dict:
    """
    Prepare the education brief for today's newsletter.
    
    Returns a dict with:
    - topic: what to teach today
    - difficulty: how hard to make it
    - recent_topics: what was taught recently (for continuity)
    - newsletters_sent: total count (for progress tracking)
    - prompt_context: formatted string for Claude's prompt
    """
    lesson = get_next_topic()
    recent = get_recent_topics(5)
    total_sent = get_newsletters_sent()
    
    difficulty_desc = DIFFICULTY_DESCRIPTIONS.get(lesson["difficulty_level"], DIFFICULTY_DESCRIPTIONS[1])
    
    recent_str = ", ".join(recent) if recent else "none yet (this is the first newsletter)"
    
    prompt_context = f"""
EDUCATION SECTION BRIEF:
- Today's topic: {lesson['topic']}
- This is lesson #{lesson['lesson_number']} on this topic
- Difficulty level: {lesson['difficulty_level']}/3 ({difficulty_desc})
- Recent topics covered: {recent_str}
- Total newsletters sent so far: {total_sent}
- Reader background: Undergraduate degree not in finance; 
  preparing for University of Miami MSF program;
  familiar with basic investing from YouTube/personal experience

INSTRUCTIONS FOR EDUCATION SECTION:
Write a ~400-600 word lesson on "{lesson['topic']}" at the specified difficulty level.
Structure it as:
1. One-sentence hook connecting to current market events if possible
2. Core concept explanation with at least one concrete example
3. Why this matters for a finance master's program
4. One formula or key metric (if applicable at this difficulty level)
5. A "Remember this" one-liner summary at the end

Build on recent topics where natural: {recent_str}
"""
    
    return {
        "topic": lesson["topic"],
        "topic_index": lesson["topic_index"],
        "difficulty": lesson["difficulty_level"],
        "recent_topics": recent,
        "newsletters_sent": total_sent,
        "prompt_context": prompt_context,
    }
