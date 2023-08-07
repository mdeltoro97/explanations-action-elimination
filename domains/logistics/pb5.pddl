(define (problem pb5)
  (:domain logistics)
  (:requirements :strips :typing) 
  (:objects alex - package
	    jason - package
	    airplane1 - airplane
	    lonairport - airport
	    parairport -  airport
		jkairport -  airport
    )
  (:init (at airplane1 lonairport)
	 (at alex lonairport)
	 (at jason lonairport)
	 )
  (:goal (and 
	  (at jason parairport)
      (at alex parairport)

	  )
	 )
  )