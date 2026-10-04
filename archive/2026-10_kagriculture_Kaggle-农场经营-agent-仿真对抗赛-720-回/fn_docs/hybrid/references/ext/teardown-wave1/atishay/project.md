Kaggriculture — A Farming-Game Agent, Built in Phases · Atishay Kasliwal                              
 [][]  
 
 
 Kaggriculture An agent that plans ahead by simulating the real rules. Nine versions, each built to beat the last. 
 
Kaggriculture is a two-player Kaggle competition: farm a shared board, sell into a moving market, out-earn an opponent over 720 turns. I built a simulator that matches the real engine exactly, then a planner that searches ahead through it instead of reacting turn by turn.
  
StackPython · kaggle-environments · React strategy desk
 
StatusOpen source · [GitHub ↗︎]
   
- 9agent versions
 
- 720turns per season
 
- 1,738lines of Python
  
 
  
 

 
Kaggriculture
 
Python · kaggle-environments[View code ↗︎]
 
 
 
![img](/projects/video/kaggriculture-poster.webp)
  Hover to play 
  
  01 / Overview 
![img](/projects/video/kaggriculture-poster.webp)
  
 
  
  
01 · Problem
 
A reactive agent can't see the trap it's walking into.
 
Land, water, harvest, sell, repeat: an agent that only reacts to the current turn buys land too late, plants the wrong crop for the days left in the season, or gets outpaced by a competitor at the market.
   
02 · Solution
 
Simulate first, then search through the simulation.
 
A deterministic simulator reproduces the game's rules, checked turn by turn against Kaggle's own engine. A planner searches move sequences through it, models the opponent, and hands off to an emergency handler near the end of the season.
   
03 · Engineering
 
 
Simulatormatches engine
→
Plannersearch · candidates
→
Opponent modelrollouts
 

Emergency handlerendgame

Strategy deskReact

 
 
Tests assert the simulator against Kaggle's real engine turn by turn, so a planner search through it searches the actual rules, not an approximation.
   
04 · Key decisions
  
- Simulator validated, exact-match vs. real engine
 
- Opponent modeled by rollouts, not a formula
 
- Data-driven thresholds, not hardcoded guesses
 
- Endgame guard, added after two timing bugs
 
- Nine agent versions, each beating the last
    
 
Engineering note
 
The planner earned its search budget one phase at a time. Ten phases in three days, each one validated before the next began.
 
Phase 2 checked the price formula against the live engine before Phase 3 trusted the simulator to search through. Phase 5's planner had to beat every earlier agent before it became the baseline, and Phase 9 replaced a discount-formula guess at the opponent with rollouts of its own policy.
   [][] []
