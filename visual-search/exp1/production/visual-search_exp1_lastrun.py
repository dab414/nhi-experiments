﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2021.1.4),
    on Tue 07 Sep 2021 12:52:27 PM EDT
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

lines_rectangles_counter = 0
lines_rectangles_container = []

import copy


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2021.1.4'
expName = 'visual-search_exp1'  # from the Builder filename that created this script
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='visual-search_exp1_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[1920, 1080], fullscr=True, screen=1, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0.75,0.75,0.75], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "trial1"
trial1Clock = core.Clock()
import psychopy
win.units = 'pix'
## print_line_widths
## ^ flag for troubleshooting



class DrawHexGrid:
    '''
    The general idea here is to think, for any given hexagon I want to draw, what position (eg, top left) in the hex am i starting at, what position do i want to finish at, and what's the starting coordinate
    Given this information, we rely on the formulas below to draw however many lines are needed to connect the starting position to the ending position
    In the process, I save out starting coordinates that will be used for the next hexagon and for the first hexagon in a new row, as well as handling some other edge case things
    
    Formula for calculating coordinates:
    xx = x + (d * cos(alpha))
    yy = y + (d * sin(alpha))
    '''
    def __init__(self, top_left_origin, edge_length = 120, x_count = 4, y_count = 4):
        ## print_line_widths
        self.build_diagnostic_container = True
        self.build_diagnostic_count = 0
        self.diagnostic_container = []
        self.diagnostic_widths = []

        self.top_left_origin = top_left_origin
        self.edge_length = edge_length
        self. x_count = x_count
        self.y_count = y_count
        self.point_list = ['top_left', 'bottom_left', 'bottom', 'bottom_right', 'top_right', 'top']
        self.point_dictionary = {
'top_left': '[start_coord[0], start_coord[1] - self.edge_length]',
'bottom_left': '[start_coord[0] + self.edge_length * cos(120), start_coord[1] - self.edge_length * sin(120)]',
'bottom': '[start_coord[0] + self.edge_length * cos(120), start_coord[1] + self.edge_length * sin(120)]',
'bottom_right': '[start_coord[0], start_coord[1] + self.edge_length]',
'top_right': '[start_coord[0] - self.edge_length * cos(120), start_coord[1] + self.edge_length * sin(120)]',
'top': '[start_coord[0] - self.edge_length * cos(120), start_coord[1] - self.edge_length * sin(120)]'
}
        self.angle_dictionary = {
        'top_left': 0,
        'bottom_left': -55,
        'bottom': 55,
        'bottom_right': 0,
        'top_right': -55,
        'top': 55
        }
        
    def make_grid(self):
        for row in range(self.y_count):
            for col in range(self.x_count):
                ## print_line_widths
                self.row = row
                self.col = col
                
                ## if it's the first hex
                if not row and not col:
              
                    ## reset the line width drawer
                    self.line_width_container_draw = copy.deepcopy(line_width_container_original)
                    
                    self._draw_hex('top_left', 'top_left', self.top_left_origin)
                    self.first_row_start_coord = self._coord_calculator(self.top_left_origin, 'top_left', 2)
                    self.new_hex_start_coord = self._coord_calculator(self.top_left_origin, 'top_left', 3)
                
                ## if it's the first row
                elif not row:
                    self._draw_hex('bottom_left', 'top_left', self.new_hex_start_coord)
                    self.new_hex_start_coord = self._coord_calculator(self.new_hex_start_coord, 'bottom_left', 2)
                    
                ## if it's the first column
                elif not col:
                    
                    ## conditional to account for the staggered pattern
                    if not row % 2:
                    ## if even
                        start_pos = 'top'
                        new_hex_n_turns = 4
                        first_row_n_turns = 3
                        
                    else:
                    ## if odd
                        start_pos = 'top_left'
                        new_hex_n_turns = 3
                        first_row_n_turns = 1
                        
                    self._draw_hex(start_pos, 'top_right', self.first_row_start_coord)
                    self.new_hex_start_coord = self._coord_calculator(self.first_row_start_coord, start_pos, new_hex_n_turns)
                    self.first_row_start_coord = self._coord_calculator(self.first_row_start_coord, start_pos, first_row_n_turns)
                    
                ## for all internal hex's
                else:
                    ## catch the last hex on odd rows
                    if col == self.x_count - 1 and row % 2:
                        end_pos = 'top'
                    else:
                        end_pos = 'top_right'

                    self._draw_hex('bottom_left', end_pos, self.new_hex_start_coord)
                    self.new_hex_start_coord = self._coord_calculator(self.new_hex_start_coord, 'bottom_left', 2)

                    
    def _coord_calculator(self, start_coord, start_pos, n_turns):
        ## takes in a starting coordinate, starting pos, and number of calcs to do
        ## returns ending coord as [x, y]
        ## this function will fail if you try to turn past top left, which i dont think ill need to do
        
        ## calc a slice out of point_list to iterate over what's appropriate
        new_point_list = self._rearrange_point_list(start_pos)
        
        for pos in new_point_list[:n_turns]:
            start_coord = eval(self.point_dictionary[pos])
        
        return start_coord
            
            
    
    def _draw_hex(self, start_pos, end_pos, start_coord):
        
        ## draws a line from start_pos to end_pos
        new_point_list = self._rearrange_point_list(start_pos)

        for position in new_point_list:
            if start_pos != end_pos and position == end_pos:
                break
                
            if self.build_diagnostic_container:
                self.diagnostic_container.append(['{}-{}-{}'.format(self.col, self.row, start_pos)])
            
            line = self._define_line_type()
            line.start = start_coord
            line.end = eval(self.point_dictionary[position])
            line.draw()
            ## draw rect
            is_exterior = self._determine_exterior(self.row, self.col, self.x_count, self.y_count, position)
            

            lines_rectangles_container.append([line])
                
            self._draw_rect(start_coord, line.end, position, is_exterior)
            
            start_coord= line.end


    def _draw_rect(self, line_start, line_end, position, is_exterior = False):

        edge_length = self.edge_length
        center = [(line_end[0] + line_start[0]) / 2, (line_end[1] + line_start[1]) / 2]
        rotation = self.angle_dictionary[position]
        if not is_exterior:
            rect =  psychopy.visual.Rect(
            win = win,
            pos = center,
            units = 'pix',
            width = 20,
            height = edge_length - 20,
            opacity = 0,
            ori = rotation
            )
            rect.draw()
            
            lines_rectangles_container[-1] += [rect, 'not_clicked']
        else:
            lines_rectangles_container[-1].append(None)

    def _determine_exterior(self, row, col, x_count, y_count, position):
        ## i should write good comments here but not now lol
        ## basically just using position in the array to check relative line position to determine whether to draw rectangles
        if not row:
            if position in ['top_right', 'top']:
                return True
        if not col:
            if not row % 2:
                to_check = ['top_left', 'bottom_left', 'top']
            else:
                to_check = ['top_left']
            if position in to_check:
                return True
        if row == y_count - 1:
            if position in ['bottom_left', 'bottom']:
                return True
        if col == x_count - 1:
            if not row % 2:
                to_check = ['bottom_right']
            else:
                to_check = ['bottom', 'bottom_right', 'top_right']
            if position in to_check:
                return True

        return False


    def _rearrange_point_list(self, start_pos):
        ## outputs a list where the first element is start_pos and the last element is the one before start_pos in point_list

        if start_pos == 'top_left':
            return self.point_list

        return self.point_list[self.point_list.index(start_pos):] + self.point_list[:self.point_list.index(start_pos)-1]

    def _define_line_type(self):
        if not self.line_width_container_draw:
            self.line_width_container_draw = copy.deepcopy(line_width_container_original)
        lineWidth = self.line_width_container_draw.pop(0)

        #lineWidth = self.line_width_container_draw[0]
        #del self.line_width_container_draw[0]
        
        ## print_line_widths
        if self.build_diagnostic_container:
            self.diagnostic_container[-1].append(lineWidth)
            
        return psychopy.visual.Line(
            lineWidth = lineWidth,
            win = win,
            units='pix',
            lineColor=[-1, -1, -1]
            )

line_width_container = np.linspace(1, 4, 10)
#line_width_container = [round(x, 4) for x in line_width_container]


range_to_width = {}

percentages = [.02, .07, .07] + [.17]*4 + [.07, .07, .02]

base_percentage = 0
for percentage, line_width in zip(percentages, line_width_container):
    range_to_width[base_percentage, base_percentage+percentage] = line_width
    base_percentage += percentage +.000001
    

def choose_line_width():
    ## draw random from uniform distribution, choose line width
    random_number  = round(np.random.uniform(), 3)
    for key in range_to_width:
        if random_number >= key[0]  and random_number < key[1]:
            return range_to_width[key]


## initialize full container
line_width_container_original = []

for i in range(400):
    line_width_container_original.append(choose_line_width())
    


key_resp_2 = keyboard.Keyboard()
PromptToContinue = visual.TextStim(win=win, name='PromptToContinue',
    text='Press the space bar when you are ready to select the three thinnest lines.',
    font='Open Sans',
    units='pix', pos=(-700, 400), height=35.0, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0);

# Initialize components for Routine "trial2_2"
trial2_2Clock = core.Clock()
key_resp_3 = keyboard.Keyboard()
PromptToSelect = visual.TextStim(win=win, name='PromptToSelect',
    text='',
    font='Open Sans',
    units='pix', pos=(-700, 400), height=35.0, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "trial1"-------
continueRoutine = True
# update component parameters for each repeat

dhg = DrawHexGrid([-400, 400])

dhg.make_grid()

line_width_container_original = []

for i in range(400):
    line_width_container_original.append(choose_line_width())
    


key_resp_2.keys = []
key_resp_2.rt = []
_key_resp_2_allKeys = []
# keep track of which components have finished
trial1Components = [key_resp_2, PromptToContinue]
for thisComponent in trial1Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
trial1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "trial1"-------
while continueRoutine:
    # get current time
    t = trial1Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=trial1Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    for entry in lines_rectangles_container:
        entry[0].draw()
        if entry[1] is not None:
            entry[1].draw()
    
    
    
    
    
    
    
    
    # *key_resp_2* updates
    waitOnFlip = False
    if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp_2.frameNStart = frameN  # exact frame index
        key_resp_2.tStart = t  # local t and not account for scr refresh
        key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
        key_resp_2.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_2.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_2.getKeys(keyList=['y', 'n', 'left', 'right', 'space'], waitRelease=False)
        _key_resp_2_allKeys.extend(theseKeys)
        if len(_key_resp_2_allKeys):
            key_resp_2.keys = _key_resp_2_allKeys[-1].name  # just the last key pressed
            key_resp_2.rt = _key_resp_2_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *PromptToContinue* updates
    if PromptToContinue.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        PromptToContinue.frameNStart = frameN  # exact frame index
        PromptToContinue.tStart = t  # local t and not account for scr refresh
        PromptToContinue.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(PromptToContinue, 'tStartRefresh')  # time at next scr refresh
        PromptToContinue.setAutoDraw(True)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in trial1Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "trial1"-------
for thisComponent in trial1Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_2.keys in ['', [], None]:  # No response was made
    key_resp_2.keys = None
thisExp.addData('key_resp_2.keys',key_resp_2.keys)
if key_resp_2.keys != None:  # we had a response
    thisExp.addData('key_resp_2.rt', key_resp_2.rt)
thisExp.addData('key_resp_2.started', key_resp_2.tStartRefresh)
thisExp.addData('key_resp_2.stopped', key_resp_2.tStopRefresh)
thisExp.nextEntry()
thisExp.addData('PromptToContinue.started', PromptToContinue.tStartRefresh)
thisExp.addData('PromptToContinue.stopped', PromptToContinue.tStopRefresh)
# the Routine "trial1" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "trial2_2"-------
continueRoutine = True
# update component parameters for each repeat
key_resp_3.keys = []
key_resp_3.rt = []
_key_resp_3_allKeys = []
mouse = psychopy.event.Mouse(win = win)

clicked_lines = []

show_text = 'Select three of the thinnest lines'
# keep track of which components have finished
trial2_2Components = [key_resp_3, PromptToSelect]
for thisComponent in trial2_2Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
trial2_2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "trial2_2"-------
while continueRoutine:
    # get current time
    t = trial2_2Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=trial2_2Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *key_resp_3* updates
    waitOnFlip = False
    if key_resp_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp_3.frameNStart = frameN  # exact frame index
        key_resp_3.tStart = t  # local t and not account for scr refresh
        key_resp_3.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_3, 'tStartRefresh')  # time at next scr refresh
        key_resp_3.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_3.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_3.getKeys(keyList=['y', 'n', 'left', 'right', 'space'], waitRelease=False)
        _key_resp_3_allKeys.extend(theseKeys)
        if len(_key_resp_3_allKeys):
            key_resp_3.keys = _key_resp_3_allKeys[-1].name  # just the last key pressed
            key_resp_3.rt = _key_resp_3_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    import time
    
    for entry in lines_rectangles_container:
        if entry[1] is not None:
            entry[1].draw()
            
            if entry[2] == 'clicked':
                if entry[1].contains(mouse):
                    entry[0].lineColor = [0,  1, 0]
                else:
                    entry[0].lineColor = [-1, 1, -1]
            elif entry[1].contains(mouse):
                entry[0].lineColor = [1, -1, -1]
            else:
                entry[0].lineColor = [-1] * 3
        
        entry[0].draw()
        time.sleep(0.001)
    
    
    
    if mouse.getPressed()[0]:
        mouse_pos = mouse.getPos()
        for entry in lines_rectangles_container:
            if entry[1] is not None and entry[1].contains(mouse_pos):
    
                if entry[2] == 'clicked':
                    entry[2] = 'not_clicked'
                    del clicked_lines[clicked_lines.index(entry)]
                    show_text = 'Select three of the thinnest lines'
    
                else:
                    if len(clicked_lines) < 3:
                        show_text = 'Select three of the thinnest lines'
                        entry[2] = 'clicked'
                        clicked_lines.append(entry)
                    else:
                        show_text = 'Youve clicked too many lines already!'
                    
                time.sleep(.1)
    
                break
    
                
                
    
    # *PromptToSelect* updates
    if PromptToSelect.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        PromptToSelect.frameNStart = frameN  # exact frame index
        PromptToSelect.tStart = t  # local t and not account for scr refresh
        PromptToSelect.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(PromptToSelect, 'tStartRefresh')  # time at next scr refresh
        PromptToSelect.setAutoDraw(True)
    if PromptToSelect.status == STARTED:  # only update if drawing
        PromptToSelect.setText(show_text)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in trial2_2Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "trial2_2"-------
for thisComponent in trial2_2Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_3.keys in ['', [], None]:  # No response was made
    key_resp_3.keys = None
thisExp.addData('key_resp_3.keys',key_resp_3.keys)
if key_resp_3.keys != None:  # we had a response
    thisExp.addData('key_resp_3.rt', key_resp_3.rt)
thisExp.addData('key_resp_3.started', key_resp_3.tStartRefresh)
thisExp.addData('key_resp_3.stopped', key_resp_3.tStopRefresh)
thisExp.nextEntry()
thisExp.addData('PromptToSelect.started', PromptToSelect.tStartRefresh)
thisExp.addData('PromptToSelect.stopped', PromptToSelect.tStopRefresh)
# the Routine "trial2_2" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
