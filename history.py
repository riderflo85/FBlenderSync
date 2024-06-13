from enum import Enum
from datetime import datetime
from typing import List, Dict, Any

from bpy.props import CollectionProperty
from bpy import types, context

from .mixins import FContextMixin

bpy_context = context


class OperatorHistoryType(Enum):
    UNFOLDING = "unfolding_folder"
    FOLDING = "folding_folder"


class MenuOperatorHistory(FContextMixin):
    """Create a history for all menu operator like expand a folder to show
    childrens.
    """

    op_type: OperatorHistoryType
    op_datetime: datetime
    item_id: str
    item_index: int
    is_folder: bool
    childrens: List[Dict[str, Any]] # [{"name": Toto, "data": Item object},]
    # menu_data: CollectionProperty

    def __init__(self,
        type: OperatorHistoryType,
        item_id: str,
        item_index: int,
        childs: List[Dict[str, Any]],
        collection: CollectionProperty,
        timestamp: datetime=datetime.now(),
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
        collection = self.collection
        for child in self.childrens:
            # La collection subit une mutation et les index ne sont donc plus correct.
            child_index = collection.find(child["name"])
            collection.remove(child_index)
        self._set_items_index(collection)
    
    def _reset_items_in_bpy_context(self):
        pass

    def exec_callback(self):
        if self.op_type == OperatorHistoryType.FOLDING:
            self._remove_items_in_bpy_context()
        elif self.op_type == OperatorHistoryType.UNFOLDING:
            self._reset_items_in_bpy_context()


def register():
    # utils.register_class(MenuOperatorHistory)
    
    types.Scene.menu_history = []


def unregister():
    # utils.unregister_class(MenuOperatorHistory)
    
    del types.Scene.menu_history