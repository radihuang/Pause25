from pause25.timer import CountdownTimer


class FakeClock:
    def __init__(self) -> None:
        self.now = 100.0

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


def test_timer_completes_and_emits_event_once():
    clock = FakeClock()
    timer = CountdownTimer(duration_seconds=10, clock=clock)

    timer.start()
    clock.advance(10)

    assert timer.remaining_seconds == 0
    assert timer.status == "completed"
    assert timer.consume_completion() is True
    assert timer.consume_completion() is False


def test_pause_preserves_remaining_time():
    clock = FakeClock()
    timer = CountdownTimer(duration_seconds=10, clock=clock)

    timer.start()
    clock.advance(3)
    timer.pause()
    clock.advance(100)

    assert timer.status == "paused"
    assert timer.remaining_seconds == 7

    timer.start()
    clock.advance(7)
    assert timer.consume_completion() is True


def test_reset_clears_pending_completion():
    clock = FakeClock()
    timer = CountdownTimer(duration_seconds=5, clock=clock)
    timer.start()
    clock.advance(5)
    assert timer.status == "completed"

    timer.reset()

    assert timer.status == "idle"
    assert timer.remaining_seconds == 5
    assert timer.consume_completion() is False
