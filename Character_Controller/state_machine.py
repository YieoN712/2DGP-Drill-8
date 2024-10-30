from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT

def start_event(e):
    return e[0] == 'START'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


# 이벤트 체크 함수
# 상태 이벤트 e = (종류, 실제값) 튜플로 정의
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

# time_out = lamda e : e[0] == 'TIME_OUT' 이렇게도 사용 가능


class StateMachine:
    def __init__(self, obj):
        self.obj = obj  # 어떤 객체를 위한 state_machine인지 알려줌. obj = boy.self
        # 상태 이벤트를 보관할 리스트
        self.event_q = []

    def start(self, state):
        self.cur_state = state  # 시작 상태를 받아서 현재 상태로 정의
        self.cur_state.enter(self.obj, ('START', 0))
        print(f'Enter into {state}')

    def add_event(self, e):
        print(f'    DEBUG: New event {e} added to event Que')
        self.event_q.append(e)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def update(self):
        self.cur_state.do(self.obj) # Idle.do()
        # 이벤트 확인
        if self.event_q:    # list에 맴버가 있으면 true
            e = self.event_q.pop(0)
            # 현재 상태와 현재 발생한 이벤트에 따라 다음 상태 결정
            # 상태 변환 테이블 사용(딕셔너리)
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):
                    print(f'Exit from {self.cur_state}')
                    self.cur_state.exit(self.obj, e)
                    self.cur_state = next_state
                    print(f'Enter into {self.cur_state}')
                    self.cur_state.enter(self.obj, e)
                    return  # 상태 변환 끝
            # 이 시점으로 오면 전환 처리가 안 됬다는 의미
            print(f'        WARING: {e} not handle at state {self.cur_state}')

    def draw(self):
        self.cur_state.draw(self.obj)
