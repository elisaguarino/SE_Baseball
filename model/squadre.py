from dataclasses import dataclass
@dataclass
class Squadre:
    id:int
    name:str
    team_code:str
    salaryTot:float

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.salaryTot > other.salaryTot