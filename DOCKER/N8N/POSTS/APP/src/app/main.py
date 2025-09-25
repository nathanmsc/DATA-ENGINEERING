#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from app.crew import App

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'Topic': 'Sorriso radiante, coração leve! Transformando sorrisos, odontologia com amor.',
        'Description': 'Um detalhe fotográfico que destaque o sorriso enquanto o paciente realiza o tratamento dentário, destacando sua confiança em si mesmo.', 
        'Prompt_image': 'Image of a patient smiling while on dental care, highlighting their confidence in themselves.', 
        'Voice': 'Descolado e acessível',
        'Audience': 'Pessoas entre 25-45 anos, que valorizam saúde bucal e estética, buscando dicas práticas e inspiração para um sorriso saudável.', 
        'Platform': 'Instagram', 
        'Current_year': str(datetime.now().year)
    }
    
    try:
        App().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")



###################################################################################
# The following functions are examples of how you can use the crew programmatically
# to train, replay or test it. You can remove them if you don't need them.
def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        App().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        App().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        App().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
