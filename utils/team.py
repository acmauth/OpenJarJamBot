class Team:
    def __init__(self, team_name: str, leader_id: int):
        self.name = team_name
        self.leader = leader_id
        self.members = list()

    @property
    def name(self) -> str:
        return self.name

    @property
    def leader(self) -> int:
        return self.leader

    @property
    def members(self) -> list:
        return self.members

    @name.setter
    def name(self, team_name: str) -> None:
        self.name = team_name

    @leader.setter
    def leader(self, user_id: int) -> None:
        self.leader = user_id

    @members.setter
    def members(self, members_list: list) -> None:
        self.members = members_list

    def add_member(self, user_id: int) -> bool:
        if len(self.members) >= 3: return False
        self.members.append(user_id)
        return True

    def remove_member(self, user_id: int) -> bool:
        if not user_id in self.members: return False
        self.members.remove(user_id)
        return True