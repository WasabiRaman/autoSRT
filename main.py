from SRT import SRT
from SRT.seat_type import SeatType


if __name__ == '__main__':  # TODO 추후에 카카오톡으로 알림 받게 만들어드림
    # 회원정보 기입
    srt_id = "아이디 입력 (전화번호 OR 이메일)"  # 전화번호 입력시 010-1234-5678형태로 입력해야됨.
    srt_pw = "비밀번호 입력"

    # 목표 좌석 (일반실 우선, 일반실만, 특실 우선, 특실만) -> SeatType 클래스 참고
    # class SeatType(Enum):
    #     GENERAL_FIRST = 1  # 일반실 우선
    #     GENERAL_ONLY = 2  # 일반실만
    #     SPECIAL_FIRST = 3  # 특실 우선
    #     SPECIAL_ONLY = 4  # 특실만
    seat_type = SeatType.GENERAL_ONLY

    target_dep = '부산'  # 출발역
    target_arr = '수서'  # 도착역

    target_date = '20231120'  # yyyymmdd 형태로 입력
    target_time = sorted(['10:30', '10:48', '12:10, 12:40'])  # hh:mm 형태로 입력 (8시간 범위까지만 허용됨)
    target_tickets = 1  # 몇 장 필요한지
    count_print = True  # 몇 트째인지 출력함

    search_time = target_time[0].replace(':', '') + '00'  # hhmmss 형태로 들어가야됨

    success_count = 0
    fail_count = 0

    srt = SRT(srt_id, srt_pw)

    def get_train() -> bool:
        trains = srt.search_train(target_dep, target_arr, target_date, search_time)
        allow_train_list = []

        # 중복 코드 제거하기 귀찮아서 걍 냅둠
        for i in trains:
            string_train = str(i)
            if seat_type != SeatType.GENERAL_ONLY:  # 특실 우선 및 특실만 일때
                if '특실 예약가능' in string_train:
                    for j in target_time:
                        if f'{target_arr}({j}' in string_train:
                            allow_train_list.append(i)

            if seat_type != SeatType.SPECIAL_ONLY:
                if '일반실 예약가능' in string_train:
                    for j in target_time:
                        if f'{target_arr}({j}' in string_train:
                            if i not in allow_train_list:
                                allow_train_list.append(i)
        if len(allow_train_list) > 0:
            reserve = srt.reserve(allow_train_list[0], special_seat=seat_type)  # 가장 우선인거
            print(reserve)
            return True
        else:
            return False

    while success_count != target_tickets:
        status = get_train()
        if status:
            success_count += 1
        else:
            fail_count += 1
            if count_print:
                print(f'{fail_count}트째 못구하고 있음')

    print('SRT 구하기 개쉽노')
