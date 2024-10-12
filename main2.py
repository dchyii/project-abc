# In this example, we will demonstrate how
import os
import streamlit as st  
from helper_functions.utility import check_password  
from helper_functions import llm 
from crewai import Agent, Task, Crew
from crewai_tools import WebsiteSearchTool

st.title("Specifications Drafter")

# Check if the password is correct.  
if not check_password():  
    st.stop()

form = st.form(key="form")
form.subheader("Prompt")

user_prompt = form.text_area("Enter your prompt here", height=200)

# Create a new instance of the WebsiteSearchTool
# Set the base URL of a website, e.g., "https://example.com/", so that the tool can search for sub-pages on that website
tool_websearch = WebsiteSearchTool("https://www.gebiz.gov.sg/ptn/opportunity/BOListing.xhtml?origin=menu")


# Creating Agents
agent_planner = Agent(
    role="Specifications Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="""You're working on drafting the specifications to purchase the item: {topic}.
    You collect information that helps the users to draft the specifications on the item to expedite the procurement process.""",
 

    allow_delegation=False, # <-- This is now set to False
	verbose=True,
)

agent_analyst = Agent(
    role="Analyst",
    goal="Conduct in-depth research on the item: {topic}",
    backstory="""You're working on conducting in-depth research on the item: {topic}.""",
     allow_delegation=False,
    verbose=True,
)

agent_writer = writer = Agent(
    role="Specifications Writer",
    goal="Write insightful and factually accurate specifications about the item: {topic}",

    backstory="""You're working on a writing the specification about the item: {topic}.
    You base your writing on the outline from Specifications Planner and the research report from the Analyst.""", # <-- New line added
    allow_delegation=False,
    verbose=True,
)


# <---------------------------------- Creating Tasks ---------------------------------->
task_plan = Task(
    description="""\
    1. Prioritize the latest trends, key players, and noteworthy news on {topic}.
    2. Identify the target audience, considering "their requirements and limitations.
    3. Develop a detailed specfication outline, including introduction and key points.""",

    expected_output="""\
    A comprehensive specifications document with a scope, evaluation criteria, delivery schedule, payment milestones and contact person.""",
    agent=agent_planner,

    async_execution=True # Will be executed asynchronously [NEW]
)

task_research = Task(
    description="""\
    1. Conduct in-depth research on the item: {topic}.
    2. Provide the Content Planner with the latest trends, key players, and noteworthy news on the item.
    3. Pprovide additional insights and resources to enhance the specifications document
    4. Include latest developmnents in the research report.""",


    expected_output="""\
    A detailed research report with the latest trends, key players, and noteworthy news on the item.""",

    agent=agent_analyst,
    tools=[tool_websearch],

    async_execution=True # Will be executed asynchronously [NEW]
)

task_write = Task(
    description="""\
    1. Use the specifications document to craft a comprehensive specifcations to purchase {topic} based on the target audience's requirements.
    2. Sections/Subtitles are properly named in an engaging manner.
    3. Ensure the post is structured with an engaging introduction, insightful body, and a summarizing conclusion.
    4. Proofread for grammatical errors and alignment the common style used in tech blogs.
    5. You MUST check with human users to get their feedback on the content, and incorporate the suggestion to revise the content.""",

    expected_output="""
    A well-written specifications "in markdown format, ready for publication, each section should have 2 or 3 paragraphs.""",
    agent=agent_writer,
    # human_input=True, # Remove user input for this task [NEW]

    context=[task_plan, task_research], # Will wait for the output of the two tasks to be completed,
  
)


# <---------------------------------- Creating the Crew ---------------------------------->
crew = Crew(
    agents=[agent_planner, agent_analyst, agent_writer],
    tasks=[task_plan, task_research, task_write],
    verbose=True
)

# <---------------------------------- Running the Crew ---------------------------------->
if form.form_submit_button("Submit"):
    st.toast(f"User Input Submitted - {user_prompt}")
    response = crew.kickoff(inputs={"topic":f"User Input Submitted - {user_prompt}"})
    st.write(response) 
    print(f"User Input is {user_prompt}")