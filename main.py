from src.core.game import Game
from src.graphics.renderer import Renderer
from src.graphics.gui_player import GuiPlayer
from src.agents import GuiPacman, AiGhost


def main() -> None:
    renderer = Renderer()
    player = GuiPlayer(renderer=renderer)
    game = Game(
        player=player,
        pacman_agent=GuiPacman(),
        ghost_agents=[AiGhost()],
    )
    game.add_on_state_changed_callback(renderer.render_state)
    game.run()


if __name__ == '__main__':
    main()
