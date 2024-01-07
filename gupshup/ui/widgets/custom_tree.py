from rich.text import TextType
from textual.widgets import (
    TreeControl,
    NodeID,
    TreeNode,
)
from textual.reactive import Reactive
from ...src.utils import CustomNode, Parser


class CustomTree(TreeControl):
    """
    A Tree Control structure for slight modifications
    to be inherited by `HouseTree` and `MemberList`
    """

    has_focus = Reactive(False)

    def __init__(self, name: TextType, data: CustomNode):
        super().__init__(name, data)
        self.root._expanded = True

    def on_focus(self) -> None:
        self.has_focus = True

    def on_blur(self) -> None:
        self.has_focus = False

    async def watch_hover_node(self, hover_node: NodeID) -> None:
        for node in self.nodes.values():
            node.tree.guide_style = (
                Parser().get_data("branch_hover") if node.id == hover_node else "black"
            )
        self.refresh(layout=True)

    def get_node_index(self, parent: TreeNode, name: str) -> int:
        for index, node in enumerate(parent.children):
            if str(node.label) == name:
                return index
        return -1

    async def add_under_root(self, name: str, tag: CustomNode) -> None:
        if name not in (str(child.label) for child in self.root.children):
            await self.root.add(name, tag)
        # self.refresh(layout=True)

    async def add_under_child(self, child: str, name: str, tag: CustomNode) -> None:
        for node in self.root.children:
            if str(node.label) == child:
                if name not in (str(child.label) for child in node.children):
                    await node.add(name, tag)
                    break
        # self.refresh(layout=True)

    def del_under_root(self, name: str):
        index = self.get_node_index(self.root, name)
        if index == -1:
            return

        self.root.children.pop(index)
        self.root.tree.children.pop(index)
        self.refresh()

    def del_under_child(self, parent: str, child: str):
        parent_index = self.get_node_index(self.root, parent)
        parent_node = self.root.children[parent_index]
        child_index = self.get_node_index(parent_node, child)

        parent_node.children.pop(child_index)
        parent_node.tree.children.pop(child_index)
        self.refresh()

    def change_data_parent(self, name: str, param: str, data: str):
        node = self.root.children[self.get_node_index(self.root, name)]
        setattr(node.data, param, data)
        self.refresh()

    def change_data_child(self, parent: str, name: str, param: str, data: str):
        parent_node = self.root.children[self.get_node_index(self.root, parent)]
        node = parent_node.children[self.get_node_index(parent_node, name)]
        setattr(node.data, param, data)
        self.refresh()

    def get_data_parent(self, name: str, param: str):
        node = self.root.children[self.get_node_index(self.root, name)]
        return getattr(node.data, param)

    def get_data_child(self, parent: str, name: str, param: str):
        parent_node = self.root.children[self.get_node_index(self.root, parent)]
        node = parent_node.children[self.get_node_index(parent_node, name)]
        return getattr(node.data, param)

    def change_name_parent(self, name: str, data: str):
        node = self.root.children[self.get_node_index(self.root, name)]
        setattr(node, "label", data)
        self.refresh()

    def change_name_child(self, parent: str, name: str, data: str):
        parent_node = self.root.children[self.get_node_index(self.root, parent)]
        node = parent_node.children[self.get_node_index(parent_node, name)]
        setattr(node, "label", data)
        self.refresh()
