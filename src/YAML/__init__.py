from pydantic import BaseModel,Field
import yaml
class LoadYaml(BaseModel):
    url:str = Field(title="Path", description="Path of your config.yaml File",default="config.yaml")

    def Load_Yaml(self):
        with open(self.url,"r") as file:
            config = yaml.safe_load(file)
        return config