"""
Update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- get_member: Should return a member from the self._members list
"""

from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = []

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generate_Id(self):
        generated_Id = self._next_id
        self._next_id += 1
        return generated_Id

    def add_member(self, member):
        new_id = self._generate_Id()
        member["id"] = new_id
        self._members.append(member)
        # fill this method and update the return
        return f"{member} fue agregado a la familia exitosamente con el id {new_id}"

    def delete_member(self, id):
        for index, member in enumerate(self._members):
            if member["id"] == id:
                self._members.pop(index)
                return f"{id} fue eliminado de la familia exitosamente"
        # fill this method and update the return
        return "Miembro no encontrado"

    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member
        return None

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members