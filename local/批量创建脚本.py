from project_creation import create_project
from task_creation import create_task


token_list=["wkyo!vmv9@*o0g8wemo?sbjqbs4mg@"]
projectnum=3
tasknum=3


for token in token_list:
    for i in range(projectnum):
        project_name="project%d"%i
        responce = create_project(token, project_name)
        if responce["result"]==True:
            print(f"create {project_name}")
        
        for j in range(tasknum):
                task_name = "project%d task%d"%(i,j)
                level_required = "1"
                result = create_task(token, project_name, task_name, level_required)
                if responce["result"]==True:
                    print(f"create {task_name}")


