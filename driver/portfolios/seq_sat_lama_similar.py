OPTIMAL = False

CONFIGS = [
     # lazy greedy
     (-1, ["--evaluator", "hlm=lmcount(lm_reasonable_orders_hps(lm_rhw()),transform=H_COST_TRANSFORM, pref=false)",
           "--evaluator", "hff=ff(transform=H_COST_TRANSFORM)",
           "--search", "lazy_greedy([hff,hlm],preferred=[hff,hlm], cost_type=S_COST_TYPE, bound=BOUND)"]),
     # lazy wastar w=5
     (-1, ["--evaluator", "hlm=lmcount(lm_reasonable_orders_hps(lm_rhw()),transform=H_COST_TRANSFORM, pref=false)",
           "--evaluator", "hff=ff(transform=H_COST_TRANSFORM)",
           "--search", "lazy_wastar([hff,hlm],preferred=[hff,hlm], cost_type=S_COST_TYPE, w=5, bound=BOUND)"]),
     # lazy wastar w=3
     (-1, ["--evaluator", "hlm=lmcount(lm_reasonable_orders_hps(lm_rhw()),transform=H_COST_TRANSFORM, pref=false)",
           "--evaluator", "hff=ff(transform=H_COST_TRANSFORM)",
           "--search", "lazy_wastar([hff,hlm],preferred=[hff,hlm], cost_type=S_COST_TYPE, w=3, bound=BOUND)"]),
     # lazy wastar w=2
     (-1, ["--evaluator", "hlm=lmcount(lm_reasonable_orders_hps(lm_rhw()),transform=H_COST_TRANSFORM, pref=false)",
           "--evaluator", "hff=ff(transform=H_COST_TRANSFORM)",
           "--search", "lazy_wastar([hff,hlm],preferred=[hff,hlm], cost_type=S_COST_TYPE, w=2, bound=BOUND)"]),
     # lazy wastar w=1
     (-1, ["--evaluator", "hlm=lmcount(lm_reasonable_orders_hps(lm_rhw()),transform=H_COST_TRANSFORM, pref=false)",
           "--evaluator", "hff=ff(transform=H_COST_TRANSFORM)",
           "--search", "lazy_wastar([hff,hlm],preferred=[hff,hlm], cost_type=S_COST_TYPE, w=1, bound=BOUND)"]),
     # lazy wastar w=1 iterated search
     (-1, ["--evaluator", "hlm=lmcount(lm_reasonable_orders_hps(lm_rhw()),transform=H_COST_TRANSFORM, pref=false)",
           "--evaluator", "hff=ff(transform=H_COST_TRANSFORM)",
           "--search", "iterated(lazy_wastar([hff,hlm],preferred=[hff,hlm], cost_type=S_COST_TYPE, w=1, bound=BOUND), bound=BOUND,repeat_last=true,continue_on_fail=true"])
    ]
