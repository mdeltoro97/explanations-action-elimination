#ifndef SEARCH_ENGINE_H
#define SEARCH_ENGINE_H

#include "operator_cost.h"
#include "operator_id.h"
#include "plan_manager.h"
#include "search_progress.h"
#include "search_space.h"
#include "search_statistics.h"
#include "state_registry.h"
#include "task_proxy.h"

#include "utils/logging.h"

#include <parallel_hashmap/phmap.h>

#include <vector>

namespace options {
class OptionParser;
class Options;
}

namespace ordered_set {
template<typename T>
class OrderedSet;
}

namespace successor_generator {
class SuccessorGenerator;
}

enum SearchStatus {IN_PROGRESS, TIMEOUT, FAILED, SOLVED, UNSOLVABLE};

class SearchEngine {
protected:
    SearchStatus status;
    bool solution_found;
    Plan plan;

    // Hold a reference to the task implementation and pass it to objects that need it.
    const std::shared_ptr<AbstractTask> task;
    // Use task_proxy to access task information.
    TaskProxy task_proxy;

    mutable utils::LogProxy log;
    PlanManager plan_manager;
    StateRegistry state_registry;
    const successor_generator::SuccessorGenerator &successor_generator;
    SearchSpace search_space;
    SearchProgress search_progress;
    SearchStatistics statistics;
    int bound;
    const bool only_use_operators_from_incumbent_plan;
    std::unique_ptr<phmap::flat_hash_set<int>> operators_in_incumbent_plan;
    OperatorCost cost_type;
    bool is_unit_cost;
    double max_time;

    virtual void initialize() {}
    virtual SearchStatus step() = 0;

    void set_plan(const Plan &plan);
    bool check_goal_and_set_plan(const State &state);
    int get_adjusted_cost(const OperatorProxy &op) const;
public:
    SearchEngine(const options::Options &opts);
    virtual ~SearchEngine();
    virtual void print_statistics() const = 0;
    virtual void save_plan_if_necessary();
    bool found_solution() const;
    SearchStatus get_status() const;
    const Plan &get_plan() const;
    void search();
    const SearchStatistics &get_statistics() const {return statistics;}
    void set_bound(int b) {bound = b;}
    int get_bound() {return bound;}
    void set_incumbent_plan(const Plan &plan);
    PlanManager &get_plan_manager() {return plan_manager;}

    /* The following three methods should become functions as they
       do not require access to private/protected class members. */
    static void add_pruning_option(options::OptionParser &parser);
    static void add_options_to_parser(options::OptionParser &parser);
    static void add_succ_order_options(options::OptionParser &parser);
};

/*
  Print evaluator values of all evaluators evaluated in the evaluation context.
*/
extern void print_initial_evaluator_values(
    const EvaluationContext &eval_context);

extern void collect_preferred_operators(
    EvaluationContext &eval_context, Evaluator *preferred_operator_evaluator,
    ordered_set::OrderedSet<OperatorID> &preferred_operators);

#endif
