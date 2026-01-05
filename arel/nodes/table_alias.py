from arel.nodes.binary import Binary

class TableAlias(Binary):
    @property
    def name(self) -> str:
        return self.right

    @property
    def relation(self) -> any:
        return self.left

    def __getitem__(self, name: str) -> 'Attribute':
        from arel.attributes.attribute import Attribute
        return Attribute(self, name)

    def able_to_type_cast(self) -> bool:
        return self.left.able_to_type_cast()

    def type_cast_for_database(self, name: str, value: any) -> any:
        return self.left.type_cast_for_database(name, value)

    def type_for_attribute(self, name: str) -> any:
        return self.left.type_for_attribute(name)

    def to_cte(self) -> 'Cte':
        from arel.nodes.cte import Cte
        return Cte(self.name, self.relation)

