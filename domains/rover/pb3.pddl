(define (problem rover-1)

    (:domain 
        rover-domain    
    )
    
    (:objects
        waypoint1 waypoint2 waypoint3 waypoint4
        
        sample1 sample2 sample3 
        
        objective1 objective2 
        
        rover1
    )
    
    (:init
        
        (waypoint waypoint1) (waypoint waypoint2) (waypoint waypoint3) (waypoint waypoint4) 
        
        (sample sample1) (sample sample2)  
        
        (objective objective1) (objective objective2) 
        
        (can-move waypoint1 waypoint3) 
        (can-move waypoint3 waypoint1) 
        (can-move waypoint2 waypoint3) 
        (can-move waypoint3 waypoint2) 
        (can-move waypoint2 waypoint1) 
        (can-move waypoint2 waypoint4) 
        (can-move waypoint4 waypoint2) 
        
        (is-visible objective1 waypoint4) 
        (is-visible objective2 waypoint3)
        
        
        (is-in sample1 waypoint4) (is-in sample2 waypoint3)   
        
        (is-dropping-dock waypoint1)
        
        (rover rover1)
        (empty rover1)
        (at rover1 waypoint2)
    )
    
    (:goal
        (and 
            (stored-sample sample1)
            (stored-sample sample2)
            
            (taken-image objective1)
            (taken-image objective2)   
            
            (at rover1 waypoint2))
    )
)
