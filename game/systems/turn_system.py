from engine.core.system import system
from engine.core.system import System
from game.components.animation import Animation
from game.components.draggable import Draggable
from game.components.turn import Turn


def next_turn_wrapper(self):
    def next_turn(event):
        self.current_turn = event["next"] or (self.current_turn + 1)
        if self.current_turn > self.last_turn:
            self.current_turn = 0
        self.event_bus.emit("turn_update", {"current": self.current_turn})
    return next_turn


def turn_wrapper(self, entity):
    def turn_function(event):
        if turn := entity.get_component(Turn):
            if turn.next is not None:
                if turn.next == (self.current_turn + 1):
                    if animation := entity.get_component(Animation):
                        animation.skip()
                if turn.next == 0:
                    turn.current = turn.order <= self.current_turn
                else:
                    turn.current = turn.order <= self.current_turn < turn.next
            else:
                turn.current = self.current_turn == turn.order
            if animation := entity.get_component(Animation):
                animation.active = turn.current
            if draggable := entity.get_component(Draggable):
                draggable.active = turn.current
    return turn_function


def turn_animation_wrapper(self, turn, animation):
    def turn_animation(event):
        if animation.target == event["animation"].target:
            self.event_bus.emit("next_turn", {"next": turn.next})
    return turn_animation


@system
class TurnSystem(System):
    current_turn: int = 0
    last_turn: int = 0

    def start(self, entities):
        self.current_turn = 0

        self.event_bus.subscribe("next_turn", self, next_turn_wrapper(self))

        for entity in entities:
            if turn := entity.get_component(Turn):
                if turn.order > self.last_turn:
                    self.last_turn = turn.order
                turn.current = self.current_turn == turn.order
                if animation := entity.get_component(Animation):
                    self.event_bus.subscribe("turn_animation_complete", entity, turn_animation_wrapper(self, turn, animation))
                    animation.active = turn.current
                if draggable := entity.get_component(Draggable):
                    draggable.active = turn.current
                self.event_bus.subscribe("turn_update", entity, turn_wrapper(self, entity))
