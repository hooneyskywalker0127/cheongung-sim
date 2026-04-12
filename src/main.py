import pygame
import random
from threat import BallisticMissile, CruiseMissile, Drone
from radar import Radar
from engagement import Engagement
from judgement import HitJudgement
from metrics import Metrics
from visualizer import Visualizer, ResultGraph, show_intro


def spawn_threat():
    t = random.choice(["ballistic", "cruise", "drone"])
    direction = random.choice(["right", "top", "bottom"])

    if direction == "right":
        x, y = 780, random.randint(100, 500)
        vx, vy_base = random.uniform(-1.2, -0.8), 0
    elif direction == "top":
        x, y = random.randint(100, 700), 10
        vx, vy_base = 0, random.uniform(0.8, 1.2)
    else:  # bottom
        x, y = random.randint(100, 700), 590
        vx, vy_base = 0, random.uniform(-1.2, -0.8)

    if t == "ballistic":
        speed = random.uniform(150, 180)
        return BallisticMissile(location=(x, y), velocity=(vx * speed, vy_base * speed + random.uniform(-40, -20)), power=150)
    elif t == "cruise":
        speed = random.uniform(80, 120)
        return CruiseMissile(location=(x, y), velocity=(vx * speed, vy_base * speed), power=80)
    else:
        speed = random.uniform(40, 70)
        return Drone(location=(x, y), velocity=(vx * speed + random.uniform(-10, 10), vy_base * speed + random.uniform(-15, 15)), power=30)


def spawn_salvo():
    """포화공격 — 위협 5~8개 동시 생성"""
    count = random.randint(5, 8)
    return [spawn_threat() for _ in range(count)]


def main():
    # 초기화
    radar = Radar(detection_range=600, radar_x=400, radar_y=300)
    engagement = Engagement(radar=radar, remaining_missiles=20)
    judgement = HitJudgement(target_x=400, target_y=300)
    metrics = Metrics()

    # 초기 위협 생성
    threats = [spawn_threat() for _ in range(4)]

    # pygame 초기화
    target_hp = 1000
    visualizer = Visualizer(threats, engagement.missiles, radar, target_hp, engagement)
    clock = pygame.time.Clock()

    # 인트로
    show_intro(visualizer.screen, visualizer.font_large, visualizer.font)

    spawn_timer = 0
    spawn_interval = 4.0
    salvo_timer = 0
    salvo_interval = 15.0
    reload_timer = 0
    reload_interval = 10.0  # 10초마다 재장전
    reload_amount = 4       # 한 번에 4발 충전
    max_missiles = 20
    battle_duration = 60.0
    elapsed = 0

    running = True
    while running:
        dt = clock.tick(60) / 1000

        running = visualizer.event()

        # 위협 위치 업데이트
        for threat in threats:
            threat.location_update(dt)

        # 레이더 스캔
        detected = radar.scan(threats)

        # 우선순위 → 요격
        if detected:
            prioritized = engagement.assign_priority(detected)
            engagement.intercept(prioritized, dt)

        # 미사일 업데이트
        engagement.update_missiles(dt)

        # 충돌 판정 — 요격 성공
        for missile in engagement.missiles[:]:
            for threat in threats[:]:
                if judgement.check_intercept(missile, threat):
                    metrics.record_success(threat.type)
                    metrics.record_used_missile()
                    visualizer.add_explosion(threat.x, threat.y)
                    engagement.missiles.remove(missile)
                    threats.remove(threat)
                    break

        # 충돌 판정 — 피격 (HP 데미지)
        for threat in threats[:]:
            if judgement.check_hit(threat):
                target_hp -= threat.power
                visualizer.target_hp = target_hp
                metrics.record_hit(threat.type)
                metrics.record_fail(threat.type)
                threats.remove(threat)

        # 화면 밖 위협 제거
        for threat in threats[:]:
            if threat.x < 0 or threat.x > 800 or threat.y < 0 or threat.y > 600:
                threats.remove(threat)

        # 화면 밖 미사일 제거 + 타겟 사라진 미사일 제거
        active_threat_ids = {id(t) for t in threats}
        for missile in engagement.missiles[:]:
            if missile.x < 0 or missile.x > 800 or missile.y < 0 or missile.y > 600:
                engagement.missiles.remove(missile)
            elif id(missile.threat) not in active_threat_ids:
                engagement.missiles.remove(missile)

        # 새 위협 스폰
        spawn_timer += dt
        if spawn_timer >= spawn_interval:
            threats.append(spawn_threat())
            spawn_timer = 0

        # 포화공격
        salvo_timer += dt
        if salvo_timer >= salvo_interval:
            threats.extend(spawn_salvo())
            salvo_timer = 0

        # 재장전
        reload_timer += dt
        visualizer.reload_timer = reload_timer
        if reload_timer >= reload_interval:
            engagement.remaining_missiles = min(engagement.remaining_missiles + reload_amount, max_missiles)
            reload_timer = 0

        # 시간 기록
        metrics.record_battle_time(dt)
        elapsed += dt

        # 렌더링
        visualizer.rendering()
        visualizer.status_update()
        pygame.display.flip()

        # HP 0 또는 60초 후 종료
        if target_hp <= 0 or elapsed >= battle_duration:
            running = False

    pygame.quit()
    metrics.save_csv()

    graph = ResultGraph(metrics)
    graph.draw_graph()


if __name__ == "__main__":
    main()
