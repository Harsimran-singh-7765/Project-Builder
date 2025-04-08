from typing import List, Dict

class ProjectInput:
    def __init__(self, idea_title: str, description: str, team_members: List[Dict[str, str]],refined_idea:str):
        """
        A class to hold the structured input for the SDF Project Helper.

        :param idea_title: Title of the project idea.
        :param description: Short description of the project.
        :param team_members: List of dictionaries containing name and enrollment number.
                             Example: [{"name": "Harsimran", "enrollment": "2110999999"}]
        """
        self.idea_title = idea_title
        self.description = description
        self.team_members = team_members
        self.refined_idea = refined_idea

    def __repr__(self): 
        return f"<ProjectInput(title={self.idea_title}, members={len(self.team_members)} students)>"

class QuestionInput:
    def __init__(self, project: ProjectInput, question: str, history: List[Dict[str, str]] = None):
        """
        :param project: Dictionary containing project details (idea, desc, team_members, refined_idea)
        :param question: The new question being asked by the user
        :param history: Optional chat history as list of {"q": question, "a": answer}
        """
        self.project = project
        self.question = question
        self.history = history if history is not None else []

    def __repr__(self):
        return f"<QuestionInput(project={self.project.get('idea', 'No Idea')}, Q='{self.question[:20]}...', history={len(self.history)} items)>"