# wumpus_kb.py
# ------------
# Licensing Information:
# Please DO NOT DISTRIBUTE OR PUBLISH solutions to this project.
# You are free to use and extend these projects for EDUCATIONAL PURPOSES ONLY.
# The Hunt The Wumpus AI project was developed at University of Arizona
# by Clay Morrison (clayton@sista.arizona.edu), spring 2013.
# This project extends the python code provided by Peter Norvig as part of
# the Artificial Intelligence: A Modern Approach (AIMA) book example code;
# see http://aima.cs.berkeley.edu/code.html
# In particular, the following files come directly from the AIMA python
# code: ['agents.py', 'logic.py', 'search.py', 'utils.py']
# ('logic.py' has been modified by Clay Morrison in locations with the
# comment 'CTM')
# The file ['minisat.py'] implements a slim system call wrapper to the minisat
# (see http://minisat.se) SAT solver, and is directly based on the satispy
# python project, see https://github.com/netom/satispy .

import utils

#-------------------------------------------------------------------------------
# Wumpus Propositions
#-------------------------------------------------------------------------------

### atemporal variables

proposition_bases_atemporal_location = ['P', 'W', 'S', 'B']

def pit_str(x, y):
    "There is a Pit at <x>,<y>"
    return 'P{0}_{1}'.format(x, y)
def wumpus_str(x, y):
    "There is a Wumpus at <x>,<y>"
    return 'W{0}_{1}'.format(x, y)
def stench_str(x, y):
    "There is a Stench at <x>,<y>"
    return 'S{0}_{1}'.format(x, y)
def breeze_str(x, y):
    "There is a Breeze at <x>,<y>"
    return 'B{0}_{1}'.format(x, y)

### fluents (every proposition who's truth depends on time)

proposition_bases_perceptual_fluents = ['Stench', 'Breeze', 'Glitter', 'Bump', 'Scream']

def percept_stench_str(t):
    "A Stench is perceived at time <t>"
    return 'Stench{0}'.format(t)
def percept_breeze_str(t):
    "A Breeze is perceived at time <t>"
    return 'Breeze{0}'.format(t)
def percept_glitter_str(t):
    "A Glitter is perceived at time <t>"
    return 'Glitter{0}'.format(t)
def percept_bump_str(t):
    "A Bump is perceived at time <t>"
    return 'Bump{0}'.format(t)
def percept_scream_str(t):
    "A Scream is perceived at time <t>"
    return 'Scream{0}'.format(t)

proposition_bases_location_fluents = ['OK', 'L']

def state_OK_str(x, y, t):
    "Location <x>,<y> is OK at time <t>"
    return 'OK{0}_{1}_{2}'.format(x, y, t)
def state_loc_str(x, y, t):
    "At Location <x>,<y> at time <t>"
    return 'L{0}_{1}_{2}'.format(x, y, t)

def loc_proposition_to_tuple(loc_prop):
    """
    Utility to convert location propositions to location (x,y) tuples
    Used by HybridWumpusAgent for internal bookkeeping.
    """
    parts = loc_prop.split('_')
    return (int(parts[0][1:]), int(parts[1]))

proposition_bases_state_fluents = ['HeadingNorth', 'HeadingEast',
                                   'HeadingSouth', 'HeadingWest',
                                   'HaveArrow', 'WumpusAlive']

def state_heading_north_str(t):
    "Heading North at time <t>"
    return 'HeadingNorth{0}'.format(t)
def state_heading_east_str(t):
    "Heading East at time <t>"
    return 'HeadingEast{0}'.format(t)
def state_heading_south_str(t):
    "Heading South at time <t>"
    return 'HeadingSouth{0}'.format(t)
def state_heading_west_str(t):
    "Heading West at time <t>"
    return 'HeadingWest{0}'.format(t)
def state_have_arrow_str(t):
    "Have Arrow at time <t>"
    return 'HaveArrow{0}'.format(t)
def state_wumpus_alive_str(t):
    "Wumpus is Alive at time <t>"
    return 'WumpusAlive{0}'.format(t)

proposition_bases_actions = ['Forward', 'Grab', 'Shoot', 'Climb',
                             'TurnLeft', 'TurnRight', 'Wait']

def action_forward_str(t=None):
    "Action Forward executed at time <t>"
    return ('Forward{0}'.format(t) if t != None else 'Forward')
def action_grab_str(t=None):
    "Action Grab executed at time <t>"
    return ('Grab{0}'.format(t) if t != None else 'Grab')
def action_shoot_str(t=None):
    "Action Shoot executed at time <t>"
    return ('Shoot{0}'.format(t) if t != None else 'Shoot')
def action_climb_str(t=None):
    "Action Climb executed at time <t>"
    return ('Climb{0}'.format(t) if t != None else 'Climb')
def action_turn_left_str(t=None):
    "Action Turn Left executed at time <t>"
    return ('TurnLeft{0}'.format(t) if t != None else 'TurnLeft')
def action_turn_right_str(t=None):
    "Action Turn Right executed at time <t>"
    return ('TurnRight{0}'.format(t) if t != None else 'TurnRight')
def action_wait_str(t=None):
    "Action Wait executed at time <t>"
    return ('Wait{0}'.format(t) if t != None else 'Wait')


def add_time_stamp(prop, t): return '{0}{1}'.format(prop, t)

proposition_bases_all = [proposition_bases_atemporal_location,
                         proposition_bases_perceptual_fluents,
                         proposition_bases_location_fluents,
                         proposition_bases_state_fluents,
                         proposition_bases_actions]


#-------------------------------------------------------------------------------
# Axiom Generator: Current Percept Sentence
#-------------------------------------------------------------------------------

#def make_percept_sentence(t, tvec):
def axiom_generator_percept_sentence(t, tvec):
    """
    Asserts that each percept proposition is True or False at time t.

    t := time
    tvec := a boolean (True/False) vector with entries corresponding to
            percept propositions, in this order:
                (<stench>,<breeze>,<glitter>,<bump>,<scream>)

    Example:
        Input:  [False, True, False, False, True]
        Output: '~Stench0 & Breeze0 & ~Glitter0 & ~Bump0 & Scream0'
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    for i in range(len(tvec)):#Iterate over the given vector
            if tvec[i]==True:#If any of the percepts are true add them directly with and
                if i==0:
                    axiom_str+=percept_stench_str(t)#Adding Stench Percept
                if i==1:
                    axiom_str+=' & '+ percept_breeze_str(t)#Adding Breeze Percept with & to the previous axiom string
                if i==2:
                    axiom_str+=' & '+ percept_glitter_str(t)#Adding Glitter Percept with & to the previous axiom string
                if i==3:
                    axiom_str+=' & '+ percept_bump_str(t)#Adding Bump Percept with & to the previous axiom string
                if i==4:
                    axiom_str+=' & '+ percept_scream_str(t)#Adding Scream Percept with & to the previous axiom string
            else:#If any of the percepts is not true,it implies it is false and we add them with negation
                if i==0:
                    axiom_str+='~'+ percept_stench_str(t)#Adding negation of Stench Percept
                if i==1:
                    axiom_str+=' & ~'+ percept_breeze_str(t)#Adding negation of Breeze Percept with & to the previous axiom string
                if i==2:
                    axiom_str+=' & ~'+ percept_glitter_str(t)#Adding negation of Glitter Percept with & to the previous axiom string
                if i==3:
                    axiom_str+=' & ~'+ percept_bump_str(t)#Adding negation of Bump Percept with & to the previous axiom string
                if i==4:
                    axiom_str+=' & ~'+ percept_scream_str(t)#Adding negation of Scream Percept with & to the previous axiom string     
    # Comment or delete the next line once this function has been implemented.
    return axiom_str


#-------------------------------------------------------------------------------
# Axiom Generators: Initial Axioms
#-------------------------------------------------------------------------------

def axiom_generator_initial_location_assertions(x, y):
    """
    Assert that there is no Pit and no Wumpus in the location

    x,y := the location
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    #Ensure no pit, no wumpus together or individually
    axiom_str='((~'+ pit_str(x,y)+'&'+'~'+wumpus_str(x,y)+')'+'&'+'(~'+ pit_str(x,y)+'|'+'~'+wumpus_str(x,y)+')'+'&'+'(~'+ pit_str(x,y)+')'+'&'+'(~'+ wumpus_str(x,y)+')'+')'
    # Comment or delete the next line once this function has been implemented.
    return axiom_str

def neighbouring_points_checker(x, y, xmin, xmax, ymin, ymax,func_to_check): # Function defined to check the neighboring points for the given input function
    axiom_str = ''
    if x>xmin:
        axiom_str+='|'+func_to_check(x-1,y)#To the left of current block
    if x<xmax:
        axiom_str+='|'+func_to_check(x+1,y)#To the right of current block
    if y>ymin:
        axiom_str+='|'+func_to_check(x,y-1)#To the bottom of current block
    if y<ymax:
        axiom_str+='|'+func_to_check(x,y+1)#To the top of current block
    return axiom_str

def axiom_generator_pits_and_breezes(x, y, xmin, xmax, ymin, ymax):
    """
    Assert that Breezes (atemporal) are only found in locations where
    there are one or more Pits in a neighboring location (or the same location!)

    x,y := the location
    xmin, xmax, ymin, ymax := the bounds of the environment; you use these
           variables to 'prune' any neighboring locations that are outside
           of the environment (and therefore are walls, so can't have Pits).
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    #Assert that the breeze is present only if there is a pit in the block or in any of the adjacent blocks by using the function defined above passing pit _str
    axiom_str = '('+breeze_str(x,y)+'<=>('+pit_str(x,y)+neighbouring_points_checker(x, y, xmin, xmax, ymin, ymax,pit_str)+'))'
    return axiom_str

def generate_pit_and_breeze_axioms(xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_pits_and_breezes(x, y, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_pits_and_breezes')
    return axioms

def axiom_generator_wumpus_and_stench(x, y, xmin, xmax, ymin, ymax):
    """
    Assert that Stenches (atemporal) are only found in locations where
    there are one or more Wumpi in a neighboring location (or the same location!)

    (Don't try to assert here that there is only one Wumpus;
    we'll handle that separately)

    x,y := the location
    xmin, xmax, ymin, ymax := the bounds of the environment; you use these
           variables to 'prune' any neighboring locations that are outside
           of the environment (and therefore are walls, so can't have Wumpi).
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    #Assert that the stench is present only if there is a wumpus in the block or in any of the adjacent blocks by using the function defined above passing wumpus_str 
    axiom_str = '('+stench_str(x,y)+'<=>('+wumpus_str(x,y)+neighbouring_points_checker(x, y, xmin, xmax, ymin, ymax,wumpus_str)+'))'
    return axiom_str

def generate_wumpus_and_stench_axioms(xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_wumpus_and_stench(x, y, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_wumpus_and_stench')
    return axioms

def wumpus_iterator(xmin, xmax, ymin, ymax, func_to_check,logic_to_pass): # Define an iterator function to check the boundaries and return the function to be passed
    axiom_str = ''
    x_iter=xmin #Start with lower bound for x
    while x_iter<=xmax: #Check x max bound
        y_iter=ymin #Start with lower bound for y
        while y_iter<=ymax: # Check y max bound
            axiom_str += func_to_check(x_iter, y_iter) + logic_to_pass 
            y_iter+=1 #increment
        x_iter+=1 #increment
    return axiom_str[:-1] #discard the last logic


def axiom_generator_at_least_one_wumpus(xmin, xmax, ymin, ymax):
    """
    Assert that there is at least one Wumpus.

    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    #Use the wumpus iterator defined above and check for wumpus
    axiom_str = wumpus_iterator(xmin, xmax, ymin, ymax, wumpus_str,'|') 
    # Comment or delete the next line once this function has been implemented.
    return axiom_str

def axiom_generator_at_most_one_wumpus(xmin, xmax, ymin, ymax):
    """
    Assert that there is at at most one Wumpus.

    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    allcells = []
    temp = [] #Define temporary variables
    
    x=xmin#Set lower bound of x
    while x<=xmax:#Check x max bound
        y=ymin#Set lower bound of y
        while y<=ymax:#Check y max bound
            allcells.append((x, y)) 
            y+=1
        x+=1    
    for cell in allcells: #iterate through all the blocks
        allothercells = []
        for othercells in allcells: #For every block, create an array which checks if wumpus is present in all the other blocks
            if othercells != cell: #Identify all the blocks which are not current block
                allothercells+=[othercells]
        wumpuscheck = []
        for item in allothercells:# for all the other blocks
            wumpuscheck+=['~' + wumpus_str(item[0], item[1])]#Assert wumpus is not present
        wumpuscheckoutput=' & '.join(wumpuscheck)#Join the prepositions with and
        temp+=['('+wumpus_str(cell[0],cell[1])+' >> ('+wumpuscheckoutput+'))'] #If wumpus is present in current location it means it is not present in all other locations
    axiom_str = ' & '.join(temp) #Join the expressions with the and clause
    # Comment or delete the next line once this function has been implemented.
    return axiom_str

def axiom_generator_only_in_one_location(xi, yi, xmin, xmax, ymin, ymax, t = 0):
    """
    Assert that the Agent can only be in one (the current xi,yi) location at time t.

    xi,yi := the current location.
    xmin, xmax, ymin, ymax := the bounds of the environment.
    t := time; default=0
    """
    axiom_str = ''
    axiom_str_1=''
    "*** YOUR CODE HERE ***"
    x=xmin#Set lower bound for x
    while x<=xmax:#Iterate till xmax
        y=ymin#Set lower bound for y
        while y<=ymax:#Iterate till ymax
            if (x, y) != (xi, yi):#For all other locations other than current block
                axiom_str += '~(' + state_loc_str(x, y, t) + ')&'#Assert that the agent is not preseny
            axiom_str_1+= state_loc_str(x, y, t) + '|'#Present in the current location
            y+=1#incrementor
        x+=1 #incrementor
    axiom_str=state_loc_str(xi,yi,t)+'&'+axiom_str
    axiom_str = axiom_str[:-1] #Remove the last extra clause
    axiom_str+='&('+axiom_str_1[:-1]+')'   #Remove the last extra clause 
    # Comment or delete the next line once this function has been implemented.
    return axiom_str

def axiom_generator_only_one_heading(heading = 'north', t = 0):
    """
    Assert that Agent can only head in one direction at a time.

    heading := string indicating heading; default='north';
               will be one of: 'north', 'east', 'south', 'west'
    t := time; default=0
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    #Define header variables to check header direction
    north_header=state_heading_north_str(t)
    east_header=state_heading_east_str(t)
    south_header=state_heading_south_str(t)
    west_header=state_heading_west_str(t)
    if heading=='north':#Assert that north means only north direction and negation of all other directions
        axiom_str+='('+north_header+')&~('+east_header+')&~('+south_header+')&~('+west_header+')'
    if heading=='east':#Assert that east means only north direction and negation of all other directions
        axiom_str+='~('+north_header+')&('+east_header+')&~('+south_header+')&~('+west_header+')'
    if heading=='south':#Assert that south means only north direction and negation of all other directions
        axiom_str+='~('+north_header+')&~('+east_header+')&('+south_header+')&~('+west_header+')'
    if heading=='west':#Assert that west means only north direction and negation of all other directions
        axiom_str+='~('+north_header+')&~('+east_header+')&~('+south_header+')&('+west_header+')'
    # Comment or delete the next line once this function has been implemented.
    return axiom_str

def axiom_generator_have_arrow_and_wumpus_alive(t = 0):
    """
    Assert that Agent has the arrow and the Wumpus is alive at time t.

    t := time; default=0
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    axiom_str=state_have_arrow_str(t)+'&'+state_wumpus_alive_str(t) #Check current status of arrow and if wumpus is alive
    # Comment or delete the next line once this function has been implemented.
    return axiom_str


def initial_wumpus_axioms(xi, yi, width, height, heading='east'):
    """
    Generate all of the initial wumpus axioms
    
    xi,yi = initial location
    width,height = dimensions of world
    heading = str representation of the initial agent heading
    """
    axioms = [axiom_generator_initial_location_assertions(xi, yi)]
    axioms.extend(generate_pit_and_breeze_axioms(1, width, 1, height))
    axioms.extend(generate_wumpus_and_stench_axioms(1, width, 1, height))
    
    axioms.append(axiom_generator_at_least_one_wumpus(1, width, 1, height))
    axioms.append(axiom_generator_at_most_one_wumpus(1, width, 1, height))

    axioms.append(axiom_generator_only_in_one_location(xi, yi, 1, width, 1, height))
    axioms.append(axiom_generator_only_one_heading(heading))

    axioms.append(axiom_generator_have_arrow_and_wumpus_alive())
    
    return axioms


#-------------------------------------------------------------------------------
# Axiom Generators: Temporal Axioms (added at each time step)
#-------------------------------------------------------------------------------

def axiom_generator_location_OK(x, y, t):
    """
    Assert the conditions under which a location is safe for the Agent.
    (Hint: Are Wumpi always dangerous?)

    x,y := location
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    wumpus_presence='('+wumpus_str(x, y)+')' #Check if wumpus is present in the location
    pit_absence='~('+pit_str(x, y)+')'#Check if pit is not present in the location
    wumpus_dead='~('+state_wumpus_alive_str(t)+')'#Check if wumpus is dead in the location
    axiom_str=state_OK_str(x, y, t) + '<=>('+ pit_absence + '&('+wumpus_presence+'>>'+wumpus_dead+'))'#Assert that If the current state is okay, then it means pit is absent,wumpus is dead if it is present
    return axiom_str

def generate_square_OK_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_location_OK(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_location_OK')
    return list(filter(lambda s: s != '', axioms))


#-------------------------------------------------------------------------------
# Connection between breeze / stench percepts and atemporal location properties

def axiom_generator_breeze_percept_and_location_property(x, y, t):
    """
    Assert that when in a location at time t, then perceiving a breeze
    at that time (a percept) means that the location is breezy (atemporal)

    x,y := location
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    axiom_str='('+breeze_str(x, y)+'<=>'+percept_breeze_str(t)+')<<'+state_loc_str(x, y, t)#Assert that if we identify breeze in the current location, it means the location is considered breezy
    return axiom_str

def generate_breeze_percept_and_location_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_breeze_percept_and_location_property(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_breeze_percept_and_location_property')
    return list(filter(lambda s: s != '', axioms))

def axiom_generator_stench_percept_and_location_property(x, y, t):
    """
    Assert that when in a location at time t, then perceiving a stench
    at that time (a percept) means that the location has a stench (atemporal)

    x,y := location
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    axiom_str='('+stench_str(x, y)+'<=>'+percept_stench_str(t)+')<<'+state_loc_str(x, y, t)#Assert that if we identify stench in the current location, it means the location is considered has stench
    return axiom_str

def generate_stench_percept_and_location_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_stench_percept_and_location_property(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_stench_percept_and_location_property')
    return list(filter(lambda s: s != '', axioms))


#-------------------------------------------------------------------------------
# Transition model: Successor-State Axioms (SSA's)
# Avoid the frame problem(s): don't write axioms about actions, write axioms about
# fluents!  That is, write successor-state axioms as opposed to effect and frame
# axioms
#
# The general successor-state axioms pattern (where F is a fluent):
#   F^{t+1} <=> (Action(s)ThatCause_F^t) | (F^t & ~Action(s)ThatCauseNot_F^t)

# NOTE: this is very expensive in terms of generating many (~170 per axiom) CNF clauses!

def axiom_generator_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax):
    """
    Assert the condidtions at time t under which the agent is in
    a particular location (state_loc_str: L) at time t+1, following
    the successor-state axiom pattern.

    See Section 7. of AIMA.  However...
    NOTE: the book's version of this class of axioms is not complete
          for the version in Project 3.
    
    x,y := location
    t := time
    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    steps = ['('+state_loc_str(x,y,t)+'& (~'+action_forward_str(t)+'|'+action_turn_left_str(t)+'|'+action_turn_right_str(t)+'|'+action_grab_str(t)+'|'+action_shoot_str(t)+'|'+percept_bump_str(t+1)+'))']
    direc=['North','West','South','East']#For the given input directions
    xiter=x #Initialise variables
    yiter=y
    headingfunction=''
    for val in direc: #Iterate the directions array and set the x and y bounds along with the header direction
        if val=='North':
            xiter=x
            yiter=y-1
            headingfunction=state_heading_north_str(t)
        if val=='West':
            xiter=x+1
            yiter=y
            headingfunction=state_heading_west_str(t)
        if val=='South':
            xiter=x
            yiter=y+1
            headingfunction=state_heading_south_str(t)
        if val=='East':
            xiter=x-1
            yiter=y
            headingfunction=state_heading_east_str(t)
        if xiter >= xmin and xiter <= xmax and yiter >= ymin and yiter <= ymax: #Make sure the position is within boundaries
            steps+=['('+state_loc_str(xiter,yiter,t)+'&('+action_forward_str(t)+'&'+headingfunction+'))'] #Add steps to the array based on the actions depicted above
    allsteps='|'.join(steps) #Join all the propositions with or clause
    axiom_str = state_loc_str(x,y,t+1)+'<=>('+allsteps+')' #If agent is present in location in the next time instant it is because of the step it took in the previous timestep
    return axiom_str

def generate_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax, heading):
    """
    The full at_location SSA converts to a fairly large CNF, which in
    turn causes the KB to grow very fast, slowing overall inference.
    We therefore need to restric generating these axioms as much as possible.
    This fn generates the at_location SSA only for the current location and
    the location the agent is currently facing (in case the agent moves
    forward on the next turn).
    This is sufficient for tracking the current location, which will be the
    single L location that evaluates to True; however, the other locations
    may be False or Unknown.
    """
    axioms = [axiom_generator_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax)]
    if heading == 'west' and x - 1 >= xmin:
        axioms.append(axiom_generator_at_location_ssa(t, x-1, y, xmin, xmax, ymin, ymax))
    if heading == 'east' and x + 1 <= xmax:
        axioms.append(axiom_generator_at_location_ssa(t, x+1, y, xmin, xmax, ymin, ymax))
    if heading == 'south' and y - 1 >= ymin:
        axioms.append(axiom_generator_at_location_ssa(t, x, y-1, xmin, xmax, ymin, ymax))
    if heading == 'north' and y + 1 <= ymax:
        axioms.append(axiom_generator_at_location_ssa(t, x, y+1, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_at_location_ssa')
    return list(filter(lambda s: s != '', axioms))

#----------------------------------

def axiom_generator_have_arrow_ssa(t):
    """
    Assert the conditions at time t under which the Agent
    has the arrow at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    axiom_str='(~('+action_shoot_str(t)+')&'+state_have_arrow_str(t)+')<=>'+state_have_arrow_str(t + 1)#If a shot has not been fired and arrow is present then arrow is present in next timestep also
    # Comment or delete the next line once this function has been implemented.
    return axiom_str

def axiom_generator_wumpus_alive_ssa(t):
    """
    Assert the conditions at time t under which the Wumpus
    is known to be alive at time t+1

    (NOTE: If this axiom is implemented in the standard way, it is expected
    that it will take one time step after the Wumpus dies before the Agent
    can infer that the Wumpus is actually dead.)

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    axiom_str= '(~(' + percept_scream_str(t + 1) + ')&' + state_wumpus_alive_str(t) + ')<=>' + state_wumpus_alive_str(t + 1)#If a scream has not been heard and wumpus is alive then wumpus is alive in next timestep also
    # Comment or delete the next line once this function has been implemented.
    return axiom_str

#----------------------------------


def axiom_generator_heading_north_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be North at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    axiom_str = state_heading_north_str(t+1)+'<=>(('+state_heading_east_str(t)+'&'+action_turn_left_str(t)+')'+'|'+'('+state_heading_north_str(t)+'&~'+action_turn_left_str(t)+'&~'+action_turn_right_str(t)+')'+'|'+'('+state_heading_west_str(t)+'&'+action_turn_right_str(t)+'))'
    #We head north if we are previously heading north, or we are heading west and take a right action or if we are heading east and take the left action.
    # Comment or delete the next line once this function has been implemented.
    return axiom_str

def axiom_generator_heading_east_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be East at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    axiom_str = state_heading_east_str(t+1)+'<=>(('+state_heading_north_str(t)+'&'+action_turn_right_str(t)+')'+'|'+'('+state_heading_east_str(t)+'&~'+action_turn_left_str(t)+'&~'+action_turn_right_str(t)+')'+'|'+'('+state_heading_south_str(t)+'&'+action_turn_left_str(t)+'))'
    #We head east if we are previously heading east, or we are heading north and take a right action or if we are heading south and take the left action.
    # Comment or delete the next line once this function has been implemented.
    return axiom_str

def axiom_generator_heading_south_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be South at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    axiom_str = state_heading_south_str(t+1)+'<=>(('+state_heading_east_str(t)+'&'+action_turn_right_str(t)+')'+'|'+'('+state_heading_south_str(t)+'&~'+action_turn_left_str(t)+'&~'+action_turn_right_str(t)+')'+'|'+'('+state_heading_west_str(t)+'&'+action_turn_left_str(t)+'))'
    #We head south if we are previously heading south, or we are heading west and take a left action or if we are heading east and take the right action.
    # Comment or delete the next line once this function has been implemented.
    return axiom_str

def axiom_generator_heading_west_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be West at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    axiom_str = state_heading_west_str(t+1)+'<=>(('+state_heading_south_str(t)+'&'+action_turn_right_str(t)+')'+'|'+'('+state_heading_west_str(t)+'&~'+action_turn_left_str(t)+'&~'+action_turn_right_str(t)+')'+'|'+'('+state_heading_north_str(t)+'&'+action_turn_left_str(t)+'))'
    #We head west if we are previously heading west, or we are heading north and take a left action or if we are heading south and take the right action.
    # Comment or delete the next line once this function has been implemented.
    return axiom_str

def generate_heading_ssa(t):
    """
    Generates all of the heading SSAs.
    """
    return [axiom_generator_heading_north_ssa(t),
            axiom_generator_heading_east_ssa(t),
            axiom_generator_heading_south_ssa(t),
            axiom_generator_heading_west_ssa(t)]

def generate_non_location_ssa(t):
    """
    Generate all non-location-based SSAs
    """
    axioms = [] # all_state_loc_ssa(t, xmin, xmax, ymin, ymax)
    axioms.append(axiom_generator_have_arrow_ssa(t))
    axioms.append(axiom_generator_wumpus_alive_ssa(t))
    axioms.extend(generate_heading_ssa(t))
    return list(filter(lambda s: s != '', axioms))

#----------------------------------

def axiom_generator_heading_only_north(t):
    """
    Assert that when heading is North, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    north_header=state_heading_north_str(t)
    east_header=state_heading_east_str(t)
    south_header=state_heading_south_str(t)
    west_header=state_heading_west_str(t)
    axiom_str='('+north_header+')<=>(~('+east_header+')&~('+south_header+')&~('+west_header+'))'#Heading north means negate on all other directions (East,South,West)
    # Comment or delete the next line once this function has been implemented.
    return axiom_str

def axiom_generator_heading_only_east(t):
    """
    Assert that when heading is East, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    north_header=state_heading_north_str(t)
    east_header=state_heading_east_str(t)
    south_header=state_heading_south_str(t)
    west_header=state_heading_west_str(t)
    axiom_str='('+east_header+')<=>(~('+north_header+')&~('+south_header+')&~('+west_header+'))'#Heading east means negate on all other directions (North,South,West)
    # Comment or delete the next line once this function has been implemented.
    return axiom_str

def axiom_generator_heading_only_south(t):
    """
    Assert that when heading is South, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    north_header=state_heading_north_str(t)
    east_header=state_heading_east_str(t)
    south_header=state_heading_south_str(t)
    west_header=state_heading_west_str(t)
    axiom_str='('+south_header+')<=>(~('+east_header+')&~('+north_header+')&~('+west_header+'))'#Heading south means negate on all other directions (East,North,West)
    # Comment or delete the next line once this function has been implemented.
    return axiom_str

def axiom_generator_heading_only_west(t):
    """
    Assert that when heading is West, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    north_header=state_heading_north_str(t)
    east_header=state_heading_east_str(t)
    south_header=state_heading_south_str(t)
    west_header=state_heading_west_str(t)
    axiom_str='('+west_header+')<=>(~('+east_header+')&~('+south_header+')&~('+north_header+'))'#Heading west means negate on all other directions (East,South,North)
    # Comment or delete the next line once this function has been implemented.
    return axiom_str

def generate_heading_only_one_direction_axioms(t):
    return [axiom_generator_heading_only_north(t),
            axiom_generator_heading_only_east(t),
            axiom_generator_heading_only_south(t),
            axiom_generator_heading_only_west(t)]


def axiom_generator_only_one_action_axioms(t):
    """
    Assert that only one axion can be executed at a time.
    
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    temp = []
    step = proposition_bases_actions#All the actions possible
    length=len(step)
    index=0
    while index<(length): #Iterate through the actions
        other=[]
        for iter1,iter2 in enumerate(step):
            if iter1!=index: #If not current action
                other+= [('~' + iter2 + str(t))]#Negate all other actions in the input
        temp+=['('+step[index]+str(t)+'<=>('+'&'.join(other)+'))'] #If current action then we can assert the negation of all other action sin the and clause
        index+=1#Incrementor
    axiom_str = '&'.join(temp)#Join the axioms
    # Comment or delete the next line once this function has been implemented.
    return axiom_str


def generate_mutually_exclusive_axioms(t):
    """
    Generate all time-based mutually exclusive axioms.
    """
    axioms = []
    
    # must be t+1 to constrain which direction could be heading _next_
    axioms.extend(generate_heading_only_one_direction_axioms(t + 1))

    # actions occur in current time, after percept
    axioms.append(axiom_generator_only_one_action_axioms(t))

    return list(filter(lambda s: s != '', axioms))

#-------------------------------------------------------------------------------
