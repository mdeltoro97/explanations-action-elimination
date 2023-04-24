(define (domain restricted-minecraft)
(:requirements :typing)
(:types        food stick stone - object)
(:predicates (has-food ?x - food)
	     (has-stick ?x - stick)
	     (has-stone ?x - stone)
	     (hungry)
	     (has_axe)
	     (available-food  ?x - food)
	     (available-stick ?x - stick)
	     (available-stone ?x - stone)
 )
	
(:action get_food
:parameters (?food - food)
:precondition (and (available-food ?food))
:effect (and
           (not (available-food ?food))
	   (has-food ?food))
)

(:action get_stick
:parameters (?stick - stick)
:precondition (and (available-stick ?stick))
:effect (and
          (not (available-stick ?stick))
	  (has-stick ?stick))
)

;; (:action get_stone
;; :parameters (?stone - stone)
;; :precondition (and (available-stone ?stone))
;; :effect (and
;;          (not (available-stone ?stone))
;; 	 (has-stone ?stone))
;; )

(:action eat
:parameters (?food - food)
:precondition (and (has-food ?food) (hungry))
:effect (and (not (has-food ?food))
	     (not (hungry)))
)

(:action make_axe
:parameters (?stick - stick)
:precondition (and (has-stick ?stick))
:effect (and (not (has-stick ?stick))
	     (has_axe))
)

)

