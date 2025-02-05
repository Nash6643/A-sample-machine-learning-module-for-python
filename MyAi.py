import json
from difflib import get_close_matches
from typing import List, Dict, Optional

def load_knowledge_base(file_path: str) -> Dict:
    with open(file_path, "r") as file:
        data: Dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: Dict) -> None:
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: List[str]) -> Optional[str]:
    matches: List[str] = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(user_question: str, questions: List[Dict[str, str]]) -> Optional[str]:
    for q in questions:
        if q["question"] == user_question:
            return q["answer"]
    return None  # Ensure function returns None if no match is found

def chat_bot():
    knowledge_base: Dict = load_knowledge_base("knowledge_base.json")

    while True:
        user_input: str = input("You: ")

        if user_input.lower() == "quit":
            break

        best_match: Optional[str] = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: Optional[str] = get_answer_for_question(best_match, knowledge_base["questions"])
            print(f"Bot: {answer}")
        else:
            print("I don't know what you're looking for. Teach me.")
            new_answer = input("Type an answer or type 'skip': ")

            if new_answer.lower() != "skip":
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base("knowledge_base.json", knowledge_base)
                print("Bot: Thank you! I have learned a new response.")

if __name__ == "__main__":
    chat_bot()
