mport os
import random
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_ai_response(prompt, model="gpt-3.5-turbo", max_tokens=150):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful game narrator."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def generate_random_setting():
    setting_prompt = """Create a unique adventure setting with the following format:
Location: [describe the place]
Time: [describe the time period]
Background: [describe the character's role and situation]
Goal: [describe the main mission/objective]

Make it creative and engaging. Choose from genres like sci-fi, fantasy, mystery, horror, western, etc."""
    
    setting_text = get_ai_response(setting_prompt, max_tokens=200)
    
    lines = setting_text.split('\n')
    setting = {}
    
    for line in lines:
        if line.startswith('Location:'):
            setting['location'] = line.replace('Location:', '').strip()
        elif line.startswith('Time:'):
            setting['time'] = line.replace('Time:', '').strip()
        elif line.startswith('Background:'):
            setting['background'] = line.replace('Background:', '').strip()
        elif line.startswith('Goal:'):
            setting['goal'] = line.replace('Goal:', '').strip()
    
    if not all(key in setting for key in ['location', 'time', 'background', 'goal']):
        setting = {
            "location": "a mysterious dimension",
            "time": "an unknown era",
            "background": "You are an explorer in a strange new world.",
            "goal": "Discover the secrets of this realm and find your way home."
        }
    
    return setting

def get_story_beat(story_progress, setting):
    """Get the next story beat based on progress"""
    story_beats = {
        0: f"You find yourself in {setting['location']} during {setting['time']}. {setting['background']} Your mission: {setting['goal']}",
        1: "You encounter your first obstacle - a choice that will determine your path forward.",
        2: "You discover a clue or ally that helps you understand the situation better.",
        3: "A major challenge presents itself, testing your skills and determination.",
        4: "You reach a critical decision point that will shape the outcome of your journey.",
        5: "The final confrontation approaches as you near your goal.",
        6: "You face the ultimate challenge and must make your final choice."
    }
    return story_beats.get(story_progress, "The adventure continues...")

def main():
    print("🎮 Welcome to the AI-Driven Adventure! 🎮")
    print("=" * 50)
    
    # Generate random setting
    setting = generate_random_setting()
    story_progress = 0
    
    print(f"🌍 Setting: {setting['location']}")
    print(f"⏰ Time: {setting['time']}")
    print(f"🎯 Goal: {setting['goal']}")
    print("=" * 50)
    
    # Initial narrative context
    context = get_story_beat(story_progress, setting)
    print(f"\n{context}\n")

    while True:
        # Get player action
        user_input = input("\nWhat do you do? ('quit' to exit, 'status' for progress) ").strip()
        
        if user_input.lower() in ("quit", "exit"):
            print("Thanks for playing! Safe travels, adventurer.")
            break
            
        if user_input.lower() == "status":
            print(f"\n📊 Story Progress: {story_progress}/6")
            print(f"🎯 Current Goal: {setting['goal']}")
            continue

        # Build the prompt including context and player action
        prompt = f"Setting: {setting['background']}\nCurrent situation: {context}\nPlayer action: {user_input}\nNarrator:"
        
        # Fetch AI's continuation
        narration = get_ai_response(prompt)

        # Display AI response
        print("\n" + narration + "\n")

        # Update context to include this turn
        context += f"\nPlayer action: {user_input}\nNarrator: {narration}"
        
        # Progress the story every few interactions
        if random.random() < 0.3 and story_progress < 6:  # 30% chance to progress
            story_progress += 1
            next_beat = get_story_beat(story_progress, setting)
            if story_progress <= 6:
                print(f"📖 Story Progress: {next_beat}\n")
                context = next_beat

if __name__ == "__main__":
    main()
