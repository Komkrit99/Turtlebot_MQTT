import sys
import ruamel.yaml
from pathlib import Path

file_org = Path('C:\Users\natek\OneDrive\Desktop\ai_robot\mapfortestweb.yaml')
    
yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True
data = yaml.load(file_org)
yaml.dump(data, sys.stdout)