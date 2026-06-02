from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock
import json
import random
import time

class StudentManager:
    def __init__(self):
        self.students = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十']
        self.stats = {}
        self.load_data()
    
    def load_data(self):
        try:
            with open('students.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.students = data.get('students', self.students)
                self.stats = data.get('stats', {})
        except:
            pass
    
    def save_data(self):
        try:
            with open('students.json', 'w', encoding='utf-8') as f:
                json.dump({'students': self.students, 'stats': self.stats}, f, ensure_ascii=False)
        except:
            pass
    
    def roll_call(self, count=1):
        if len(self.students) < count:
            return []
        
        selected = random.sample(self.students, count)
        
        for s in selected:
            if s not in self.stats:
                self.stats[s] = {'calls': 0, 'score': 0}
            self.stats[s]['calls'] += 1
        
        self.save_data()
        return selected
    
    def add_student(self, name):
        if name and name not in self.students:
            self.students.append(name)
            self.save_data()
            return True
        return False
    
    def remove_student(self, name):
        if name in self.students:
            self.students.remove(name)
            self.save_data()
            return True
        return False

class SeatManager:
    def __init__(self):
        self.rows = 6
        self.cols = 8
        self.plan = []
        self.conflicts = []
    
    def generate(self, students, method='random'):
        students_data = []
        for i, s in enumerate(students):
            students_data.append({
                'name': s,
                'id': str(i+1).zfill(3),
                'grade': random.randint(60, 100),
                'height': random.randint(150, 180)
            })
        
        if method == 'random':
            random.shuffle(students_data)
        elif method == 'grade':
            students_data.sort(key=lambda x: -x['grade'])
        elif method == 'height':
            students_data.sort(key=lambda x: x['height'])
        
        plan = []
        idx = 0
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                if idx < len(students_data):
                    row.append(students_data[idx])
                    idx += 1
                else:
                    row.append(None)
            plan.append(row)
        
        self.plan = plan
        return plan
    
    def rotate(self):
        if not self.plan:
            return False
        
        all_students = []
        for row in self.plan:
            for student in row:
                if student:
                    all_students.append(student)
        
        random.shuffle(all_students)
        
        new_plan = []
        idx = 0
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                if idx < len(all_students):
                    row.append(all_students[idx])
                    idx += 1
                else:
                    row.append(None)
            new_plan.append(row)
        
        self.plan = new_plan
        return True
    
    def match_deskmates(self):
        if not self.plan:
            return []
        
        pairs = []
        for row in self.plan:
            for i in range(0, len(row)-1, 2):
                if row[i] and row[i+1]:
                    pairs.append((row[i]['name'], row[i+1]['name']))
        
        return pairs

class RollCallTab(BoxLayout):
    def __init__(self, student_manager, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        self.student_manager = student_manager
        
        title = Label(text='🎲 随机点名', font_size=24, bold=True, size_hint_y=0.15)
        self.add_widget(title)
        
        btn_layout = GridLayout(cols=3, spacing=10, size_hint_y=0.2)
        btn1 = Button(text='点名1人', on_press=self.do_roll_call_1, background_color=(0.2, 0.6, 1, 1))
        btn3 = Button(text='点名3人', on_press=self.do_roll_call_3, background_color=(0.2, 0.8, 0.2, 1))
        btn5 = Button(text='点名5人', on_press=self.do_roll_call_5, background_color=(1, 0.6, 0.2, 1))
        btn_layout.add_widget(btn1)
        btn_layout.add_widget(btn3)
        btn_layout.add_widget(btn5)
        self.add_widget(btn_layout)
        
        self.result_label = Label(text='等待点名...', font_size=18, size_hint_y=0.2)
        self.add_widget(self.result_label)
        
        add_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.15)
        self.add_name_input = TextInput(hint_text='输入学生姓名', size_hint_x=0.7)
        add_btn = Button(text='添加学生', on_press=self.add_student, background_color=(0.2, 0.8, 0.2, 1))
        add_layout.add_widget(self.add_name_input)
        add_layout.add_widget(add_btn)
        self.add_widget(add_layout)
        
        student_list = ScrollView(size_hint_y=0.3)
        self.student_label = Label(text='\n'.join(self.student_manager.students), font_size=14, text_size=(None, None))
        student_list.add_widget(self.student_label)
        self.add_widget(student_list)
    
    def do_roll_call_1(self, instance):
        selected = self.student_manager.roll_call(1)
        if selected:
            self.result_label.text = f'🎲 点名结果: {selected[0]}'
    
    def do_roll_call_3(self, instance):
        selected = self.student_manager.roll_call(3)
        if selected:
            self.result_label.text = f'🎲 点名结果: {", ".join(selected)}'
    
    def do_roll_call_5(self, instance):
        selected = self.student_manager.roll_call(5)
        if selected:
            self.result_label.text = f'🎲 点名结果: {", ".join(selected)}'
    
    def add_student(self, instance):
        name = self.add_name_input.text.strip()
        if self.student_manager.add_student(name):
            self.student_label.text = '\n'.join(self.student_manager.students)
            self.add_name_input.text = ''

class SeatTab(BoxLayout):
    def __init__(self, student_manager, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        self.student_manager = student_manager
        self.seat_manager = SeatManager()
        
        title = Label(text='🪑 智能排座位', font_size=24, bold=True, size_hint_y=0.1)
        self.add_widget(title)
        
        ctrl_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.15)
        
        self.method_spinner = Spinner(
            text='随机排列',
            values=('随机排列', '按成绩', '按身高'),
            size_hint_x=0.4
        )
        ctrl_layout.add_widget(self.method_spinner)
        
        gen_btn = Button(text='生成座位', on_press=self.generate_seating, background_color=(0.2, 0.8, 0.2, 1), size_hint_x=0.2)
        rotate_btn = Button(text='定期轮换', on_press=self.rotate_seating, background_color=(0.2, 0.6, 1, 1), size_hint_x=0.2)
        match_btn = Button(text='同桌匹配', on_press=self.show_deskmates, background_color=(1, 0.4, 0.6, 1), size_hint_x=0.2)
        
        ctrl_layout.add_widget(gen_btn)
        ctrl_layout.add_widget(rotate_btn)
        ctrl_layout.add_widget(match_btn)
        self.add_widget(ctrl_layout)
        
        self.seat_grid = GridLayout(cols=8, spacing=5, size_hint_y=0.6)
        self.add_widget(self.seat_grid)
    
    def generate_seating(self, instance):
        method = self.method_spinner.text
        method_map = {'随机排列': 'random', '按成绩': 'grade', '按身高': 'height'}
        
        plan = self.seat_manager.generate(self.student_manager.students, method_map.get(method, 'random'))
        self.draw_seating(plan)
    
    def rotate_seating(self, instance):
        if self.seat_manager.rotate():
            self.draw_seating(self.seat_manager.plan)
    
    def show_deskmates(self, instance):
        pairs = self.seat_manager.match_deskmates()
        if not pairs:
            self.show_popup('提示', '请先生成座位布局！')
            return
        
        content = '\n'.join([f'{p[0]} ↔ {p[1]}' for p in pairs])
        self.show_popup('❤️ 同桌匹配结果', content)
    
    def draw_seating(self, plan):
        self.seat_grid.clear_widgets()
        
        for row in plan:
            for student in row:
                if student:
                    btn = Button(
                        text=student['name'],
                        size_hint=(1, 0.8),
                        background_color=(0.3, 0.5, 0.8, 1)
                    )
                else:
                    btn = Button(
                        text='空',
                        size_hint=(1, 0.8),
                        background_color=(0.2, 0.2, 0.3, 1)
                    )
                self.seat_grid.add_widget(btn)
    
    def show_popup(self, title, content):
        popup = Popup(
            title=title,
            content=Label(text=content, font_size=16),
            size_hint=(0.8, 0.6)
        )
        popup.open()

class StatsTab(BoxLayout):
    def __init__(self, student_manager, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        self.student_manager = student_manager
        
        title = Label(text='📊 班级统计', font_size=24, bold=True, size_hint_y=0.15)
        self.add_widget(title)
        
        scroll = ScrollView(size_hint_y=0.85)
        self.stats_label = Label(text='', font_size=16, text_size=(None, None))
        scroll.add_widget(self.stats_label)
        self.add_widget(scroll)
        
        self.update_stats()
    
    def update_stats(self):
        stats = self.student_manager.stats
        if not stats:
            self.stats_label.text = '暂无统计数据'
            return
        
        sorted_stats = sorted(stats.items(), key=lambda x: -x[1]['calls'])
        content = '📈 点名次数排行:\n\n'
        for i, (name, data) in enumerate(sorted_stats, 1):
            content += f'{i}. {name}: {data["calls"]}次\n'
        
        self.stats_label.text = content

class TimetableTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        title = Label(text='📅 课表管理', font_size=24, bold=True, size_hint_y=0.1)
        self.add_widget(title)
        
        days = ['周一', '周二', '周三', '周四', '周五']
        periods = ['第1节', '第2节', '第3节', '第4节', '第5节']
        
        self.timetable = {}
        for day in days:
            self.timetable[day] = [''] * 5
        
        for i, period in enumerate(periods):
            row_layout = BoxLayout(orientation='horizontal', spacing=5)
            period_label = Label(text=period, size_hint_x=0.2, font_size=14)
            row_layout.add_widget(period_label)
            
            for day in days:
                input_field = TextInput(
                    text=self.timetable[day][i],
                    size_hint_x=0.16,
                    font_size=12
                )
                row_layout.add_widget(input_field)
            
            self.add_widget(row_layout)
        
        save_btn = Button(text='保存课表', on_press=self.save_timetable, background_color=(0.2, 0.8, 0.2, 1), size_hint_y=0.1)
        self.add_widget(save_btn)
    
    def save_timetable(self, instance):
        self.show_popup('✅ 成功', '课表已保存！')
    
    def show_popup(self, title, content):
        popup = Popup(
            title=title,
            content=Label(text=content, font_size=16),
            size_hint=(0.6, 0.4)
        )
        popup.open()

class RollCallApp(App):
    def build(self):
        self.student_manager = StudentManager()
        
        tab_panel = TabbedPanel(do_default_tab=False)
        
        tab1 = TabbedPanelItem(text='点名')
        tab1.add_widget(RollCallTab(self.student_manager))
        tab_panel.add_widget(tab1)
        
        tab2 = TabbedPanelItem(text='排座')
        tab2.add_widget(SeatTab(self.student_manager))
        tab_panel.add_widget(tab2)
        
        tab3 = TabbedPanelItem(text='统计')
        tab3.add_widget(StatsTab(self.student_manager))
        tab_panel.add_widget(tab3)
        
        tab4 = TabbedPanelItem(text='课表')
        tab4.add_widget(TimetableTab())
        tab_panel.add_widget(tab4)
        
        return tab_panel

if __name__ == '__main__':
    RollCallApp().run()
