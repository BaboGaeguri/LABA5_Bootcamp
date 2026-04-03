import smach
import time

# 1. IDLE (대기 상태)
class Idle(smach.State):
    def __init__(self):
        # person_detected라는 결과(outcome)를 뱉고 다음으로 넘어갑니다.
        smach.State.__init__(self, outcomes=['person_detected'])

    def execute(self, userdata):
        print("\n[INFO] State: IDLE - Waiting for audience...")
        time.sleep(2) # 2초 대기 (MediaPipe가 사람을 찾는 과정이라고 상상해 보세요)
        print("[INFO] Audience detected! Moving to TALKING.")
        return 'person_detected'

# 2. TALKING (대화 상태)
class Talking(smach.State):
    def __init__(self):
        # 물건을 집어야 하면 need_manipulation, 단순 대화면 done_talking을 뱉습니다.
        smach.State.__init__(self, outcomes=['need_manipulation', 'done_talking'])

    def execute(self, userdata):
        print("\n[INFO] State: TALKING - Greeting and processing LLM intent...")
        time.sleep(2) # TTS로 "안녕하세요" 인사하고 LLM JSON을 기다리는 시간
        
        # LLM이 JSON으로 {"intent": "manipulate_object"}를 줬다고 가정해 봅시다.
        simulated_intent = "manipulate_object" 
        
        if simulated_intent == "manipulate_object":
            print("[INFO] Intent is manipulation. Moving to MANIPULATING.")
            return 'need_manipulation'
        else:
            print("[INFO] Conversation ended. Returning to IDLE.")
            return 'done_talking'

# 3. MANIPULATING (조작 상태 - SmolVLA 출격)
class Manipulating(smach.State):
    def __init__(self):
        # 조작이 끝나면 task_completed를 뱉습니다.
        smach.State.__init__(self, outcomes=['task_completed'])

    def execute(self, userdata):
        print("\n[INFO] State: MANIPULATING - Running SmolVLA and controlling SO-ARM...")
        time.sleep(3) # GPU 100% 써서 스타벅스 컵을 집어 올리는 시간
        print("[INFO] Target object picked successfully! Returning to IDLE.")
        return 'task_completed'

def main():
    # 전체 상태를 담을 가장 큰 바구니(StateMachine)를 만듭니다.
    sm = smach.StateMachine(outcomes=['EMERGENCY_STOP'])

    with sm:
        # 바구니 안에 각 상태(State)를 넣고, 화살표(transitions)를 연결해 줍니다.
        smach.StateMachine.add('IDLE', Idle(), 
                               transitions={'person_detected':'TALKING'})
                               
        smach.StateMachine.add('TALKING', Talking(), 
                               transitions={'need_manipulation':'MANIPULATING', 
                                            'done_talking':'IDLE'})
                                            
        smach.StateMachine.add('MANIPULATING', Manipulating(), 
                               transitions={'task_completed':'IDLE'})

    # 상태 머신 실행!
    print("[INFO] Starting HYlion State Machine...")
    sm.execute()
    print("\n[INFO] State Machine process finished.")

if __name__ == '__main__':
    main()