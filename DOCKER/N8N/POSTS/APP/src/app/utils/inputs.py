from app.tools.googleapi import GetRandomPostTool
from datetime import datetime

class Inputs:

    def __init__(self, random_post_tool=GetRandomPostTool()):
        self.random_post_tool = random_post_tool._run()
        
    
    def get_radom_inputs(self):

        inputs = {
            'Topic': self.random_post_tool[1]['Topic'],
            'Description': self.random_post_tool[1]['Description'], 
            'Prompt_image': self.random_post_tool[1]['Prompt_image'], 
            'Voice': self.random_post_tool[1]['Voice'],
            'Audience': self.random_post_tool[1]['Audience'], 
            'Platform': self.random_post_tool[1]['Platform'], 
            'Current_year': str(datetime.now().year)
        }
        return inputs