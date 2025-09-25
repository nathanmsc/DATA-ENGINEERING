import requests
import json
import instructor
from pydantic import BaseModel, field_validator, Field
from crewai import Agent, Task, Crew, Process   # <- certo


class Person(BaseModel):
    name: str = Field(description="The person's full name")
    age: int = Field(description="The person's age in years")

    @field_validator("age", mode="before")
    def parse_age(cls, v):
        return int(v)
    
class ResearchData(BaseModel):
    topic: str = Field(description="The research topic")
    findings: list[str] = Field(description="A list of research findings")
    
    @field_validator("findings", mode="before")
    def parse_findings(cls, v):
        if isinstance(v, str):
            return [finding.strip() for finding in v.split(",")]
        return v

class Report(BaseModel):
    topic: str = Field(description="The report topic")
    analysis: str = Field(description="A detailed analysis of the research findings")
    recommendations: list[str] = Field(description="A list of actionable recommendations")

    @field_validator("recommendations", mode="before")
    def parse_recommendations(cls, v):
        if isinstance(v, str):
            return [rec.strip() for rec in v.split(",")]
        return v
    
researcher = Agent(
    role="researcher",
    goal="Coletar fatos sobre um tópico",
    backstory="Pesquisador incansável"
)

analyst = Agent(
    role="analyst",
    goal="Escrever um relatório conciso a partir de dados de pesquisa",
    backstory="Consultor de negócios"
)

# Task 1: Pesquisa
task1 = Task(
    description="Pesquise as tendências de IA em 2025.",
    agent=researcher,
        expected_output="Um JSON com {topic: string, findings: lista de strings}",

)

# Task 2: Análise (recebe dados da Task 1)
task2 = Task(
    description="Analise os dados e dê recomendações estratégicas.",
    agent=analyst,
    expected_output="Um JSON com {topic: string, analysis: string, recommendations: lista de strings}",
    context=[task1]  # Passa a saída validada do primeiro
)

crew = Crew(tasks=[task1, task2])

    
client = instructor.from_provider("ollama/llama3.2:1b")

user = client.chat.completions.create(
    response_model=Person,
    messages=[
        {"role": "user", "content": "John Doe is 30 years old."}
    ]
)

print(f"Customer name: {user.name}, age: {user.age}")

# Execução
research_result = client.chat.completions.create(
    model="ollama/llama3.2:1b",
    response_model=ResearchData,
    messages=[{"role": "user", "content": task1.description}]
)

report_result = client.chat.completions.create(
    model="ollama/llama3.2:1b",
    response_model=Report,
    messages=[
        {"role": "user",
         "content": f"Analise os seguintes achados: {research_result.json()}"}
    ]
)

print(report_result.analysis)