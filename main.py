# main.py
from config.settings import Settings
from graph.langgraph_poc import run_poc_graph

def main():
    # Ensure all env vars are present
    Settings.check()

    # Run the proof-of-concept graph
    run_poc_graph()

if __name__ == "__main__":
    main()
