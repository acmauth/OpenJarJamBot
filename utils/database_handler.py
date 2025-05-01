import aiosqlite
from utils.utilities import aprint

database_path: str = "data/database.db"

class DatabaseHandler:
    @staticmethod
    async def check_tables() -> None:
        checkTeamsTableQuery = 'select Name from Teams;'
        checkRequestsTableQuery = 'select UserId from Requests;'

        teamsTableCreationQuery = 'create table Teams (Name varchar(255) not null, Leader int not null, Members varchar(255) default null, primary key (Name));'
        requestsTableQuery = 'create table Requests (UserId int not null, Teams varchar(255) not null);'

        async with aiosqlite.connect(database_path) as db:
            try: await db.execute(checkTeamsTableQuery)
            except:
                await db.execute(teamsTableCreationQuery)
                await db.commit()
            finally:
                try:
                    await db.execute(checkRequestsTableQuery)
                except:
                    await db.execute(requestsTableQuery)
                    await db.commit()
                finally:
                    await aprint("Tables are properly registered in the database!")

    @staticmethod
    async def create_team(team: str, leader_id: int) -> None:
        teamExistsQuery = f'select case when exists (select Name from Teams where Name="{team}") then true else false end;'
        registerTeamQuery = f'insert into Teams (Name, Leader) values ("{team}", {leader_id})'

        async with aiosqlite.connect(database_path) as db:
            cursor = await db.execute(teamExistsQuery)
            row = await cursor.fetchone()
            if row[0] == 0:
                await db.execute(registerTeamQuery)
                await db.commit()

            await cursor.close()

    @staticmethod
    async def add_member_to_team(team: str, user_id: int) -> int:
        membersStringQuery = f'select Members from Teams where Name="{team}";'

        async with aiosqlite.connect(database_path) as db:
            cursor = await db.execute(membersStringQuery)
            row = await cursor.fetchone()
            members: str | None = row[0]
            await aprint(members) #for dbg

            if members is not None:
                member_list = members.split(",")
                if len(member_list) >= 3: return 1 # Team is full
                else:
                    if str(user_id) in member_list: return 2 # User is already part of the team
                    member_list.append(str(user_id))

                    final_members_string = ','.join(member_list)
                    await db.execute(f'update Teams set Members="{final_members_string}" where Name="{team}"')
                    await db.commit()
            else:
                await db.execute(f'update Teams set Members="{str(user_id)}" where Name="{team}"')
                await db.commit()

            await cursor.close()

        return 0 # No errors