users（用户）表：   
UserId： 用户的唯一标识符，作为主键。  
Username：   
Password：   
Email：   
Organization：   
 


tokens（令牌）表：  
TokenId： 令牌的唯一标识符，作为主键。  
Token： 令牌的值，用于验证用户的身份。   
Level： 令牌的权限级别  
user_id： 与用户表相关联的外键，指向拥有该令牌的用户。  


user_projects（用户项目）表：  
UserProjectId： 项目的唯一标识符，作为主键。   
ProjectName： 项目名称  
user_id： 与用户表相关联的外键，指向创建或拥有该项目的用户。  


project_tasks（项目任务）表：  
ProjectTaskId： 任务的唯一标识符，作为主键。  
TaskName：   
TaskPath：   
user_project_id： 与用户项目表相关联的外键，指向该任务所属的项目。  
