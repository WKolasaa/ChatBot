from src.embeddings import EmbeddingModel
from src.chat import Chatbot
from src.utils import print_analytics

def main():
    print("Arrhythmia Project Chatbot - CLI")
    print("Type your question, or type ':help', ':reset', ':history', ':exit'")
    embedder = EmbeddingModel()
    bot = Chatbot("data/vector_store", embedder)
    while True:
        user = input("You: ").strip()
        if user == ":exit":
            print("Goodbye!")
            break
        elif user == ":help":
            print("Ask any question about the project docs. Commands: :help, :reset, :history, :exit")
        elif user == ":reset":
            bot.history = []
            print("History reset.")
        elif user == ":history":
            bot.show_history()
        elif user == ":analytics":
            print_analytics(bot)
        elif user:
            try:
                answer = bot.ask(user)
                print("Bot:", answer)
            except Exception as e:
                print("Error:", e)

if __name__ == "__main__":
    main()
