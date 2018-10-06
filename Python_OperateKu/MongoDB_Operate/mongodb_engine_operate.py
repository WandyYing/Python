#coding:utf-8
from mongoengine import connect, Document, EmbeddedDocument, DynamicDocument, StringField, IntField,\
FloatField, ListField, EmbeddedDocumentField

connect('students')

SEX_CHICES = (
    ('male','男'),
    ('female','女')
)

class Grade(EmbeddedDocument):
    ''' 成绩 '''
    name = StringField(required=True)
    score = FloatField(required=True)

# class Student(Document):
class Student(DynamicDocument):
    '''学生'''
    name = StringField(max_length=32, required=True)
    age = IntField(required=True)
    sex = StringField(choices=SEX_CHICES, required=True)
    grade = FloatField()
    address = StringField()
    grades = ListField(EmbeddedDocumentField(Grade))

    meta = {
        'collection': 'students',
        # 排序功能，按照分数倒序
        'ordering':['-grade']
    }


class TestMongoEngine(object):
    def add_one(self):
        '''添加一条数据到数据库'''
        yuwen = Grade(
            name = '语文',
            score = 90)
        shuxue = Grade(
            name = '数学',
            score = 100)
        stu_obj = Student(
            name = '张三丰',
            age = 15,
            grades = [yuwen, shuxue],
            sex = 'male'
        )
        # 直接添加remark字段是无法添加成功的，需要引入动态添加字段的方法DynamicDocument　　　　　
        stu_obj.remark = 'remark'
        stu_obj.save()
        return stu_obj

    def get_one(self):
        ''' 获取单条数据 '''
        return Student.objects.first()

    def get_more(self):
        ''' 获取多条数据 '''
        # return Student.objects
        return Student.objects.all()

    def get_one_from_oid(self, oid):
        ''' 查询指定id的数据 '''
        return Student.objects.filter(id=oid).first()

    def update(self):
        ''' 修改数据 '''
        # 修改一条数据
        # res = Student.objects.filter(sex='male').update_one(inc__age=1)
        # return res

        # 修改多条数据
        res = Student.objects.filter(sex = 'male').update(inc__age=10)
        return res

    def delete(self):
        ''' 删除数据 '''
        # 删除一条数据
        # res = Student.objects.filter(sex='male').first().delete()
        # return res

        # 删除多条数据
        res = Student.objects.filter(gender='male').delete()
        

def main():
    en = TestMongoEngine()
    # en.add_one()

    # res = en.get_one()
    # print(res.name)

    # rows = en.get_more()
    # for row in rows:
    #     print(row.name)

    # res = en.get_one_from_oid('5a9df2e48a86b467d4a2c44f')
    # print(res.name)

    # res = en.update()
    # print(res)

    res = en.delete()
    print(res)

if __name__ == "__main__":
    main()
