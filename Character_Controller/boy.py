from pico2d import *
from state_machine import *


# 상태를 클래스를 통해 정의
class Idle:
    @staticmethod   # @ - 데코레이터, 함수의 기능을 변형한다. 즉, 뒤에 오는 함수를 staticmethod로 바꾼다.
    def enter(boy, e):    # 객체를 찍어 놓는 것이 아닌 class라는 이름으로 안에 있는 함수를 묶어 놓는다.
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.face_dir = 1

        boy.dir = 0
        boy.frame = 0
        # 현재 시작 저장
        boy.start_time = get_time()
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)


class Sleep:
    @staticmethod
    def enter(boy, e):
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_composite_draw(
                boy.frame * 100, 300, 100, 100,
                3.141592 / 2, # 90도 회전
                '',  # 상하좌우 반전 X
                boy.x - 25, boy.y - 25, 100, 100
            )
        else:
            boy.image.clip_composite_draw(
                boy.frame * 100, 200, 100, 100,
                -(3.141592 / 2),  # -90도 회전
                '',  # 상하좌우 반전 X
                boy.x + 25, boy.y - 25, 100, 100
            )


class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.dir, boy.face_dir, boy.action = 1, 1, 1
        elif left_down(e) or right_up(e):
            boy.dir, boy.face_dir, boy.action = -1, -1, 0

        boy.frame = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.x += boy.dir * 5
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)


class AutoRun:
    @staticmethod
    def enter(boy, e):
        if a_down(e):
            boy.start_time = get_time() # 현재 시각 저장
            boy.speed = 1.0
            boy.scale = 1.0
            boy.dir = 1         # 초기 값 : 오른쪽 방향

        boy.frame = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time < 5:
            boy.x += boy.speed * boy.dir
            boy.speed += 1
            boy.scale += 0.01

            if boy.x >= 375 or boy.x <= 25:
                boy.dir *= -1

        else:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x + boy.speed, boy.y, int(100 * boy.scale), int(100 * boy.scale))



class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 소년 객체의 state machine 생성
        self.state_machine.start(Idle)      # class 이름 마저도 함수의 인자로 넘길 수 있다. 초기 상태 설정
        self.state_machine.set_transitions(
            {
                Idle : { right_down : Run, left_down : Run, left_up : Run, right_up : Run, a_down : AutoRun, time_out : Sleep },
                Run : { right_down : Idle, left_down : Idle, left_up : Idle, right_up : Idle },
                Sleep : { right_down : Run, left_down : Run, left_up : Run, right_up : Run, space_down : Idle},
                AutoRun : { dir_key_down : Run, time_out : Idle }
            }
        )

    def update(self):
        self.state_machine.update()
        # self.frame = (self.frame + 1) % 8

    def handle_event(self, event):
        # 입력 이벤트, 튜플을 전달
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
