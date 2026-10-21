import re

from balrog.agents.base import BaseAgent


class CustomAgent(BaseAgent):
    """An agent that generates actions and plans based on observations with a customizable approach."""

    def __init__(self, client_factory, prompt_builder):
        super().__init__(client_factory, prompt_builder)
        self.client = client_factory()
        self.plan = None
        self.memory = None

    def act(self, obs, prev_action=None):
        """Generate the next action and update the plan based on the current observation.

        Args:
            obs (dict): The current observation in the environment.
            prev_action (str, optional): The previous action taken.

        Returns:
            LLMResponse: The response containing the updated plan and selected action.
        """
        if prev_action:
            self.prompt_builder.update_action(prev_action)
        self.prompt_builder.update_observation(obs)

        memory_text = f"Current Memory:\n{self.memory}\n" if self.memory else "You have no memory yet.\n"
        plan_text = f"Current Plan:\n{self.plan}\n" if self.plan else "You have no plan yet.\n"

        planning_instructions = """
Review the current plan and memory above if present. 
Update your own long-term memory, based on current observations and/or inventory changes.
Decide whether to continue with the current plan or make changes.
If you make changes to the plan, provide the updated plan.
Provide the next action you want to take.
Format your answer strictly in the following way, using these exact headers in order:
MEMORY: <your updated summarized long-term memory and/or current inventory>
PLAN: <your updated plan if changed, or "No changes to the plan." if the current plan is good>
ACTION: <your next action>
        """.strip()

        messages = self.prompt_builder.get_prompt()
        if messages and messages[-1].role == "user":
            messages[-1].content += "\n\n" + memory_text + "\n" + plan_text + "\n" + planning_instructions

        response = self.client.generate(messages)

        # Extract the plan and action from the LLM's response
        memory, plan, action = self._extract_plan_and_action(response.completion)

        # Update the internal plan if it has changed
        if plan != "No changes to the plan.":
            self.plan = plan
        if memory is not None:
            if memory.lower() != "none" or memory.lower() != "no changes":
                self.memory = memory

        with open("debug_response.txt", "a") as f:
            if action is None:
                f.write(str(dir(response)) + "\n\n")
                if hasattr(response, "_asdict"):
                    f.write(str(response._asdict()))

        # Save the plan in the response.reasoning field and the action in response.completion
        response = response._replace(reasoning=plan, completion=action)
        return response

    def _extract_plan_and_action(self, response_text):
        """Extract the plan and action from the LLM's response text.

        Args:
            response_text (str): The response text from the LLM.

        Returns:
            tuple: A tuple containing the extracted plan and action.
        """
        memory_match = re.search(r"MEMORY:\s*(.*?)(?=\nTHOUGHT:|\nPLAN:|\nACTION:|\Z)", response_text, re.IGNORECASE | re.DOTALL)
        plan_match = re.search(r"PLAN:\s*(.*?)(?=\nMEMORY:|\nTHOUGHT:|\nACTION:|\Z)", response_text, re.IGNORECASE | re.DOTALL)
        action_match = re.search(r"ACTION:\s*(.*)(?=\nMEMORY:|\nTHOUGHT:|\nPLAN:|\Z)", response_text, re.IGNORECASE | re.DOTALL)

        memory = memory_match.group(1).strip() if memory_match else None
        plan = plan_match.group(1).strip() if plan_match else "No changes to the plan."
        action = action_match.group(1).strip() if action_match else None

        return memory, plan, action
