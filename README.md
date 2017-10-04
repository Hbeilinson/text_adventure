# text_adventure

This is a text adventure I made as a birthday present for my friend (so it is riddled with inside jokes and odd language). 

The game map is one instance of a class I created called Adventure Graph, which is essentially a standard graph type, with Scenes being the nodes. A user can only navigate to adjacent Scenes. Additionally, the game stores information about props (called Objects--such as the title horse, Slurmp, a bathing suit, etc) and will update the user's inventory, the scene inventories, and the scene descriptions accordingly. To access a scene the user must be in an adjacent scene AND have all the necessary objects.

The file main.py includes:
  class Scene:
    attributes: 
    name = string name of the scene
    des = string description of the scene
    obj = list of objects in the scene
    needs = list of objects needed to access the scene
    has_replacement = boolean representing if the scene has a secondary description that arises under certain circumstances
    rep_des = string replacement description, if the scene has one
    rep_obj = replacement list of objects, if the scene has one
    rep_new_scene = replacement scene, if any
    
    methods:
    __init__(self, name, description)
    __repr__(self)
    add_object(self, obj)
    add_need(self, obj)
    set_up_replace(self, des, obj, new_scene)
    replace(self)
    
  class Object:
    attributes:
    name = string name
    actions = dictionary of actions that can be done to the object
    exists = boolean indicating whether or not the object still exists in the game
    
    methods:
    __init__(self, name)
    __repr__(self)
    kill(self)
    add_action(self, action, effect)
    choose_action(self, game, a)
    
  class Adventure_Graph:
    attributes:
    rep = dictionary of Scenes
    
    methods:
    __init__(self)
    __repr__(self)
    add_scene(self, scene, adjList)
    scene_replace(self, new_scene, new_list)
    replace_scene(self, old_scene, new_scene)
    
  class Game_Play:
    attributes:
    graph = the Adventure_Graph that will serve as the map for the game
    current_scene = the Scene the user is currently in
    inventory = list of objects the user currently has in her inventory
    
    methods:
    __init__(self, graph, start)
    move(self)
    take_object(self, obj)
    abandon_object(self, obj)
    
  function create_slurmp() #Creates this particular instance of the game
    
