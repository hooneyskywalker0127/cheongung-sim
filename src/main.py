import pygame
import sys
from threat import BallisticMissile, CruiseMissile, Drone
from radar import Radar
from engagement import Engagement
from judgement import HitJudgement
from metrics import Metrics
from visualizer import Visualizer, ResultGraph


def main():
    # 초기화
    radar = Radar(detection_range=600, radar_x=400, radar_y=300)
    engagement = Engagement(radar=radar, remaining_missiles=20)
    judgement = HitJudgement(target_x=400, target_y=300)
    metrics = Metrics()

    # 위협 생성
    threats = [
        BallisticMissile(location=(750, 500), velocity=(-80, -30), power=100),
        CruiseMissile(location=(780, 300), velocity=(-60, 0), power=50),
        Drone(location=(700, 250), velocity=(-20, -5), power=20),
    ]

    # pygame 초기화
    visualizer = Visualizer(threats, engagement.missiles, radar)
    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(60) / 1000  # 초 단위

        # 종료 이벤트
        running = visualizer.event()

        # 위협 위치 업데이트
        for threat in threats:
            threat.location_update(dt)

        # 레이더 스캔
        detected = radar.scan(threats)

        # 우선순위 → 요격 미사일 발사
        if detected:
            prioritized = engagement.assign_priority(detected)
            engagement.intercept(prioritized)

        # 미사일 위치 업데이트
        engagement.update_missiles(dt)

        # 충돌 판정 — 요격 성공
        for missile in engagement.missiles[:]:
            for threat in threats[:]:
                if judgement.check_intercept(missile, threat):
                    metrics.record_success(threat.type)
                    metrics.record_used_missile()
                    engagement.missiles.remove(missile)
                    threats.remove(threat)
                    break

        # 충돌 판정 — 피격
        for threat in threats[:]:
            if judgement.check_hit(threat):
                metrics.record_hit(threat.type)
                metrics.record_fail(threat.type)
                threats.remove(threat)

        # 전투 시간 기록
        metrics.record_battle_time(dt)

        # 렌더링
        visualizer.rendering()
        visualizer.status_update()

        # 위협 전부 처리되면 종료
        if not threats:
            running = False

    pygame.quit()
    metrics.save_csv()

    graph = ResultGraph(metrics)
    graph.draw_graph()


if __name__ == "__main__":
    main()
