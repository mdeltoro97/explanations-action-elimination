(define (problem restricted-minecraft-1)
(:domain restricted-minecraft)
(:objects
 food1 - food
 stone1 - stone
 stick1 - stick
 
)
(:init
 (available-food food1)
 (available-stone stone1)
 (available-stick stick1)

)
(:goal
 (and
       (not (hungry))
       (has_axe)
      )

 ))