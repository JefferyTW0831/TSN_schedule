結構：
Main.py
new_scheduler
    ObjExeSwitch.py
    Execution.py
    TimeTable.py
    Demo.py
    full_schedule
        FullScheduler.py
    tense_schedule
        TenseScheduler.py
        InitFlowFilter.py   
        ScheduleMiddle.py


流程：          
Main.py → (ObjExeSwitch.py)ObjectiveSwitch  |→  TenseScheduler.py                           
                                            |→  (FullScheduler.py)FullSchedulerContinue
                                            |→  (FullScheduler.py)FullSchedulerReschedule

→   (ObjExeSwitch.py)ExeSwitch(objective_chosen)    |→ (Execution.py)RunData(objective_chosen)
                                                    |→ (Execution.py)RunDemo(objective_chosen)
                                        
→依據objective_chosen判斷要執行哪個class(Tense_schedule, FullSchedulerContinue, FullSchedulerReschedule)