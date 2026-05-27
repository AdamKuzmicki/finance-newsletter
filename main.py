"""
main.py - Entry Point
---------------------
This is the script that runs every morning at 7 AM via GitHub Actions.

It orchestrates the entire pipeline:
  1. Initialize database
  2. Fetch market data
  3. Fetch news
  4. Prepare education lesson
  5. Generate newsletter with Claude
  6. Send via email
  7. Record progress

Each step is in its own function/module - this is called "separation of concerns"
and is a core software engineering principle.
"""

import sys
import traceback
from datetime import datetime

# Import our modules
from memory.database import initialize_database, record_lesson_taught
from agents.market_agent import get_market_data, format_market_data_for_prompt
from agents.news_agent import get_all_news, format_news_for_prompt
from agents.education_agent import get_lesson_brief
from agents.orchestrator import generate_newsletter_with_memory
from delivery.email_sender import send_newsletter


def run_newsletter_pipeline():
    """
    Main pipeline function.
    Runs every step in sequence and handles errors gracefully.
    """
    start_time = datetime.now()
    print(f"\n{'='*50}")
    print(f"Finance Newsletter Pipeline - {start_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}\n")
    
    # Step 1: Initialize database (creates it if it doesn't exist)
    print("Step 1: Initializing database...")
    initialize_database()
    
    # Step 2: Fetch market data
    print("\nStep 2: Fetching market data...")
    market_data = get_market_data()
    market_text = format_market_data_for_prompt(market_data)
    
    # Step 3: Fetch news
    print("\nStep 3: Fetching financial news...")
    news_articles = get_all_news()
    news_text = format_news_for_prompt(news_articles)
    
    # Step 4: Prepare education lesson
    print("\nStep 4: Preparing today's lesson...")
    lesson_brief = get_lesson_brief()
    print(f"  Today's topic: {lesson_brief['topic']}")
    print(f"  Difficulty: {lesson_brief['difficulty']}/3")
    print(f"  Newsletters sent so far: {lesson_brief['newsletters_sent']}")
    
    # Step 5: Generate newsletter with Claude
    print("\nStep 5: Generating newsletter with Claude...")
    newsletter_html = generate_newsletter_with_memory(
        market_text=market_text,
        news_text=news_text,
        education_context=lesson_brief["prompt_context"],
        recent_topics=lesson_brief["recent_topics"],
        newsletters_sent=lesson_brief["newsletters_sent"],
    )
    
    # Step 6: Send email
    print("\nStep 6: Sending email...")
    success = send_newsletter(newsletter_html)
    
    # Step 7: Record progress (only if email sent successfully)
    if success:
        print("\nStep 7: Recording progress...")
        record_lesson_taught(
            topic=lesson_brief["topic"],
            topic_index=lesson_brief["topic_index"],
        )
    
    # Summary
    elapsed = (datetime.now() - start_time).seconds
    print(f"\n{'='*50}")
    print(f"Pipeline complete in {elapsed}s - {'SUCCESS ✓' if success else 'FAILED ✗'}")
    print(f"{'='*50}\n")
    
    return success


if __name__ == "__main__":
    try:
        success = run_newsletter_pipeline()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Unhandled error: {e}")
        traceback.print_exc()
        sys.exit(1)
