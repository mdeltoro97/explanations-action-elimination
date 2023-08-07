(define (problem pb3)
  (:domain logistics)
  (:requirements :strips :typing) 
  (:objects alex - package
	    jason - package
	    michelle - package
	    airplane1 - airplane
	    airplane2 - airplane
	    lonairport - airport
	    parairport -  airport
	    jfkairport   - airport
    )
  (:init (at airplane1 lonairport)
	 (at airplane2 parairport)
	 (at alex parairport)
	 (at michelle lonairport)
	 (at jason lonairport)
	 )
  (:goal (and 
	  (at michelle parairport)
	  (at jason parairport)
      (at alex lonairport)

	  )
	 )
  )