import pandas as pd

class NameValidator:
    def __set_name__(self, owner, name):
        self.name = name
        
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]
    
    def __set__(self, instance, value):
        if not value.isalpha():
            raise ValueError("Имя должно содержать только буквы.")
        if not value.istitle():
            raise ValueError("Имя должно начинаться с заглавной буквы.")
        instance.__dict__[self.name] = value


class Student:
    subjects = None 

    def __init__(self, name, subjects_file):
        self.name = name
        self._load_subjects(subjects_file)
        self._init_subjects()

    def _load_subjects(self, subjects_file):
        df = pd.read_csv(subjects_file)
        self.subjects = df['Предмет'].tolist()

    def _init_subjects(self):
        self._subject_grades = {subject: [] for subject in self.subjects}
        self._subject_test_results = {subject: [] for subject in self.subjects}

    def add_grade(self, subject, grade):
        if subject not in self.subjects:
            raise ValueError(f"Недопустимый предмет: {subject}. Разрешенные предметы: {', '.join(self.subjects)}")
        if grade < 2 or grade > 5:
            raise ValueError("Недопустимая оценка. Оценка должна быть от 2 до 5.")
        self._subject_grades[subject].append(grade)

    def add_test_result(self, subject, result):
        if subject not in self.subjects:
            raise ValueError(f"Недопустимый предмет: {subject}. Разрешенные предметы: {', '.join(self.subjects)}")
        if result < 0 or result > 100:
            raise ValueError("Недопустимый результат теста. Результат должен быть от 0 до 100.")
        self._subject_test_results[subject].append(result)

    def _calculate_avg(self, values):
        return sum(values) / len(values) if values else 0

    def get_subject_avg_grade(self, subject):
        grades = self._subject_grades.get(subject, [])
        return self._calculate_avg(grades)

    def get_subject_avg_test_result(self, subject):
        results = self._subject_test_results.get(subject, [])
        return self._calculate_avg(results)

    def get_overall_avg_grade(self):
        all_grades = [grade for grades in self._subject_grades.values() for grade in grades]
        return self._calculate_avg(all_grades)

    def get_overall_avg_test_result(self):
        all_results = [result for results in self._subject_test_results.values() for result in results]
        return self._calculate_avg(all_results)



if __name__ == "__main__":
    try:
        student = Student("Иван Иванов", "subjects.csv")
        print("Имя студента:", student.name)

       
        student.add_grade("Математика", 4)
        student.add_grade("Математика", 5)
        student.add_test_result("Математика", 80)
        student.add_test_result("Математика", 90)

        student.add_grade("Наука", 3)
        student.add_test_result("Наука", 70)

      
        print("Средний балл по Математике:", student.get_subject_avg_grade("Математика"))
        print("Средний результат тестов по Математике:", student.get_subject_avg_test_result("Математика"))

        print("Средний балл по Науке:", student.get_subject_avg_grade("Наука"))
        print("Средний результат тестов по Науке:", student.get_subject_avg_test_result("Наука"))

        print("Общий средний балл:", student.get_overall_avg_grade())
        print("Общий средний результат тестов:", student.get_overall_avg_test_result())

        student.add_grade("История", 4)

    except ValueError as e:
        print("Ошибка:", e)
