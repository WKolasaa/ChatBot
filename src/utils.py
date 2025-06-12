def print_analytics(chatbot):
    print(f"Number of Q&A exchanges: {len(chatbot.history)}")
    if chatbot.history:
        print("Most recent question:", chatbot.history[-1]["question"])
