from enum import Enum
from datetime import datetime
from typing import List, Dict, Any

from bpy.props import CollectionProperty
from bpy import types

from .mixins import FContextMixin


class OperatorHistoryType(Enum):
    UNFOLDING = "unfolding_folder"
    FOLDING = "folding_folder"
    REFRESH = "refresh_folder"


class MenuOperatorHistory(FContextMixin):
    """Create a history for all menu operator like expand a folder to show
    childrens.
    """
    def __init__(self,
        type: OperatorHistoryType,
        item_id: str,
        item_index: int,
        childs: List[Dict[str, Any]],
        collection: CollectionProperty,
        timestamp: datetime,
        is_folder: bool=True,
    ) -> None:
        self.op_type = type
        self.op_datetime = timestamp
        self.item_id = item_id
        self.item_index = item_index
        self.is_folder = is_folder
        self.childrens = childs
        self.collection = collection

    def _remove_items_in_bpy_context(self):
        for child in self.childrens:
            # The collection has been mutated and the indexes are no longer correct.
            child_index = self.collection.find(child["name"])
            self.collection.remove(child_index)
        self._set_items_index(self.collection)

    def _reset_items_in_bpy_context(self):
        for index, child in enumerate(self.childrens):
            restore_item = self.collection.add()
            for key, value in child.items():
                if key == "index":
                    continue
                setattr(restore_item, key, value)
            last_index = len(self.collection) - 1
            insert_in = self.item_index + index + 1
            self.collection.move(last_index, insert_in)
        self._set_items_index(self.collection)

    def exec_callback(self):
        if self.op_type in (OperatorHistoryType.FOLDING, OperatorHistoryType.REFRESH):
            self._remove_items_in_bpy_context()
        elif self.op_type == OperatorHistoryType.UNFOLDING:
            self._reset_items_in_bpy_context()


def register():
    types.WindowManager.menu_history = []


def unregister():
    del types.WindowManager.menu_history