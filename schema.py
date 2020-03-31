import graphene

from data import get_student

class Student(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    gpa = graphene.String()


class Query(graphene.ObjectType):
    student = graphene.Field(Student, id=graphene.String())
    
    def resolve_student(self, info, id):
        return get_student(id)


schema = graphene.Schema(query=Query)