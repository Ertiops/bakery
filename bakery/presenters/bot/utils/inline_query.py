from aiogram.types import InlineKeyboardButton
from aiogram_dialog.api.internal.widgets import RawKeyboard
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd.base import Keyboard
from aiogram_dialog.widgets.text import Text


class SwitchInlineQueryCurentChat(Keyboard):
    def __init__(
        self,
        text: Text,
        switch_inline_query_current_chat: Text,
        id: str | None = None,
        when: WhenCondition = None,
    ):
        super().__init__(id=id, when=when)
        self.text = text
        self.switch_inline_query_current_chat = switch_inline_query_current_chat

    async def _render_keyboard(
        self,
        data: dict,
        manager: DialogManager,
    ) -> RawKeyboard:
        return [
            [
                InlineKeyboardButton(
                    text=await self.text.render_text(data, manager),
                    switch_inline_query_current_chat=(
                        await self.switch_inline_query_current_chat.render_text(
                            data,
                            manager,
                        )
                    ),
                ),
            ],
        ]
