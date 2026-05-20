from code_parser import index_directory

chunks =index_directory ('../rag_app')

for chunk in chunks :
    print(f"{'='*50}")
    print(f"Function : {chunk.function_name}")
    print(f"File     : {chunk.file_path}")
    print(f"Line     : {chunk.line_number}")
    print(f"Code     :\n{chunk.content[:200]}")