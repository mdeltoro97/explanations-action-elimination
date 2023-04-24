(define (problem prueba)
(:domain blocksworld)
(:objects A B C D E  - block
	  )
(:init
(handempty)
(clear A)
(ontable A) 
(clear B)
(ontable B)
(clear C)
(ontable C)
(clear D)
(ontable D)

)
(:goal
 (and
  (ontable B)
  (clear A)
  (on A B))
)
)


