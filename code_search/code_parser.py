



import ast
from dataclasses import dataclass
import os


@dataclass
class CodeChunk :
 content : str
 function_name : str 
 line_number : int 
 file_path : str

def extract_functions(file_path: str) ->list[CodeChunk]:
 
 with open(file_path,'r', encoding='utf-8') as f:
  source=  f.read()

 try:
    tree=ast.parse(source) 
 except SyntaxError:
   return[]

 chunks=[]
 lines= source.splitlines()

 for node in ast.walk(tree):
   if isinstance(node,ast.FunctionDef,ast.AsyncFunctionDef):
     start= node.lineno - 1
     end = node.end_lineno
     function_source='\n'.join(lines[start:end])

     chunks.append(CodeChunk(content=function_source,
                             function_name=node.name,
                             file_path=file_path,
                             line_number=node.lineno))
 return chunks
   

def index_directory(directory:str) ->list[CodeChunk]:
  
  all_chunks=[]

  for root, dirs, files in os.walk(directory):
    dirs[:]= [d for d in dirs if d not in  ['venv', '__pycache__', '.git', 'node_modules']]
    for file in files:
      if file.endswith('.py'):
        full_path=os.path.join(root,file)
        chunks= extract_functions(full_path)
        all_chunks.extend(chunks)

  return all_chunks
  



