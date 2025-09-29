import pydantic # type: ignore[import]
from typing import List
from crewai import Agent, Crew, Process, Task # type: ignore[import]
from crewai.project import CrewBase, agent, crew, task # type: ignore[import]
from crewai.agents.agent_builder.base_agent import BaseAgent # type: ignore[import]
from app.model.agents import Caption, Writer, Imager, Hashtags, Consolidator # type: ignore[import]
from app.tools.googleapi import GetNextPostTool, GetRandomPostTool # type: ignore[import]
from app.tools.instagramapi import InstagramPostTool # type: ignore[import]


@CrewBase
class App():
    """App crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    get_random_post_tool = GetRandomPostTool()
    get_next_post_tool = GetNextPostTool()
    instagram_post_tool = InstagramPostTool()

    @agent
    def caption_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['caption_agent'], # type: ignore[index]
            tools=[self.get_random_post_tool],
            verbose=True,
        )
    
    @agent
    def writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['writer_agent'], # type: ignore[index]
            verbose=True,
        )
    
    @agent
    def imager_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['imager_agent'], # type: ignore[index]
            verbose=True,
        )
    
    @agent
    def hashtag_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['hashtag_agent'], # type: ignore[index]
            verbose=True,
        )

    @agent
    def consolidator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['consolidator_agent'], # type: ignore[index]
            verbose=True,
        )
    
    @task
    def caption_task(self) -> Task:
        return Task(
            config=self.tasks_config['caption_task'], # type: ignore[index]
            output_model=Caption,
            output_file='caption.txt'
        )
    
    @task
    def writer_task(self) -> Task:
        return Task(
            config=self.tasks_config['writer_task'], # type: ignore[index]
            output_model=Writer,
            output_file='post.txt'
        )
    
    @task
    def imager_task(self) -> Task:
        return Task(
            config=self.tasks_config['imager_task'], # type: ignore[index]
            output_model=Imager,
            output_file='prompt_image.txt'
        )
    
    @task
    def hashtag_task(self) -> Task:
        return Task(
            config=self.tasks_config['hashtag_task'], # type: ignore[index]
            output_model=Hashtags,
            output_file='hashtags.txt'
        )
    
    @task
    def consolidator_task(self) -> Task:
        return Task(
            config=self.tasks_config['consolidator_task'], # type: ignore[index]
            output_model=Consolidator,
            output_file='result.json'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the App crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
