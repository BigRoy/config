from avalon import api
from avalon.clarisse import imprint_container

import ix


class ReferenceLoader(api.Loader):
    """Reference content into Clarisse"""
    
    label = "Reference File"
    families = ["*"]
    representations = ["abc", "usd", "usda"]
    order = 0
    
    icon = "code-fork"
    color = "orange"
    
    def load(self, context, name=None, namespace=None, data=None):

        # todo: batch commands!!
        
        filepath = self.fname
    
        # Create the file reference
        scene_context = "project://scene"
        paths = [filepath]

        # Command fails on unicode so we must force it to be strings
        # todo: can we do a better conversion, e.g. f.decode("utf8")
        paths = [str(f) for f in paths]

        node = ix.cmds.CreateFileReference(scene_context, paths)

        # Imprint it with some data so ls() can find this
        # particular loaded content and can return it as a
        # valid container
        imprint_container(
            node,
            name=name,
            namespace=namespace,
            context=context,
            loader=self.__class__.__name__
        )
    
    def update(self, container, representation):
    
        node = container["node"]
        filepath = api.get_representation_path(representation)

        import os
        print(filepath)
        print(os.path.exists(filepath))

        # Command fails on unicode so we must force it to be strings
        # todo: can we do a better conversion, e.g. f.decode("utf8")
        filepath = str(filepath)
        nodename = node.get_full_name()
        ix.cmds.SetReferenceFilename([node], filepath)
        
        # todo: do we need to explicitly trigger reload?
        
    def remove(self, container):
        node = container["node"]
        ix.cmds.DeleteItems([node.get_full_name()])