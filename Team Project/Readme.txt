                                                                Artficial Intelligence
                                                                     CSE 571
                                                                      2022
                                                                    Team 3643

                                              Topic 4: Reinforcement Learning Agent: (True online Sarsa(λ))

                                                                   Team Members:
                                                              Aasish Tammana(1225545568)
                                                          Akhilesh Udayashankar(1225622476)
                                                            Devadutt Sanka(1225362138)
                                                            Prem Suresh Kumar(1225492151)
                                                               


The main aim of the project is to implement true online sarsa agent with linear function approximation and compare it with the Q-learning agent with
linear function approximation.

All the generated Data is stored in modelperformance file.

---------------------------------------------------------------------------------------------------------------------------------------------
Files edited or created:
---------------------------------------------------------------------------------------------------------------------------------------------

layoutGenerator.py --> Generates new layouts for the pacman domain which are used in the implementation along with the existing layouts.

generatettestresults.py --> Implements Student T-Test for comparison of True Online Sarsa and Approximate Q learning agent in all the layouts.

generategraphsforallmodelruns.py --> Generates plots for all the layouts comparing True Online Sarsa agent with different lambda values and Q learning Agent.

game.py --> needed to modify the handling of sarsa during run.

pacman.py --> make an additional call to save model training information.

qlearningAgents.py --> It contains algorythm for both TrueOnlineSarsa and Approximate Q learning (implemented as part of project 4) Agent.

trainmodelsforalllayouts.py --> trains both ApproximateQ Learning and True Online Sarsa model with trace decay of 0.3 on all layouts in the layouts folder.

Plots.ipynb --> has sample code for some of the scripts above.

---------------------------------------------------------------------------------------------------------------------------------------------
Commands for running files:
---------------------------------------------------------------------------------------------------------------------------------------------
Please install packages from the requirements.txt file. (pip install -r requirements.txt)

for Approximate Q Agent
python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 2000 -n 2000 -l layoutname

for True Online Sarsa Agent.

to run for trace decay rate @0.3
python pacman.py -p TOSarsaAgent -a extractor=SimpleExtractor,tDRate=0.3 -x 2000 -n 2000 -l layoutname

to automate runnning
python trainmodelsforalllayouts.py

to run Student T Test
python generatettestresults.py

to run graph plots
python generategraphsforallmodelruns.py