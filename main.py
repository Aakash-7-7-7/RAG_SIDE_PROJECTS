from app.pipeline import RAGMemoryPipeline
from app.config import SHOW_DEBUG


def main():

    chat = RAGMemoryPipeline()

    while True:

        question = input("\nYou: ").strip()

        if not question:
            continue

        if question.lower() == "exit":
            break

        try:

            result = chat.ask(question)

            if SHOW_DEBUG:
                print("\n[Rewritten Question]")
                print(result["standalone_question"])

            print("\nAI:")
            print(result["answer"])

            if SHOW_DEBUG:
                print("\n-----------------------------")
                print("CURRENT SUMMARY:")
                print(result["summary"])
                print("\nMEMORIES EXTRACTED:")
                print(result["memories"])
                print("-----------------------------")

        except Exception as e:

            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()