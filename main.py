import re
import time

# 메모리 저장소 (간단한 DB 역할)
saved_passwords = []


def analyze_password(password):
    """암호 강도 분석"""
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    score = 0
    feedback = []

    if length >= 12: score += 2
    elif length >= 8: score += 1
    else: feedback.append("- 길이가 너무 짧습니다. (8자 이상 권장)")

    if has_upper: score += 1
    else: feedback.append("- 대문자를 포함하세요.")

    if has_lower: score += 1
    else: feedback.append("- 소문자를 포함하세요.")

    if has_digit: score += 1
    else: feedback.append("- 숫자가 없습니다.")

    if has_special: score += 1
    else: feedback.append("- 특수문자가 없습니다.")

    if re.search(r'(.)\1\1', password):
        feedback.append("- 동일 문자가 3번 이상 반복됩니다.")
        score -= 1

    levels = ["매우 위험", "약함", "보통", "강함", "매우 강함", "보안 완벽"]
    current_level = levels[max(0, min(score, 5))]

    print(f"\n[{password}] 분석 결과")
    print("-" * 40)
    print(f"강도: {current_level}")
    print(f"길이: {length}")

    if feedback:
        print("개선 사항:")
        for f in feedback:
            print(f)
    else:
        print("아주 안전한 암호입니다.")

    print("-" * 40)


def is_duplicate(password):
    """중복 검사"""
    return any(item["password"] == password for item in saved_passwords)


def save_password(site, password):
    """비밀번호 저장"""
    if is_duplicate(password):
        print("⚠ 이미 저장된 비밀번호입니다.")
        return

    saved_passwords.append({
        "site": site,
        "password": password
    })

    print("✅ 저장 완료!")


def show_saved():
    """저장된 목록 출력"""
    if not saved_passwords:
        print("저장된 비밀번호 없음")
        return

    print("\n[저장된 비밀번호 목록]")
    for i, item in enumerate(saved_passwords, 1):
        print(f"{i}. {item['site']} → {item['password']}")
    print("-" * 40)


def auto_delete(password):
    """20초 후 삭제"""
    print("⏳ 20초 후 자동 삭제됩니다 (저장하지 않으면)")
    time.sleep(20)

    if not is_duplicate(password):
        print("🗑 비밀번호가 자동 삭제되었습니다.")
    else:
        print("✔ 저장된 비밀번호는 유지됩니다.")


# -------- 실행 --------
while True:
    print("\n1. 비밀번호 분석")
    print("2. 저장된 목록 보기")
    print("3. 종료")

    choice = input("선택: ")

    if choice == "1":
        pw = input("비밀번호 입력: ")
        analyze_password(pw)

        action = input("저장하시겠습니까? (y/n): ").lower()

        if action == "y":
            site = input("사이트 이름: ")
            save_password(site, pw)
        else:
            auto_delete(pw)

    elif choice == "2":
        show_saved()

    elif choice == "3":
        print("종료합니다.")
        break

    else:
        print("잘못된 입력입니다.")
