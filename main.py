#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 22:40:50 2017

@author: Hbeilinson
"""

class Scene:
    def __init__(self, name, description):
        self.name = name
        self.des = description
        self.obj = []
        self.needs = []
        self.has_replacement = False
        self.rep_des = description
        self.rep_obj = []
        self.rep_new_scene = None
        #self.adj = adjacent

    def __repr__(self):
        return self.name + "\n" + self.des
    
    def add_object(self, obj):
        self.obj += [obj]
        
    def add_need(self, obj):
        self.needs += [obj]
        
    def set_up_replace(self, des, obj, new_scene):
        self.rep_des = des
        self.rep_obj = obj
        self.rep_new_scene = new_scene
        self.has_replacement = True
    
    def replace(self):
        new = Scene(self.name, self.rep_des)
        self.des = self.rep_des
        self.obj = self.rep_obj
        for i in self.rep_obj:
            new.add_object(i)
        return (new, self.rep_new_scene)
        
    
class Object:
    def __init__(self, name):
        self.name = name
        self.actions = {}
        self.exists = True

    def __repr__(self):
        return str(self.name)

    def kill(self):
        self.exists = False
        
    def add_action(self, action, effect):
        self.actions[action] = effect
        
    def choose_action(self, game, a):
        #print "got to choose_action"
        if a == "take":
            game.take_object(self)
        elif a == "leave":
            game.abandon_object(self)
        elif a == "kill":
            killed = False
            for i in game.inventory:
                if i.name == "Sword":
                    killed = True
                    self.kill()
                    if game.current_scene.has_replacement:
                        new_list = (game.graph.rep[game.current_scene.name] + [game.current_scene.replace()[1]])
                        game.graph.scene_replace(game.current_scene.replace()[0], new_list)
            if killed == False:
                print "you, like, don't have a sword brah. What are you even trying to do here? You ineffectively swat with your hand, but that doesn't really work out for you. So, uh, yeah, choose something else to do probably. \n"
        elif a == "jump over":
            jumped = False
            for i in game.inventory:
                if i.name == "Slurmp":
                    jumped = True
                    self.kill()
                    if game.current_scene.has_replacement:
                        new_list = (game.graph.rep[game.current_scene.name] + [game.current_scene.replace()[1]])
                        game.graph.scene_replace(game.current_scene.replace()[0], new_list)
            if jumped == False:
                print "You're telling me you want to jump over this thing without Slurmp?!?!?!?! You fool! Go get yourself the best goddamn horse in the whole world, then maybe I'll let you try again. \n"
        
        else:
            print "I don't know why on Earth you would try to do what you tried to do with what you tried to do it with. That's completely inappropriate. Ugh. Do something else please. Gosh. \n"
        
    
class Adventure_Graph:
    def __init__(self):
        self.rep = {}
        
    def __repr__(self):
        return str(self.rep)
    
    def add_scene(self, scene, adjList):
        self.rep[scene.name] = adjList
    
    def scene_replace(self, new_scene, new_list):
        del self.rep[new_scene.name]
        self.add_scene(new_scene, new_list)
        #print "added " + new_scene.name
            
    def replace_scene(self, old_scene, new_scene):
        self.rep[new_scene.name] = self.rep[old_scene.name]
        for i in self.rep:
            if old_scene in self.rep[i]:
                for n in range(len(self.rep[i])):
                    if n == old_scene:
                        self.rep[i][n] = new_scene
        #del self.rep[old_scene.name]
        
        
                
class Game_Play:
    def __init__(self, graph, start):
        assert (type(graph) == type(Adventure_Graph()) and type(start) == type(Scene('','')))
        self.graph = graph
        self.current_scene = start
        self.inventory = []
        #print self.current_scene
        
    def move(self):
        print "You are in " + self.current_scene.name + " " + self.current_scene.des + "\n"
        pm = raw_input('What would you like to do from here? ')
        player_move = pm.upper()
        
        f1 = False
        f2 = False
        f3 = False
        f4 = False
        f5 = False
        f6 = False
           
        for i in self.graph.rep[self.current_scene.name]:
            if player_move == i.name and len(i.needs) == 0:
                f1 = True
                self.current_scene = i
            elif player_move == i.name and len(i.needs) != 0:
                needs_met = True
                for n in i.needs:
                    if n not in self.inventory:
                        needs_met = False
                if needs_met == True:
                    self.current_scene = i
                    f1 = True
                else:
                    print "You don't have the tools necessary to go there. You must have forgotten something along the way. Remember, to check your inventory type INVENTORY. My goodness, this message has been far too nice so far. Not sarcastic or scathing at all really! Well that cannot be allowed to continue. You're a wobble-kneed, silly souled, weak-jointed flibbidyfloop. So there! \n"
        
        if f1 == False and player_move == "INVENTORY":
            print self.inventory
            f2 = True
            
        if f1 == False and f2 == False:
            for i in self.current_scene.obj:
                if player_move in i.actions:
                    #print "got to actions of things in current scene"
                    i.choose_action(self, i.actions[player_move])
                    f3 = True
                    print "You did the thing with the thing! Coolio. \n"
                    
        if f1 == False and f2 == False and f3 == False:
            for i in self.inventory:
                if player_move in i.actions:
                    i.choose_action(self, i.actions[player_move])
                    f4 = True
                    print "You did the thing to the thing! Nice going. \n"
                    
        if f1 == False and f2 == False and f3 == False and player_move == "OBJECTS HERE":
            print self.current_scene.obj
            f5 = True
            
        if player_move == "SECRET TUNNELS":
            gl = raw_input("\nOkay, all powerful one. You clearly know about the secret tunnels. (Queue secret tunnel song) Where do you want to go? ")
            goal_scene = gl.upper()
            for i in self.graph.rep:
                for n in self.graph.rep[i]:
                    if n.name == goal_scene:
                        self.current_scene = n
                        f6 = True
            
        if f1 == False and f2 == False and f3 == False and f4 == False and f5 == False and f6 == False:
            print "That's not an option. A less mature Slurmp might even call you a damned fool. But these days, the mighty and powerful Slurmp has started doing yoga and meditating and is generally a bit more chill. So you can try again! \n"
        print "\n"
        self.move()
        
    def take_object(self, obj):
        #Take the object with you wherever you go
        self.inventory += [obj]
        self.current_scene.obj.remove(obj)
        if self.current_scene.has_replacement:
            #print self.graph.rep.keys()
            
            new_list = self.graph.rep[self.current_scene.name]
            self.graph.scene_replace(self.current_scene.replace()[0], new_list)
    
    def abandon_object(self, obj):
        #Put the object down in this scene and leave it here
        self.inventory.remove(obj)
        self.current_scene.obj += [obj]
        
def create_slurmp():
    common = Scene('COMMON', 'You are in the common room of apt 26, birthplace of the beloved Slurmp. You have access to BEDROOM and HALLWAY. \n')
   # game = Game_Play(slurmp_the_adv, common)
    #slurmp = Object('Slurmp', {"MOUNT SLURMP":game.take_object(slurmp), "UNMOUNT SLURMP":slurmp.abandon_object(slurmp)})
    
    bedroom = Scene('BEDROOM', 'You are in Hannahs (apostrophe placement unclear and therefore left out) bedroom. I know, it is pretty scandalous tbh. You have access to COMMON, being the common room. Hanging in the closet is a BATHING SUIT that is exactly your size. You can PUT ON SWIM GEAR if you want. If you later change your mind you can always DROP BATHING SUIT, though I give no promises about the future availibility of other clothing. \n')
    hallway = Scene('HALLWAY', 'You are in the hallway (that one between the downstairs common rooms). You have access to COMMON and OUTSIDE')
    outside = Scene('OUTSIDE', 'You are now outside of apartment 26. Here stands a majestic horse. Like seriously, the most goddamn beautiful horse you can imagine. His name is... \n\n\nSlurmp!!!! From here you can MOUNT SLURMP or go to HALLWAY  or LITERAL MAGICAL SKY KINGDOM (you can later UNMOUNT SLURMP at any time, though he is very seriously the. best. so I do not really know why I would even tell you about this option). \n')
    #outside_rep = Scene("OUTSIDE", "You are now outside of apartment 26. It's a fine place really. You can go to HALLWAY or LITERAL MAGICAL SKY KINGDOM.")
    literalmagicalskykingdom = Scene('LITERAL MAGICAL SKY KINGDOM', 'You are now in the actual, unmistakable, LITERAL MAGICAL SKY KINGDOM. Wow. Like, my god. That is fucking awesome. Too bad there is a really tall wall here blocking your view of absolutely everything. You can go back to OUTSIDE or beyond the wall is the UNKNOWN. To get there you will have to be able to jump over the wall somehow. \n')
    unknown = Scene('UNKNOWN', "You got to the unknown! That's pretty cool. Good for you. Pause for a second. Give yourself a pat on the back. Feel good about this accomplishment. So what now? To the left is a frickin awesome CASTLE (like, of doom probably) and to the right is a CLOUD. That's right. It's a motherfuckin' cloud. On the ground, or whatever it is that is beneath you here in the unknown, there's a sword. You may want to PICK UP SWORD, or you may not want to. What do I know? I'm just the narrator that may or may not be the all powerful Slurmp, god amongst equines, ruler of kingdoms, really just generally chill dude. \n")
    #unknown_rep = Scene("UNKNWON", "You got to the unknown! Again, presumably. It's considerably less impressive than the first time. Don't waste time feeling proud of yourself. Just get on with your life. Meaning, go to the LITERAL MAGICAL SKY KINGDOM, the CLOUD, or the CASTLE. If you go to the CASTLE, have fun storming it! If you go to the CLOUD, say hi to Steve Jobs. If you go to the LITERAL MAGICAL SKY KINGDOM, have fun with that wall i guess?")
    
    castle = Scene("CASTLE", "You're in a castle now, i guess. wut, u thot id be enthusiastic and well spoken the whole way? well slurmp narrators need breaks too ya know! it is a cool castle tho. kinda like that mansion in boise, idaho? u no the one. Okay, really just picture it as like your dream castle, but with a slight twince of being TOO perfect. there is a staircase tho, so you can go UPSTAIRS or you can go out the really really really beautiful French doors to BEHIND THE CASTLE or you can go back to the UNKNOWN if you're lame af i guess. \n")
    behindthecastle = Scene("BEHIND THE CASTLE", "Behind you is a dank CASTLE kind of building. It looks like a mix between the entire Bryn Mawr campus and a White Castle. It's kind of confusing actually. Well never mind that. In front of you is a SWIMMING POOL, and a SLIDE. This is the fun part of the adventure! Take a break. Relax. Go for a swim or a slide, your choice. \n" )
    swimmingpool = Scene("SWIMMING POOL", "You're in a magical underwater world of vinyl and chlorine. If this isn't for you, you can go to the surface, where you will be BEHIND THE CASTLE. Otherwise, you dive deeper and then even deeper. This is surprising, partly cuz if we're being honest you're really not all that great of a swimmer, and partly because you don't expect such depth out of a backyard swimming pool. It's kind of a refreshing surprise really. Here you are expecting a shallow experience, and it has undiscovered depths and emotions. Suddenly, just as you're beginning to finally suspect you may need to breathe soon, a MYSTERIOUS CAVERN opens before you. \n")
    slide = Scene("SLIDE", "The slide is red, like the blood of your enemies, or Haverford's flag, or raspberries. You can either chicken out and go back to BEHIND THE CASTLE while all the other kids laugh at you, or go down the slide into the MYSTERIOUS CAVERN. \n" )
    mysteriouscavern = Scene("MYSTERIOUS CAVERN", "Wow. This cavern sure is mysterious. The only thing in it, besides the slow dripping of red liquid and distant sound of bats fluttering (the narrator said ominously) is a button. It says, in scrawled red ink (or is it ink?) BUCKINGHAM PALACE. \n")
    buckinghampalace = Scene("BUCKINGHAM PALACE", "You, probably, are in an apartment that looks pretty much the same as the common room where you started out. But I don't know for sure that it looks the same, because none of my friends would go visit it with me (ahem ahem). To be more specific, you are in the common room of apartment 2d in 800 Ardmore Ave. If you're confused about why this is called Buckingham Palace, it's a fucking fantastic pun and you'd better not question it any further. There is a skeleton on the wall that is offering you access to the OTHER PORTAL. That's weird. Even weirder, behind one of the bedroom doors you hear noises as if your friends were singing the YMCA. On this door is a sign, reading SUPER SECRET SURPRISE WORLD JUST FOR YOU, YES YOU. \n")
    ymca = Scene("YMCA", "The YMCA isn't a place, you dumbass. I mean, it is. But, you're not, like, suddenly in a headquarters of the young men's christian association. You're in a magical song world i guess? I don't know, just go back to where you came from, namely BUCKINGHAM PALACE or HELL or ANOTHER MAGICAL SKY KINGDOM. \n")
    
    upstairs = Scene("UPSTAIRS", "You're upstairs in the castle. If there was eerie music playing in your head before, it has gotten louder. If it wasn't there to begin with, it was probably because you didn't really understand the situation. Add in some eerie music. This place is eerie as shit. You could retreat back downstairs to CASTLE or you could soldier on like the brave soul Slurmp knows you are (or hopes you are, because he's really bought into you at this point. Like, seriously. If you're not brave we gonna have some problems, because Slurmp doesn't hang around with losers.) If you decide to go on, you could enter CASTLE BEDROOM or BATHROOM. \n")
    bathroom = Scene("BATHROOM", "Really? You're in an eerie castle and you chose to go to the bathroom? That's kind of lame tbh. But kay. You shit. Good job. Now you can return to UPSTAIRS. That's it, that's the only option. Don't chicken out bro. \n")
    castlebedroom = Scene("CASTLE BEDROOM", "There's a goddamn dragon!!!!!! Ahhhhhh!!!!!!!!. You can ATTACK or go the hell back to UPSTAIRS. Really, this time I won't judge you for doing that. This shit is scary. \n")
    #castlebedroom_rep = Scene("CASTLE BEDROOM", "There's a dragon dead on the floor. It's kind of sad actually. Maybe we should stop for a moment and think about the consequences of video game violence on modern society. Like, if you came across a dragon in real life, and you had a sword, would you kill it? What if it was nice? Not all dragons, ya know? Huh. Well it's dead now, so I guess that's that. Just, like, don't let this senseless video game violence affect your psyche, okay? Well, moving on. Now that that's dead, a PORTAL is revelead behind it. There's also always the option of going back to UPSTAIRS if you like really need to use the bathroom or explore behind the castle or something.")
    portal = Scene("PORTAL", "The world is a blinding swirl of swirliness. Like the intro to Doctor Who kind of? If you haven't seen it, just look up the intro. It's like that, maybe even with Doctor Who music? But also like real cool. As you swirl through dimensions and watch scenes from our storied past flash before your eyes, you feel yourself being pulled in two directions. One is confusingly labeled with a flashing neon sign OTHER PORTAL. The other one looks like a SWING SET but is unlabeled, so who knows really? It could just be some pieces of rubber attached to chains attached to metal attached to the ground for other, more nefarious purposes. That is for me to know and you to not care too much about. Worried about this choice between neon and potential nefariousness, you glance back and notice that you can also take a step back out of the portal into CASTLE BEDROOM. But why would you do that? \n")
    swingset = Scene("SWING SET", "Turns out this is a swing set. The one on Ardmore Ave, specifically. It's not particularly nefarious, except that directly below it is a tunnel that Satan is slowly crawling out of. If you jump off the swing (which, by the way, you're on) you can go to HELL. If you swing really really really high and then jump off from there, you can go to HEAVEN. (And yes, in case you were concerned, Slurmp can come to both of those places if you should choose to bring him. I know, he's just that loyal. He would literally go to the pits of hell for you. You better give him, like, I don't know, an apple at least for all this.) If literally choosing between HEAVEN and HELL is too much for you, a hole in the space time continuum glistens next to you, and you can dive back into the PORTAL if that suits you (wimp). \n")
    hell = Scene("HELL", "Everything is red and fiery. In front of you stands Satan. He talks in a funny voice and is bad at algebra and overall is pretty cute if we're being totally honest. Nonetheless, behind me seems to be some glowy pretty shit that looks like probably where you're trying to go from here, so you're going to have to ATTACK him probably. Alternatively, you can choose not to ATTACK and to instead retreat to SWING SET or STEVE JOBS (if you didn't come from STEVE JOBS, don't worry it sort of makes sense once you get there. Actually, no it doesn't. It's fine, Steve Jobs is here, it's okay, don't worry about it.) \n")
    heaven = Scene("HEAVEN", "Wow. Like goshdarn (Slurmp wouldn't normally censor his swearwords like that, but we are in heaven after all.) Who woulda thunk it? After the life you've lived (yeah, i know about that thing that time). You gaze around and see a throne, with the inscription, 'Reserved for the gloriously wonderful Hannah Beilinson.' That's odd. Who could that be? Ah well. Anyway, you can't just stay here. And it kind of sucks (sorry angels, etc. I have to use such language from time to time to really express myself) because from here you can only go down. Below you you can see a SWING SET, sadly swinging away to itself. A little bit less low down are shiny offices with all sorts of fun and games. They're pretty cool, so you presume they're APPLE HQ. You must wave goodbye to the angels and continue on. \n")
    
    cloud = Scene("CLOUD", "You step into the cloud and are instantly awed by how cold and damp it is. Like shiiiittt man! You thought clouds would be light and fluffy and taste like marshmallows! We've all been there. I get it. That's rough buddy. Once the initial shock passes, you notice two things: One is the glistening ghost of STEVE JOBS, who you can go talk to. The other is an AIRPLANE that is flying by, that you can hop into (Slurmp is magical, remember? Maybe not. I might not have mentioned that... huh. Well he is, I swear! So you can do cool stuff like hop into moving airplanes in the sky. You know, on second thought, that's definitely not the least realistic element of this whole scenario. I don't even know why I'm bothering to explain it really). You can also go back to the UNKNOWN if you'd like to, though now that you know what it is, I feel like it's kind of lost its appeal, no? \n")
    stevejobs = Scene("STEVE JOBS", "You're talking to Steve Jobs. He's brilliant, but kind of an asshole. Because of that, you can TAKE MACBOOK from him if you'd like to. If you do he won't put up a fight, cuz he's kind of a nerd tbh (but don't tell him I told you that). He tells you that you can either take a tour of the APPLE HQ (he doesn't normally allow that kind of thing, but he sees how totally kickass your horse is, if I do say so myself, and so will allow it on the condition that you're Slurmp's friend) or invites you to come to tea with him in HELL. So that's a tough choice I'd say. Follow your gut, ya know? \n")
    applehq = Scene("APPLE HQ", "You're in the Apple HQ. It's, like, not as cool as the Google hq if we're being completely honest? But it is still fancy af, so don't complain. You had to work hard to get here! Well, I mean, mostly you had to have cool friends (ahem ahem, Slurmp, the real true bestest). This is basically the end of the line. I don't even know why you'd want to go anywhere from here. The only options are to go to HEAVEN, or to go back to talking to STEVE JOBS. \n")
    airplane = Scene("AIRPLANE", "In a shocking turn of events, you are in an airplane. But not just any airplane -- it's either a Lost style airplane, meaning you can take it straight to OTHER PORTAl or the dumb movie kind of airplane, meaning you can take it to the LAND OF DUMB MOVIES. This is a choice only you can make. (And don't you dare ask why it's called OTHER PORTAL, and not just the portal. If you don't know, you aren't meant to know.) Oh, you can also decide that these are both terrible choices, and jump out of the airplane back into the CLOUD. \n")
    otherportal = Scene("OTHER PORTAL", "This portal is more like the portals in the game Portal. Your loyal and all-knowing narrator has unfortunately never played Portal, and so doesn't know what they're like (all-knowing is just a title, okay?). So just picture something really fucking neat. In front of you the portal splits. You can just glimpse some red chairs and half-okay food that appears to be THE DC, FOR SOME REASON in one direction, and BUCKINGAM PALACE in the other. Behind you are some spotty punch lines and uncomfortable seats, indicating that you can also go to the AIRPLANE. \n")
    landofdumbmovies = Scene("LAND OF DUMB MOVIES", "I mean that in the best way possible, really. From here you can see AIRPLANE and also a bunch of other things, like Kung Fury, and Wayne's World, and, admittedly, Holy Musical B@tman (which, granted, is not actually a movie, but somehow got here anyway). However, the only one you can visit is AIRPLANE. Or you can talk to the guy from Kung Fury and he can hack you back in time to visit STEVE JOBS. \n")
    
    thedcforsomereason = Scene("THE DC, FOR SOME REASON", "You're in the DC, for some reason. That's weird. K. Moving on. Eat a meal, talk to friends, talk to enemies, stage a fight with your bff to scare off the bullies. Once you're done with all that, you can hop on into the OTHER PORTAL that is taking up the entire friggin' ceiling, or you can head down to OUTSIDE of apartment 26. Oh! And I almost forgot! There's ANOTHER MAGICAL SKY KINGDOM, if that's your kind of thing. \n")
    anothermagicalskykingdom = Scene("ANOTHER MAGICAL SKY KINGDOM", "Woot to the woot. You're in another magical sky kingdom! It's better than the first one, because this time there's no giant wall. Instead, there is an incredibly deep chasm. You can try to JUMP THE CHASM if you want. On the other side you can just barely see a door that says SUPER SECRET SURPRISE WORLD JUST FOR YOU, YES YOU in streamers. From behind the doors come the faint echoes of what seems to be your friends singing the YMCA. If this isn't too appealing, you can always return to THE DC, FOR SOME REASON. \n")
    
    secretsss = Scene("SUPER SECRET SURPRISE WORLD JUST FOR YOU, YES YOU", "Happy birthday!!!!!! (If it's not your birthday, it's fine, just have a nice normal day). Everyone you've ever loved is here. They've stopped singing the YMCA and are now singing happy birthday. The room overflows with presents and love and joy and maybe just a tiny bit of too much body odor from people having waited for you for so long. I hope your day is amazing. \n")
    
    slurmp_the_adv = Adventure_Graph()
    slurmp_the_adv.add_scene(common, [bedroom, hallway])
    slurmp_the_adv.add_scene(bedroom, [common])
    slurmp_the_adv.add_scene(hallway, [common, outside])
    slurmp_the_adv.add_scene(outside, [hallway, literalmagicalskykingdom])
    slurmp_the_adv.add_scene(literalmagicalskykingdom, [outside, unknown])
    slurmp_the_adv.add_scene(unknown, [castle, cloud])
    slurmp_the_adv.add_scene(castle,[upstairs, unknown, behindthecastle])
    slurmp_the_adv.add_scene(upstairs, [bathroom, castlebedroom, castle])
    slurmp_the_adv.add_scene(bathroom, [upstairs])
    slurmp_the_adv.add_scene(castlebedroom, [upstairs])
    slurmp_the_adv.add_scene(portal, [castlebedroom, swingset, otherportal])
    slurmp_the_adv.add_scene(swingset, [portal, hell, heaven])
    slurmp_the_adv.add_scene(hell, [swingset, stevejobs, ymca])
    slurmp_the_adv.add_scene(heaven, [swingset, applehq])
    slurmp_the_adv.add_scene(cloud,[stevejobs, airplane])
    slurmp_the_adv.add_scene(stevejobs, [cloud, applehq, hell])
    slurmp_the_adv.add_scene(applehq, [stevejobs, heaven])
    slurmp_the_adv.add_scene(behindthecastle, [castle, swimmingpool, slide])
    slurmp_the_adv.add_scene(swimmingpool, [behindthecastle, mysteriouscavern])
    slurmp_the_adv.add_scene(slide, [behindthecastle, mysteriouscavern])
    slurmp_the_adv.add_scene(mysteriouscavern, [buckinghampalace])
    slurmp_the_adv.add_scene(buckinghampalace,[ymca, secretsss, otherportal])
    slurmp_the_adv.add_scene(airplane, [cloud, otherportal, landofdumbmovies])
    slurmp_the_adv.add_scene(otherportal, [airplane, buckinghampalace, thedcforsomereason])
    slurmp_the_adv.add_scene(landofdumbmovies, [airplane, stevejobs])
    slurmp_the_adv.add_scene(thedcforsomereason, [otherportal, outside, anothermagicalskykingdom])
    slurmp_the_adv.add_scene(anothermagicalskykingdom, [thedcforsomereason, ymca])
    slurmp_the_adv.add_scene(secretsss, [ymca])
    slurmp_the_adv.add_scene(ymca, [buckinghampalace, hell, anothermagicalskykingdom])

    game = Game_Play(slurmp_the_adv, common) 
    
    slurmp = Object('Slurmp')
    slurmp.add_action("MOUNT SLURMP","take")
    slurmp.add_action("UNMOUNT SLURMP", "leave")
    outside.add_object(slurmp)
    
    sword = Object("Sword")
    sword.add_action("PICK UP SWORD", "take")
    sword.add_action("DROP SWORD", "leave")
    unknown.add_object(sword)
    #sword.add_action("ATTACK","attack")
    
    dragon = Object("Dragon!!!!! (like, fuck man) His name is actually Bill, if you were wondering.")
    dragon.add_action("ATTACK", "kill")
    castlebedroom.add_object(dragon)
    
    macbook = Object("MacBook")
    macbook.add_action("TAKE MACBOOK","take")
    macbook.add_action("DROP MACBOOK","leave")
    stevejobs.add_object(macbook)
    
    satan = Object("Satan")
    satan.add_action("ATTACK", "kill")
    hell.add_object(satan)
    
    bathingsuit = Object("Bathing Suit")
    bathingsuit.add_action("PUT ON SWIM GEAR", "take")
    bathingsuit.add_action("DROP BATHING SUIT", "leave")
    bedroom.add_object(bathingsuit)
    
    chasm = Object("Chasm")
    chasm.add_action("JUMP THE CHASM", "jump over")
    anothermagicalskykingdom.add_object(chasm)
    
    applehq.add_need(macbook)
    applehq.add_need(slurmp)
    unknown.add_need(slurmp)
    swimmingpool.add_need(bathingsuit)
    
    
    #bedroom.add_prec(not dragon.exists)
    
    anothermagicalskykingdom.set_up_replace("You're now on the other side of the chasm (the one near the door), still in ANOTHER MAGICAL SKY KINGDOM. Since THE DC, FOR SOME REASON is kind of magical (i guess?) you can still access it from this side of the chasm. But you can also accessSUPER SECRET SURPRISE WORLD JUST FOR YOU, YES YOU, from whence the YMCA seems to be coming, if you so choose. \n", [chasm], secretsss)
    bedroom.set_up_replace("You are now in Hannahs (apostrophes vague) bedroom. It's pretty gnarly yo. You have access to COMMON. \n", [], None)
    outside.set_up_replace("You are now outside of apartment 26. It's a fine place really. You can go to HALLWAY or LITERAL MAGICAL SKY KINGDOM.", [], None)
    unknown.set_up_replace("You're in the unknown (allegedly). But in reality, you don't know. Hence the name. Don't waste time lollygagging. Just get on with your life. Meaning, go to the LITERAL MAGICAL SKY KINGDOM, the CLOUD, or the CASTLE. If you go to the CASTLE, have fun storming it! If you go to the CLOUD, say hi to Steve Jobs. If you go to the LITERAL MAGICAL SKY KINGDOM, have fun with that wall i guess? \n", [], None)
    castlebedroom.set_up_replace("There's a dragon dead on the floor. It's kind of sad actually. Maybe we should stop for a moment and think about the consequences of video game violence on modern society. Like, if you came across a dragon in real life, and you had a sword, would you kill it? What if it was nice? Not all dragons, ya know? Huh. It's not a video game culture -- it's a slaughter. Well the dragon is dead now, so I guess that's that. Just, like, don't let this senseless video game violence affect your psyche, okay? Well, moving on. Now that that's dead, a PORTAL is revelead behind it. There's also always the option of going back to UPSTAIRS if you like really need to use the bathroom or explore behind the castle or something. \n", [], portal)
    hell.set_up_replace("You are in a deep cavern. Now that Satan is dead, it's not quite hell anymore really. It's a bit sad actually. A bunch of asshole dead people are kinda wandering around looking confused. Sucks for them i guess. Actually it's probably good for them? I don't know, we could have some real deep philosophical and religious arguments around the morality and effects of killing Satan. But this may not be the ideal format. So, moving on. If you're a rube you can turn back and visit STEVE JOBS or SWING SET. But, alternatively, and you better really prepare yourself for this one, in front of you is a door. It's a fucking ornate door that is like just so goddamn cool you would not even believe how cool it is like wow, really. From the edges of it is glowing some really bright but also occasionally multicolored lights. From the background you think you can just faintly hear the sounds of your friends singing the YMCA. On the door is printed, in real nice script with a kinda glowy effect, SUPER SECRET SURPRISE WORLD JUST FOR YOU, YES YOU. \n",[], secretsss)
    #Add secret to set_up_replace of hell
    
    print "READ EVERYTHING CAREFULLY!!! Welcome to this text adventure! Before you continue, you should know that you can type INVENTORY at any time to see a list of objects in your inventory, and you can type OBJECTS HERE any time to see a list of objects in the current scene. Other than that, basically only type options that are given in bold in the scene description. Meaning don't be a fool and say things like 'go to the bathroom'. Just say BATHROOM. We get it, you have to shit. It's fine, you don't need to elaborate. In addition to these bolded options, if you currently have any items in your inventory you can say DROP and then the item name, and mostly that will work. Also, you don't actually need to use all caps yourself if you don't want to. Slurmp is smart and can figure it out. \n"
    game.move()
    #user_input = raw_input("Where would you like to go?")
    
create_slurmp()
