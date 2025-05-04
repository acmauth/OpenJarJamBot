import aiosqlite
from utils.utilities import aprint

database_path: str = "data/database.db"

class DatabaseHandler:
    @staticmethod
    async def check_tables() -> None:
        checkTeamsTableQuery = 'select Name from Teams;'
        checkRequestsTableQuery = 'select UserId from Requests;'

        teamsTableCreationQuery = 'create table Teams (Name varchar(255) not null, Leader int not null, Members varchar(255) default null, primary key (Name));'
        requestsTableQuery = 'create table Requests (UserId int not null, Team varchar(255) not null);'

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
            async with db.execute(teamExistsQuery) as cursor:
                row = await cursor.fetchone()
                if row[0] == 0:
                    await db.execute(registerTeamQuery)
                    await db.commit()

    @staticmethod
    async def transfer_team_leadership(team: str) -> None:
        members = await DatabaseHandler.get_team_total_members(team)
        old_leader = members.pop(0)

        leader = members[0] # new leader
        members.pop(0) #remove him to form the members string
        members.append(old_leader)
        member_string = ','.join(members)

        async with aiosqlite.connect(database_path) as db:
            await db.execute(f'update Teams set Leader={leader}, Members="{member_string}" where Name="{team}";')
            await db.commit()

    @staticmethod
    async def delete_team(team: str) -> None:
        deleteTeamQuery = f'delete from Teams where Name="{team}";'
        deleteRemainingRequestsQuery = f'delete from Requests where Team="{team}";'

        async with aiosqlite.connect(database_path) as db:
            await db.execute(deleteTeamQuery)
            await db.execute(deleteRemainingRequestsQuery)
            await db.commit()

    @staticmethod
    async def get_all_teams() -> dict:
        infoGatheringQuery = 'select Name from Teams;'
        result = dict()

        async with aiosqlite.connect(database_path) as db:
            async with db.execute(infoGatheringQuery) as cursor:
                rows = await cursor.fetchall()

                for row in rows:
                    team: str = row[0]
                    total_members = await DatabaseHandler.get_team_total_members(team)
                    result[team] = total_members

        return result

    @staticmethod
    async def get_team_total_members(team: str) -> list:
        infoGatheringQuery = f'select Leader, Members from Teams where Name="{team}";'
        members = list()

        async with aiosqlite.connect(database_path) as db:
            async with db.execute(infoGatheringQuery) as cursor:
                row = await cursor.fetchone()

                members.append(row[0]) # the leader is always there...

                if row[1] is not None:
                    member_list = row[1].split(",")
                    fixed_list = list()
                    for member in member_list: fixed_list.append(int(member))
                    members.extend(fixed_list)

        return members

    @staticmethod
    async def is_user_on_any_team(user_id: int) -> bool:
        checkQuery = f'select Leader, Members from Teams;'
        result: bool = False

        async with aiosqlite.connect(database_path) as db:
            async with db.execute(checkQuery) as cursor:
                rows = await cursor.fetchall()

                for row in rows:
                    leader, members = row
                    if members is not None: member_list = members.split(",")
                    else: member_list = []

                    if user_id != leader and not str(user_id) in member_list: continue
                    else: result = True; break

        return result

    @staticmethod
    async def get_team_by_member(user_id: int) -> str:
        teams = await DatabaseHandler.get_all_teams()
        result = ''

        for team, members in teams.items():
            if user_id in members:
                result = team
                break

        return result

    @staticmethod
    async def team_exists(team: str) -> bool:
        checkQuery = f'select 1 from Teams where Name="{team}";'
        result: bool = True

        async with aiosqlite.connect(database_path) as db:
            async with db.execute(checkQuery) as cursor:
                row = await cursor.fetchone()
                if row is None: result = False

        return result

    @staticmethod
    async def add_user_to_team(team: str, user_id: int) -> None:
        membersStringQuery = f'select Members from Teams where Name="{team}";'

        async with aiosqlite.connect(database_path) as db:
            cursor = await db.execute(membersStringQuery)
            row = await cursor.fetchone()
            members: str | None = row[0]

            if members is not None:
                member_list = members.split(",")
                member_list.append(str(user_id))

                final_members_string = ','.join(member_list)
                await db.execute(f'update Teams set Members="{final_members_string}" where Name="{team}";')
                await db.commit()
            else:
                await db.execute(f'update Teams set Members="{str(user_id)}" where Name="{team}";')
                await db.commit()

            await cursor.close()

    @staticmethod
    async def remove_member_from_team(team: str, user_id: int) -> bool:
        membersStringQuery = f'select Members from Teams where Name="{team}";'
        result = True

        async with aiosqlite.connect(database_path) as db:
            async with db.execute(membersStringQuery) as cursor:
                row = await cursor.fetchone()
                members_string: str = row[0]

                if members_string is not None:
                    members_list = members_string.split(',')
                    if str(user_id) in members_list:
                        members_list.remove(str(user_id))
                        final_members_string = ','.join(members_list)
                        await db.execute(f'update Teams set Members="{final_members_string}" where Name="{team}";')
                        await db.commit()
                    else: result = False
                else: result = False

        return result

    @staticmethod
    async def create_team_request(team: str, user_id: int) -> int:
        requestExistsQuery = f'select Teams from Requests where UserId={user_id};'
        requestCreationQuery = f'insert into Requests values ({user_id}, "{team}");'


        async with aiosqlite.connect(database_path) as db:
            async with db.execute(requestExistsQuery) as cursor:
                rows = await cursor.fetchone()

                if rows is None:
                    await db.execute(requestCreationQuery)
                    await db.commit()
                else:
                    team_list = []
                    for row in rows: team_list.append(row[0])
                    if not team in team_list:
                        if len(await DatabaseHandler.get_team_total_members(team)) >= 4: return -1 #team is full
                        else:
                            await db.execute(requestCreationQuery)
                            await db.commit()
                    else: return 0 #request already exists

        return 1 #all ended well...

    @staticmethod
    async def dismiss_team_request(team: str, user_id: int) -> None:
        deletionQuery = f'delete from Requests where UserId={user_id} and Team="{team}";'

        async with aiosqlite.connect(database_path) as db:
            await db.execute(deletionQuery)
            await db.commit()

    @staticmethod
    async def get_team_total_requests(team: str) -> list:
        infoGatheringQuery = f'select UserId from Requests where Team="{team}";'
        requests = list()

        async with aiosqlite.connect(database_path) as db:
            async with db.execute(infoGatheringQuery) as cursor:
                rows = await cursor.fetchall()
                await aprint(rows)

                for row in rows:
                    if row is None: break
                    if row[0] is not None: requests.append(row[0])

        return requests

    @staticmethod
    async def request_exists(team: str, user_id: int) -> bool:
        requested_users = await DatabaseHandler.get_team_total_requests(team)
        if user_id in requested_users: return True
        return False