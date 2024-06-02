数据库结构
1. 用户表（Users）  此表用于存储用户的基本信息。
用户ID (UserId) - 主键，唯一标识用户。
用户名 (Username) - 唯一
密码 (Password) 
邮箱 (Email) 
组织 (Organization) 

2. 令牌表（Tokens）  存储关于令牌的信息，每个令牌与一个用户关联。
令牌ID (TokenId) - 主键，唯一标识令牌。
令牌 (Token) 
等级 (Level) 
用户ID (UserId) - 外键，关联到用户表的用户ID。

3. 项目表（Projects）  存储用户的项目信息，每个项目与一个用户关联。
项目ID (ProjectId) - 主键，唯一标识项目。
项目名称 (ProjectName) 
用户ID (UserId) - 外键，关联到用户表的用户ID。


4. 任务表（Tasks）  存储在特定项目下的任务信息。

任务ID (TaskId) - 主键，唯一标识任务。
任务描述 (Description) 
项目ID (ProjectId) - 外键，关联到项目表的项目ID。


+--------+        +--------+        +---------+        +-------+
| Users  |        | Tokens |        | Projects|        | Tasks |
+--------+        +--------+        +---------+        +-------+
| UserId |<----+  | TokenId|        | ProjectId|<----+  | TaskId|
| Username|    |  | Token  |        | ProjectName|    |  | Description|
| Password|    |  | Level  |        | UserId    |----+  | ProjectId   |
| Email   |    |  | UserId |----+   +-----------+       +------------+
| Organization| |  +--------+   |                         
+--------+    |                  |                         
              +------------------+
